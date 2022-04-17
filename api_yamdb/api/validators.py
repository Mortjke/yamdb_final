from rest_framework import serializers
from reviews.models import CustomUser


def validate_username(self, name):
    if name == 'me':
        raise serializers.ValidationError('Имя "me" нельзя использовать')
    elif name is None or name == "":
        raise serializers.ValidationError('Вы не указали имя')
    return name


def validate_email(self, email):
    if email is None or email == "":
        raise serializers.ValidationError('Вы не указали email')
    return email


def validate_correct_data(self, data):
    username = data.get('username')
    email = data.get('email')
    if (
        CustomUser.objects.filter(username=username).exists()
        and CustomUser.objects.get(username=username).email != email
    ):
        raise serializers.ValidationError('Такое имя уже существует')
    if (
        CustomUser.objects.filter(email=email).exists()
        and CustomUser.objects.get(email=email).username != username
    ):
        raise serializers.ValidationError('Такой адрес уже существует')
    return data


def validate_correct_code(self, data):
    username = data.get('username')
    confirmation_code = data.get('confirmation_code')
    if username is None:
        raise serializers.ValidationError('Вы не указали имя')
    if confirmation_code is None:
        raise serializers.ValidationError('Вы не указали код')
    return data
