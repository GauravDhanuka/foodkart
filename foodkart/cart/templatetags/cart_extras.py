from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    """
    Multiplies the value by the argument.
    Usage: {{ value|mul:arg }}
    Example: {{ item.quantity|mul:item.price_per_kg }}
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return '' # Return empty string or 0.0 if multiplication is not possible
