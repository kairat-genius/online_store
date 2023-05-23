
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductView.as_view(), name='store_list'),
    path('filter/', views.FilterProductView.as_view(), name='filter'),
    path('search/', views.Search.as_view(), name='search'),
    path("json-filter/", views.JsonFilterMoviesView.as_view(), name='json_filter'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='store_detail'),
    path('<slug:cat_slug>/', views.CategoryView.as_view(), name='category')
]
