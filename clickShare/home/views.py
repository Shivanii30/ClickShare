import logging

from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Folder
from .serializers import FileListSerializer

logger = logging.getLogger(__name__)


def index(request):
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


def error(request):
    return render(request, "error.html")


def healthcheck(request):
    return JsonResponse({"status": "ok"})


def contact(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        message = request.POST.get("comment", "").strip()

        try:
            send_mail(
                "Your feedback was appreciated",
                message,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return render(request, "success.html")
        except Exception:
            logger.exception("Failed to send contact email to %s", email)
            return render(request, "error.html")

    return render(request, "contact.html")


def sendEmail(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        try:
            send_mail(
                "Appreciation for feedback",
                "Demo Email",
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
        except Exception:
            logger.exception("Failed to send demo email to %s", email)
            return render(request, "error.html")

    return render(request, "error.html")


def download(request, uid):
    folder = get_object_or_404(Folder, uid=uid)
    return render(
        request,
        "download.html",
        context={"uid": folder.uid, "zip_url": folder.zip_url},
    )


class Handle_Uploaded_Files(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        serializer = FileListSerializer(data=request.data)
        if serializer.is_valid():
            try:
                payload = serializer.save()
            except Exception:
                logger.exception("Upload pipeline failed")
                return Response(
                    {
                        "status": 500,
                        "message": "We could not finish creating your download bundle.",
                        "data": {},
                    },
                    status=status.HTTP_502_BAD_GATEWAY,
                )

            return Response(
                {
                    "status": 200,
                    "message": "Files uploaded successfully.",
                    "data": payload,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {
                "status": 400,
                "message": "Upload failed.",
                "data": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
