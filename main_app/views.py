from hashlib import new
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from .models import Chapter, Sister, Pnm, Nickname_Request
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .serializers import ChapterSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
# from rest_framework import viewsets


# Serialized Views
@api_view(['GET', 'POST'])
def chapters_list(request):
    if request.method == 'GET':
        data = Chapter.objects.all()
        serializer = ChapterSerializer(
            data, context={'request': request}, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ChapterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # class ChapterView(LoginRequiredMixin, viewsets.ModelViewSet):
        #     serializer_class = ChapterSerializer
        #     queryset = Chapter.objects.all()

        # Define the home view
