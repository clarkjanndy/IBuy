from datetime import datetime
from decimal import Decimal

from django.db.models import Sum, Count, Func, Value, F, CharField, ExpressionWrapper, Q
from django.db.models.functions import  ExtractYear, ExtractMonth, Concat
from backend.models import Payment, User, Expense, Order, OrderItem


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
    expenses = Expense.objects.all().order_by('billing_date')
    
    if date_from:
        _date_from = datetime.strptime(date_from, '%Y-%m')
        expenses = expenses.filter(billing_date__year__gte=_date_from.year, billing_date__month__gte=_date_from.month)
        
    if date_to:
        _date_to = datetime.strptime(date_to, '%Y-%m')
        expenses = expenses.filter(billing_date__year__lte=_date_to.year, billing_date__month__lte=_date_to.month)
    
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

def uniform_sales_ranking(num_rows=6):
    ranking = OrderItem.objects.select_related(
            'order',
        ).values(
            'uniform',
            'uniform__name',
            'uniform__inventory__unit',
            'uniform__price',
            'uniform__images__image'
        ).filter(
            order__payment__status='approved'
        ).annotate(
            total_revenue = Sum('order__total'),
            total_sold = Sum('quantity'),
        ).order_by('-total_revenue')[:num_rows]

    return ranking


def sales_and_expense_pie_chart():
    total_sales = sales_sum()
    total_expenses = expenses_sum()
    
    return [
        {
            "name": "Sales",
            "value": total_sales
        },
        {
            "name": "Expense",
            "value": total_expenses
        }
    ]
    
def report_bar_graph():
   # get sales
   sales = Payment.objects.filter(status='approved').annotate(
       month=ExtractMonth('modified_at'),
       year=ExtractYear('modified_at')
   ).values('month', 'year').annotate(
       total=Sum('amount'),
       month_year=ExpressionWrapper(
            Concat(F('month'), Value('-'), F('year')),
            output_field=CharField()
        )
   ).order_by('month', 'year')
   
   # get expenses
   expenses = Expense.objects.all().annotate(
       month=ExtractMonth('billing_date'),
       year=ExtractYear('billing_date')
   ).values('month', 'year').annotate(
       total=Sum('amount'),
       month_year=ExpressionWrapper(
            Concat(F('month'), Value('-'), F('year')),
            output_field=CharField()
        )
   ).order_by('month', 'year')
   
   
   # get users
   users = User.objects.all().annotate(
       month=ExtractMonth('date_joined'),
       year=ExtractYear('date_joined')
   ).values('month', 'year').annotate(
       total=Count('pk'),
       month_year=ExpressionWrapper(
            Concat(F('month'), Value('-'), F('year')),
            output_field=CharField()
        )
   ).order_by('month', 'year')
   
   # generate series
   series = []  
   sales_series = {"name": "Sales", "data": [sl['total'] for sl in sales]}
   series.append(sales_series)
   # --- #
   expense_series = {"name": "Expenses","data": [ex['total'] for ex in expenses]}
   series.append(expense_series)
   # --- #
   user_series = {"name": "Users","data": [usr['total'] for usr in users]}
   series.append(user_series)
   
   # generate categories(x-axis)
   querysets = [sales, expenses, users]
   # get the longest_querysets as we are going to generate the categories based on it
   longest_queryset = max(querysets, key=len)
   categories = [datetime.strptime(ctg['month_year'], "%m-%Y").strftime("%b %Y") for ctg in longest_queryset]
   
   return {
       "series": series,
       "categories": categories
   }
   
def capitals():
    qs = Expense.objects.exclude(Q(capital_type__isnull=True) | Q(capital_type='')).\
        values('capital_type').\
        annotate(total_amount = Sum('amount'))
        
    return qs
    
    