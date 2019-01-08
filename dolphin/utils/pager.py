# -*- coding: UTF-8 -*-

from rest_framework import serializers
from dolphin.models import word_model


class PagerSerialiser(serializers.ModelSerializer):
    class Meta:
        model = word_model
        fields = "__all__"