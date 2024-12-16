from django import template

register = template.Library()

@register.filter
def cedi(value):
    """Formats the value with the Ghanaian cedi symbol."""
    try:
        return f"GH¢ {float(value):,.2f}"
    except (ValueError, TypeError):
        return value
