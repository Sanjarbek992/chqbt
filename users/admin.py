from django.contrib import admin
from django.utils.html import format_html
from .models import CustomUser, UserProfile, MilitaryRank
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


@admin.register(MilitaryRank)
class MilitaryRankAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profil'
    fk_name = 'user'
    extra = 0
    fieldsets = (
        (None, {
            'fields': (
                'school', 'middle_name', 'military_rank', 'jshir',
                'department', 'birth_date', 'birth_place',
                'phone', 'passport_series', 'profile_image', 'image_preview'
            )
        }),
    )
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover; border-radius: 8px;">', obj.profile_image.url)
        return "—"
    image_preview.short_description = 'Rasm'


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    inlines = [UserProfileInline]
    list_display = ('username', 'first_name', 'last_name', 'role', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name')
    ordering = ('username',)
    readonly_fields = ['date_joined', 'last_login']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Shaxsiy maʼlumotlar', {'fields': ('first_name', 'last_name', 'role')}),
        ('Ruxsatlar', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Muhim sanalar', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'role', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser')}
        ),
    )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)
