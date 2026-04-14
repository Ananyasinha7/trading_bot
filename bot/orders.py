from .client import BinanceFuturesClient
from .logging_config import (
    get_logger,
    configure_market_order_logger,
    configure_limit_order_logger,
    get_market_order_logger,
    get_limit_order_logger
)
from typing import Dict, Optional, Any

logger = get_logger()


def _extract_order_response(api_response: Dict) -> Dict[str, Any]:
    if not api_response.get('success', True) is not False:
        if 'error' in api_response:
            logger.error(f'Order failed: {api_response["error"]}')
            return {
                'success': False,
                'error': api_response['error']
            }

    order_response = {
        'orderId': api_response.get('orderId'),
        'status': api_response.get('status'),
        'executedQty': api_response.get('executedQty'),
    }

    if api_response.get('avgPrice'):
        order_response['avgPrice'] = api_response.get('avgPrice')

    logger.info(f'Order response extracted: {order_response}')
    return order_response


def place_market_order(
    client: BinanceFuturesClient,
    symbol: str,
    side: str,
    quantity: float
) -> Dict[str, Any]:
    configure_market_order_logger()
    market_logger = get_market_order_logger()
    
    logger.info(f'Placing MARKET order: {symbol} {side} {quantity}')
    market_logger.info(f'MARKET ORDER: {symbol} {side} {quantity}')

    response = client.create_order(
        symbol=symbol,
        side=side,
        order_type='MARKET',
        quantity=quantity,
        price=None
    )

    market_logger.info(f'Request Params: symbol={symbol}, side={side}, type=MARKET, quantity={quantity}')
    market_logger.info(f'API Response: {response}')

    if 'error' in response:
        logger.warning(f'Market order failed: {response["error"]}')
        market_logger.error(f'Order failed: {response["error"]}')
        return {'success': False, 'error': response['error']}

    logger.info(f'Market order placed successfully: {response.get("orderId")}')
    market_logger.info(f'Order placed successfully - orderId: {response.get("orderId")}, status: {response.get("status")}')
    return _extract_order_response(response)


def place_limit_order(
    client: BinanceFuturesClient,
    symbol: str,
    side: str,
    quantity: float,
    price: float
) -> Dict[str, Any]:
    configure_limit_order_logger()
    limit_logger = get_limit_order_logger()
    
    logger.info(f'Placing LIMIT order: {symbol} {side} {quantity} @ {price}')
    limit_logger.info(f'LIMIT ORDER: {symbol} {side} {quantity} @ {price}')

    response = client.create_order(
        symbol=symbol,
        side=side,
        order_type='LIMIT',
        quantity=quantity,
        price=price
    )

    limit_logger.info(f'Request Params: symbol={symbol}, side={side}, type=LIMIT, quantity={quantity}, price={price}')
    limit_logger.info(f'API Response: {response}')

    if 'error' in response:
        logger.warning(f'Limit order failed: {response["error"]}')
        limit_logger.error(f'Order failed: {response["error"]}')
        return {'success': False, 'error': response['error']}

    logger.info(f'Limit order placed successfully: {response.get("orderId")}')
    return _extract_order_response(response)
