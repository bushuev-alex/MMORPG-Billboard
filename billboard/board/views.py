from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.translation import gettext
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse, reverse_lazy
from django.http import Http404, HttpResponse
from django.views import View
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.conf import settings

from datetime import datetime
import pytz
from pprint import pprint

# from rest_framework import viewsets
# from rest_framework import permissions

from board.filters import FeedbackFilter
from board.forms import FeedbackForm, AdvertisementForm
# from board.utils import too_many_posts, msg
# from board.signals import notify_about_new_creation, printer2
# from board.tasks import printer
# from board.serializers import *

from board.models import *


# LIST OF ADs
class AdList(ListView):
    model = Advertisement  # Указываем модель, объекты которой мы будем выводить
    ordering = '-date_time'  # Поле, которое будет использоваться для сортировки объектов
    template_name = 'ads.html'  # Указываем имя шаблона, в котором будут все инструкции о том, # как именно пользователю должны быть показаны наши объекты
    context_object_name = 'ads'  # Это имя списка, в котором будут лежать все объекты. # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = timezone.now()
        return context


# CREATE
class AdCreate(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    permission_required = ('board.add_advertisement',)
    form_class = AdvertisementForm
    model = Advertisement
    template_name = "ads_edit.html"

    def form_valid(self, form):
        advertisement = form.save(commit=True)


        # if too_many_posts(model=self.model, post=post):
        #     return HttpResponse(msg)
        # else:
        # notify_about_new_creation.delay(post.pk)
        return super().form_valid(form)


# DETAIL AD
class AdDetail(DetailView):
    model = Advertisement
    template_name = 'ads_by_id.html'
    context_object_name = 'ads'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Feedback.objects.filter(advertisement=self.kwargs['pk']).order_by('-date_time')
        context['form'] = FeedbackForm
        return context

    def post(self, request, *args, **kwargs):
        text = request.POST.get("text")
        user = request.user
        Feedback.objects.create(advertisement=self.model.objects.filter(id=self.kwargs['pk'])[0],
                                user=user,
                                text=text)
        return redirect(f"/board/{self.kwargs['pk']}/")


# LIST OF Comments
class Comments(LoginRequiredMixin, ListView):
    model = Feedback
    ordering = "-date_time"
    template_name = 'comments.html'
    context_object_name = 'comments'
    paginate_by = 20

    def get_queryset(self):
        # queryset = super().get_queryset()
        queryset = self.model.objects.filter(advertisement__author__user=self.request.user)
        self.filterset = FeedbackFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = timezone.now()
        # context['models'] = self.model.objects.all()
        context['filterset'] = self.filterset
        return context


# ACCEPT
@login_required
def accept(request, pk):
    comment = Feedback.objects.get(id=pk)
    comment.accepted = True
    comment.save()
    message = "You successfully accept a comment"
    return redirect('comments')


# DELETE
@login_required
def delete(request, pk):
    comment = Feedback.objects.get(id=pk)
    comment.delete()
    message = "You successfully delete a comment"
    return redirect('comments')
