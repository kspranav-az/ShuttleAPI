from rest_framework import serializers
from django.contrib.auth import authenticate
from datetime import timedelta, datetime
from .models import User, OTP,  Account, Transaction

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('balance',)  # Consider including additional user information if needed

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('amount', 'timestamp', 'type', 'rfid_used', 'rfid_id' , 'reference_id')
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('registration_number', 'email', 'password', 'rfid_id')  # Include rfid_id

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['registration_number'],
            validated_data['email'],
            validated_data['password']
        )
        if 'rfid_id' in validated_data:
            user.rfid_id = validated_data['rfid_id']
            user.save()
        return user
class LoginSerializer(serializers.Serializer):
    registration_number = serializers.CharField()
    otp = serializers.CharField()

    def validate(self, data):
        registration_number = data['registration_number']
        otp = data['otp']

        # Authenticate user with registration number and OTP
        user = authenticate(registration_number=registration_number, otp=otp)

        if not user:
            raise serializers.ValidationError('Invalid username or password')

        # Check for valid OTP within the last 5 minutes
        valid_otp_window = datetime.now() - timedelta(minutes=5)
        otp_object = OTP.objects.filter(user=user, created_at__gt=valid_otp_window).first()

        if not otp_object or otp_object.code != otp:
            raise serializers.ValidationError('Invalid OTP')

        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('registration_number', 'email', 'rfid_id')  # Include rfid_id in serializer output

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ('code',)

