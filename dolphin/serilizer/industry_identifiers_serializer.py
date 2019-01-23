from rest_framework import serializers
from dolphin.models.book_industry_identifiers_model import BookIndustryIdentifiers

class IndustryIdentifiersSerializer(serializers.Serializer):                
    book_id = serializers.IntegerField(required=False)
    identifier = serializers.CharField(required=False)
    type = serializers.CharField(required=False)  

    def create(self, validated_data):
        return BookIndustryIdentifiers.objects.create(**validated_data)