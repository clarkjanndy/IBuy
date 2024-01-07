from backend.models import OrderHistory, Order

class OrderService:
    
    def __init__(self, order:Order):
        self.order = order
        
    def notify_admin(self):
        pass
        
    def create_history(self, user, remarks, status):
        history = OrderHistory.objects.create(
            order = self.order,
            modified_by = user,
            remarks = remarks,
            status = status
        )
        return history
    