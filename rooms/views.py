from django.shortcuts import render
from django.http import HttpResponse
from .models import Room

# Create your views here.


def see_all_rooms(request):
    rooms = Room.objects.all()  # django ORM
    # 두 번째 인자: html파일, 세 번째 인자: html로 보낼 데이터
    return render(
        request,
        "all_rooms.html",
        {
            "rooms": rooms,
            "title": "This is title!",
        },
    )


def see_one_room(request, room_id):
    return HttpResponse(f"see room with id: {room_id}")
