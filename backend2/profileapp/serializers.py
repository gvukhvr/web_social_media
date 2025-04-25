# profileapp/serializers.py
from rest_framework import serializers
from .models import Profile

class ProfileSerializer(serializers.Serializer):
    username = serializers.CharField(source='user.username', required=False)
    avatar = serializers.ImageField(required=False)

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        username = user_data.get('username')
        
        if username:
            instance.user.username = username
            instance.user.save()

        instance.bio = validated_data.get('bio', instance.bio)
        instance.avatar = validated_data.get('avatar', instance.avatar)
        instance.save()

        return instance

    def create(self, validated_data):
        user_data = validated_data.pop('user', {})
        user = user_data.get('user', None)

        profile = Profile.objects.create(user=user, **validated_data)
        return profile