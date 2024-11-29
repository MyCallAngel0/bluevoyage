from rest_framework import serializers
from .models import User
import uuid


class UserSerializer(serializers.ModelSerializer):
    """Serializer used to get the sign-up data"""
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'password', 'verify_token']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        
        instance.verify_token = uuid.uuid4()

        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance


