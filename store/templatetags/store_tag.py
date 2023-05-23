from django import template
from store.models import *


register = template.Library()


@register.inclusion_tag('store/tags/last_store.html')
def get_last_store(count=5):
    store = Product.objects.order_by("id")[:count]
    return {"last_store": store}


@register.simple_tag(name='getcats')
def get_categories(filter=None):
    if not filter:
        return Category.objects.all()
    else:
        return Category.objects.filter(pk=filter)

@register.inclusion_tag('store/tags/list_category.html')
def show_categories(sort=None, cat_selected=0):
    if not sort:
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)

    return {"cats": cats, "cat_selected": cat_selected}



