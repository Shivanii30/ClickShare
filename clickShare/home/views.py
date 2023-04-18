from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.core.mail import send_mail







def contact(request):
    if request.method == "POST":
        try:
            email = request.POST.get("email")
            subject="Your Feedback was appreciated"
            message=f'Meow Meow'
            email_from= settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject,message,email_from,recipient_list)
            print(email,recipient_list,subject)
            return render(request,'success.html')
        except Exception as e:
            print(e)
            return render(request,'error.html')
    
    
    
    
    
    return render(request,'contact.html')

def home(request):
    return render(request,'home.html')

def error(request):
    return render(request,'error.html')



def sendEmail(request):
    if request.method == "POST":
        try:
            email = request.POST.get("email")
            message=request.POST.get("comment")
            subject="Appreciation for Feedback"
            email_from= settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject,message,email_from,recipient_list)
            print(email,recipient_list,subject,message)
            return render(request,'success.html')
        except Exception as e:
            print(e)
            return render(request,'error.html')
    
    # return render(request,'error.html')
    
    
    
    return render(request,'email.html')

def download(request, uid):
    return render(request, 'download.html',context = {'uid':uid})


class Handle_Uploaded_Files(APIView):
    parser_classes = [MultiPartParser]
    def post(self , request):
        try:
            data = request.data

            serializer = FileListSerializer(data = data)
        
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status' : 200,
                    'message' : 'files uploaded successfully',
                    'data' : serializer.data
                })
            
            return Response({
                'status' : 400,
                'message' : 'something went wrong',
                'data'  : serializer.errors
            })
        except Exception as e:
            print(e)


        
    
    # def get(self,request):
        
    #     try:
    #         # print(data)
    #         return Response({
    #             "status":200,
    #             "message":"success"
    #         })
    #     except Exception as e:
    #         print(e)
                
            
            