from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("", views.ProductListView.as_view(), name="list"),
    # path("<int:pk>", views.detail, name="상세페이지"),
    path("<int:pk>", views.ProductDetail.as_view(), name="상세페이지"),
]
