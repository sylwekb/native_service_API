from django.contrib import admin
from .models import NativePost, FinalPricing

admin.register(admin)
admin.site.register(NativePost)
admin.site.register(FinalPricing)

