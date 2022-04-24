from django.contrib import admin

from .models import GLOBAL_MATERIALS
from .models import GLOBAL_COLOURS
# Register your models here.
admin.site.register(GLOBAL_MATERIALS)
admin.site.register(GLOBAL_COLOURS)