from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.urls import reverse
from django.views.generic import ListView, CreateView, RedirectView as SuperRedirectView, DetailView

from shortener.forms import CreateLinkForm
from shortener.models import URL, Transition


class IndexView(LoginRequiredMixin, ListView):
    template_name = 'index.html'
    context_object_name = 'links'

    def get_queryset(self):
        return URL.objects.filter(owner=self.request.user).order_by('-created_at')


class CreateLinkView(LoginRequiredMixin, CreateView):
    template_name = 'create_link.html'
    form_class = CreateLinkForm

    def get_success_url(self):
        return reverse('index')

    def form_valid(self, form):
        print('form valid')
        url = form.save(commit=False)
        url.owner = self.request.user
        url.generate_short_link(commit=False)
        url.save()
        return super().form_valid(form)


class LinkDetailView(LoginRequiredMixin, DetailView):
    template_name = 'link_detail.html'
    model = URL
    context_object_name = 'link'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.owner != self.request.user:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transitions'] = self.object.transition_set.order_by('-transition_datetime')[:10]
        return context


class RedirectView(SuperRedirectView):
    http_method_names = ['get']

    def get_redirect_url(self, *args, **kwargs):
        short_link = kwargs['short_link']
        print(self.request.META.get('HTTP_X_FORWARDED_FOR'))
        try:
            if len(short_link) != URL.short_link_length:
                raise Http404
            url = URL.objects.get(short_link=short_link)
        except ObjectDoesNotExist:
            raise Http404
        else:
            transition = Transition(ip=self.request.META.get('REMOTE_ADDR', ''), url=url)
            transition.set_location(commit=False)
            transition.save()
            return url.full_link
