from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme


class LoginUser(LoginView):
    def get_success_url(self):
        return self.get_redirect_url()

    def get_redirect_url(self):
        redirect_to = ''
        if self.request.user.has_perm('lib_app.view_book'):
            redirect_to = reverse_lazy('redaction')
        else:
            redirect_to = reverse_lazy('home')

        url_is_safe = url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),

        )

        return redirect_to if url_is_safe else reverse_lazy('login')
