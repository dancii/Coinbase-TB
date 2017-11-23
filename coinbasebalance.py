from coinbase.wallet.client import Client
import math
import colorama
from colorama import Fore, Back, Style
import keys

client = Client(
    keys.api_key,
    keys.api_secret,
    api_version='2017-05-09')

accounts = client.get_accounts()
colorama.init()

total_profit = 0
total_account_balance = 0

def calculate_percentage(current_amount, bought_for):
    return int((float(current_amount)/float(bought_for) * 100 - 100))

for account in accounts.data:
    crypto_amount = 0.0
    usd_amount = 0.0
    balance = account.balance
    total_account_balance += float(account.native_balance.amount)

    print(Style.RESET_ALL + "%s: %s %s, worth: %s$" % (account.name, balance.amount, balance.currency, account.native_balance.amount))

    transactions = account.get_transactions()

    for x in range(0, len(transactions["data"])):
        crypto_amount += float(transactions[x]["amount"]["amount"])
        usd_amount += float(transactions[x]["native_amount"]["amount"])

    if (int(usd_amount) == 0):
        continue
    
    print("Bought for %s$" % (math.floor(usd_amount)))

    total_profit += int(math.floor(float(account.native_balance.amount)-usd_amount))

    if balance.currency == "BTC":
        print(Fore.YELLOW + "Profit: %s$ (%s%%)" % (math.floor(float(account.native_balance.amount)-usd_amount), calculate_percentage(account.native_balance.amount, usd_amount)))
    else:
        print(Back.MAGENTA + Fore.CYAN + Style.BRIGHT + "Profit: %s$ (%s%%)" % (math.floor(float(account.native_balance.amount)-usd_amount), calculate_percentage(account.native_balance.amount, usd_amount)))

total_bought_for = total_account_balance - total_profit

print(Back.BLACK + Fore.GREEN + "Total profit: %s$ (%s%%)" % (total_profit, calculate_percentage(total_account_balance, total_bought_for)))
print(Fore.WHITE + "Total bought for: %s$" % int(total_bought_for))
print("Total balance: %s$" % int(total_account_balance))