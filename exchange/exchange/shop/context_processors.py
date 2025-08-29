from .models import Category


def menu_links(request):
    categories = Category.objects.all().order_by("name")
    return {"categories": categories}
