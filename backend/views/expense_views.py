from django.contrib import messages

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from backend.serializers import ExpenseSerializer
from backend.models import Expense

__all__ = ['ExpenseListCreate', 'ExpenseById']

class ExpenseListCreate(ListCreateAPIView):
    permission_classes = (IsAdminUser, )
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        messages.success(request, "Expense entry created successfully!")
        return Response({
            "status": "success", 
            "data": response.data
        })
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        return Response({
            "status": "success", 
            "data": response.data
        })
    
class ExpenseById(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAdminUser, )
    queryset = Expense.objects.all()
    lookup_field='pk'
    serializer_class = ExpenseSerializer

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)

        return Response({
            "status": "success", 
            "data": response.data
        })
    
    def patch(self, request, *args, **kwargs):
        response = super().patch(request, *args, **kwargs)
        
        messages.success(request, "Expense entry updated succesfully!")
        return Response({
            "status": "success", 
            "data": response.data
        })

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        msg = 'Expense entry deleted successfully!'
        
        messages.success(request, msg)
        return Response({
            "status": "success", 
            "data": {
                "message": msg
            }
        })