from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from .models import Category, Product


def prod_list(request, category_id=None):
    category = None
    products = Product.objects.filter(available=True)
    if category_id:
        category = get_object_or_404(Category, id=category_id)
        products = products.filter(category=category)

    paginator = Paginator(products, 6)
    page_number = request.GET.get("page", 1)
    try:
        products_page = paginator.page(page_number)
    except (EmptyPage, InvalidPage):
        products_page = paginator.page(paginator.num_pages)

    return render(
        request,
        "shop/products.html",   # ✅ match your actual template
        {"category": category, "products": products_page},
    )


def menu_links(request):
    categories = Category.objects.all().order_by("name")
    return {"categories": categories}


def product_detail(request, category_id, product_id):
    product = get_object_or_404(Product, category_id=category_id, id=product_id)
    return render(request, "shop/product.html", {"product": product})


def category_list(request):
    categories = Category.objects.all().order_by("name")
    return render(request, "shop/categories.html", {"categories": categories})  # ✅ match your template


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category, available=True)
    return render(
        request,
        "shop/category_items.html",   # ✅ match your template
        {"category": category, "products": products},
    )
