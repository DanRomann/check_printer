from django.contrib import admin
from .models import *


# Register your models here.
class PrinterAdmin(admin.ModelAdmin):
    list_display = ('name', 'api_key', 'check_type', 'point_id')


class CheckAdmin(admin.ModelAdmin):
    list_display = ('printer_id', 'type', 'order', 'status')


admin.site.register(Printer, PrinterAdmin)
admin.site.register(Check, CheckAdmin)