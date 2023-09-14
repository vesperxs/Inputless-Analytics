from django.urls import path
from . import views

urlpatterns = [
    path("checkout", views.checkout, name="checkout"),
    path("create-sub", views.create_sub, name="create_sub"),	
    path("billing", views.billing_view, name="billing"),	
    path("complete", views.complete, name="complete"),
    path("convert", views.convert, name="convert"), 
    path("cancel", views.cancel, name="cancel"),
]
