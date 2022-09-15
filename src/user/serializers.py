from django.contrib.auth import authenticate

from rest_framework import serializers
from user import models


class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * email
      * password.
    It will try to authenticate the user with when validated.
    """
    email = serializers.EmailField(
        label="Email",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take email and password from request
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            # user = authenticate(email=email, password=password)
            # user = authenticate(request=self.context.get('request'), username=email, password=password)
            
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong email or password.'
                raise serializers.ValidationError(msg, code='authorization')
            if not user.is_active:
                msg = 'Account disabled, contact admin.'
                raise serializers.ValidationError(msg, code='authorization')
            if not user.is_verified:
                msg = 'Email is not verified.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "email" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    cartao_list = serializers.PrimaryKeyRelatedField(
        many=True, 
        read_only=False,
        queryset=cartao_models.Cartao.objects.all()
    )

    class Meta:
        model = models.User
        fields = [
            'email',
            'full_name',
            'is_active',
            'is_verified',
            'is_superuser',
            'created_at',
            'updated_at',
            'cartao_list',
        ]
