class OrderBook:
    """Order management system for AI trading bot."""
    
    def __init__(self):
        self.orders = []

    def place_order(self, order_type, quantity, price):
        """Execute order based on AI trading signals."""
        order = {"type": order_type, "quantity": quantity, "price": price}
        self.orders.append(order)

    def get_orders(self):
        """Return all executed orders."""
        return self.orders
