"""daily_reoort URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include   # ←, includeを追加
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include('day.urls', namespace='day')),   # ←ここを追加
    url(r'^$', 'django.contrib.auth.views.login', {'template_name': 'day/login.html'}),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'template_name': 'day/logged_out.html'}),
    # url(r'^$', 'day.views.index'),
    url(r'^register$', 'day.views.create_user'),
    # url(r'^create_user$', 'day.views.create_user'),
]