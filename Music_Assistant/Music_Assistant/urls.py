"""
URL configuration for Music_Assistant project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users_core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("add-to-library/", views.add_to_library, name="add_to_library"),
    path("main", views.main, name="main"),
    path("form_reg_sending", views.form_reg_sending, name="form_reg_sending"),
    path("form_aut_sending", views.form_aut_sending, name="form_aut_sending"),
    path("", views.hi, name="hi.html"),
]

if settings.DEBUG:
    import debug_toolbar
    from django.urls import include

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
