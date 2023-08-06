import n26.api as api
import click
import webbrowser
from tabulate import tabulate

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


# Cli returns command line requests
@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """Interact with the https://n26.com API via the command line."""


@cli.command()
def info():
    """ Get account information """
    account_info = api.Api()
    print('Account info:')
    print('-------------')
    # TODO: make it python2 compatible using unicode
    print('Name: ' + str(account_info.get_account_info()['firstName'] + ' ' +
                         account_info.get_account_info()['lastName']))
    print('Email: ' + account_info.get_account_info()['email'])
    print('Nationality: ' + account_info.get_account_info()['nationality'])
    print('Phone: ' + account_info.get_account_info()['mobilePhoneNumber'])


@cli.command()
def balance():
    """ 💵 Show account balance """
    balance = api.Api()
    print('Current balance:')
    print('----------------')
    print(str(balance.get_balance()['availableBalance']))


@cli.command()
def browse():
    """ 🌍 Browse on the web https://app.n26.com/ """
    webbrowser.open('https://app.n26.com/')


@cli.command()
# @click.option('--all', default=False, help='Blocks all n26 cards.')
def card_block():
    """ 🛑 Block card """
    card = api.Api()
    for i in card.get_cards():
        card_id = i['id']
        card.block_card(card_id)
        print('Blocked card: ' + card_id)


@cli.command()
def card_unblock():
    """ ✅ Unblocks card """
    card = api.Api()
    for i in card.get_cards():
        card_id = i['id']
        card.unblock_card(card_id)
        print('Unblocked card: ' + card_id)


@cli.command()
def limits():
    """ 🚨 Show n26 account limits  """
    limits = api.Api()
    print(limits.get_account_limits())


@cli.command()
def contacts():
    """ 📇 Show your n26 contacts  """
    contacts = api.Api()
    print('Contacts:')
    print('---------')
    print(contacts.get_contacts())


@cli.command()
def statements():
    """ 📖 Show your n26 statements  """
    statements = api.Api()
    print('Statements:')
    print('-----------')
    print(statements.get_statements())


@cli.command()
@click.option('--limit', default=5, help='Limit transaction output.')
def transactions(limit):
    """ 💸 Show transactions (default: 5) """
    transactions = api.Api()
    output = transactions.get_transactions_limited(str(limit))
    print('Transactions:')
    print('-------------')
    li = []
    for i, val in enumerate(output):
        try:
            if val['merchantName'] in val.values():
                li.append([i, str(val['amount']), val['merchantName']])
        except KeyError:
            if val['referenceText'] in val.values():
                li.append([i, str(val['amount']), val['referenceText']])
            else:
                li.append([i, str(val['amount']), 'no details available'])

    # Tabulate
    table = li
    headers = ['index', 'amount', 'details']
    print(tabulate(table, headers, tablefmt='simple', numalign='right'))


if __name__ == '__main__':
    cli()
