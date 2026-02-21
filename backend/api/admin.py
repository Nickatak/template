from django.contrib import admin
from django.contrib.admin.forms import AdminAuthenticationForm

from .models.user import CustomUser


class EmailAdminAuthenticationForm(AdminAuthenticationForm):
    """Use email wording on the admin login form for custom email auth."""

    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        self.fields["username"].label = "Email"


admin.site.login_form = EmailAdminAuthenticationForm
admin.site.register(CustomUser)
