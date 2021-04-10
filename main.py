import models
from peewee import fn
from datetime import datetime

__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

# not implemented bonus assignments because of time-sensitive-course
# no pytest: takes more time because of new concept for me
# creation data/tests in this file in if __name__ == __main__


def create_tables():
    with models.db:
        models.db.create_tables([
            models.User,
            models.Product,
            models.Ownership,
            models.Tag,
            models.ProductTag,
            models.Transaction])


def store_data():
    models.User.create(
        user_name='kittie',
        first_name='Kittie',
        last_name='de Jong - ter Elst',
        address='Donk 1A',
        postal_code='5768XM',
        city='Meijel',
        country='The Netherlands',
        iban='NoneOfYourBusiness')

    models.User.create(
        user_name='winc',
        first_name='Winc',
        last_name='Academy',
        address='Reinaert de Vosstraat 27',
        postal_code='1055CL',
        city='Amsterdam',
        country='The Netherlands',
        iban='NL10RABO0123456789')

    models.Product.create(
        product_name='BED',
        description='Back-end Development Opleiding',
        unit_price='2295',
        number_in_stock=1000)

    models.Product.create(
        product_name='FED',
        description='Front-end Development Opleiding',
        unit_price='2495',
        number_in_stock=1000)

    models.Product.create(
        product_name='FST',
        description='Full-stack Development Opleiding',
        unit_price='4495',
        number_in_stock=1000)

    models.Tag.create(tag_text='bed')

    models.Tag.create(tag_text='fed')

    models.ProductTag.create(
        tag='bed',
        product_name='BED')

    models.ProductTag.create(
        tag='bed',
        product_name='FST')

    models.ProductTag.create(
        tag='fed',
        product_name='FED')

    models.ProductTag.create(
        tag='fed',
        product_name='FST')


def search(term):  # checked by test
    return models.Product.select().where(fn.Lower(
        models.Product.product_name.contains(term.lower())))


def list_user_products(user_id):  # checked by test
    return (models.Product.select()
            .join(models.Ownership)
            .join(models.User)
            .where(models.User.user_name == user_id))


def list_products_per_tag(tag_id):  # checked by test
    return (models.Product.select()
            .join(models.ProductTag)
            .join(models.Tag)
            .where(models.Tag.tag_text == tag_id))


def add_product_to_catalog(user_id, product):  # checked by test
    models.Ownership.get_or_create(
        user_name=user_id,
        product_name=product,
        defaults={'number_owned': 0})
    query = (models.Ownership
             .update(number_owned=models.Ownership.number_owned + 1)
             .where(models.Ownership.user_name == user_id and
                    models.Ownership.product_name == product))
    query.execute()


def remove_product(user_id, product_id):  # checked by test
    owner = models.Ownership.get_or_none(
        models.Ownership.user_name == user_id and
        models.Ownership.product_name == product_id)
    if owner:
        owner.delete_instance()


def update_stock(product_id, new_quantity):  # checked by test
    query = models.Product.update(
        number_in_stock=new_quantity).where(
        models.Product.product_name == product_id)
    query.execute()


def purchase_product(product_id, buyer_id, quantity):
    # Register transaction
    models.Transaction.create(
        buyer=buyer_id,
        product_name=product_id,
        number_sold=quantity,
        datetime_sold=datetime.now()
    )

    # Remove from stock
    sold_product = models.Product.get(
                   models.Product.product_name == product_id)
    new_quantity = sold_product.number_in_stock - quantity
    update_stock(product_id, new_quantity)

    # Add to new user
    add_product_to_catalog(buyer_id, product_id)
    (models.Ownership
        .update(number_owned=models.Ownership.number_owned + quantity)
        .where(models.Ownership.user_name == buyer_id,
               models.Ownership.product_name == product_id))


# def remove_product(product_id):
# not according to specs assignment! Replaced above
# (added user_id as input var)


if __name__ == "__main__":
    pass

    # create_tables()
    # store_data()

    # # test search
    # # check lowercase
    # prod_list = search('ed')
    # for prod in prod_list:
    #     print('search ed:', prod.product_name)
    # print(prod_list)
    # # check uppercase
    # prod_list = search('ED')
    # for prod in prod_list:
    #     print('search ED:', prod.product_name)
    # print(prod_list)

    # # test list_products_per_tag
    # # check BED + FST have bed-tag
    # prod_list = list_products_per_tag('bed')
    # print(prod_list)
    # for prod in prod_list:
    #     print('tag bed:', prod.product_name)
    # # check none have fst-tag
    # prod_list = list_products_per_tag('fst')
    # print(prod_list)
    # for prod in prod_list:
    #     print('tag fst:', prod.product_name)

    # # test add_product_to_catalog
    # add_product_to_catalog(user_id='kittie', product='BED')
    # # check add BED to kittie
    # # check only add number when exists
    # # repeat to add more (+1)
    # courses_by_users = models.Ownership.select()
    # for course in courses_by_users:
    #     print('after add/update:',
    #           course.user_name,
    #           course.product_name,
    #           course.number_owned)

    # # test list_user_products
    # prod_list = list_user_products('kittie')
    # print(prod_list)
    # for prod in prod_list:
    #     print('prod kittie:', prod.product_name)

    # # test remove_product
    # remove_product(user_id='kittie', product_id='BED')
    # courses_by_users = models.Ownership.select()
    # for course in courses_by_users:
    #     print('after remove:',
    #           course.user_name,
    #           course.product_name,
    #           course.number_owned)

    # # test update_stock
    # products = models.Product.select()
    # for product in products:
    #     print('before update', product.product_name, product.number_in_stock)
    # update_stock(product_id='FED', new_quantity=10)
    # products = models.Product.select()
    # for product in products:
    #     print('after update', product.product_name, product.number_in_stock)

    # # test purchase_product
    # products = models.Product.select()
    # for product in products:
    #     print('stock before transaction',
    #           product.product_name,
    #           product.number_in_stock)
    # products = models.Ownership.select()
    # for product in products:
    #     print('ownership before transaction',
    #           product.product_name,
    #           product.user_name,
    #           product.number_owned)
    # transactions = models.Transaction.select()
    # for action in transactions:
    #     print('transactions before transaction',
    #           action.buyer,
    #           action.product_name,
    #           action.number_sold,
    #           action.datetime_sold)
    # purchase_product(product_id='BED', buyer_id='kittie', quantity=1)
    # products = models.Product.select()
    # for product in products:
    #     print('stock after update',
    #           product.product_name,
    #           product.number_in_stock)
    # products = models.Ownership.select()
    # for product in products:
    #     print('ownership after transaction',
    #           product.product_name,
    #           product.user_name,
    #           product.number_owned)
    # transactions = models.Transaction.select()
    # for action in transactions:
    #     print('transactions after transaction',
    #           action.buyer,
    #           action.product_name,
    #           action.number_sold,
    #           action.datetime_sold)
