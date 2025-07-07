# zenabot.py (modo DOGE/USDT, baixo capital)

try:
    import ccxt
except ModuleNotFoundError:
    import subprocess
    subprocess.check_call(["pip", "install", "ccxt"])
    import ccxt

import time

# Configuração da conta OKX
okx = ccxt.okx({
    'apiKey': "51dfa216-427f-40fb-85d1-5292967594fa",
    'secret': "125D94D97976E3428657EC0C522B8CD3",
    'password': "TradeBot@2025",
    'enableRateLimit': True,
    'options': {'defaultType': 'spot'}
})

symbol = 'DOGE/USDT'
capital_usdt = 5.00  # Valor bem baixo
max_loss_pct = 5
profit_target_pct = 3
bought_price = None

print("ZenaInvest iniciado com DOGE/USDT - Estratégia conservadora")

while True:
    try:
        ticker = okx.fetch_ticker(symbol)
        price = ticker['last']
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if not bought_price:
            amount = round(capital_usdt / price, 2)
            try:
                okx.create_market_buy_order(symbol, amount)
                bought_price = price
                print(f"[{timestamp}] ✅ COMPRADO {amount} DOGE a {price:.4f} USDT")
            except Exception as buy_err:
                print(f"[{timestamp}] ⚠️ Falha na compra: {buy_err}")
        else:
            change_pct = ((price - bought_price) / bought_price) * 100
            amount = round(capital_usdt / bought_price, 2)

            if change_pct >= profit_target_pct:
                okx.create_market_sell_order(symbol, amount)
                lucro = amount * (price - bought_price)
                print(f"[{timestamp}] 💰 VENDIDO {amount} DOGE a {price:.4f} USDT | Lucro: ${lucro:.2f}")
                bought_price = None
            elif change_pct <= -max_loss_pct:
                okx.create_market_sell_order(symbol, amount)
                preju = amount * (bought_price - price)
                print(f"[{timestamp}] 🛑 STOP-LOSS {amount} DOGE a {price:.4f} USDT | Prejuízo: -${preju:.2f}")
                bought_price = None
            else:
                print(f"[{timestamp}] 🔄 Aguardando... Preço: {price:.4f} USDT | Variação: {change_pct:.2f}%")

        time.sleep(60)  # Roda a cada 1 minuto

    except Exception as e:
        print(f"[ERRO] {e}")
        time.sleep(30)
