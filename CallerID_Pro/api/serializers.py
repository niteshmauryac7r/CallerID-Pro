from rest_framework import serializers
from .models import User, Contact, Spam

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('name', 'phone_number')

class UserSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'name', 'phone_number', 'email', 'contacts')

    def validate_phone_number(self, value):
        if not value.isdigit() or len(value) != 10:
            raise serializers.ValidationError("Phone number must be exactly 10 digits.")
        return value


class SpamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spam
        fields = ('phone_number', 'is_spam')
