from django.db import models
from django.urls import reverse


class Category(models.Model):
    """категория"""
    name = models.CharField("Категория", max_length=150)
    slug = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категория'
        ordering = ['id']


class Available(models.Model):
    """наличие товара"""
    name = models.CharField("Наличие товара", max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Наличие товара'
        verbose_name_plural = 'Наличие товара'


class Product(models.Model):
    """Товар"""
    title = models.CharField("Название товара", max_length=200)
    description = models.TextField("Описание")
    characteristic = models.TextField("Характеристика")
    poster = models.ImageField("Постер", upload_to="product/")
    price = models.PositiveIntegerField("Цена", default=0, help_text="указывать сумму в сомах")
    category = models.ForeignKey(
        Category, verbose_name="Категория", on_delete=models.PROTECT)

    available = models.ForeignKey(Available, verbose_name='Наличие товара', on_delete=models.SET_NULL, null=True)
    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField("Черновик", default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("store_detail", kwargs={"slug": self.url})


    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class ProductShots(models.Model):
    """Доп постеры"""
    title = models.CharField("Заголовок", max_length=100, default="Photo")
    image = models.ImageField("Изображение", upload_to="product_shots/")
    product = models.ForeignKey(Product, verbose_name="Товары", on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Изображение"
        verbose_name_plural = "Изображение"


class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.SmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ["-value"]


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="звезда")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="товар", related_name="ratings")

    def __str__(self):
        return f"{self.star} - {self.product}"

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Reviews(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
    )
    product = models.ForeignKey(Product, verbose_name="товар", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.product}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
