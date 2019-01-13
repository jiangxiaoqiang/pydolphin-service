# -*- coding: UTF-8 -*-

import time
import threading
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from django.http import QueryDict
from dolphin.biz.book_persist_consumer import BookPersistConsumer

class ConsumerController(APIView):
    def get(self,request):
        self.index(request)
        return JsonResponse("Book consumer deamon started",safe=False)

    def background_process(self):
        print("process started")
        bookPersistConsumer = BookPersistConsumer()
        bookPersistConsumer.run()        

    def index(self,request):        
        t = threading.Thread(target=self.background_process, args=(), kwargs={})
        t.setDaemon(True)
        t.start()
        return HttpResponse("main thread content")