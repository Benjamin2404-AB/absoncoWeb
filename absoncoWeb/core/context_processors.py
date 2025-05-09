# context_processors.py
from django.db.models import Sum
from django.utils import timezone
from .models import Order, OrderItem

def cart_count(request):
    # Default
    total_items = 0

    if request.user.is_authenticated:
        # Try to fetch the active (not yet ordered) cart
        order = (
            Order.objects
                 .filter(user=request.user, ordered=False)
                 .prefetch_related('items')
                 .first()
        )

        if order:
            # Aggregate sum of `quantity` across its items
            agg = order.items.aggregate(total=Sum('quantity'))
            total_items = agg['total'] or 0

    return {'cart_count': total_items}
