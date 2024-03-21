from datetime import datetime

from django.http import HttpResponse
from django.template.loader import get_template
from django.db.models import Sum, Q

from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAdminUser

from backend.utils.pdf_generator import PDFGenerator
from backend.utils.constants import base_64_ibuy_logo, base_64_bcc_logo
from backend.models import Payment, Expense


__all__ = ['ReportPDF']

class ReportPDF(GenericAPIView):
    permission_classes = (IsAdminUser, )
    
    @staticmethod
    def get_data(request):
        params = request.query_params
        sales = Payment.objects.filter(status='approved')
        expenses = Expense.objects.all()
        
        if 'from' in params:
            date_from = datetime.strptime(params['from'], '%Y-%m')
            sales = sales.filter(modified_at__year__gte=date_from.year, modified_at__month__gte=date_from.month)
            expenses = expenses.filter(billing_month__year__gte = date_from.year, billing_month__month__gte=date_from.month)
        
        if 'to' in params:
            date_to = datetime.strptime(params['to'], '%Y-%m')
            sales = sales.filter(modified_at__year__lte=date_to.year, modified_at__month__lte=date_to.month)
            expenses = expenses.filter(billing_month__year__lte = date_to.year, billing_month__month__lte=date_to.month)
        
        total_sales, total_expenses = 0, 0
        if sales:
            total_sales = sales.aggregate(total=Sum('amount'))['total']
            
        if expenses:       
            total_expenses = expenses.aggregate(total=Sum('amount'))['total']
        
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

        