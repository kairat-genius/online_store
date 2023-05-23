from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .forms import RatingForm, ReviewForm
from .models import Category, Rating, Reviews, Product
from django.core.cache import cache
from django.db.models import Count

# class Category:
#     """Категория"""
#
#     def get_category(self):
#         return Category.objects.all()
#
#     paginate_by = 1


class DataMixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = cache.get('cats')
        if not cats:
            cats = Category.objects.annotate(Count('tests'))
            cache.set('cats', cats, 60)
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context

class CategoryView(DataMixin, ListView):
    model = Product
    template_name = 'store/store_list.html'
    context_object_name = 'store_list'
    allow_empty = False

    def get_queryset(self):
        return Product.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk)
        return context | c_def


def test(request):
    return render(request, 'store/index.html')



class ProductView(Category, ListView):
    """Список Товаров"""
    model = Product
    queryset = Product.objects.filter(draft=False)
    paginate_by = 4
    template_name = "store/store_list.html"


class ProductDetailView(Category, DetailView):
    """описание Товаров"""
    model = Product
    queryset = Product.objects.filter(draft=False)
    slug_field = "url"
    template_name = "store/store_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        context["form"] = ReviewForm()
        return context


class FilterProductView(Category, ListView):
    """Фильтр Товаров"""
    paginate_by = 4
    template_name = 'store/store_list.html'

    def get_queryset(self):
        queryset = Product.objects.filter(
            Q(category__in=self.request.GET.getlist("category"))
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["category"] = ''.join([f"category={x}&" for x in self.request.GET.getlist("category")])
        return context


class JsonFilterMoviesView(ListView):
    """Фильтр товаров в json"""
    template_name = 'store/store_list.html'

    def get_queryset(self):
        queryset = Product.objects.filter(
            Q(genres__in=self.request.GET.getlist("category"))
        ).distinct().values("title", "url", "poster")
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"store": queryset}, safe=False)


class Search(Category, ListView):
    """Поиск ТОВАРОВ"""

    template_name = "store/store_list.html"

    def get_queryset(self, ):
        return Product.objects.filter(title__iregex=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context
