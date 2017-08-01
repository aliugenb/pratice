from django.contrib import admin
from models import Event,Guest

# Register your models here.

# 通知Admin管理工具为这些模块提供界面
admin.site.register(Event)
admin.site.register(Guest)