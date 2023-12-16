from django.db.models import Q
from django.shortcuts import render
from django.views.generic import ListView, DetailView, View
from .models import Product
from .forms import *
from django.shortcuts import redirect
from PIL import Image


class HomeView(ListView):
    """ОБщий список товаров"""
    model = Product
    paginate_by = 9
    template_name = "store/store_category_list.html"

    def get_queryset(self):
        # Получаем слаг категории из URL
        category_slug = self.kwargs.get("slug")

        # Получаем параметры фильтрации из GET-параметров запроса
        price_min = self.request.GET.get("price_min")
        price_max = self.request.GET.get("price_max")
        # Начинаем с базового запроса к базе данных для получения недоработанных товаров в указанной категории
        queryset = Product.objects.filter(draft=False)

        # Применяем фильтры на основе параметров
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Добавляем форму фильтрации в контекст
        context['filter_form'] = ProductFilterForm(self.request.GET)

        return context


class ProductView(ListView):
    """Список товаров по категорий"""
    model = Product
    template_name = "store/store_category_list.html"
    paginate_by = 10  # Количество товаров на странице (пагинация)

    def get_queryset(self):
        # Получаем слаг категории из URL
        category_slug = self.kwargs.get("slug")

        # Получаем параметры фильтрации из GET-параметров запроса
        price_min = self.request.GET.get("price_min")
        price_max = self.request.GET.get("price_max")
        # Начинаем с базового запроса к базе данных для получения недоработанных товаров в указанной категории
        queryset = Product.objects.filter(draft=False, category__slug=category_slug).select_related('category')

        # Применяем фильтры на основе параметров
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Добавляем форму фильтрации в контекст
        context['filter_form'] = ProductFilterForm(self.request.GET)

        return context

    # def get_queryset(self):
    #     return Product.objects.filter(draft=False, category__slug=self.kwargs.get("slug")).select_related('category')


class ProductDetailView(DetailView):
    """описание Товаров"""
    model = Product
    template_name = "store/store_detail.html"
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Добавляем форму фильтрации в контекст
        context['form'] = ReviewForm(self.request.GET)

        return context


class Search(ListView):
    """Поиск ТОВАРОВ"""
    template_name = "store/store_category_list.html"

    def get_queryset(self, ):
        return Product.objects.filter(
            Q(title__iregex=self.request.GET.get("q"))
            |
            Q(description__iregex=self.request.GET.get("q"))
        )

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = self.request.GET.get("q")
        return context


class AddReView(View):
    """Добавление отзыва"""

    template_name = "store/store_detail.html"

    # def post(self, request, pk):
    #     form = ReviewForm(request.POST)
    #     product = Product.objects.get(id=pk)
    #
    #     if form.is_valid():
    #         review = form.save(commit=False)
    #
    #         # Получаем parent_id из данных POST
    #         parent_id = request.POST.get("parent", None)
    #
    #         if parent_id:
    #             try:
    #                 parent_review = Reviews.objects.get(id=int(parent_id))
    #                 review.parent = parent_review
    #             except Reviews.DoesNotExist:
    #                 pass  # Обработка случая, когда отзыв с указанным parent_id не существует
    #
    #         # Связываем отзыв с продуктом и сохраняем его в базе данных
    #         review.product = product
    #         review.save()
    #
    #     return redirect(product.get_absolute_url())

    def post(self, request, pk):
        form = ReviewForm(request.POST, request.FILES)
        product = Product.objects.get(id=pk)
        parent_user = None  # Инициализируем переменную для имени пользователя

        if form.is_valid():
            review = form.save(commit=False)

            # Получаем parent_id из данных POST
            parent_id = request.POST.get("parent", None)

            if parent_id:
                try:
                    parent_review = Reviews.objects.get(id=int(parent_id))
                    review.parent = parent_review
                    parent_user = parent_review.name  # Получаем имя пользователя
                except Reviews.DoesNotExist:
                    pass  # Обработка случая, когда отзыв с указанным parent_id не существует

            # Связываем отзыв с продуктом и обновляем текст комментария
            review.product = product
            review.text = f"{parent_user}, {review.text}"  # Добавляем имя пользователя в текст комментария
            review.save()

            if review.avatar:
                max_size = (60, 60)
                image = Image.open(review.avatar.path)
                image.thumbnail(max_size)
                image.save(review.avatar.path)

        return render(request, self.template_name, {'form': form, 'parent_user': parent_user, 'product': product})

    # def post(self, request, pk):
    #     form = ReviewForm(request.POST)
    #     product = Product.objects.get(id=pk)
    #
    #     if form.is_valid():
    #         review = form.save(commit=False)
    #         review.product = product
    #
    #         # Получаем parent_id из данных POST
    #         parent_id = request.POST.get("parent_id")
    #
    #         if parent_id:
    #             try:
    #                 parent_review = Reviews.objects.get(id=int(parent_id))
    #                 review.parent = parent_review
    #             except Reviews.DoesNotExist:
    #                 pass  # Обработка случая, когда отзыв с указанным parent_id не существует
    #
    #         review.save()
    #
    #     return redirect(product.get_absolute_url())
