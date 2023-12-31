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

        # почему-то сессии в этой функции вызывают непонятную ошибку, связанную с django_sessions
        # загрузка данных в сессию для дальнейшей работы
        # request.session["user_nickname"] = nickname
        # request.session["user_email"] = email

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

                # не работает из-за переадресации
                # messages.add_message(request, messages.INFO, f"{email}")
                # messages.info(request, email, extra_tags="INFO")

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
            # не работают из-за переадресации
            # messages.add_message(request, messages.INFO, f"{email}")

            # та же проблема с сессиями
            # загрузка в сессию для дальнейшей работы
            # nickname = existing_user.nickname
            # request.session["user_nickname"] = nickname
            # request.session["user_email"] = email
            return response
        except Users.DoesNotExist:
            messages.error(request, "Неверная почта или пароль!")
            return render(request, "hi.html", context=data)
    else:
        return HttpResponseBadRequest("Разрешены только POST-запросы!")

# -------------------- КОСТЫЛЬ --------------------
# это ужасный костыль, который относится только к функции main и общей музыкальной базе
# проблема в том, что в mongodb по данным ходит итератор (курсор)
# если этот запрос к бд реализовать в функции main, то он будет происходить каждый раз при заходе на /main
# а проблема в том, что курсор не возвращается в начало сам, и в ручную его туда перетащить в django нельзя
# и при повторном заходе мы получаем error - чтение пустых данных
# так что, пока пусть будет так

field_names = [field.name for field in MusicBase._meta.fields][2:]
music_objects = MusicBase.objects.all()
table_data = []
for obj in music_objects:
    row_data = [getattr(obj, field) for field in field_names]
    music_id = obj.dop_id
    add_button = f'<button class="dop-button" data-id="{music_id}">Добавить</button>'
    row_data.append(add_button)
    table_data.append(row_data)
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
                        </div>
                    </div>
                    <div class="adaptive">
                        <h4>Моя бибилиотека</h4>
                        <div class="my-library" id="myLibrary">
                            <div class="whole-library-textarea" style="display: none;" id="myLibraryTextarea">
                    '''
    all_data_4 = '''
                            </div>
                            <button class="button-popup button-slide slide-inside" type="button" id="openMyLibrary">ПОКАЗАТЬ</button>
                        </div>
                        <div class="button-center">
                            <button class="button-popup button-slide slide-inside" style="display: none;" type="button" id="closeMyLibrary">ЗАКРЫТЬ</button>
                        </div>
                    </div>
                    <div class="adaptive">
                        <h4>Узнать рекомендации</h4>
                        <div class="recomendation-library" id="recomendationLibrary">
                            <button class="button-popup button-slide slide-inside" type="button" id="openRecomendationLibrary">ПОКАЗАТЬ</button>
                        </div>
                        <div class="button-center">
                            <button class="button-popup button-slide slide-inside" style="display: none;" type="button" id="closeRecomendationLibrary">ЗАКРЫТЬ</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
                '''

    # загрузка данных в личную библиотеку на странице
    user_coll = request.COOKIES.get('user_collection')
    user = Users.objects.get(nickname=user_coll)
    client = MongoClient('mongodb://localhost:27017/')
    db = client[settings.DATABASES['links_mongodb']['NAME']]
    # получаем список всех коллекций в базе данных
    collection_names = db.list_collection_names()
    # проверяем, есть ли нужная коллекция
    for collection_name in collection_names:
        if collection_name == user_coll:
            user_collection = db.get_collection(collection_name)
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

    data = {"links": links, "scripts": scripts, "title": title, "videos": videos, "all_data_1": all_data_1,
            "all_data_2": all_data_2, "field_data": field_names, "table_data": table_data, "all_data_3": all_data_3,
            "field_data_2": field_order, "table_data_2": table_data_2, "all_data_4": all_data_4}
    return render(request, "main.html", context=data)
# -------------------- КОНЕЦ КОСТЫЛЯ --------------------


@csrf_exempt
def add_to_library(request):
    """Добавление записи в библиотеку при каждом нажатии кнопки"""
    if request.method == "POST":
        user_coll = request.COOKIES.get('user_collection')  # Получаем значение cookie с коллекцией пользователя
        user = Users.objects.get(nickname=user_coll)
        # try:
        # загружаем json c id, ищем нужную запись
        data = json.loads(request.body)
        music_id = data.get('music_id')
        music = MusicBase.objects.get(dop_id=music_id)
        with MongoClient(settings.DATABASES['links_mongodb']['CLIENT']['host']) as client:
            db = client[settings.DATABASES['links_mongodb']['NAME']]
            # user_collection = db.get_collection(user_coll)
            user_collection = db[user_coll]
            user_collection.update_one(
                {"email": user.email},
                {"$push": {"links": {
                    "dop_id": music.dop_id,
                    "genre": music.genre,
                    "author": music.author,
                    "co_author": music.co_author,
                    "album": music.album,
                    "title": music.title
                }}}
            )
        return JsonResponse({'status': 'success', 'message': f'Получили id = {music_id} и коллекцию = {user_coll}, успешно добавили запись!'})
        # except Exception as e:
            # print(f"Error: {str(e)}")  # эта хрень пустая (ошибка есть, но какая - хз))))))))
            # return JsonResponse({'status': 'error', 'message': f'{str(e)}'})  # ошибка-невидимка, прикольно)
    else:
        return JsonResponse({'status': 'error', 'message': 'Разрешены только POST запросы!'})
