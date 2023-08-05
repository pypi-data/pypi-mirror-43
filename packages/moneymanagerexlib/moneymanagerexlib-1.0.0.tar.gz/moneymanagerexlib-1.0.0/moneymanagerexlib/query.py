'''
Make querying the data easier
'''
from typing import List
#from sqlalchemy import or_
from sqlalchemy.orm import aliased
from moneymanagerexlib.dal import Account, CheckingAccount, get_session


class QueryFilter:
    ''' Filter for the data '''
    accounts = []
    date_from = None
    date_to = None


class Queries:
    ''' Contains queries for MMEx database. '''
    def __init__(self, db_path: str):
        #self.session = session
        self.session = get_session(db_path)

    def __apply_filter(self, filter:QueryFilter, query):
        ''' Apply the filters to the query '''
        if filter.accounts:
            query = query.outerjoin(CheckingAccount.account)

            to_alias = aliased(Account, name="to_account")
            query = query.outerjoin(to_alias, CheckingAccount.account_to)

            query = query.filter((Account.ACCOUNTNAME.in_(filter.accounts)) | 
                (to_alias.ACCOUNTNAME.in_(filter.accounts)))

        return query

    def load_account_by_name(self, account_name: str) -> Account:
        ''' Load account by name'''
        account = self.session.query(Account).filter(Account.ACCOUNTNAME == account_name).first()
        return account

    def load_transactions(self, filter: QueryFilter) -> List[CheckingAccount]:
        ''' Load transactions from the database '''
        query = self.session.query(CheckingAccount)
        
        # filters
        query = self.__apply_filter(filter, query)

        txs = query.order_by(CheckingAccount.TRANSDATE).all()

        return txs

    def load_splits_for(self, tx: CheckingAccount):
        ''' Load splits records for transaction '''
        from moneymanagerexlib.dal import SplitTransaction

        splits = (
            self.session.query(SplitTransaction)
                .filter(SplitTransaction.TRANSID == tx.TRANSID)
                .all()
        )
        return splits
