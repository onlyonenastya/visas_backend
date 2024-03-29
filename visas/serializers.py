from rest_framework import serializers

from .models import *


class VisaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visa
        fields = "__all__"

class UserOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email'] 

class OrderSerializer(serializers.ModelSerializer):
    reactor = VisaSerializer(read_only=True, many=True)
    user = UserOrderSerializer(read_only=True)

    class Meta:
        model = Order
        fields = "__all__"


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
            name=validated_data['name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

