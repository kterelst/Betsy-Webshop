from peewee import *

db = SqliteDatabase('betsy.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    user_name = CharField(primary_key=True, unique=True)
    first_name = CharField()
    last_name = CharField()
    address = CharField()
    postal_code = CharField()
    city = CharField()
    country = CharField()  # pycountry could be used for check
    iban = CharField()  # schwifty.IBAN could be used for check


class Product(BaseModel):
    product_name = CharField(primary_key=True, unique=True)
    description = CharField()
    unit_price = DecimalField(decimal_places=2)
    number_in_stock = IntegerField()  # not negative could be used for check


class Ownership(BaseModel):
    user_name = ForeignKeyField(User)
    product_name = ForeignKeyField(Product)
    number_owned = IntegerField()  # not negative could be used for check


class Tag(BaseModel):
    tag_text = CharField(primary_key=True, unique=True)


class ProductTag(BaseModel):
    tag = ForeignKeyField(Tag)
    product_name = ForeignKeyField(Product)


class Transaction(BaseModel):
    buyer = ForeignKeyField(User)
    product_name = ForeignKeyField(Product)
    number_sold = IntegerField()
    datetime_sold = DateTimeField()
