"""dolphin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from rest_framework.documentation import include_docs_urls
from dolphin.api.book_controller import BookController
from dolphin.api.doubanbookcontroller import doubanbookcontroller
from dolphin.api.spider_urls_controller import SpiderUrlsController
from dolphin.api.word_controller import WordController
from dolphin.api.consumer_controller import ConsumerController

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^docs/', include_docs_urls(title="Dolphin's book spider api")),
    url(r'^spider/api/v1/book$', BookController.as_view()),
    url(r'^spider/api/v1/doubanbook$', doubanbookcontroller.as_view()),
    url(r'^spider/api/v1/word',WordController.as_view()),
    url(r'^spider/api/v1/consumer',ConsumerController.as_view()),
    url(r'^spider/api/v1/spiderurls',SpiderUrlsController.as_view())
]
