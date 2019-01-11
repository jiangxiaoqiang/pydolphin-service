from rest_framework import serializers
from dolphin.models.word_model import Word
from rest_framework.pagination import PageNumberPagination

class WordSerializer(serializers.Serializer):                
    id = serializers.CharField(allow_blank=False)
    word = serializers.CharField(required=True, allow_blank=False)
    remark = serializers.CharField(required=True)
    state = serializers.IntegerField(required=True)    

    def get(self):        
        word_result = Word.objects.filter(state=0)[:1]      
        return word_result

    def create(self, validated_data):
        return Word.objects.create(**validated_data)

    def updateStatus(self, state,id):
        return Word.objects.filter(id=id).update(state=state)