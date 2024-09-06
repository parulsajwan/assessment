import pandas as pd

from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.db.models import Sum, F, Subquery, OuterRef, Max
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from products.serializers import (
    CustomLoginSerializer,
    CustomUserSerializer,
)
from .models import Product

User = get_user_model()


class SignupView(APIView):
    '''
    The SignupView class is an API view that handles the signup functionality. It receives a POST request with user data, validates the data using the CustomUserSerializer,
    and creates a new user if the data is valid.
    '''
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = CustomUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Signup successful'}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Something went wrong', 'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    '''
    The LoginView class is an API view that handles the login functionality. It receives a POST request with user credentials, validates them using the CustomLoginSerializer,
    and returns a response indicating whether the login was successful or not.
    '''
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = CustomLoginSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data['user']
                refresh = RefreshToken.for_user(user)
                return Response({'access_token': str(refresh.access_token), 'refresh_token': str(refresh)}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Something went wrong', 'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SummaryReportView(APIView):
    '''
    API view for generating a summary report in CSV format based on product data. Requires authentication.
    Retrieves product information and calculates total revenue, top-selling product, and quantity sold per category.
    Returns a CSV file as a response.
    '''

    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):

        top_product_subquery = Product.objects.filter(
            category=OuterRef('category')
        ).order_by('-quantity_sold').values('product_name')[:1]

        query = Product.objects.values('category').annotate(
            total_revenue=Sum(F('price') * F('quantity_sold')),
            top_product=Subquery(top_product_subquery),
            top_product_quantity_sold=Max('quantity_sold')
        ).order_by('category')

        df = pd.DataFrame.from_records(query)

        if df.empty:
            return HttpResponse("No data available", status=204)
        df = df[['category', 'total_revenue', 'top_product', 'top_product_quantity_sold']]


        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="summary_report.csv"'

        df.to_csv(response, index=False)

        return response
