import datetime
import os, random, json
from django.conf import settings
from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404
from basketapp.models import Basket
from .models import Product, ProductCategory


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)



def get_hot_product():
    products_list = Product.objects.all()
    return random.sample(list(products_list), 1)[0]

def get_same_products(hot_product):
    return Product.objects.filter(category__pk=hot_product.category.pk).exclude(pk=hot_product.pk)[:3]

def main(request):
    title = 'Главная'
    # products = Product.objects.all()[:3]
    # products = Product.objects.filter(is_active=True, category__is_active=True)[:3]
    products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')[:3]
    content = {'title': title,
               'products': products,
               }
    return render(request, 'mainapp/index.html', content)

def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk)

def products(request, pk=None, page=1):
    title = 'продукты'
    # links_menu = ProductCategory.objects.filter(is_active=True)
    links_menu = get_links_menu()
    if pk is not None:
        if pk == 0:
            category = {'name': 'все', 'pk': 0}
            products = Product.objects.filter(is_active=True).order_by('price')
        else:
            category = get_category(pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')

        paginator = Paginator(products, 2)
        try:
            products_paginator = paginator.page(page)
        except PageNotAnInteger:
            products_paginator = paginator.page(1)
        except EmptyPage:
            products_paginator = paginator.page(paginator.num_pages)


        content = {
            'title': title,
            'links_menu': links_menu,
            'category': category,
            'products': products_paginator,
        }
        return render(request, 'mainapp/products_list.html', content)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    content = {'title': title,
               'links_menu': links_menu,
               'same_products': same_products,
               'hot_product': hot_product,
               }
    return render(request, 'mainapp/products.html', content)


def product(request, pk):
    title = 'продукты'

    content = {
        'title': title,
        'links_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
    }

    return render(request, 'mainapp/product.html', content)


def contact(request):
    title = 'О нас'
    visit_date = datetime.datetime.now()
    locations = []
    file_path = os.path.join(settings.BASE_DIR, 'contacts.json')
    with open((file_path), encoding='utf-8') as file_contacts:
        locations = json.load(file_contacts)
    content = {'title': title,
               'visit_date': visit_date,
               'locations': locations,
               }
    return render(request, 'mainapp/contact.html', content)

def products_all(request):
    links_menu = [
        {'href': 'products_all', 'name': 'все'},
        {'href': 'products_home', 'name': 'дом'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_classic', 'name': 'классика'},
    ]
    content = {
        'title': 'Продукты',
        'links_menu': links_menu
    };
    return render(request, 'mainapp/products.html', content)

def products_home(request):
    links_menu = [
        {'href': 'products_all', 'name': 'все'},
        {'href': 'products_home', 'name': 'дом'},
        {'href': 'products_office', 'name': 'офис'},
        {'href': 'products_modern', 'name': 'модерн'},
        {'href': 'products_classic', 'name': 'классика'},
    ]
    content = {
        'title': 'Продукты',
        'links_menu': links_menu
    };
    return render(request, 'mainapp/products.html', content)

