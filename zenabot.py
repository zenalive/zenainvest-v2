# zenabot.py (versão backend separada para Render)
try:
    import ccxt
except ModuleNotFoundError:
    import subprocess
    subprocess.check_call(["pip", "install", "ccxt"])
    import ccxt

import time
from datetime import datetime

# Credenciais fixas para uso pessoal (substitua se quiser usar variáveis de ambiente)
okx = ccxt.okx({
    'apiKey': "51dfa216-427f-40fb-85d1-5292967594fa",
    'secret': "125D94D97976E3428657EC0C522B8CD3",
    'password': "TradeBot@2025",
    'enableRateLimit': True,
    'options': {'defaultType': 'spot'}
})

symbol = 'BTC/USDT'
capital_usdt = 20.00
max_loss_pct = 5
profit_target_pct = 3
bought_price = None

print("ZenaInvest iniciado - Estratégia conservadora BTC")

while True:
    try:
        ticker = okx.fetch_ticker(symbol)
        price = ticker['last']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if not bought_price:
            amount = round(capital_usdt / price, 6)
            okx.create_market_buy_order(symbol, amount)
            bought_price = price
            print(f"[{timestamp}] COMPRADO {amount} BTC a {price:.2f} USDT")
        else:
            change_pct = ((price - bought_price) / bought_price) * 100
            amount = round(capital_usdt / bought_price, 6)

            if change_pct >= profit_target_pct:
                okx.create_market_sell_order(symbol, amount)
                lucro = amount * (price - bought_price)
                print(f"[{timestamp}] VENDIDO {amount} BTC a {price:.2f} USDT | Lucro: ${lucro:.2f}")
                bought_price = None
            elif change_pct <= -max_loss_pct:
                okx.create_market_sell_order(symbol, amount)
                preju = amount * (bought_price - price)
                print(f"[{timestamp}] STOP-LOSS VENDIDO {amount} BTC a {price:.2f} USDT | Prejuízo: -${preju:.2f}")
                bought_price = None

        time.sleep(300)  # Espera 5 minutos antes da próxima execução

    except Exception as e:
        print(f"[ERRO] {e}")
        time.sleep(60)
