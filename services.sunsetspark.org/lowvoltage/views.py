from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Workshop


class AccountDetail(TemplateView):
    template_name = "account_detail.html"

    def signup_or_login():
        pass
        # if user exists, send an auth token to sign up
        # if user does not exist, create user, login for them, send auth token as verification


class WorkshopIndex(TemplateView):
    template_name = "workshop_index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workshops'] = Workshop.objects.upcoming_workshops()
        return context


class WorkshopDetail(TemplateView):
    template_name = "workshop_detail.html"

    def get_context_data(self, slug, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workshop'] = Workshop.objects.get(slug=slug)
        return context
