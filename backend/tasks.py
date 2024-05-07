from django.db.models import Q

from background_task import background
from backend.models import Notification, Order, OrderHistory, User

@background(schedule=5)  
def notify_admin_order_placement(order_ref_no):
    admins = User.objects.filter(Q(role="admin") | Q(is_superuser=True))
    order = Order.objects.get(ref_no=order_ref_no)
    
    notified_count = 0
    for adm in admins:
        Notification.objects.create(
            user = adm,
            level = 'success',
            content = f'A new order has been placed with reference number {order.ref_no}.',
            link = f'/admin/manage-orders/{order.ref_no}'
        )
        notified_count += 1
        
    print(f'{notified_count} admin has been notified about order {order.ref_no}')