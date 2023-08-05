from unittest import TestCase, main
from seneca.engine.interface import SenecaInterface
from decimal import *

GENESIS_AUTHOR = 'davis'
STAMP_AMOUNT = None
MINT_WALLETS = {
    'davis': 10000,
    'stu': 69,
    'birb': 8000,
    'ghu': 9000,
    'tj': 8000,
    'ethan': 8000
}


class TestImporting(TestCase):
    CONTRACTS_TO_STORE = {
        'birb_bucks': 'birb_bucks.sen.py',
        'cat_cash': 'cat_cash.sen.py',
        'dynamic_imports': 'dynamic_imports.sen.py',
        'currency': 'currency.sen.py'}

    def setUp(self):
        # overwrite_logger_level(0)
        with SenecaInterface(False, 6379, '', bypass_currency=True) as interface:
            interface.r.flushall()
            # Store all smart contracts in CONTRACTS_TO_STORE
            import seneca
            test_contracts_path = seneca.__path__[0] + '/../test_contracts/'

            for contract_name, file_name in self.CONTRACTS_TO_STORE.items():
                with open(test_contracts_path + file_name) as f:
                    code_str = f.read()
                    interface.publish_code_str(contract_name, GENESIS_AUTHOR, code_str)

            rt = {
                'author': GENESIS_AUTHOR,
                'sender': GENESIS_AUTHOR,
                'contract': 'minter'
            }

    def test_import(self):
        import os
        os.environ['IS_IMPORT'] = 'TTTT'
        with SenecaInterface(False, 6379, '', bypass_currency=True) as interface:
            f = interface.execute_function(
                module_path='seneca.contracts.dynamic_imports.get_token_balance',
                sender=GENESIS_AUTHOR,
                stamps=None,
                token_name='birb_bucks',
                account='birb'
            )

            self.assertEqual(f['output'], 1000000)

            f = interface.execute_function(
                module_path='seneca.contracts.dynamic_imports.get_token_balance',
                sender=GENESIS_AUTHOR,
                stamps=None,
                token_name='cat_cash',
                account='cat'
            )

            self.assertEqual(f['output'], 1000000)

            f = interface.execute_function(
                module_path='seneca.contracts.dynamic_imports.get_token_balance',
                sender=GENESIS_AUTHOR,
                stamps=None,
                token_name='cat_cash',
                account='birb'
            )

            self.assertEqual(f['output'], 0)

        os.environ['IS_IMPORT'] = ''

if __name__ == '__main__':
    main()
