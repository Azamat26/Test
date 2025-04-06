from django.http import JsonResponse, HttpResponse
from .models import Music
import json
from django.views.decorators.csrf import csrf_exempt
from .forms import RegisterForm
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_music_data(request):
    # # music_objects = Music.objects.select_related('genre', 'artist').all()

    # track_name = request.GET.get('title')
    # track_genre = request.GET.get('genre')
    # track_year = request.GET.get('year')
    # #return HttpResponse(track_name)
    # filters = {}

    # if track_name:
    #     # music_objects = music_objects.filter(title__icontains=track_name)
    #     filters["title__icontains"] = track_name
    
    # # if track_genre:
    # #     music_objects = music_objects.filter(genre_id__icontains=track_genre)
    # if track_year:
    #     # music_objects = music_objects.filter(year__icontains=track_year)
    #     filters["year__icontains"] = track_year

    # music_objects = Music.objects.select_related('genre', 'artist').filter(**filters)

    music_objects = Music.objects.select_related('genre', 'artist').all()

    track_name = request.GET.get('title')
    track_genre = request.GET.get('genre')
    track_year = request.GET.get('year')
    #return HttpResponse(track_name)
    filters = {}

    if track_name:
        music_objects = music_objects.filter(title__icontains=track_name)
        # filters["title__icontains"] = track_name
    
    # if track_genre:
    #     music_objects = music_objects.filter(genre_id__icontains=track_genre)
    if track_year:
        music_objects = music_objects.filter(year__icontains=track_year)
        # filters["year__icontains"] = track_year

    # music_objects = Music.objects.select_related('genre', 'artist').filter(**filters)




    data = {"music": []}

    for track in music_objects:
        data["music"].append({
            "id": track.id,
            "title": track.title,
            "urlLink": track.url,
            "year": track.year,
            "source": track.source,
            "created": track.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "genre": {
                "id": track.genre.id if track.genre else None,
                "name": track.genre.name if track.genre else None
            },
            "artist": {
                "id": track.artist.id if track.artist else None,
                "name": track.artist.name if track.artist else None
            }
        })

    return JsonResponse(data, safe=False)

@csrf_exempt
def register(request):
    if request.method == "POST":
        try:
            form = RegisterForm(request.POST)  # Передаём данные в форму

            if form.is_valid():
                user = form.save(commit=False)  # Создаём пользователя, но не сохраняем
                user.set_password(form.cleaned_data['password'])  # Хешируем пароль
                user.save()  # Сохраняем пользователя

                return JsonResponse({"message": "Регистрация успешна!", "username": user.username})
            else:
                return JsonResponse({"errors": form.errors}, status=400)

        except Exception as e:
            return JsonResponse({"error": f"Ошибка: {e}"}, status=500)

    return JsonResponse({"error": "Метод не поддерживается"}, status=405)


def creat_token(user):
    token = RefreshToken.for_user(user)
    return {
        'refresh': str(token),
        'access': str(token.access_token),
    }

def login(request):
    user = User.objects.get(username='Aza')
    tokens = creat_token(user)
    return JsonResponse(tokens)