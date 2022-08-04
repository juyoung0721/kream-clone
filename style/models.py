from django.db import models
from core.models import TimeStampedModel


class Photo(TimeStampedModel):
    image = models.ImageField(upload_to="product/%Y/%m/%d/")
    style = models.ForeignKey("style", on_delete=models.CASCADE)


class Style(TimeStampedModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    comment = models.CharField(verbose_name="내용", max_length=120)
    products = models.ManyToManyField("products.Product")

    def __str__(self) -> str:
        return f"{self.user}의 STYLE"

    def count_products(self):
        return self.products.count()

    count_products.short_description = "상품 태그 수"
