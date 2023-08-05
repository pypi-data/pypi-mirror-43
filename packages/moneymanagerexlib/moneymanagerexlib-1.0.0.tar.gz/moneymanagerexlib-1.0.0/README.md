# MoneyManagerExLib

Python library (Data Access Layer) for reading Money Manager Ex database.

It uses SQLAlchemy to define the data schema for the MMEX database.

Useful for scripts that read/write the data in .mmb files.

Available on PyPi at https://pypi.org/project/moneymanagerexlib/

## GnuCash Import

GnuCash CSV import offers a "Multi-split" mode. This will import multiple splits for one transaction based on the transaction id.
