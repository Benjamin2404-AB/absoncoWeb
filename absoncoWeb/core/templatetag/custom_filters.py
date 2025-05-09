from django import template

register = template.Library()

@register.filter
def cedi(value):
    """Formats the value with the Ghanaian cedi symbol."""
    try:
        return f"GH¢ {float(value):,.2f}"
    except (ValueError, TypeError):
        return value


@register.filter
def sum_total_price(cart_items):
    """Sums up the total_price attribute of each item in cart_items."""
    return sum(cart_item['total_price'] for cart_item in cart_items)



@register.filter
def sum_quantity(cart_items):
    total_quantity = 0
    for cart_item in cart_items:
        total_quantity += cart_item['quantity']  # Assuming 'quantity' is in the cart item dictionary
    return total_quantity