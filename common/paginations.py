from django.conf import settings
import math


class PagePagination:
    limit = settings.LIMIT

    def paginate(self, request, queryset):

        try:
            page = int(request.query_params.get("page", 1))
        except ValueError:
            page = 1
        limited_queryset = queryset[page * self.limit - self.limit : page * self.limit]
        return limited_queryset

    def response(self, serialized_data, count_of_queryset):
        return {
            "total_page": math.ceil(count_of_queryset / self.limit),
            "data": serialized_data,
        }
