import os
import requests
import time
import hmac
import hashlib
from typing import Dict, Optional, Any
from .logging_config import get_logger

logger = get_logger()


class BinanceFuturesClient:
    def __init__(self):
        self.api_key = os.getenv('BINANCE_API_KEY')
        self.api_secret = os.getenv('BINANCE_API_SECRET')
        self.base_url = 'https://testnet.binancefuture.com'
        self.session = requests.Session()

        if not self.api_key or not self.api_secret:
            raise ValueError('BINANCE_API_KEY and BINANCE_API_SECRET environment variables are required')

    def _get_timestamp(self):
        return int(time.time() * 1000)

    def _generate_signature(self, params: Dict) -> str:
        query_string = '&'.join([f'{k}={v}' for k, v in params.items()])
        signature = hmac.new(
            self.api_secret.encode(),
            query_string.encode(),
            hashlib.sha256
        ).hexdigest()
        return signature

    def _make_request(self, method: str, endpoint: str, params: Optional[Dict] = None, signed: bool = False) -> Dict:
        url = f'{self.base_url}{endpoint}'
        headers = {'X-MBX-APIKEY': self.api_key}

        if params is None:
            params = {}

        try:
            if signed:
                params['timestamp'] = self._get_timestamp()
                params['signature'] = self._generate_signature(params)

            logger.debug(f'API Request: {method} {endpoint} | Params: {params}')

            if method.upper() == 'GET':
                response = self.session.get(url, params=params, headers=headers, timeout=10)
            elif method.upper() == 'POST':
                response = self.session.post(url, params=params, headers=headers, timeout=10)
            else:
                raise ValueError(f'Unsupported HTTP method: {method}')

            response.raise_for_status()
            result = response.json()

            logger.debug(f'API Response: {result}')
            return result

        except requests.exceptions.Timeout:
            error_msg = 'Request timeout - server took too long to respond'
            logger.error(error_msg)
            return {'error': error_msg, 'success': False}
        except requests.exceptions.ConnectionError:
            error_msg = 'Connection error - failed to connect to Binance server'
            logger.error(error_msg)
            return {'error': error_msg, 'success': False}
        except requests.exceptions.HTTPError as e:
            try:
                error_data = e.response.json()
                error_msg = error_data.get('msg', str(e))
            except:
                error_msg = str(e)
            logger.error(f'HTTP Error: {error_msg}')
            return {'error': error_msg, 'success': False}
        except Exception as e:
            error_msg = f'Unexpected error: {str(e)}'
            logger.error(error_msg)
            return {'error': error_msg, 'success': False}

    def ping(self) -> Dict[str, Any]:
        result = self._make_request('GET', '/fapi/v1/ping')
        logger.info('Ping request completed')
        return result

    def create_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None
    ) -> Dict[str, Any]:
        params = {
            'symbol': symbol,
            'side': side,
            'type': order_type,
            'quantity': quantity,
        }

        if order_type == 'LIMIT' and price is not None:
            params['price'] = price
            params['timeInForce'] = 'GTC'

        logger.info(f'Creating order: symbol={symbol}, side={side}, type={order_type}, qty={quantity}, price={price}')
        result = self._make_request('POST', '/fapi/v1/order', params, signed=True)
        return result
