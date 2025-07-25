from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from rest_framework import status, permissions, viewsets, generics, filters
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response

from .serializers import PasswordResetSerializer, PasswordResetConfirmSerializer

User = get_user_model()

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def reset_password(request):
    serializer = PasswordResetSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    try:
        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_url = f"http://example.com/reset/{uid}/{token}/"
        send_mail(
            'Password Reset',
            f'Click here to reset your password: {reset_url}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )
    except User.DoesNotExist:
        pass  # Don't reveal user existence
    return Response({'detail': 'If your email is registered, you will receive reset instructions.'})


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def reset_password_confirm(request):
    serializer = PasswordResetConfirmSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    uid = force_str(urlsafe_base64_decode(serializer.validated_data['uid']))
    token = serializer.validated_data['token']
    new_password = serializer.validated_data['new_password']
    try:
        user = User.objects.get(pk=uid)
        if default_token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            return Response({'detail': 'Password reset successful'})
        else:
            return Response({'detail': 'Invalid token'}, status=400)
    except User.DoesNotExist:
        return Response({'detail': 'Invalid user'}, status=400)
