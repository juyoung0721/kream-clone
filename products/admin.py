from django.contrib import admin
from .models import Brand, Photo, Product


class PhotoInline(admin.StackedInline):
    model = Photo
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    inlines = [
        PhotoInline,
    ]
    list_display = (
        "brand",
        "name_en",
        "name_kr",
    )

    search_fields = (
        "brand__name",
        "name_en",
        "name_kr",
    )


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass
