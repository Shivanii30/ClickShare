from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Folder
from .serializers import FileListSerializer


@override_settings(
    MAX_UPLOAD_FILES=2,
    MAX_UPLOAD_FILE_SIZE_MB=1,
    MAX_TOTAL_UPLOAD_SIZE_MB=2,
)
class UploadFlowTests(TestCase):
    def test_healthcheck(self):
        response = self.client.get(reverse("healthcheck"))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "ok"})

    @patch("home.serializers.default_storage.url")
    @patch("home.serializers.default_storage.save")
    def test_upload_creates_cloud_zip_url(self, mock_save, mock_url):
        mock_save.return_value = "bundles/test-folder.zip"
        mock_url.return_value = "https://example.supabase.co/storage/v1/object/public/swift-share/bundles/test-folder.zip"
        response = self.client.post(
            reverse("handle-upload"),
            {
                "files": [
                    SimpleUploadedFile("hello.txt", b"hello world", content_type="text/plain")
                ]
            },
        )

        self.assertEqual(response.status_code, 201)
        folder = Folder.objects.get()
        self.assertEqual(folder.original_file_count, 1)
        self.assertTrue(folder.zip_url.startswith("https://"))
        self.assertEqual(response.json()["data"]["folder"], str(folder.uid))

    def test_serializer_rejects_oversized_batches(self):
        serializer = FileListSerializer(
            data={
                "files": [
                    SimpleUploadedFile("first.txt", b"a" * (1024 * 1024), content_type="text/plain"),
                    SimpleUploadedFile("second.txt", b"b" * (1024 * 1024), content_type="text/plain"),
                    SimpleUploadedFile("third.txt", b"c", content_type="text/plain"),
                ]
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("files", serializer.errors)
