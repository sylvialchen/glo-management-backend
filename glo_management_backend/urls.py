from django.contrib import admin
# Add the include function to the import
from django.urls import path, include, re_path
from main_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # In this case '' represents the root route
    path('', include('main_app.urls')),
    re_path(r'^api/chapters/$', views.chapters_list),
    re_path(r'^api/jobs/$', views.jobs_list),
    re_path(r'^api/sisters/$', views.sisters_list),
]
