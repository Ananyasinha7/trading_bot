import sys
import argparse
from dotenv import load_dotenv
from .logging_config import configure_logging, get_logger
from .client import BinanceFuturesClient
from .orders import place_market_order, place_limit_order
from .validators import validate_all_inputs

logger = None


def format_order_output(response):
    if response.get('error'):
        return f"Order Failed: {response['error']}"

    output_lines = [
        '\n' + '='*50,
        'ORDER PLACED SUCCESSFULLY',
        '='*50,
    ]

    if 'orderId' in response:
        output_lines.append(f"Order ID:     {response['orderId']}")
    if 'status' in response:
        output_lines.append(f"Status:       {response['status']}")
    if 'executedQty' in response:
        output_lines.append(f"Executed Qty: {response['executedQty']}")
    if 'avgPrice' in response:
        output_lines.append(f"Average Price: {response['avgPrice']}")

    output_lines.append('='*50 + '\n')
    return '\n'.join(output_lines)


def print_order_summary(symbol, side, order_type, quantity, price=None):
    print('\n' + '-'*50)
    print('ORDER REQUEST SUMMARY')
    print('-'*50)
    print(f'Symbol:      {symbol}')
    print(f'Side:        {side}')
    print(f'Type:        {order_type}')
    print(f'Quantity:    {quantity}')
    if price is not None:
        print(f'Price:       {price}')
    print('-'*50 + '\n')


def prompt_for_missing_input(param_name, current_value=None):
    if current_value is not None:
        return current_value

    valid_sides = ['BUY', 'SELL']
    valid_types = ['MARKET', 'LIMIT']

    if param_name == 'symbol':
        return input(f'Enter {param_name} (e.g., BTCUSDT): ').strip()
    elif param_name == 'side':
        while True:
            value = input(f'Enter {param_name} ({", ".join(valid_sides)}): ').strip().upper()
            if value in valid_sides:
                return value
            print(f'Invalid input. Must be one of: {", ".join(valid_sides)}')
    elif param_name == 'type':
        while True:
            value = input(f'Enter order {param_name} ({", ".join(valid_types)}): ').strip().upper()
            if value in valid_types:
                return value
            print(f'Invalid input. Must be one of: {", ".join(valid_types)}')
    elif param_name == 'quantity':
        while True:
            try:
                value = float(input(f'Enter {param_name} (positive number): ').strip())
                if value > 0:
                    return value
                print('Quantity must be greater than 0')
            except ValueError:
                print('Invalid input. Please enter a valid number')
    elif param_name == 'price':
        while True:
            try:
                value = float(input(f'Enter {param_name} (positive number): ').strip())
                if value > 0:
                    return value
                print('Price must be greater than 0')
            except ValueError:
                print('Invalid input. Please enter a valid number')


def handle_order_command(args):
    symbol = prompt_for_missing_input('symbol', args.symbol)
    side = prompt_for_missing_input('side', args.side)
    order_type = prompt_for_missing_input('type', args.type)
    quantity = prompt_for_missing_input('quantity', args.quantity)

    price = None
    if order_type == 'LIMIT':
        price = prompt_for_missing_input('price', args.price)

    try:
        validated = validate_all_inputs(symbol, side, order_type, quantity, price)
        print_order_summary(validated['symbol'], validated['side'], validated['order_type'], 
                          validated['quantity'], validated['price'])

    except ValueError as e:
        logger.error(f'Validation error: {str(e)}')
        print(f'\nValidation Error: {str(e)}\n')
        return 1

    try:
        client = BinanceFuturesClient()
        logger.info(f'Client initialized, attempting to place order')

        if validated['order_type'] == 'MARKET':
            response = place_market_order(
                client,
                validated['symbol'],
                validated['side'],
                validated['quantity']
            )
        else:
            response = place_limit_order(
                client,
                validated['symbol'],
                validated['side'],
                validated['quantity'],
                validated['price']
            )

        print(format_order_output(response))

        if 'error' in response:
            return 1
        return 0

    except ValueError as e:
        logger.error(f'Configuration error: {str(e)}')
        print(f'\nConfiguration Error: {str(e)}')
        print('Ensure BINANCE_API_KEY and BINANCE_API_SECRET are set.\n')
        return 1
    except Exception as e:
        logger.error(f'Unexpected error: {str(e)}')
        print(f'\nError: {str(e)}\n')
        return 1


def main():
    global logger
    load_dotenv()
    configure_logging()
    logger = get_logger()

    parser = argparse.ArgumentParser(
        description='Binance Futures Testnet Trading Bot',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python -m bot --symbol BTCUSDT --side BUY --type MARKET --quantity 0.1
  python -m bot --symbol ETHUSDT --side SELL --type LIMIT --quantity 1.5 --price 2000
        '''
    )

    parser.add_argument('--symbol', help='Trading symbol (e.g., BTCUSDT)')
    parser.add_argument('--side', help='Order side: BUY or SELL')
    parser.add_argument('--type', help='Order type: MARKET or LIMIT')
    parser.add_argument('--quantity', type=float, help='Order quantity')
    parser.add_argument('--price', type=float, help='Order price (required for LIMIT orders)')

    args = parser.parse_args()

    logger.info('Trading Bot CLI started')
    exit_code = handle_order_command(args)
    logger.info(f'Trading Bot CLI exited with code: {exit_code}')

    return exit_code


if __name__ == '__main__':
    sys.exit(main())
