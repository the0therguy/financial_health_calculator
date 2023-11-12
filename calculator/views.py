from django.shortcuts import render
from .models import *
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password


# Create your views here.

class SignUpView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SigninView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = MyTokenObtainPairSerializer


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.data.get('old_password')
            new_password = serializer.data.get('new_password')

            # Check if the old password matches the current password
            if not check_password(old_password, request.user.password):
                return Response({"message": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

            # Change the password and save the user object
            request.user.set_password(new_password)
            request.user.save()
            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateFinancialData(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        year = request.GET.get('year')
        if year:
            data = FinancialData.objects.filter(user=request.user, year=year).order_by('month_name', 'year')
        else:
            data = FinancialData.objects.filter(user=request.user).order_by('month_name', 'year')
        serializer = FinancialDataSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = FinancialData.objects.filter(user=request.user, business_name=request.data.get('business_name'),
                                            month_name=request.data.get('month_name'), year=request.data.get('year'))
        if data:
            return Response("Data already exists", status=status.HTTP_400_BAD_REQUEST)
        if request.data.get('monthly_income') == 0 or request.data.get('expenses') == 0:
            income_ratio = 0.0
        else:
            income_ratio = round(request.data.get('monthly_income', 0) / request.data.get('expenses', 0),
                                 2)

        if request.data.get('debts') == 0 or request.data.get('assets') == 0:
            debt_to_asset_ratio = 0.0
        else:
            debt_to_asset_ratio = round(request.data.get('debts', 0) / request.data.get('assets', 0), 2)

        request.data['user'] = request.user.id
        request.data['income_ratio'] = income_ratio
        request.data['debt_to_asset_ratio'] = debt_to_asset_ratio
        request.data['financial_health_score'] = income_ratio * 0.4 + debt_to_asset_ratio * 0.6
        if request.data['financial_health_score'] <= 0.25:
            request.data['financial_health_description'] = 'Poor'
        elif 0.25 < request.data['financial_health_score'] <= 0.5:
            request.data['financial_health_description'] = 'Average'
        elif 0.50 < request.data['financial_health_score'] <= 0.75:
            request.data['financial_health_description'] = 'Good'
        else:
            request.data['financial_health_description'] = 'Excellent'
        serializer = FinancialDataCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FinanceData(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return FinancialData.objects.get(pk=pk)
        except FinancialData.DoesNotExist:
            raise None

    def get(self, request, pk):
        financial_data = self.get_object(pk)
        if financial_data:
            serializer = FinancialDataSerializer(financial_data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("No financial data found with this email", status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        financial_data = self.get_object(pk)
        if financial_data:
            financial_data.delete()
            return Response("Financial data deleted successfully", status=status.HTTP_204_NO_CONTENT)
        return Response("No financial data found with this email", status=status.HTTP_404_NOT_FOUND)
