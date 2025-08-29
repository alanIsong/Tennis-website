from django.views.generic import ListView
from django.db.models import Q
from shop.models import Product


class SearchResultsListView(ListView):
    model = Product
    context_object_name = "results"
    template_name = "search_app/results.html" 


    def get_queryset(self):
        query = self.request.GET.get("q", "").strip()
        if not query:
            return Product.objects.none()
        return Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q", "").strip()
        context["search_query"] = query
        context["results_count"] = self.object_list.count()
        return context
