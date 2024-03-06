from backend.models import OrderHistory, Order
from backend.tasks import notify_admin_order_placement

class OrderService:
    
    def __init__(self, order:Order):
        self.order = order
    
    def post_order_placement_process(self, user):
        history = OrderHistory.objects.create(
            order = self.order,
            modified_by = user,
            remarks = 'Order Placed',
            status = self.order.status
        )
        notify_admin_order_placement(self.order.ref_no, verbose_name='Notify Admin for Order Placement.')
        