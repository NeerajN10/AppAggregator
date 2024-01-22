import requests
from django.db import transaction
from rest_framework import serializers, status
from bs4 import BeautifulSoup

from app_aggregator.model_choices import UserTypes
from app_aggregator.models import AppData, UserPurchasedApps, User


class AppDataSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)

    class Meta:
        model = AppData
        fields = "__all__"
        extra_kwargs = {
            'name': {
                'required': False
            },
            'description': {
                'required': False
            }
        }

    def validate(self, validated_data):
        url = validated_data.get('url', '')

        if not url.startswith("https://play.google.com/store/apps/details?id="):
            raise serializers.ValidationError(
                "Invalid Play Store URL.",
                code=status.HTTP_412_PRECONDITION_FAILED)

        return super().validate(validated_data)

    @transaction.atomic
    def create(self, validated_data):
        url = validated_data['url']

        response = requests.get(url)

        active = validated_data.get('active', False)

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'lxml')

        # Extract information using BeautifulSoup methods, we can add more data after carefully parsing the contents.
        if not soup.find('h1'):
            raise serializers.ValidationError(detail='Looks like the URL is malformed.',
                                              code=status.HTTP_412_PRECONDITION_FAILED)
        name = soup.find('h1').text
        description = soup.find('div', class_='bARER').contents[0]
        validated_data['name'] = name
        validated_data['description'] = description
        validated_data['active'] = active
        instance = super(AppDataSerializer, self).create(validated_data=validated_data)
        return instance


class UserPurchasedAppsSerializer(serializers.ModelSerializer):
    app_name = serializers.CharField(source='app.name', read_only=True)

    class Meta:
        model = UserPurchasedApps
        fields = "__all__"
        extra_kwargs = {
            'user': {
                'required': False
            },
        }

    def validate(self, validated_data):
        logged_in_user = self.context.get('request').user
        validated_data['user'] = logged_in_user
        validated_data['active'] = True

        if logged_in_user.purchased_app.filter(app_id=validated_data['app'].id).exists():
            raise serializers.ValidationError(detail='You have already purchased this app.',
                                              code=status.HTTP_412_PRECONDITION_FAILED)

        return super().validate(validated_data)

    @transaction.atomic
    def create(self, validated_data):
        instance = super(UserPurchasedAppsSerializer, self).create(validated_data=validated_data)
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
