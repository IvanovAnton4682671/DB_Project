
from django.shortcuts import render
from django.templatetags.static import static


def hi(request):
    links = [static("css/hi.css")]
    scripts = [static("js/popup.js")]
    title = "Добро пожаловать!"
    videos = [static("video/equalizer.mp4")]
    all_data = '''
    <div class="blur"></div>
        <div class="content">
            <div class="container">
                <h3>Добро пожаловать в гости к музыкальному помощнику! Он всегда подскажет вам музыку по вкусу!</h3>
                <h4>Однако, сначала нам с вами нужно познакомиться</h4>
                <button class="button-popup button-slide slide-inside" type="button" id="showPopup">ЗАРЕГИСТРИРОВАТЬСЯ</button>
                <div class="popup-blur" id="popup-blur"></div>
                <div class="popup-center">
                    <div class="popup" id="popup">
                        <form class="form" id="form-reg">
                            <h4>Регистрация</h5>
                            <input type="text" placeholder="Ник-нейм">
                            <input type="text" placeholder="Почта">
                            <div class="passwordContainer">
                                <input type="password" placeholder="Пароль" id="reg-passwordInput">
                                <button class="togglePassword" type="button" id="reg-togglePassword" style="margin-top:-7px;"><span style="font-size:20px;">&#x1F441;</span></button>
                            </div>
                            <button class="button-popup button-slide slide-inside" type="submit">ПРИСОЕДИНИТЬСЯ</button>
                            <h4>Уже зарегистрированы?</h4>
                            <button class="button-popup button-slide slide-right" type="button" id="showAut">АВТОРИЗОВАТЬСЯ</button>
                        </form>
                        <form class="form" id="form-aut">
                            <h4>Авторизация</h4>
                            <input type="text" placeholder="Почта">
                            <div>
                                <input type="password" placeholder="Пароль" id="aut-passwordInput">
                                <button class="a-togglePassword" type="button" id="aut-togglePassword" style="margin-top:-29px;"><span style="font-size:20px;">&#x1F441;</span></button>
                            </div>
                            <button class="button-popup button-slide slide-inside" type="submit">ВОЙТИ</button>
                            <h4>Ещё не зарегистрировались?</h4>
                            <button class="button-popup button-slide slide-left" type="button" id="showReg">ЗАРЕГИСТРИРОВАТЬСЯ</button>
                        </form>
                        <div class="dop-div" id="dop-div"></div>
                    </div>
                </div>
            </div>
        </div>
    '''
    data = {"links": links, "scripts": scripts, "title": title, "videos": videos, "all_data": all_data}
    return render(request, "hi.html", context=data)
