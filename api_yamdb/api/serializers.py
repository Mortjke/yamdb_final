from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from reviews.models import Category, Comment, CustomUser, Genre, Review, Title


def not_me(name):
    if name == 'me':
        raise serializers.ValidationError('Имя "me" нельзя использовать')
    if name is None or name == "":
        raise serializers.ValidationError('Вы не указали имя')


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )

    def validate_username(self, name):
        not_me(name)
        return name

    def validate_email(self, email):
        if email is None or email == "":
            raise serializers.ValidationError('Вы не указали email')
        return email


class ReadOnlyRoleSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)

    def validate_username(self, name):
        not_me(name)
        return name

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        user = CustomUser.objects.filter(username=username).first()
        if user and user.email != email:
            raise serializers.ValidationError('Такой адрес уже существует')
        return data


class AuthSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    confirmation_code = serializers.CharField(max_length=6)

    class Meta:
        model = CustomUser
        fields = ('username', 'confirmation_code')

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')
        if username is None:
            raise serializers.ValidationError('Вы не указали имя')
        if confirmation_code is None:
            raise serializers.ValidationError('Вы не указали код')
        return data


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        exclude = ['id']


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        exclude = ['id']


class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        many=False
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        required=False,
        many=True
    )

    class Meta:

        model = Title
        fields = '__all__'


class Titleserializer(serializers.ModelSerializer):
    category = CategoriesSerializer(
        many=False,
        read_only=True
    )
    genre = GenreSerializer(
        many=True,
        read_only=True
    )
    rating = serializers.IntegerField(read_only=True)

    def validate(self, data):
        request = self.context['request']
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(
                title=title,
                author=request.user
            ).exists()
        ):
            raise ValidationError('Разрешено не более одного отзыва!')
        return data

    class Meta:

        model = Title
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    def validate(self, data):
        request = self.context['request']
        title_id = self.context.get('view').kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(
                title=title,
                author=request.user
            ).exists()
        ):
            raise ValidationError('Один отзыв, не более!')
        return data

    class Meta:

        model = Review
        exclude = ('title',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
    )

    class Meta:

        model = Comment
        exclude = ('review',)
