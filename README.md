# Trading Bot

## Project Title
Binance Futures Testnet Trading Bot

## Overview
A production-grade Python CLI application for placing orders on Binance Futures Testnet (USDT-M). Features clean architecture, strict separation of concerns, comprehensive logging, and strong input validation.

## Architecture
The application follows clean architecture principles with distinct layers:

- **CLI Layer** (`cli.py`) - User interface and input handling
- **Validation Layer** (`validators.py`) - Input validation with clear error messages
- **Business Logic Layer** (`orders.py`) - Order placement logic
- **API Layer** (`client.py`) - Binance API communication
- **Infrastructure Layer** (`logging_config.py`) - Logging setup

## Working Flow Diagram

```
User CLI Input
      ↓
Validators (schema validation)
      ↓
Orders Module (business logic)
      ↓
Binance Client (API integration)
      ↓
Binance Futures Testnet
      ↓
Response Processing
      ↓
Logger (file & console)
      ↓
Formatted CLI Output
```

## Outputs wrt the current logs
# Market Order 
<img width="1912" height="800" alt="image" src="https://github.com/user-attachments/assets/55b132ec-ddbe-4e18-ae02-12232a1e1a91" />

# Limit Order
<img width="1913" height="717" alt="image" src="https://github.com/user-attachments/assets/160dff26-69e6-4a00-ba12-4262c74ca9f9" />




## Setup Steps

### 1. Clone or Download the Repository
```bash
cd trading_bot
```

### 2. Create Python Virtual Environment
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
# or
source venv/bin/activate      # Linux/Mac
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables
Create a `.env` file in the project root:
```
BINANCE_API_KEY=your_api_key
BINANCE_API_SECRET=your_api_secret
```

Or set them in your shell:
```bash
export BINANCE_API_KEY=your_api_key
export BINANCE_API_SECRET=your_api_secret
```

## Environment Variables
- `BINANCE_API_KEY`: Your Binance Futures Testnet API Key
- `BINANCE_API_SECRET`: Your Binance Futures Testnet API Secret

Obtain these from: https://testnet.binancefuture.com

## How to Run

### With All Arguments Provided
```bash
python -m bot --symbol BTCUSDT --side BUY --type MARKET --quantity 0.1
```

### With Interactive Prompts (Missing Arguments)
```bash
python -m bot --symbol BTCUSDT --side BUY --type MARKET --quantity 0.1
```
Missing arguments will be prompted interactively.

### MARKET Order Example
```bash
python -m bot --symbol ETHUSDT --side BUY --type MARKET --quantity 1.0
```

### LIMIT Order Example
```bash
python -m bot --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.5 --price 45000
```

### View Distinct Logs
```bash
tail -f trading.log
tail -f limit_order.log
tail -f market_order.log
```

## Example Commands

**Interactive mode (prompts for inputs):**
```bash
python -m bot
```

**Buy BTC at market price:**
```bash
python -m bot --symbol BTCUSDT --side BUY --type MARKET --quantity 0.1
```

**Sell ETH with limit price:**
```bash
python -m bot --symbol ETHUSDT --side SELL --type LIMIT --quantity 2.0 --price 2500
```

## Assumptions

- Testnet credentials are set up in Binance Futures Testnet
- Network connectivity to `testnet.binancefuture.com` is available
- Python 3.7+ is installed
- API keys have appropriate permissions (Futures order placement)
- Quantity precision matches symbol requirements
- USDT-M margin type is used

## Log Files
All API requests, responses, and errors are logged to `trading.log` in the project root directory.
#
