from rest_framework import serializers

from apps.accounts.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "url",
            "first_name",
            "last_name",
            "username",
            "added_field",
        )
