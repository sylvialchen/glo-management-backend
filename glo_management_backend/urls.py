from django.contrib import admin
# Add the include function to the import
from django.urls import path, include
from main_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # In this case '' represents the root route
    path('', include('main_app.urls')),
    path('api/accounts/', include('authemail.urls'))
    # path('accounts/', include('django.contrib.auth.urls'))
]
