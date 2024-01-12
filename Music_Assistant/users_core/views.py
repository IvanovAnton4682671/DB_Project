
from django.conf import settings
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponseBadRequest
from django.templatetags.static import static
from django.contrib import messages
from .models import *
import re
import hashlib
from pymongo import MongoClient
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from collections import Counter
import random


def hi(request):
    """Стартовая функция, которая нас приветствует на странице"""
    # загрузка статических файлов и статичных переменных (таких как all_data)
    links = [static("css/hi.css")]
    scripts = [static("js/popup.js")]
    title = "Добро пожаловать!"
    videos = [static("video/equalizer.mp4")]
    all_data_1 = '''
                           <div class="content">
                               <div class="container">
                       '''
    all_data_2 = '''
                       <h3>Добро пожаловать в гости к музыкальному помощнику! Он всегда подскажет вам музыку по вкусу!</h3>
                                   <h4>Однако, сначала нам с вами нужно познакомиться</h4>
                                   <button class="button-popup button-slide slide-inside" type="button" id="showPopup">ЗАРЕГИСТРИРОВАТЬСЯ</button>
                                   <div class="popup-blur" id="popup-blur"></div>
                                   <div class="popup-center">
                                       <div class="popup" id="popup">
                       '''
    all_data_3 = '''
                                           <div class="dop-div" id="dop-div"></div>
                                       </div>
                                   </div>
                               </div>
                           </div>
                       '''
    data = {"links": links, "scripts": scripts, "title": title, "videos": videos, "all_data_1": all_data_1,
            "all_data_2": all_data_2, "all_data_3": all_data_3}
    return render(request, "hi.html", context=data)


def form_reg_sending(request):
    """Регистрация пользователя, проверка по базе"""
    if request.method == 'POST':
        # обработка регистрации
        nickname = request.POST.get("nickname", "-undefined-")
        email = request.POST.get("regEmail", "-undefined-")
        password = request.POST.get("reg-passwordInput", "-undefined-")
        nickname_regex = r"^[a-zA-Z0-9_]{5,40}$"
        email_regex = r"^[\w.-]+@[a-zA-Z\d.-]+\.[a-zA-Z]{2,40}$"
        password_regex = r"^(?=.*[0-9])(?=.*[A-Z])(?=.*[!@#$%^&*])(.{8,})$"

        # статичные объекты
        links = [static("css/hi.css")]
        scripts = [static("js/popup.js")]
        title = "Добро пожаловать!"
        videos = [static("video/equalizer.mp4")]
        all_data_1 = '''
                        <div class="content">
                            <div class="container">
                    '''
        all_data_2 = '''
                    <h3>Добро пожаловать в гости к музыкальному помощнику! Он всегда подскажет вам музыку по вкусу!</h3>
                                <h4>Однако, сначала нам с вами нужно познакомиться</h4>
                                <button class="button-popup button-slide slide-inside" type="button" id="showPopup">ЗАРЕГИСТРИРОВАТЬСЯ</button>
                                <div class="popup-blur" id="popup-blur"></div>
                                <div class="popup-center">
                                    <div class="popup" id="popup">
                    '''
        all_data_3 = '''
                                        <div class="dop-div" id="dop-div"></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    '''
        data = {"links": links, "scripts": scripts, "title": title, "videos": videos, "all_data_1": all_data_1,
                "all_data_2": all_data_2, "nickname": nickname, "regEmail": email, "regPass": password,
                "all_data_3": all_data_3}

        # проверка корректности данных для создания пользователя
        if re.match(nickname_regex, nickname) and re.match(email_regex, email) and re.match(password_regex, password):
            existing_user = Users.objects.filter(Q(nickname=nickname) | Q(email=email))
            if not existing_user:
                sha224 = hashlib.sha224(password.encode("utf-8")).hexdigest()
                user = Users(nickname=nickname, email=email, password=sha224)
                user.save()

                # создание отдельной коллекции для каждого пользователя - очень нестандартная вещь
                # для классической работы MongoDB с Django, придётся работать через pymongo
                client = MongoClient(settings.DATABASES['links_mongodb']['CLIENT']['host'])
                db = client[settings.DATABASES['links_mongodb']['NAME']]
                user_collection = db[nickname]  # используем никнейм пользователя как имя новой коллекции
                user_collection.insert_one({"email": email, "links": []})  # для инициализации коллекции, музыку храним в links

                messages.success(request, "Вы успешно зарегистрировались!")
                response = render(request, "hi_redirect.html", context=data)
                response.set_cookie("user_collection", nickname)  # запоминаем ник пользователя для дальнейшей работы
                return response
            # различные исключения
            else:
                if Users.objects.filter(nickname=nickname, email=email).exists():
                    messages.error(request, "Пользователь с таким ник-неймом и почтой уже существует!")
                elif Users.objects.filter(nickname=nickname).exists():
                    messages.error(request, "Пользователь с таким ник-неймом уже существует!")
                elif Users.objects.filter(email=email).exists():
                    messages.error(request, "Пользователь с такой почтой уже существует!")
            return render(request, "hi.html", context=data)
        else:
            messages.error(request, "Пожалуйста, вводите корректные данные!")
            return render(request, "hi.html", context=data)
    else:
        return HttpResponseBadRequest("Разрешены только POST-запросы!")


def form_aut_sending(request):
    """Авторизация пользователя, проверка по базе"""
    if request.method == "POST":
        # обработка авторизации пользователя
        email = request.POST.get("autEmail", "-undefined-")
        password = request.POST.get("aut-passwordInput", "-undefined-")
        sha224 = hashlib.sha224(password.encode("utf-8")).hexdigest()

        # статичные объекты
        links = [static("css/hi.css")]
        scripts = [static("js/popup.js")]
        title = "Добро пожаловать!"
        videos = [static("video/equalizer.mp4")]
        all_data_1 = '''
                                <div class="content">
                                    <div class="container">
                            '''
        all_data_2 = '''
                            <h3>Добро пожаловать в гости к музыкальному помощнику! Он всегда подскажет вам музыку по вкусу!</h3>
                                        <h4>Однако, сначала нам с вами нужно познакомиться</h4>
                                        <button class="button-popup button-slide slide-inside" type="button" id="showPopup">ЗАРЕГИСТРИРОВАТЬСЯ</button>
                                        <div class="popup-blur" id="popup-blur"></div>
                                        <div class="popup-center">
                                            <div class="popup" id="popup">
                            '''
        all_data_3 = '''
                                                <div class="dop-div" id="dop-div"></div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            '''
        data = {"links": links, "scripts": scripts, "title": title, "videos": videos, "all_data_1": all_data_1,
                "all_data_2": all_data_2, "autEmail": email, "autPass": password, "all_data_3": all_data_3}

        try:
            existing_user = Users.objects.get(email=email, password=sha224)
            messages.success(request, "Вы успешно авторизовались!")
            response = render(request, "hi_redirect.html", context=data)
            response.set_cookie("user_collection", existing_user.nickname)  # запоминаем ник для работы
            return response
        except Users.DoesNotExist:
            messages.error(request, "Неверная почта или пароль!")
            return render(request, "hi.html", context=data)
    else:
        return HttpResponseBadRequest("Разрешены только POST-запросы!")


# записываем все данные во временное хранилище, чтобы постоянно не обращаться к БД (уменьшение нагрузки)
# примерно по принципу работы Redis`a
all_music = []
music_objects = MusicBase.objects.all()
for obj in music_objects:
    all_music.append({"dop_id": obj.dop_id, "genre": obj.genre, "author": obj.author,
                      "co_author": obj.co_author, "album": obj.album, "title": obj.title})
def main(request):
    """Загрузка музыкальной базы и на главную страницу"""
    # загрузка статичных объектов
    links = [static("css/main.css")]
    scripts = [static("js/main.js")]
    title = "Рабочая зона"
    videos = [static("video/equalizer.mp4")]
    all_data_1 = '''
                <div class="content">
                    <div class="container">
                '''
    all_data_2 = '''
                <div class="horizontal-orientation">
                    <div class="adaptive">
                        <h4>Музыкальная база</h4>
                        <div class="whole-library" id="wholeLibrary">
                            <div class="whole-library-textarea" style="display: none;" id="wholeLibraryTextarea">
                '''
    all_data_3 = '''
                            </div>
                            <button class="button-popup button-slide slide-inside" type="button" id="openWholeLibrary">ПОКАЗАТЬ</button>
                        </div>
                        <div class="button-center">
                            <button class="button-popup button-slide slide-inside" style="display: none;" type="button" id="closeWholeLibrary">ЗАКРЫТЬ</button>
                '''
    all_data_4 = '''
                        </div>
                    </div>
                    <div class="adaptive">
                        <h4>Моя библиотека</h4>
                        <div class="my-library" id="myLibrary">
                            <div class="whole-library-textarea" style="display: none;" id="myLibraryTextarea">
                    '''
    all_data_5 = '''
                            </div>
                            <button class="button-popup button-slide slide-inside" type="button" id="openMyLibrary">ПОКАЗАТЬ</button>
                        </div>
                        <div class="button-center">
                            <button class="button-popup button-slide slide-inside" style="display: none;" type="button" id="closeMyLibrary">ЗАКРЫТЬ</button>
                    '''
    all_data_6 = '''
                        </div>
                    </div>
                    <div class="adaptive">
                        <h4>Узнать рекомендации</h4>
                        <div class="recomendation-library" id="recomendationLibrary">
                            <div class="recommendation-library-textarea" style="display: none;" id="recLibraryTextarea">
                            </div>
                            <button class="button-popup button-slide slide-inside" type="button" id="openRecomendationLibrary">ПОКАЗАТЬ</button>
                        </div>
                        <div class="button-center">
                            <button class="button-popup button-slide slide-inside" style="display: none;" type="button" id="closeRecomendationLibrary">ЗАКРЫТЬ</button>
                            <button class="button-popup button-slide slide-inside find-rec" style="display: none; margin-left: 20px;" type="button" id="findOutTheRecomendations">УЗНАТЬ РЕКОМЕНДАЦИИ</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
                '''

    # ЗАГРУЗКА ДАННЫХ В ЛИЧНУЮ БИБЛИОТЕКУ НА СТРАНИЦЕ
    user_coll = request.COOKIES.get('user_collection')
    user = Users.objects.get(nickname=user_coll)
    with MongoClient(settings.DATABASES['links_mongodb']['CLIENT']['host']) as client:
        db = client[settings.DATABASES['links_mongodb']['NAME']]
        user_collection = db[user_coll]
        user_doc = user_collection.find_one({"email": user.email})
        music_entries = user_doc["links"] if "links" in user_doc else []
        field_order = ['genre', 'author', 'co_author', 'album', 'title']
        table_data_2 = []
        for entry in music_entries:
            # тут код обработки данных отличается, так как в mongodb всё хранится в виде словарей
            row_data_2 = [entry.get(field, "") for field in field_order]  # используем obj[field] или obj.get(field) (словарный доступ)
            music_id_2 = entry.get('dop_id')  # используем словарный доступ к 'dop_id'
            del_button = f'<button class="del-button" data-id="{music_id_2}">Удалить</button>'
            row_data_2.append(del_button)
            table_data_2.append(row_data_2)

        # создаем set из Music ID личной коллекции для ускорения проверки вхождения
        user_music_ids = set(entry['dop_id'] for entry in music_entries)

    # ЗАГРУЗКА ДАННЫХ В ОБЩУЮ БИБЛИОТЕКУ НА СТРАНИЦЕ
    with MongoClient(settings.DATABASES['music_mongodb']['CLIENT']['host']) as client:
        db = client[settings.DATABASES['music_mongodb']['NAME']]
        user_collection = db['music_base']
        user_doc = user_collection.find()
        field_names = ["genre", "author", "co_author", "album", "title"]
        table_data = []
        for record in user_doc:
            row_data = [record.get(field, "") for field in field_names]
            music_id = record.get("dop_id")
            # проверяем, существует ли запись в личной коллекции пользователя
            if music_id in user_music_ids:
                # если запись существует, кнопка невидимая
                add_button = f'<button class="dop-button" style="display: none;" data-id="{music_id}">Добавить</button>'
            else:
                # если записи нет, кнопка видимая
                add_button = f'<button class="dop-button" data-id="{music_id}">Добавить</button>'
            row_data.append(add_button)
            table_data.append(row_data)

    data = {"links": links, "scripts": scripts, "title": title, "videos": videos, "all_data_1": all_data_1,
            "all_data_2": all_data_2, "field_data": field_names, "table_data": table_data, "all_data_3": all_data_3,
            "all_data_4": all_data_4, "field_data_2": field_order, "table_data_2": table_data_2,
            "all_data_5": all_data_5, "all_data_6": all_data_6}
    return render(request, "main.html", context=data)

# тот же принцип Redis`a, храним данные во временном хранилище, а потом одним запросом к БД всё добавляем
save_music = []
@csrf_exempt
def add_to_library(request):
    """Добавление записи во временный массив, чтобы потом одним запросом к бд всё добавить"""
    if request.method == "POST":
        # загружаем json c id, ищем нужную запись
        data = json.loads(request.body)
        music_id = int(data.get('music_id'))  # изначально json-строка, так что переводим в int
        # ищем итератором по списку словарей
        music = next((music_record for music_record in all_music if music_record["dop_id"] == music_id), None)
        save_music.append(music)
        return JsonResponse({'status': 'success', 'message': f'Получили id = {music_id} и нашли запись {music}, которую сохранили в список!'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Разрешены только POST запросы!'})


# тот самый один запрос к БД и очистка временного хранилища
def save_to_library(request):
    """Добавляем все записи одним запросом и перезагружаем страницу, чтобы пользователь увидел изменения"""
    if request.method == "POST":
        user_coll = request.COOKIES.get("user_collection")  # получаем значение cookie с коллекцией пользователя
        user = Users.objects.get(nickname=user_coll)
        with MongoClient(settings.DATABASES['links_mongodb']['CLIENT']['host']) as client:
            db = client[settings.DATABASES['links_mongodb']['NAME']]
            user_collection = db[user_coll]
            user_collection.update_one(
                {"email": user.email},  # используем email как идентификатор для нахождения нужного документа
                {"$push": {"links": {"$each": save_music}}}  # используем $each для добавления всех записей
            )
            save_music.clear()
        # чтобы не дублировать код переадресации и вывода данных - просто вызываем функцию
        return main(request)
    else:
        return HttpResponseBadRequest("Разрешены только POST запросы!")


# тот же принцип Redis`a, храним данные во временном хранилище, а потом одним запросом к БД всё удаляем
del_music = []
@csrf_exempt
def del_from_library(request):
    """Добавляем записи во временный массив, чтобы одним запросом к бд всё удалить"""
    if request.method == "POST":
        # загружаем json c id, ищем нужную запись
        data = json.loads(request.body)
        music_id = int(data.get('music_id'))  # изначально json-строка, так что переводим в int
        # ищем итератором по списку словарей
        music = next((music_record for music_record in all_music if music_record["dop_id"] == music_id), None)
        del_music.append(music)
        return JsonResponse({'status': 'success', 'message': f'Получили id = {music_id} и нашли запись {music}, которую сохранили в список!'})
    else:
        return JsonResponse({"status": "error", "message": "Разрешены только POST запросы!"})


# тот самый один запрос к БД и очистка временного хранилища
def save_delete_from_library(request):
    """Удаляем записи одним запросом и перезагружаем страницу, чтобы пользователь увидел изменения"""
    if request.method == "POST":
        user_coll = request.COOKIES.get("user_collection")  # получаем значение cookie с коллекцией пользователя
        user = Users.objects.get(nickname=user_coll)
        # делаем так, чтобы массив записей содержал только dop_id, нам этого хватит для удаления
        music_ids_to_remove = [music["dop_id"] for music in del_music]
        with MongoClient(settings.DATABASES['links_mongodb']['CLIENT']['host']) as client:
            db = client[settings.DATABASES['links_mongodb']['NAME']]
            user_collection = db[user_coll]
            user_collection.update_one(
                {"email": user.email},  # используем email как идентификатор для нахождения нужного документа
                {"$pull": {"links": {"dop_id": {"$in": music_ids_to_remove}}}}  # применяем $pull операцию с использованием $in
            )
            del_music.clear()  # очистить массив после удаления
        # чтобы не дублировать код переадресации и вывода данных - просто вызываем функцию
        return main(request)
    else:
        return HttpResponseBadRequest("Разрешены только POST запросы!")


@csrf_exempt
def find_out_rec(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_coll = request.COOKIES.get("user_collection")
        user = Users.objects.get(nickname=user_coll)

        with MongoClient(settings.DATABASES['links_mongodb']['CLIENT']['host']) as client:
            db = client[settings.DATABASES['links_mongodb']['NAME']]
            user_collection = db[user_coll]
            user_doc = user_collection.find_one({"email": user.email})

            # определяем самый популярный жанр
            genre_counter = Counter()
            for entry in user_doc["links"]:
                genre = entry.get("genre", "").title()
                if genre:
                    genre_counter[genre] += 1

            if not genre_counter:
                return JsonResponse({
                    "status": "error",
                    "message": "Не достаточно данных для рекомендации."
                })

            # получаем самый популярный жанр
            recommended_genre = genre_counter.most_common(1)[0][0]

            # находим всех авторов и альбомы этого жанра
            authors_in_genre = []
            authors_albums = {}
            for entry in user_doc["links"]:
                if entry.get("genre", "").title() == recommended_genre:
                    author = entry.get("author")
                    album = entry.get("album", None)  # используем None вместо '-нет-'
                    authors_in_genre.append(author)
                    if album:
                        authors_albums.setdefault(author, set()).add(
                            album)  # используем set для хранения альбомов без повторений

            author_counter = Counter(authors_in_genre)
            if not author_counter:
                return JsonResponse({
                    "status": "error",
                    "message": "Не найдено авторов в самом популярном жанре."
                })

            # находим самого популярного автора в этом жанре
            recommended_author = author_counter.most_common(1)[0][0]

            # исключаем самого популярного автора для рекомендации других авторов
            other_authors = [author for author in authors_in_genre if author != recommended_author]

            # если нет других авторов, выводим сообщение
            if not other_authors:
                return JsonResponse({
                    "status": "error",
                    "message": f"Не найдено других авторов в жанре {recommended_genre}."
                })

            new_recommended_author = random.choice(other_authors)

            recommended_album = None
            # проверяем, есть ли у нового рекомендуемого автора альбомы
            if new_recommended_author in authors_albums and authors_albums[new_recommended_author]:
                recommended_album = random.choice(list(authors_albums[new_recommended_author]))

            # создаём итоговый ответ
            if recommended_album and recommended_album != "-нет-":
                result_message = (f"Рекомендации: Так как вы любите слушать музыку в жанре '{recommended_genre}', "
                                  f"и у вас много треков от '{recommended_author}', "
                                  f"предлагаем послушать '{new_recommended_author}'. "
                                  f"Мы выбрали для вас альбом '{recommended_album}'.")
            else:
                result_message = (f"Рекомендации: Так как вы любите слушать музыку в жанре '{recommended_genre}', "
                                  f"и у вас много треков от '{recommended_author}', "
                                  f"предлагаем послушать '{new_recommended_author}'.")

            response_data = {"status": "success", "message": result_message.strip()}
            return JsonResponse(response_data)
    else:
        return JsonResponse({"status": "error", "message": "Разрешены только POST запросы!"})
