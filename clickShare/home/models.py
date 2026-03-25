import os
import uuid

from django.db import models
from django.utils import timezone


class Folder(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    zip_public_id = models.CharField(max_length=255, blank=True)
    zip_url = models.URLField(blank=True)
    original_file_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)


def get_upload_path(instance, filename):
    safe_name = os.path.basename(filename)
    return os.path.join(str(instance.folder.uid), safe_name)


class Files(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name="files")
    file = models.FileField(upload_to=get_upload_path)
    original_name = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
