import mimetypes

import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible


@deconstructible
class SupabaseStorage(Storage):
    def _headers(self, content_type=None):
        headers = {
            "apikey": settings.SUPABASE_SERVICE_ROLE_KEY,
            "Authorization": f"Bearer {settings.SUPABASE_SERVICE_ROLE_KEY}",
            "x-upsert": "true",
        }
        if content_type:
            headers["Content-Type"] = content_type
        return headers

    def _object_url(self, name):
        return (
            f"{settings.SUPABASE_URL}/storage/v1/object/"
            f"{settings.SUPABASE_STORAGE_BUCKET}/{name}"
        )

    def _save(self, name, content):
        if hasattr(content, "seek"):
            content.seek(0)
        name = name.replace("\\", "/")  # Ensure consistent path separators

        payload = content.read()
        if isinstance(payload, str):
            payload = payload.encode("utf-8")

        content_type = getattr(content, "content_type", None)
        if not content_type:
            content_type = mimetypes.guess_type(name)[0] or "application/octet-stream"

        response = requests.post(
            self._object_url(name),
            headers=self._headers(content_type=content_type),
            data=payload,
            timeout=30,
        )
        response.raise_for_status()
        return name

    def get_available_name(self, name, max_length=None):
        return name

    def delete(self, name):
        response = requests.delete(
            self._object_url(name),
            headers=self._headers(),
            timeout=30,
        )
        if response.status_code not in (200, 204, 404):
            response.raise_for_status()

    def exists(self, name):
        return False

    def size(self, name):
        response = requests.head(
            self._object_url(name),
            headers={
                "apikey": settings.SUPABASE_SERVICE_ROLE_KEY,
                "Authorization": f"Bearer {settings.SUPABASE_SERVICE_ROLE_KEY}",
            },
            timeout=15,
        )
        response.raise_for_status()
        return int(response.headers.get("Content-Length", 0))

    def url(self, name):
        return (
            f"{settings.SUPABASE_URL}/storage/v1/object/public/"
            f"{settings.SUPABASE_STORAGE_BUCKET}/{name}"
        )

    def open(self, name, mode="rb"):
        response = requests.get(self.url(name), timeout=30)
        response.raise_for_status()
        return ContentFile(response.content, name=name)
