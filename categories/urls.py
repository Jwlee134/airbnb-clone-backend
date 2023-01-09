from django.urls import path
from . import views

urlpatterns = [
    path("room", views.RoomCategoryViewSet.as_view({"get": "list", "post": "create"})),
    path(
        "experience",
        views.ExperienceCategoryViewSet.as_view({"get": "list", "post": "create"}),
    ),
    path(
        "<int:pk>",
        views.RoomCategoryViewSet.as_view(
            {"get": "retrieve", "put": "partial_update", "delete": "destroy"}
        ),
    ),
]
