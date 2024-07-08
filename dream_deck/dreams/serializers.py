from rest_framework import serializers
from .models import Dream, Emotion, Theme, DreamEmotion, DreamTheme
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password


class DreamSerializer(serializers.ModelSerializer):
    emotions = serializers.ListField(
        child=serializers.DictField(), write_only=True, required=False
    )
    themes = serializers.ListField(
        child=serializers.CharField(), write_only=True, required=False
    )

    class Meta:
        model = Dream
        fields = [
            "id",
            "title",
            "content",
            "date",
            "is_lucid",
            "audio_recording",
            "emotions",
            "themes",
        ]
        read_only_fields = ["id", "date"]

    def create(self, validated_data):
        emotions_data = validated_data.pop("emotions", [])
        themes_data = validated_data.pop("themes", [])

        dream = Dream.objects.create(**validated_data)

        for emotion_data in emotions_data:
            emotion, _ = Emotion.objects.get_or_create(name=emotion_data["name"])
            DreamEmotion.objects.create(
                dream=dream, emotion=emotion, intensity=emotion_data["intensity"]
            )

        for theme_name in themes_data:
            theme, _ = Theme.objects.get_or_create(name=theme_name)
            DreamTheme.objects.create(dream=dream, theme=theme)

        return dream
    

class EmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotion
        fields = ['id', 'name']

class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ['id', 'name']


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True, required=True)
    name = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "name",
            "date_of_birth",
            "password",
            "confirm_password",
        )
        extra_kwargs = {"email": {"required": True}}

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        name = validated_data.pop("name", "")
        first_name, last_name = name.split(" ", 1) if " " in name else (name, "")
        user = User.objects.create_user(
            first_name=first_name, last_name=last_name, **validated_data
        )
        return user


class LoginSerializer(serializers.Serializer):
    usernameOrEmail = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)