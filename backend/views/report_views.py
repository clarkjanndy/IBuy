from datetime import datetime

from django.http import HttpResponse
from django.template.loader import get_template
from django.db.models import Sum

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser

from backend.utils.pdf_generator import PDFGenerator
from backend.utils.constants import base_64_ibuy_logo, base_64_bcc_logo
from backend.models import Payment, Expense
from backend.analytics import sales_sum, expenses_sum


__all__ = ['ReportPDF']

class ReportPDF(GenericAPIView):
    permission_classes = (IsAdminUser, )
    
    @staticmethod
    def get_data(request):
        params = request.query_params
        date_from = params.get('from')
        date_to = params.get('to')
        
        total_sales, sales = sales_sum(date_from, date_to, return_objects=True)
        total_expenses, expenses = expenses_sum(date_from, date_to, return_objects=True)
        total_profit = total_sales - total_expenses
        
        return {
            'sales': {
                "objects": sales,
                "total": total_sales           
            },
            'expenses': {
                "objects": expenses,
                "total": total_expenses           
            },
            'period': {
                'date_from':  date_from,
                'date_to':  date_to,
            },
            'total_profit': total_profit
        }
              
    def get(self, request, *args, **kwargs):
        template = get_template('backend/report.html')
        data = self.get_data(request)
        context = {
            'data': data,
            'base_64_ibuy_logo': base_64_ibuy_logo,
            'base_64_bcc_logo': base_64_bcc_logo
        }
        
        generator = PDFGenerator(template, context)
        pdf = generator.generate()
        
        response = HttpResponse(content=pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'filename="report.pdf"'
        
        return response

        