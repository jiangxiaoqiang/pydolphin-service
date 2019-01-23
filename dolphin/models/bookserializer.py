# -*- coding: UTF-8 -*-

from rest_framework import serializers
from dolphin.models.bookmodel import Book
from dolphin.serilizer.industry_identifiers_serializer import IndustryIdentifiersSerializer

class BookSerializer(serializers.Serializer):                
    name = serializers.CharField(allow_blank=False)
    isbn = serializers.CharField(required=True, allow_blank=False)
    author = serializers.ListField(required=True)
    publisher = serializers.ListField(required=True)
    publish_year = serializers.CharField(required=False,allow_blank=True)
    binding = serializers.CharField(required=False,allow_blank=True)
    price = serializers.CharField(required=False, allow_blank=True)
    subtitle = serializers.CharField(required=False,allow_blank=True)
    original_name = serializers.CharField(required=False,allow_blank=True)
    translator = serializers.ListField(required=False)
    pages = serializers.CharField(required=False,allow_blank=True)
    issuer = serializers.CharField(required=False,allow_blank=True)
    creator = serializers.CharField(required=False,allow_blank=True)
    douban_id = serializers.CharField(required=False,allow_blank=True)
    source = serializers.CharField(required=False,allow_blank=True)
    isbn10 = serializers.CharField(required=False,allow_blank=True)
    industryi_dentifiers = serializers.CharField(required=False,allow_blank=True)


    def create(self, validated_data):
        return Book.objects.create(**validated_data)