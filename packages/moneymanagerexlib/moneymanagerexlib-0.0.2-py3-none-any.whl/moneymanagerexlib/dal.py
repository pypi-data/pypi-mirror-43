"""
Data layer

Basic Relationships:
https://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html

"""
from sqlalchemy import create_engine, types, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, REAL
from decimal import Decimal

Base = declarative_base()


class SqliteDecimal(types.TypeDecorator):
    '''
    Ref: https://stackoverflow.com/questions/10355767/how-should-i-handle-decimal-in-sqlalchemy-sqlite
    '''
    # This TypeDecorator use Sqlalchemy Integer as impl. It converts Decimals
    # from Python to Integers which is later stored in Sqlite database.
    impl = Integer

    def __init__(self, scale):
        # It takes a 'scale' parameter, which specifies the number of digits
        # to the right of the decimal point of the number in the column.
        types.TypeDecorator.__init__(self)
        self.scale = scale
        self.multiplier_int = 10 ** self.scale

    def process_bind_param(self, value, dialect):
        # e.g. value = Column(SqliteDecimal(2)) means a value such as
        # Decimal('12.34') will be converted to 1234 in Sqlite
        if value is not None:
            value = int(Decimal(value) * self.multiplier_int)
        return value

    def process_result_value(self, value, dialect):
        # e.g. Integer 1234 in Sqlite will be converted to Decimal('12.34'),
        # when query takes place.
        if value is not None:
            value = Decimal(value) / self.multiplier_int
        return value


class Category(Base):
    __tablename__ = 'CATEGORY_V1'

    CATEGID = Column(Integer, primary_key=True)
    CATEGNAME = Column(String)


class Subcategory(Base):
    __tablename__ = 'SUBCATEGORY_V1'

    SUBCATEGID = Column(Integer, primary_key=True)
    SUBCATEGNAME = Column(String, nullable=False)
    CATEGID = Column(Integer, nullable=False)


class Currency(Base):
    __tablename__ = 'CURRENCYFORMATS_V1'

    CURRENCYID = Column(Integer, primary_key=True)
    CURRENCYNAME = Column(String, nullable=False, unique=True)
    PFX_SYMBOL = Column(String)
    SFX_SYMBOL = Column(String)
    DECIMAL_POINT = Column(String)
    GROUP_SEPARATOR = Column(String)
    UNIT_NAME = Column(String)
    CENT_NAME = Column(String)
    SCALE = Column(Integer)
    BASECONVRATE = Column(REAL)
    CURRENCY_SYMBOL = Column(String, nullable=False, unique=True)


class Account(Base):
    __tablename__ = 'ACCOUNTLIST_V1'

    ACCOUNTID = Column(Integer, primary_key=True)
    ACCOUNTNAME = Column(String, nullable=False, unique=True)
    ACCOUNTTYPE = Column(String, nullable=False)
    ACCOUNTNUM = Column(String)
    STATUS = Column(String, nullable=False)
    NOTES = Column(String)
    HELDAT = Column(String)
    WEBSITE = Column(String)
    CONTACTINFO = Column(String)
    ACCESSINFO = Column(String)
    INITIALBAL = Column(REAL)
    FAVORITEACCT = Column(String, nullable=False)
    #CURRENCYID = Column(Integer, ForeignKey("currency.currencyid"))
    #CURRENCYID = Column(Integer, ForeignKey("Currency.CURRENCYID"))
    CURRENCYID = Column(Integer, ForeignKey(Currency.CURRENCYID))
    STATEMENTLOCKED = Column(Integer)
    STATEMENTDATE = Column(String)
    MINIMUMBALANCE = Column(REAL)
    CREDITLIMIT = Column(REAL)
    INTERESTRATE = Column(REAL)
    PAYMENTDUEDATE = Column(String)
    MINIMUMPAYMENT = Column(REAL)

    currency = relationship("Currency", uselist=False)
    # , back_populates="account")
    #currency = relationship("Currency", foreign_keys=[CURRENCYID]) 
    #currency = relationship("Currency", back_populates="user", userlist=False)


class Payee(Base):
    __tablename__ = 'PAYEE_V1'

    PAYEEID = Column(Integer, primary_key=True)
    PAYEENAME = Column(String, nullable=False, unique=True)
    CATEGID = Column(Integer, ForeignKey(Category.CATEGID), nullable=True)
    SUBCATEGID = Column(Integer, ForeignKey(Subcategory.SUBCATEGID), nullable=True)

    category = relationship("Category")
    subcategory = relationship("Subcategory")


class CheckingAccount(Base):
    """ Transactions """
    __tablename__ = 'CHECKINGACCOUNT_V1'

    TRANSID = Column(Integer, primary_key=True)
    ACCOUNTID = Column(Integer, ForeignKey(Account.ACCOUNTID), nullable=False)
    TOACCOUNTID = Column(Integer, ForeignKey(Account.ACCOUNTID))
    PAYEEID = Column(Integer, ForeignKey(Payee.PAYEEID), nullable=False)
    TRANSCODE = Column(String, nullable=False)
    #TRANSAMOUNT = Column(SqliteDecimal(4))
    TRANSAMOUNT = Column(REAL, nullable=False)
    STATUS = Column(String)
    TRANSACTIONNUMBER = Column(String)
    NOTES = Column(String)
    CATEGID = Column(Integer, ForeignKey(Category.CATEGID))
    SUBCATEGID = Column(Integer, ForeignKey(Subcategory.SUBCATEGID))
    TRANSDATE = Column(String)
    FOLLOWUPID = Column(Integer)
    TOTRANSAMOUNT = Column(REAL)

    account = relationship("Account",  foreign_keys=[ACCOUNTID], uselist=False)
    account_to = relationship("Account", foreign_keys=[TOACCOUNTID], uselist=False)
    payee = relationship("Payee")
    category = relationship("Category")
    subcategory = relationship("Subcategory")


    # accounts = relationship('Account',
    #                     back_populates='commodity',
    #                     cascade='all, delete-orphan',
    #                     collection_class=CallableList)
    # transactions = relationship('Transaction',
    #                         back_populates='currency',
    #                         cascade='all, delete-orphan',
    #                         collection_class=CallableList,
    #                         )
    # prices = relationship("Price",
    #                   back_populates='commodity',
    #                   foreign_keys=[Price.commodity_guid],
    #                   cascade='all, delete-orphan',
    #                   lazy="dynamic",
    #                   )

    def __repr__(self):
        return f"<CheckingAccount ({self.ACCOUNTID})>"


class SplitTransaction(Base):
    ''' Splits '''
    __tablename__ = 'SPLITTRANSACTIONS_V1'

    SPLITTRANSID = Column(Integer, primary_key=True)
    TRANSID = Column(Integer, ForeignKey(CheckingAccount.TRANSID), nullable=False)
    CATEGID = Column(Integer, ForeignKey(Category.CATEGID))
    SUBCATEGID = Column(Integer, ForeignKey(Subcategory.SUBCATEGID))
    SPLITTRANSAMOUNT = Column(REAL)

    transaction = relationship("CheckingAccount")
    category = relationship("Category")
    subcategory = relationship("Subcategory")

# def get_default_session():
#     """ Return the default session. The path is read from the default config. """
#     from .config import Config, ConfigKeys

#     db_path = Config().get(ConfigKeys.price_database)
#     if not db_path:
#         raise ValueError("Price database not set in the configuration file!")
#     return get_session(db_path)

def get_session(db_path: str):
    """ Creates and opens a database session """
    #from sqlalchemy import engine_from_config

    # connection
    con_str = "sqlite:///" + db_path
    # Display all SQLite info with echo.
    #echo = True
    echo = False
    engine = create_engine(con_str, echo=echo)
    # To configure the engine with external parameters use:
    # config = { echo = True }
    # engine_from_config(config)

    # create metadata (?)
    Base.metadata.create_all(engine)

    # create session
    Session = sessionmaker(bind=engine)
    session = Session()

    return session
