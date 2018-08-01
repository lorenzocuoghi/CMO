from django.contrib import admin
from . import models
from .models import CompiledField, Field


class FieldInline(admin.StackedInline):
    model = Field


class DocumentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['titolo']}),
        ('Data di pubblicazione', {'fields': ['pub_date'], 'classes': ['collapse']}),
        (None, {'fields': ['content']}),
    ]
    inlines = [FieldInline]
    list_display = ('titolo', 'pub_date')
    list_filter = ['pub_date', 'titolo']
    search_fields = ['titolo']


class CompiledFieldInline(admin.StackedInline):
    model = CompiledField


class CompiledDocAdmin(admin.ModelAdmin):
    inlines = [CompiledFieldInline]
    list_display = ('document', 'date')
    list_filter = ['document']
    search_fields = ['document']


admin.site.register(models.Document, DocumentAdmin)
admin.site.register(models.CompiledDoc, CompiledDocAdmin)
