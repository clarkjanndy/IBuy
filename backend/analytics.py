from datetime import datetime
from decimal import Decimal

from django.db.models import Sum
from backend.models import Payment, User, Expense, Order


def sales_sum(date_from=None, date_to=None, return_objects=False):
    sales = Payment.objects.filter(status='approved')

    if date_from:
        _date_from = datetime.strptime(date_from, '%Y-%m')
        sales = sales.filter(modified_at__year__gte=_date_from.year, modified_at__month__gte=_date_from.month)
        
    if date_to:
        _date_to = datetime.strptime(date_to, '%Y-%m')
        sales = sales.filter(modified_at__year__lte=_date_to.year, modified_at__month__lte=_date_to.month)
        
    total_sales = sales.aggregate(total=Sum('amount')).get('total') if sales else Decimal(0)
    
    if return_objects:
        return total_sales, sales
    
    return total_sales

def expenses_sum(date_from=None, date_to=None, return_objects=False):
    expenses = Expense.objects.all().order_by('billing_month')
    
    if date_from:
        _date_from = datetime.strptime(date_from, '%Y-%m')
        expenses = expenses.filter(billing_month__year__gte=_date_from.year, billing_month__month__gte=_date_from.month)
        
    if date_to:
        _date_to = datetime.strptime(date_to, '%Y-%m')
        expenses = expenses.filter(billing_month__year__lte=_date_to.year, billing_month__month__lte=_date_to.month)
    
    total_expenses = expenses.aggregate(total=Sum('amount')).get('total') if expenses else Decimal(0)
        
    if return_objects:
        return total_expenses, expenses

    return total_expenses

def user_count():
    return User.count()

def order_recent(num_rows=6):
    if not num_rows:
        return []
    
    return Order.objects.all().order_by('-created_at')[:num_rows]