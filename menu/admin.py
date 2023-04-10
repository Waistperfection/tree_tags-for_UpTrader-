from django.contrib import admin

from .models import MenuItem
from .long_strings import menu_id_description


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("__str__", "parent", "slug", "url_path", "menu_id",)
    fieldsets = (
        (None, {"fields": ("data", "parent", "slug",)}),
        ("Название меню", {"fields": ("menu_id",),
                           "description": menu_id_description})
    )
    prepopulated_fields = {"slug": ("data",)}
