"""
API file for login app

consists of the viewsets for the apis in the login app

"""

from rest_framework import status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework import viewsets


from login.functions import login, register, forgot_password, reset_password, verify_email


class UserViewSet(viewsets.ViewSet):
    """
    Viewset for registering and logging in users
    """
    
    authentication_classes = ()
    permission_classes = ()
    
    @list_route(methods=['post'])
    def login(self, request):
        """
        Logging in a user
        ---
        # YAML
        
        parameters:
            -   name: email
                description: User's email
                required: true
                type: string
                paramType: form
            -   name: password
                description: User's password
                required: true
                type: string
                paramType: form
        """
        response = login(request)
            
        return Response(response, status=status.HTTP_200_OK)
        
    @list_route(methods=['post'])
    def register(self, request, format=None):
        """
        Registering a new user
        ---
        # YAML
        
        parameters:
            - name: email
              description: user email
              required: true
              type: string
              paramType: form
            - name: password
              required: true
              type: string
              paramType: form
            - name: first_name
              required: true
              type: string
              paramType: form
            - name: last_name
              required: true
              type: string
              paramType : form
            - name: designation
              required: true
              paramType: form
              type: string
              description: Teacher or Student
        
        """
        response = register(request)
        
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    @list_route()
    def verify_email(self, request, format=None):
        """
        Verify user's email after registration
        ---
        # YAML
        
        parameters:
            - name: code
              description: code for email verification
              required: true
              type: string
              paramType: query
        """
        
        response = verify_email(request)
        
        return Response(response, status=status.HTTP_200_OK)


class UserPasswordViewSet(viewsets.ViewSet):
    """
    Viewsets for password related apis
    """
    
    authentication_classes = ()
    permission_classes = ()
    
    @list_route()
    def forgot_password(self, request):
        """
        Send password reset email to user
        ---
        # YAML
        
        parameters:
            - name: email
              description: user email
              required: true
              type: string
              paramType: query
        
        """
        response = forgot_password(request)
            
        return Response(response, status=status.HTTP_200_OK)
    
    @list_route(methods=['post'])
    def reset_password(self, request):
        """
        Reset user's password
        ---
        # YAML
        
        parameters:
            - name: reset_code
              description: Password reset code mailed to the user
              required: true
              type: string
              paramType: form
            - name: password
              description: New password to set for the user
              required: true
              type: string
              paramType: form
        
        """
        
        response = reset_password(request)
            
        return Response(response, status=status.HTTP_200_OK)

