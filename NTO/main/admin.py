from django.contrib import admin
from .models import ShareInfo
# Register your models here.


@admin.register(ShareInfo)
class ShareInfoAdmin(admin.ModelAdmin):
    fields = ('name', 'info')