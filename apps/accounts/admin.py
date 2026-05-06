# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.models import User
# from .models import UserProfile


# class ProfileInline(admin.StackedInline):
#     model = UserProfile
#     can_delete = False


# class CustomUserAdmin(UserAdmin):
#     inlines = [ProfileInline]


# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class ProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline]

    list_display = (
        "username",
        "email",
        # "get_phone",
        "is_active",
        # "is_staff",
        "date_joined",
    )

    search_fields = ("username", "email")
    list_filter = ("is_active", "is_staff")
    ordering = ("-date_joined",)

    def get_phone(self, obj):
        return obj.userprofile.phone if hasattr(obj, "userprofile") else "-"
    
    get_phone.short_description = "Phone"


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)