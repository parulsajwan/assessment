from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    '''
    The CustomUserSerializer class is a serializer class in Django that is used to serialize and deserialize user data.
    This class provides validation for the username field, creates new user instances, and specifies the fields to be included in the serialized output.
    '''
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class CustomLoginSerializer(serializers.Serializer):
    '''
    The CustomLoginSerializer class is a serializer class in Django that is used for validating user login credentials.
    It checks if the provided username and password are valid and returns the corresponding user if they are.
    '''
    password = serializers.CharField()
    username = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = User.objects.filter(username__iexact=username).first()
            if user and user.check_password(password):
                return {'user': user}
            raise serializers.ValidationError(
                {'error': 'Invalid username or password'})
        raise serializers.ValidationError(
            {'error': 'username and password are required'})
