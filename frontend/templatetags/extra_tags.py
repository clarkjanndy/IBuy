from django import template
from backend.models import Expense

EXPENSE_CAPITAL_TYPE_MAPPING = Expense.capital_type_mapping()

register = template.Library()

@register.filter()
def is_selected(value, current_option):
    return 'selected' if value == current_option else ""

@register.filter()
def is_checked(value):
    return 'checked' if value else ""

@register.filter()
def bootstrapy_alert(string: str):
    MAPPING = {
        "success":  "success",
        "info":  "info",
        "warning": "warning",
        "error": "danger",
        "debug": "secondary"
    }

    return MAPPING.get(string)

@register.filter()
def long_gender(string: str):
    MAPPING = {
        "M":  "Male",
        "F":  "Female"
    }

    return MAPPING.get(string)


@register.filter()
def to_human_readable(string: str):    
    return EXPENSE_CAPITAL_TYPE_MAPPING.get(string)





