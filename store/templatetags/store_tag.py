from django import template
from store.models import Category, Product
from ..forms import *

register = template.Library()


def get_all_categories():
    return Category.objects.all()


@register.simple_tag()
def get_list_category():
    """Вывод всех категорий"""
    return get_all_categories()


@register.inclusion_tag('include/sidebar.html')
def get_categories():
    category = get_all_categories()
    return {"list_category": category}


