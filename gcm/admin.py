from django.contrib import admin

from gcm.utils import get_device_model

Device = get_device_model()


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ['dev_id', 'dev_type', 'modified_date', 'is_active']
    search_fields = ('dev_id', 'dev_type')
    list_filter = ['is_active']
    date_hierarchy = 'modified_date'
    readonly_fields = ('dev_id', 'reg_id')
