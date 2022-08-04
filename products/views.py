from math import ceil
from django.shortcuts import redirect, render
from django.utils import timezone
from django.core.paginator import Paginator
from django.views.generic import ListView
from .models import Product

# 장고만 사용하는 경우
class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 15
    # ordering = ["created"]
    # paginate_orphans = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        context["product_count"] = Product.objects.count()
        return context

    # 글자순으로 정렬 (-붙이면 반대로)
    # def get_queryset(self):
    #     return Product.objects.order_by("-name_en")


# 장고와 파이썬을 활용한 경우
# def products_list(request):
#     page = int(request.GET.get("page", 1))
#     # 파이썬만 사용한 경우
#     # page_size = 10
#     # limit = page_size * page
#     # offset = limit - page_size
#     # page_count = ceil(Product.objects.count() / page_size)
#     # products = Product.objects.all()[offset:limit]
#     # if page > page_count:
#     #     return redirect("/products")

#     product_list = Product.objects.all()
#     paginator = Paginator(product_list, 13)
#     products = paginator.get_page(page)

#     # html에서 사용하는 변수설정
#     return render(
#         request,
#         "products_list.html",
#         {
#             "products": products,
#             "page": page,
#         },
#     )
