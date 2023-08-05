'''
CSV export helper for GnuCash
Columns:
date, account, description, deposit, withdrawal
'''
from typing import List

NOT_SET = -1


class CsvRow:
    ''' CSV row for import into GnuCash '''
    # mandatory fields
    date = ''
    description = ''
    deposit = ''
    withdrawal = ''
    # extra fields
    tx_id = ''
    memo = ''
    account = ''
    transfer_account = ''

    def __repr__(self):
    #def __str__(self):
        ''' string representation '''
        id = self.tx_id
        date = self.date

        description = ''
        if self.description:
            description = f"\"{self.description}\""

        deposit = self.deposit
        withdrawal = self.withdrawal

        account = ''
        if self.account:
            account = f"\"{self.account}\""

        # transfer_account = ''
        # if self.transfer_account:
        #     transfer_account = f"\"{self.transfer_account}\""

        memo = ''
        if self.memo:
            memo = f"\"{self.memo}\""

        # Format suitable for multi-split import.
        result = f"{id},{date},{description},{deposit},{withdrawal},{account},{memo}"
        # ,{transfer_account}

        return result


class CsvGenerator:
    ''' Generate a CSV file from a list of MMEx transactions '''
    from moneymanagerexlib.dal import CheckingAccount, SplitTransaction

    def __init__(self, db_path):
        self.db_path = db_path

    def generate_for(self, transactions: List[CheckingAccount]) -> str:
        '''
        Create a CSV content for the list of transactions.
        Convert the list of transactions to .csv suitable for import to GnuCash.
        '''
        all_rows = []

        for tx in transactions:
            tx_rows = []

            if tx.TRANSCODE == "Transfer":
                tx_rows = self.__create_transfer(tx)
            elif tx.TRANSCODE == "Withdrawal":
                tx_rows = self.__create_withdrawal(tx)
            elif tx.TRANSCODE == "Deposit":
                row = self.__create_deposit(tx)
                all_rows.append(row)

            for row in tx_rows:
                all_rows.append(row)

        #return result

        csv = ''
        for row in all_rows:
            csv += f"{row}\n"
        return csv

    def generate_multiline_for(self, transactions: List[CheckingAccount]) -> str:
        '''
        Saves each individual split.
        To be used with Multi-split import option in GnuCash
        '''
        all_rows = []

        for tx in transactions:
            tx_rows = self.__create_csv_rows_for(tx)

            for row in tx_rows:
                all_rows.append(row)

        csv = ''
        for row in all_rows:
            csv += f"{row}\n"
        return csv

    def __create_csv_rows_for(self, tx: CheckingAccount) -> List[CsvRow]:
        '''
        Create all split rows for transaction.
        Deposits and Withdrawals have two splits, one for the account and one for the category.
        '''
        tx_rows = []
        if tx.TRANSCODE == "Transfer":
            tx_rows = self.__create_multisplit_transfer(tx)
        elif tx.TRANSCODE == "Withdrawal":
            tx_rows = self.__create_multisplit_withdrawal(tx)
        elif tx.TRANSCODE == "Deposit":
            tx_rows = self.__create_multisplit_deposit(tx)

        return tx_rows

    def __create_base_csv_record(self, tx: CheckingAccount) -> CsvRow:
        ''' Create a CSV record '''
        result = CsvRow()
        result.tx_id = tx.TRANSID

        # date
        result.date = tx.TRANSDATE

        # account
        result.account = tx.account.ACCOUNTNAME

        # description is the Payee name.
        result.description = ''
        if tx.payee:
            result.description = tx.payee.PAYEENAME
        # Transfers have no payee but may have memo.
        # if description is None:
        #     description = tx.NOTES

        result.memo = tx.NOTES

        return result

    def __create_multisplit_withdrawal(self, tx: CheckingAccount) -> List[CsvRow]:
        '''
        Create a multi-split for a withdrawal transaction.
        '''
        from moneymanagerexlib.query import Queries

        rows = []
        
        # account split
        acc_row = self.__create_base_csv_record(tx)
        acc_row.withdrawal = tx.TRANSAMOUNT
        rows.append(acc_row)

        # category split
        cat_row = self.__create_base_csv_record(tx)
        # adjust the account
        if tx.CATEGID == NOT_SET:
            # We have splits here.
            q = Queries(self.db_path)
            splits = q.load_splits_for(tx)
            if splits:
                for split in splits:
                    split_row = self.__create_multisplit_row_for_split(split)
                    rows.append(split_row)
        else:
            cat_row.account = self.__get_category_text_for_tx(tx)

        cat_row.deposit = tx.TRANSAMOUNT
        if tx.CATEGID != NOT_SET:
            # add the record only if there are no splits already.
            rows.append(cat_row)

        return rows

    def __create_multisplit_deposit(self, tx: CheckingAccount) -> List[CsvRow]:
        '''
        Create a multi-split for a deposit transaction.
        '''
        from moneymanagerexlib.query import Queries

        rows = []
        
        # account split
        acc_row = self.__create_base_csv_record(tx)
        acc_row.deposit = tx.TRANSAMOUNT
        rows.append(acc_row)

        # category split
        cat_row = self.__create_base_csv_record(tx)
        # adjust the account
        if tx.CATEGID == NOT_SET:
            # We have splits here.
            q = Queries(self.db_path)
            splits = q.load_splits_for(tx)
            if splits:
                for split in splits:
                    split_row = self.__create_multisplit_row_for_split(split)
                    rows.append(split_row)
        else:
            cat_row.account = self.__get_category_text_for_tx(tx)

        # Amount sign if f'd up in MMEx.
        cat_row.withdrawal = tx.TRANSAMOUNT

        if tx.CATEGID != NOT_SET:
            # add the record only if there are no splits already.
            rows.append(cat_row)

        return rows

    def __create_multisplit_transfer(self, tx: CheckingAccount) -> List[CsvRow]:
        '''
        Create a multi-split for a transfer transaction.
        '''
        rows = []
        
        # source split
        from_row = self.__create_base_csv_record(tx)
        from_row.withdrawal = tx.TRANSAMOUNT
        rows.append(from_row)

        # destination split
        to_row = self.__create_base_csv_record(tx)
        # adjust the account
        to_row.account = tx.account_to.ACCOUNTNAME
        to_row.deposit = tx.TOTRANSAMOUNT
        rows.append(to_row)

        return rows

    def __create_multisplit_row_for_split(self, split: SplitTransaction) -> CsvRow:
        ''' Create a row for the split record '''
        tx = split.transaction
        row = self.__create_base_csv_record(tx)

        row.account = self.__get_category_text_for_split(split)
        
        amount = split.SPLITTRANSAMOUNT
        # The sign is opposite for deposit splits!
        if tx.TRANSCODE == 'Deposit':
            amount *= -1

        if amount > 0:
            row.deposit = abs(amount)
        else:
            row.withdrawal = abs(amount)

        return row

    def __create_csv_row(self, id, account, date, description, deposit, withdrawal, memo) -> CsvRow:
        ''' simple factory method '''
        result = CsvRow()
        result.account = account
        result.date = date
        result.deposit = deposit
        result.description = description
        result.memo = memo
        result.withdrawal = withdrawal
        result.tx_id = id

        return result

    def __create_withdrawal_for_split(self, split: SplitTransaction) -> CsvRow:
        ''' Create withdrawal transactions for splits '''
        tx = split.transaction
        record: CsvRow = self.__create_base_csv_record(tx)
        
        # Amount
        record.withdrawal = split.SPLITTRANSAMOUNT

        # Category
        if split.category:
            record.transfer_account = split.category.CATEGNAME
            if split.subcategory:
                record.transfer_account += ":" + split.subcategory.SUBCATEGNAME

        record.memo = tx.NOTES

        return record

    def __create_withdrawal(self, tx: CheckingAccount) -> List[CsvRow]:
        ''' Create a withdrawal record '''
        from moneymanagerexlib.query import Queries

        result = []

        # Multiple splits?
        q = Queries(self.db_path)

        if tx.CATEGID == NOT_SET:
            splits = q.load_splits_for(tx)
            if splits:
                for split in splits:
                    record = self.__create_withdrawal_for_split(split)
                    result.append(record)
                return result

        # No splits, process the transaction

        record: CsvRow = self.__create_base_csv_record(tx)
        # Add the withdrawal-specific records.
        record.withdrawal = tx.TRANSAMOUNT
        #record.transfer_account = self.__get_category_text_for_tx(tx)

        record.memo = tx.NOTES

        result.append(record)
        return result

    def __create_deposit(self, tx: CheckingAccount) -> CsvRow:
        ''' Create the deposit record '''
        record: CsvRow = self.__create_base_csv_record(tx)

        if tx.TRANSCODE == 'Deposit':
            record.account = tx.account.ACCOUNTNAME
            record.deposit = tx.TRANSAMOUNT
        elif tx.TRANSCODE == 'Transfer':
            record.account = tx.account_to.ACCOUNTNAME
            record.deposit = tx.TOTRANSAMOUNT

        return record

    def __create_transfer(self, tx: CheckingAccount) -> List[CsvRow]:
        ''' Trying with one row which has Transfer Account column '''
        if tx.TRANSCODE != 'Transfer':
            return

        rows = self.__create_withdrawal(tx)
        # There should be only one row
        assert len(rows) == 1
        row = rows[0]
        # Add Transfer account
        row.transfer_account = tx.account_to.ACCOUNTNAME
        #row.deposit = tx.TOTRANSAMOUNT

        return rows

    def __get_category_text_for_tx(self, tx: CheckingAccount) -> str:
        ''' extract the category/subcategory name from the transaction '''
        result = ''
        if tx.category:
            result = tx.category.CATEGNAME
            if tx.subcategory:
                result += ":" + tx.subcategory.SUBCATEGNAME

        return result

    def __get_category_text_for_split(self, split: SplitTransaction) -> str:
        ''' extract the category/subcategory name from the transaction '''
        result = ''
        if split.category:
            result = split.category.CATEGNAME
            if split.subcategory:
                result += ":" + split.subcategory.SUBCATEGNAME

        return result
