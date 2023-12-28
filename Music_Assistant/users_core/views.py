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


def hi(request):
    """Стартовая функция, которая нас приветствует на странице."""

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
    """Регистрация пользователя, проверка по базе."""

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

                # создание отдельной коллекции для каждого пользователя - очень нестандартная вещь
                # для классической работы MongoDB с Django, придётся работать через pymongo
                client = MongoClient(settings.DATABASES['links_mongodb']['CLIENT']['host'])
                db = client[settings.DATABASES['links_mongodb']['NAME']]
                user_collection = db[nickname]  # используем никнейм пользователя как имя новой коллекции
                user_collection.insert_one({"email": email, "links": []})  # только для инициализации коллекции

                messages.success(request, "Вы успешно зарегистрировались!")
                return render(request, "hi_redirect.html", context=data)
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
    """Авторизация пользователя, проверка по базе."""
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

        existing_user = Users.objects.get(email=email, password=sha224)

        # та же проблема с сессиями
        # загрузка в сессию для дальнейшей работы
        # nickname = existing_user.nickname
        # request.session["user_nickname"] = nickname
        # request.session["user_email"] = email

        # различные исключения
        if not existing_user:
            messages.error(request, "Неверная почта или пароль!")
        else:
            messages.success(request, "Вы успешно авторизовались!")
            return render(request, "hi_redirect.html", context=data)
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

field_names = [field.name for field in MusicBase._meta.fields][1:]
music_objects = MusicBase.objects.all()
# table_data = [[getattr(obj, field) for field in field_names] for obj in music_objects]
table_data = []
for obj in music_objects:
    row_data = [getattr(obj, field) for field in field_names]
    add_button = f'<button class="dop-button">Добавить</button>'
    row_data.append(add_button)
    table_data.append(row_data)

def main(request):
    """Загрузка музыкальной базы и на главную страницу."""
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
    data = {"links": links, "scripts": scripts, "title": title, "videos": videos, "all_data_1": all_data_1,
            "all_data_2": all_data_2, "field_data": field_names, "table_data": table_data, "all_data_3": all_data_3}
    return render(request, "main.html", context=data)
# -------------------- КОНЕЦ КОСТЫЛЯ --------------------
