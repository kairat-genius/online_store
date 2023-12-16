from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('feedback/', views.ContactFormView.as_view(), name='feedback'),
    path('delivery/', views.delivery, name='delivery'),
    path('basket/', views.basket, name='basket'),
    path('contact/', views.contact, name='contact'),
    path('answer/', views.AnswerViews.as_view(), name='answer'),
]
