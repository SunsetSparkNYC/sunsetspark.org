from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from .models import Workshop


class AccountDetail(TemplateView):
    template_name = "account_detail.html"


class WorkshopIndex(TemplateView):
    template_name = "workshop_index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['upcoming_workshops'] = Workshop.objects.order_by('-starts_at')
        return context


class WorkshopDetail(TemplateView):
    template_name = "workshop_detail.html"

    def get_context_data(self, slug, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workshop'] = Workshop.objects.get(slug=slug)
        return context
