import random

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, OTP
from .serializers import LoginSerializer
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from django.conf import settings
from django.core.mail import send_mail
from .serializers import UserSerializer

from .models import Transaction, Account, User
from .serializers import TransactionSerializer
import uuid

class TransactionView(APIView):

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            # Get user from request (if authenticated) or from RFID
            user = None
            if request.user.is_authenticated:  # Check for authenticated user
                user = request.user
            else:
                rfid_tag = request.data.get('rfid_id')  # Get RFID tag from request data
                if rfid_tag:
                    try:
                        user = User.objects.get(rfid_id=rfid_tag)
                    except User.DoesNotExist:
                        return Response({'error': 'Invalid RFID tag'}, status=status.HTTP_400_BAD_REQUEST)

            if not user:  # Handle case where no user is found
                return Response({'error': 'User not found'}, status=status.HTTP_401_UNAUTHORIZED)

            # Check for sufficient balance for subtractions
            if serializer.validated_data['type'] == 'SUBTRACT' and Account.objects.get(user=user).balance < serializer.validated_data['amount']:
                return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)

            # Generate unique reference ID (optional for preventing multiple taps)
            reference_id = None
            if settings.PREVENT_MULTIPLE_TAPS:  # Use a setting flag
                while not reference_id:
                    reference_id = uuid.uuid4().hex
                    if Transaction.objects.filter(reference_id=reference_id).exists():
                        reference_id = None  # Try again if already exists

            # Create transaction and update account balance
            transaction = serializer.save(user=user, rfid_used=True, reference_id=reference_id)
            account = Account.objects.get(user=user)
            if transaction.type == 'ADD':
                account.balance += transaction.amount
            else:
                account.balance -= transaction.amount
            account.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class CreateUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            account = Account.objects.create(user=user)  # Create account linked to the user
            account.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(registration_number=serializer.validated_data['registration_number'], otp=serializer.validated_data['otp'])
        if user:
            login(request, user)
            token, _ = Token.objects.create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class GenerateOTPView(APIView):
    def post(self, request):
        registration_number = request.data.get('registration_number')
        if not registration_number:
            return Response({'error': 'Missing username'}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.filter(registration_number=registration_number).first()
        if not user:
            return Response({'error': 'Invalid username'}, status=status.HTTP_400_BAD_REQUEST)

        # Generate random OTP logic
        otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        # Delete existing OTPs for the user (optional to prevent code reuse)
        OTP.objects.filter(user=user).delete()
        OTP.objects.create(user=user, code=otp)

        # Send OTP to user email
        subject = 'Your OTP for Login'
        message = f'Your OTP for logging in to your account is {otp}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        send_mail(subject, message, email_from, recipient_list)

        return Response({'message': 'OTP sent to your email address'})
