from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from backend.analytics import sales_and_expense_pie_chart, report_bar_graph

__all__ = ['SalesExpensePieChart', 'ReportBarGraph']

class SalesExpensePieChart(GenericAPIView):
    permission_classes = (IsAdminUser, )

    def get(self, request, *args, **kwargs):

        return Response({
            "status": "success", 
            "data": sales_and_expense_pie_chart()
        })
        
class ReportBarGraph(GenericAPIView):
    permission_classes = (IsAdminUser, )

    def get(self, request, *args, **kwargs):

        return Response({
            "status": "success", 
            "data": report_bar_graph()
        })