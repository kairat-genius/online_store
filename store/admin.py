from django.contrib import admin

from .models import Category, ProductShots, Rating, RatingStar, Reviews, Product, Available

from django import forms

from django.utils.safestring import mark_safe





@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Available)
class AvailableAdmin(admin.ModelAdmin):
    """Наличие товара"""

    list_display = ("name",)
    list_display_links = ("name",)

class ReviewInline(admin.TabularInline):
    """Отзывы на странице товара"""
    model = Reviews
    extra = 1
    readonly_fields = ("name", "email")


class ProductShotsInline(admin.TabularInline):
    model = ProductShots
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" height="110"')

    get_image.short_description = "Изображение"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Товары"""
    list_display = ("title", "category", "slug", "draft", "available")
    list_filter = ("category",)
    search_fields = ("title", "category__name")
    inlines = [ProductShotsInline, ReviewInline]
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    actions = ["publish", "unpublish"]
    readonly_fields = ("get_image",)
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        (None, {
            "fields": (("title", "price"),)
        }),
        (None, {
            "fields": ("characteristic", "description", "poster")
        }),
        ("Options", {
            "fields": (("slug", "draft", "available", "category"),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="250" height="358"')


    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ('change', )

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ('change',)

    get_image.short_description = "Постер"


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы"""
    list_display = ("name", "email", "parent", "product", "id", "time_create", "avatar")
    readonly_fields = ("name", "email")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("star", "product", "ip")


@admin.register(ProductShots)
class ProductShotsAdmin(admin.ModelAdmin):

    list_display = ("product", "get_image")
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Изображение"


admin.site.register(RatingStar)

admin.site.site_title = "Django Movies"
admin.site.site_header = "Django Movies"
