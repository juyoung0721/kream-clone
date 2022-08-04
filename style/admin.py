from django.contrib import admin
from .models import Style, Photo


class PhotoInline(admin.StackedInline):
    model = Photo
    extra = 5


@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    inlines = [
        PhotoInline,
    ]
    list_display = (
        "__str__",
        "count_products",
    )
    filter_horizontal = ("products",)
