from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('search/', views.Search.as_view(), name='search'),
    path('info/', include('help_services.urls')),
    path("review/<int:pk>/", views.AddReView.as_view(), name="add_review"),

    path('<slug:slug>/', views.ProductView.as_view(), name='list'),
    path('<slug:slug>/<slug:post_slug>/', views.ProductDetailView.as_view(), name='store_detail'),



    # path('comment/<int:pk>/', views.CreateComment.as_view(), name="create_comment"),
    # path('<slug:slug>/<slug:post_slug>/', views.PostDetailView.as_view(), name="post_single"),
    # path('<slug:slug>/', views.PostListView.as_view(), name="post_list"),
    # # path('', cache_page(60 * 15)(views.HomeView.as_view()), name='home'),
    # path('', views.HomeView.as_view(), name='home'),

]
