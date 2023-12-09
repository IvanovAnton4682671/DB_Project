
from django.shortcuts import render
from django.templatetags.static import static


def hi(request):
    links = [static("css/hi.css")]
    scripts = [static("js/popup.js")]
    title = "Добро пожаловать!"
    videos = [static("video/equalizer.mp4")]
    all_data_1 = '''
    <div class="blur"></div>
        <div class="content">
            <div class="container">
                <h3>Добро пожаловать в гости к музыкальному помощнику! Он всегда подскажет вам музыку по вкусу!</h3>
                <h4>Однако, сначала нам с вами нужно познакомиться</h4>
                <button class="button-popup button-slide slide-inside" type="button" id="showPopup">ЗАРЕГИСТРИРОВАТЬСЯ</button>
                <div class="popup-blur" id="popup-blur"></div>
                <div class="popup-center">
                    <div class="popup" id="popup">
    '''
    all_data_2 = '''
                        <div class="dop-div" id="dop-div"></div>
                    </div>
                </div>
            </div>
        </div>
    '''
    data = {"links": links, "scripts": scripts, "title": title, "videos": videos, "all_data_1": all_data_1, "all_data_2": all_data_2}
    return render(request, "hi.html", context=data)
