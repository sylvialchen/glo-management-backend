from hashlib import new
from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.views.generic.detail import DetailView

from .models import Chapter, Chapter_Stats, Sister, Pnm, Nickname_Request, Job_Opps_And_Referrals, Member_Experiences
from .serializers import ChapterSerializer, JobOppsAndReferralsSerializer, SistersSerializer, MemberExperiencesSerializer, ChapterStatsSerializer

from django.views.generic import ListView
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
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


@api_view(['PUT', 'DELETE'])
def chapters_detail(request, id):
    try:
        chapter = Chapter.objects.get(id=id)
    except Chapter.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ChapterSerializer(
            chapter, data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def jobs_list(request):
    if request.method == 'GET':
        data = Job_Opps_And_Referrals.objects.all()
        serializer = JobOppsAndReferralsSerializer(
            data, context={'request': request}, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = JobOppsAndReferralsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def sisters_list(request):
    if request.method == 'GET':
        data = Sister.objects.all()
        serializer = SistersSerializer(
            data, context={'request': request}, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SistersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'DELETE'])
def sisters_detail(request, id):
    try:
        sister = Sister.objects.get(id=id)
    except Sister.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = SistersSerializer(
            sister, data=request.data, context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # elif request.method == 'DELETE':
    #     sister.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def coach_list(request):
    if request.method == 'GET':
        data = Sister.objects.filter(coach_fg=True)
        serializer = SistersSerializer(
            data, context={'request': request}, many=True)
        return Response(serializer.data)
    # elif request.method == 'POST':
    #     serializer = SistersSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def experiences_list(request):
    if request.method == 'GET':
        experiences = Member_Experiences.objects.all()
        serializer = MemberExperiencesSerializer(
            experiences, context={'request': request}, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MemberExperiencesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)