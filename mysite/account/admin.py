from django.contrib import admin
from account.models import Account
from django.contrib.auth.admin import UserAdmin
from account.models import Video,Comment,Like

class AccountAdmin(UserAdmin):
    list_display=('phone','email','username','date_joined','last_login','is_admin','is_staff')
    search_fields=('phone','email','username')
    readonly_fields=('date_joined','last_login')

    filter_horizontal=()
    list_filter=()
    fieldsets=()

# Register your models here.
admin.site.register(Account, AccountAdmin)
admin.site.register(Comment)
admin.site.register(Video)
admin.site.register(Like)