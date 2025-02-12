from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from .models import User, Contact, Spam
from .serializers import UserSerializer, SpamSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        # Allow public access to registration (create) but require authentication for other actions
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def perform_create(self, serializer):
        # Save the user and hash the password after saving
        user = serializer.save()
        password = self.request.data.get('password')
        if password:
            user.set_password(password)
            user.save()

    @action(detail=False, methods=['get'])
    def search_by_name(self, request):
        query = request.query_params.get('name', '')
        
        if query:
            # Search in the User table based on name
            users_start = User.objects.filter(name__istartswith=query)
            users_contain = User.objects.filter(name__icontains=query).exclude(name__istartswith=query)
            users = users_start | users_contain
            
            # Search in the Contact table based on name
            contacts = Contact.objects.filter(name__icontains=query)
            
            # Initialize results list
            results = []

            # Process users from the User table
            for user in users:
                spam = Spam.objects.filter(phone_number=user.phone_number).first()
                spam_status = spam.is_spam if spam else False

                # Check if the current user is in the person's contact list
                contact = Contact.objects.filter(user=request.user, phone_number=user.phone_number).first()

                result = {
                    'name': user.name,
                    'phone_number': user.phone_number,
                    'spam': spam_status,
                    'email': user.email if contact else None  # Only display email if in contact list
                }
                results.append(result)

            # Process contacts from the Contact table
            for contact in contacts:
                spam = Spam.objects.filter(phone_number=contact.phone_number).first()
                spam_status = spam.is_spam if spam else False

                # Check if the current user is in the contact list of the person
                contact_details = Contact.objects.filter(user=request.user, phone_number=contact.phone_number).first()

                result = {
                    'name': contact.name,
                    'phone_number': contact.phone_number,
                    'spam': spam_status,
                    'email': contact.email if contact_details else None  # Only display email if in contact list
                }
                results.append(result)

            # Deduplicate results to avoid multiple entries for the same person
            results = {result['phone_number']: result for result in results}.values()

            return Response(results)
        
        return Response({"message": "No query parameter provided."}, status=status.HTTP_400_BAD_REQUEST)

    
    @action(detail=False, methods=['get'])
    def search_by_phone(self, request):
        query = request.query_params.get('phone_number', '')

        if query:
            results = []
            
            # Check for a registered user with the phone number
            user = User.objects.filter(phone_number=query).first()
            if user:
                spam = Spam.objects.filter(phone_number=user.phone_number).first()
                spam_status = spam.is_spam if spam else False

                # Check if the current user is in the person's contact list
                contact = Contact.objects.filter(user=request.user, phone_number=user.phone_number).first()

                result = {
                    'name': user.name,
                    'phone_number': user.phone_number,
                    'spam': spam_status,
                    'email': user.email if contact else None  # Only display email if in contact list
                }
                results.append(result)
            else:
                # If no registered user is found, search in the Contact table
                contacts = Contact.objects.filter(phone_number=query)
                for contact in contacts:
                    spam = Spam.objects.filter(phone_number=contact.phone_number).first()
                    spam_status = spam.is_spam if spam else False
                    contact_details = Contact.objects.filter(user=request.user, phone_number=contact.phone_number).first()

                    result = {
                        'name': contact.name,
                        'phone_number': contact.phone_number,
                        'spam': spam_status,
                        'email': contact.email if contact_details else None # No email shown as it's not a registered user
                    }
                    results.append(result)

            if not results:
                return Response({"message": "No contacts found with this phone number."}, status=status.HTTP_404_NOT_FOUND)

            return Response(results)

        return Response({"message": "No phone number provided."}, status=status.HTTP_400_BAD_REQUEST)
            
    
    @action(detail=True, methods=['get'])
    def contact_details(self, request, pk=None):
        user = self.get_object()  # Get the user object from the URL parameter pk
        current_user = request.user  # Get the currently logged-in user
        
        # Check if the current user is in the contact list of the user being viewed
        contact = Contact.objects.filter(user=current_user, phone_number=user.phone_number).first()

        result = {
            'name': user.name,
            'phone_number': user.phone_number,
            'spam': Spam.objects.filter(phone_number=user.phone_number).first().is_spam,
            'email': user.email if contact else None  # Display email only if the user is in the contact list
        }

        return Response(result)
    
'''
class SpamViewSet(viewsets.ModelViewSet):
    queryset = Spam.objects.all()
    serializer_class = SpamSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Save the spam record (this will add the contact to the spam list)
        spam = serializer.save()
        
        # Return a custom response
        return Response({
            'message': 'Successfully added the contact to the spam list',
            'phone_number': spam.phone_number,
            'is_spam': spam.is_spam
        }, status=status.HTTP_201_CREATED)
'''    
class SpamViewSet(viewsets.ModelViewSet):
    queryset = Spam.objects.all()
    serializer_class = SpamSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Save the spam record
        serializer.save()

    def create(self, request, *args, **kwargs):
        # Call the original create method
        response = super().create(request, *args, **kwargs)
        
        # Add a custom response message
        return Response({
            'message': 'Successfully added the contact to the spam list',
            'phone_number': response.data['phone_number'],
            'is_spam': response.data['is_spam']
        }, status=status.HTTP_201_CREATED)
        
class LoginView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')

        if not phone_number or not password:
            return Response({'detail': 'Phone number and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=phone_number, password=password)
        if user is not None:
            # Generate token
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            })
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
