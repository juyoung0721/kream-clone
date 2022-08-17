from math import ceil
from django.shortcuts import redirect, render
from django.utils import timezone
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from .models import Product
from products import forms
from django.db.models import Q

# 장고만 사용하는 경우
class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 16
    ordering = ["created"]
    paginate_orphans = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["now"] = timezone.now()
        return context


def detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
        return render(request, "products/detail.html", {"product": product})
    except Product.DoesNotExist:
        return redirect("/products")


class ProductDetail(DetailView):
    model = Product


def search(request):
    keyword = request.GET.get("keyword", None)
    price = request.GET.getlist("price", None)
    brands = request.GET.getlist("brands", None)
    form = forms.SearchForms(request.GET)
    q = Q()
    filter_args = {}
    if form.is_valid():
        if len(brands) > 0:
            filter_args["brand__id__in"] = brands

        if len(price) > 0:

            if "-100000" in price:  # lt gt는 초과라는 뜻
                q.add(Q(released_price__lt=100000), q.OR)
            if "100000-300000" in price:
                q.add(Q(released_price__gt=100000, released_price__lt=300000), q.OR)
            if "300000-500000" in price:
                q.add(Q(released_price__gt=300000, released_price__lt=500000), q.OR)
            if "500000-" in price:
                q.add(Q(released_price__gt=500000), q.OR)
            # result = Product.objects.filter(q)

        if keyword is not None and keyword != "":
            q.add(
                Q(name_en__contains=keyword)
                | Q(model_number__contains=keyword)
                | Q(brand__name__contains=keyword),
                q.AND,
            )
    result = Product.objects.filter(q, **filter_args)  # filter 한거를 정렬하고 싶으면 order_by 사용
    # else:
    #     result = Product.objects.all()

    return render(
        request,
        "products/search.html",
        {"result": result, "keyword": keyword, "price": price, "form": form},
    )


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
