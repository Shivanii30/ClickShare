import io
import logging
import os
import zipfile

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework import serializers

from .models import Files, Folder

logger = logging.getLogger(__name__)


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Files
        fields = "__all__"


class FileListSerializer(serializers.Serializer):
    files = serializers.ListField(
        child=serializers.FileField(
            max_length=255,
            allow_empty_file=False,
            use_url=False,
        )
    )
    folder = serializers.CharField(required=False)

    def validate_files(self, files):
        if not files:
            raise serializers.ValidationError("Please select at least one file.")

        if len(files) > settings.MAX_UPLOAD_FILES:
            raise serializers.ValidationError(
                f"You can upload up to {settings.MAX_UPLOAD_FILES} files at a time."
            )

        max_file_size = settings.MAX_UPLOAD_FILE_SIZE_MB * 1024 * 1024
        max_total_size = settings.MAX_TOTAL_UPLOAD_SIZE_MB * 1024 * 1024
        total_size = 0

        for upload in files:
            file_size = getattr(upload, "size", 0)
            total_size += file_size
            if file_size > max_file_size:
                raise serializers.ValidationError(
                    f"{upload.name} is larger than the {settings.MAX_UPLOAD_FILE_SIZE_MB} MB limit."
                )

        if total_size > max_total_size:
            raise serializers.ValidationError(
                f"Combined uploads must stay under {settings.MAX_TOTAL_UPLOAD_SIZE_MB} MB."
            )

        return files

    def create_zip_archive(self, folder, files):
        archive_buffer = io.BytesIO()
        with zipfile.ZipFile(archive_buffer, "w", zipfile.ZIP_DEFLATED) as archive:
            for upload in files:
                upload.seek(0)
                archive.writestr(os.path.basename(upload.name), upload.read())
                upload.seek(0)

        archive_buffer.seek(0)
        zip_path = f"bundles/{folder.uid}.zip"
        saved_path = default_storage.save(
            zip_path,
            ContentFile(archive_buffer.getvalue(), name=f"{folder.uid}.zip"),
        )
        folder.zip_public_id = saved_path
        folder.zip_url = default_storage.url(saved_path)
        folder.save(update_fields=["zip_public_id", "zip_url"])
        return folder.zip_url

    def create(self, validated_data):
        uploads = validated_data.pop("files")
        folder = Folder.objects.create(original_file_count=len(uploads))

        for upload in uploads:
            upload.seek(0)
            Files.objects.create(
                folder=folder,
                file=upload,
                original_name=os.path.basename(upload.name),
            )

        self.create_zip_archive(folder, uploads)
        logger.info("Created upload bundle for folder %s", folder.uid)

        return {
            "folder": str(folder.uid),
            "zip_url": folder.zip_url,
            "original_file_count": folder.original_file_count,
        }
