from django.contrib import admin

from .models import MATERIAL_GLOBAL
from .models import COLOUR_GLOBAL
# Register your models here.
admin.site.register(MATERIAL_GLOBAL)
admin.site.register(COLOUR_GLOBAL)