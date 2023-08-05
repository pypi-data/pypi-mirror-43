'''
SQL commands
'''
from decimal import Decimal

class Commands:
    ''' execute commands '''
    def __init__(self, db_path: str):
        from moneymanagerexlib.dal import get_session

        self.session = get_session(db_path)
    
    def delete_transaction(self, id: int) -> str:
        ''' obvious '''
        from moneymanagerexlib import CheckingAccount

        q = (
            self.session.query(CheckingAccount)
                .filter(CheckingAccount.TRANSID == id)
        )
        
        tx = q.first()
        output = f"{tx.payee.PAYEENAME}, {tx.TRANSAMOUNT} in {tx.account.ACCOUNTNAME}."

        q.delete()
        self.session.commit()

        return f"deleted " + output

    def set_account_balance(self, name: int, balance: Decimal):
        ''' update account balance '''
        from moneymanagerexlib import Account

        q = (
            self.session.query(Account)
                .filter(Account.ACCOUNTNAME == name)
        )
        account = q.first()
        account.INITIALBAL = balance
        self.session.commit()
