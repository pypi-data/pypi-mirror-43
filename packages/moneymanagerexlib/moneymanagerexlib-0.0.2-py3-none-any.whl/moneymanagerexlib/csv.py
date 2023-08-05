'''
CSV export helper for GnuCash
Columns:
date, account, description, deposit, withdrawal
'''

class CsvRow:
    ''' CSV row for import into GnuCash '''
    # mandatory fields
    date = ''
    description = ''
    deposit = ''
    withdrawal = ''
    # extra fields
    memo = ''
    account = ''
    transfer_account = ''

    def __repr__(self):
    #def __str__(self):
        ''' string representation '''
        date = self.date

        description = ''
        if self.description:
            description = f"\"{self.description}\""

        deposit = self.deposit
        withdrawal = self.withdrawal

        account = ''
        if self.account:
            account = f"\"{self.account}\""

        transfer_account = ''
        if self.transfer_account:
            transfer_account = f"\"{self.transfer_account}\""

        result = f"{date},{description},{deposit},{withdrawal},{account},{transfer_account}"

        return result
