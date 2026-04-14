def validate_symbol(symbol):
    if not symbol or not isinstance(symbol, str):
        raise ValueError('Symbol must be a non-empty string')
    symbol_upper = symbol.upper()
    if len(symbol_upper) < 2:
        raise ValueError('Symbol must be at least 2 characters')
    return symbol_upper


def validate_side(side):
    if not side or not isinstance(side, str):
        raise ValueError('Side must be a non-empty string')
    side_upper = side.upper()
    if side_upper not in ('BUY', 'SELL'):
        raise ValueError('Side must be BUY or SELL')
    return side_upper


def validate_order_type(order_type):
    if not order_type or not isinstance(order_type, str):
        raise ValueError('Order type must be a non-empty string')
    order_type_upper = order_type.upper()
    if order_type_upper not in ('MARKET', 'LIMIT'):
        raise ValueError('Order type must be MARKET or LIMIT')
    return order_type_upper


def validate_quantity(quantity):
    if quantity is None:
        raise ValueError('Quantity is required')
    try:
        qty = float(quantity)
    except (ValueError, TypeError):
        raise ValueError('Quantity must be a valid positive number')
    if qty <= 0:
        raise ValueError('Quantity must be greater than 0')
    return qty


def validate_price(price, order_type='MARKET'):
    if order_type == 'MARKET':
        return None
    if price is None:
        raise ValueError('Price is required for LIMIT orders')
    try:
        p = float(price)
    except (ValueError, TypeError):
        raise ValueError('Price must be a valid positive number')
    if p <= 0:
        raise ValueError('Price must be greater than 0')
    return p


def validate_all_inputs(symbol, side, order_type, quantity, price=None):
    validated = {
        'symbol': validate_symbol(symbol),
        'side': validate_side(side),
        'order_type': validate_order_type(order_type),
        'quantity': validate_quantity(quantity),
        'price': validate_price(price, order_type)
    }
    return validated
