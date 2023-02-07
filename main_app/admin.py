from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from main_app.models import Account

# Register your models here.

class AccountAdmin(UserAdmin):
    # Account page setup
    list_display    = ('username', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields   = ('username', )
    readonly_fields = ('id', 'date_joined', 'last_login')

    # required fields
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Account, AccountAdmin)