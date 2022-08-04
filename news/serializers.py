from rest_framework import serializers
from .models import *


class NewsSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = News
        fields = ('title', 'content', 'category')


class NewsByCategorySerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = News
        fields = ('title', 'content', 'category')

