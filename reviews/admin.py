from django.contrib import admin
from .models import Review


class WordFilter(admin.SimpleListFilter):
    title = "Filter by words!"
    parameter_name = "word"  # 필터 선택시 url에 나타날 쿼리 파라미터 이름

    def lookups(self, request, model_admin):
        return [
            ("great", "great"),  # (필터링할 단어, admin 패널에 보여지는 이름)
            ("bad", "bad"),
        ]

    def queryset(self, request, reviews):
        param = self.value()
        if param == None:
            return reviews
        return reviews.filter(payload__contains=param)


class RatingFilter(admin.SimpleListFilter):
    title = "is good review"
    parameter_name = "is good"

    def lookups(self, request, model_admin):
        return [
            ("good", "good"),
            ("bad", "bad"),
        ]

    def queryset(self, request, reviews):
        param = self.value()
        if param == None:
            return reviews
        elif param == "good":
            return reviews.filter(rating__gte=3)
        else:
            return reviews.filter(rating__lt=3)


# Register your models here.
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("__str__", "payload")
    list_filter = (
        WordFilter,
        RatingFilter,
        "rating",
        "user__is_host",  # foreign key filtering
        "room__category",
    )
