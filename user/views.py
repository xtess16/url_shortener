from django.contrib.auth.views import LoginView as SuperLoginView, LogoutView as SuperLogoutView
from django.urls import reverse
from django.views.generic import FormView
from shortener.models import URL
from user.forms import SignupForm, LoginForm


class SignupView(FormView):
    template_name = 'signup.html'
    form_class = SignupForm

    def get_success_url(self):
        return reverse('index')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.generate_email_token(commit=False)
        user.save()
        # TODO: отправить письмо на почту
        return super().form_valid(form)


class LoginView(SuperLoginView):
    template_name = 'login.html'
    authentication_form = LoginForm

    def get_success_url(self):
        if not URL.objects.filter(owner=self.request.user).exists():
            return reverse('create_link')
        return super().get_success_url()


class LogoutView(SuperLogoutView):
    next_page = 'login'
