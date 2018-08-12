from django.contrib import admin
from . import models
from .models import CompiledField, Field


class FieldInline(admin.StackedInline):
    model = Field
    extra = 0


class DocumentAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['titolo']}),
        ('Data di pubblicazione', {'fields': ['date'], 'classes': ['collapse']}),
        (None, {'fields': ['content']}),
    ]
    inlines = [FieldInline]
    list_display = ('titolo', 'date')
    list_filter = ['date', 'titolo']
    search_fields = ['titolo']


class CompiledFieldInline(admin.StackedInline):
    model = CompiledField
    extra = 0


class CompiledDocAdmin(admin.ModelAdmin):
    inlines = [CompiledFieldInline]
    list_display = ('document', 'date')
    list_filter = ['document']
    search_fields = ['document']


admin.site.register(models.Document, DocumentAdmin)
admin.site.register(models.CompiledDoc, CompiledDocAdmin)
