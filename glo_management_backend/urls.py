from django.contrib import admin
# Add the include function to the import
from django.urls import path, include
from main_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # In this case '' represents the root route
    path('', include('main_app.urls')),
    path('api/chapters/', views.chapters_list),
    path('api/chapters/edit/<int:id>', views.chapters_detail),
    path('api/jobs/', views.jobs_list),
    path('api/sisters/', views.sisters_list),
    path('api/sisters/edit/<int:id>', views.sisters_detail),
    path('api/experiences', views.experiences_list)
]
