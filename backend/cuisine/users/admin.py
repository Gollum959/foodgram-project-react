from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Displaying the user model in the admin panel."""

    list_display = ('username', 'email', 'first_name', 'last_name', 'role')
    list_filter = ('username', 'email', )
    search_fields = ('username', 'email', )
    list_editable = ('role', )

    def save_model(self, request, obj, form, change):
        """Save or change objec - user."""

        if not change:
            obj.set_password(obj.password)
        elif User.objects.get(pk=obj.id).password != obj.password:
            obj.set_password(obj.password)
        obj.is_staff = True if obj.role == 'admin' else False
        obj.is_superuser = True if obj.role == 'admin' else False
        obj.save()
