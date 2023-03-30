from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated




def home(request):
    return render(request,'home.html')


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
                'message' : 'somethign went wrong',
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
                
            
            