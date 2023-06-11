from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from store.models import Product
from tag.models import TagItem
from store.admin import ProductAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", 'email', 'first_name', 'last_name'),
            },
        ),
    )

class CustomTagItemAdmin(GenericTabularInline):
    model = TagItem
    autocomplete_fields = ['tag']


class CustomProductAdmin(ProductAdmin):
    inlines = [CustomTagItemAdmin]

admin.site.unregister(Product)
admin.site.register(Product, CustomProductAdmin)


    
    


