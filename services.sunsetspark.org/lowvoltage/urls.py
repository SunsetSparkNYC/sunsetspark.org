from django.urls import path

from . import views

urlpatterns = [
    path("account/", views.AccountDetail.as_view(), name="account-detail"),
    path("workshops/", views.WorkshopIndex.as_view(), name="workshop-index"),
    path("workshops/<slug:slug>/", views.WorkshopDetail.as_view(), name="workshop-detail"),
]
