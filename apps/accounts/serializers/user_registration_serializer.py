# ecom/apps/accounts/serializers/user_registration_serializer.py

from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers


class UserRegistrationSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    added_field = serializers.CharField(required=True)

    def get_cleaned_data(self):
        super(UserRegistrationSerializer, self).get_cleaned_data()
        self.validated_data['first_name'] = self.validated_data.get('first_name', '')
        self.validated_data['last_name'] = self.validated_data.get('last_name', '')
        self.validated_data['added_field'] = self.validated_data.get('added_field', '')
        return self.validated_data

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])

        # add custom fields
        user.added_field = self.cleaned_data.get("added_field")

        user.save()
        return user
