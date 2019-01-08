from rest_framework import serializers
from dolphin.models.word_model import Word
from rest_framework.pagination import PageNumberPagination

class WordSerializer(serializers.Serializer):                
    id = serializers.CharField(allow_blank=False)
    word = serializers.CharField(required=True, allow_blank=False)
    remark = serializers.CharField(required=True)    

    def get(self):
        # get all data
        word_result = Word.objects.all()       
        return word_result