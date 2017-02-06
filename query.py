"""

This file is the place to write solutions for the
skills assignment called skills-sqlalchemy. Remember to
consult the exercise instructions for more complete
explanations of the assignment.

All classes from model.py are being imported for you
here, so feel free to refer to classes without the
[model.]User prefix.

"""

from model import *

init_app()


# -------------------------------------------------------------------
# Part 2: Discussion Questions


# 1. What is the datatype of the returned value of
# ``Brand.query.filter_by(name='Ford')``?

# That query does not actually return any data. It simply returns a SQLAlchemy
# BaseQuery object. BaseQuery comes from the SQLAlchemy Model. To return data,
# you would need to append the query with .all(), .one(), etc.

# 2. In your own words, what is an association table, and what type of
# relationship (many to one, many to many, one to one, etc.) does an
# association table manage?

# An association table sits between tables that have a many to many relationship.
# It does not contain meaningful data on its own, but serves to represent all the
# relationships between the two tables.


# -------------------------------------------------------------------
# Part 3: SQLAlchemy Queries

# Get the brand with the ``id`` of "ram."
q1 = Brand.query.get('ram')

# Get all models with the name "Corvette" and the brand_id "che."
q2 = Model.query.filter_by(name='Corvette', brand_id='che').all()

# Get all models that are older than 1960.
q3 = Model.query.filter(Model.year < 1960).all()

# Get all brands that were founded after 1920.
q4 = Brand.query.filter(Brand.founded > 1920).all()

# Get all models with names that begin with "Cor."
q5 = Model.query.filter(Model.name.like('Cor%')).all()

# Get all brands that were founded in 1903 and that are not yet discontinued.
q6 = Brand.query.filter(Brand.founded == 1903, Brand.discontinued == None).all()

# Get all brands that are either 1) discontinued (at any time) or 2) founded
# before 1950.
q7 = Brand.query.filter((Brand.discontinued != None) | (Brand.founded < 1950)).all()

# Get any model whose brand_id is not "for."
q8 = Model.query.filter(Model.brand_id != 'for').all()


# -------------------------------------------------------------------
# Part 4: Write Functions


def get_model_info(year):
    """Takes in a year and prints out each model name, brand name, and brand
    headquarters for that year using only ONE database query."""

    models_per_year = db.session.query(Model.name, Brand.name, Brand.headquarters).outerjoin(Brand).filter(Model.year == year).all()

    for name, brand_name, headquarters in models_per_year:
        print "{} by {} from {}".format(name, brand_name, headquarters)


def get_brands_summary():
    """Prints out each brand name and each model name with year for that brand
    using only ONE database query."""

    models_for_brand = db.session.query(Brand.name, Model.name, Model.year).join(Model).order_by(Brand.name).all()

    for brand_name, name, year in models_for_brand:
        print "{}'s car, the {} released in {}".format(brand_name, name, year)


def search_brands_by_name(mystr):
    """Returns all Brand objects corresponding to brands whose names include
    the given string."""

    sqa_expression = '%{}%'.format(mystr)

    brands_containing = db.session.query(Brand).filter(Brand.name.ilike(sqa_expression)).all()

    for brand in brands_containing:
        print brand


def get_models_between(start_year, end_year):
    """Returns all Model objects corresponding to models made between
    start_year (inclusive) and end_year (exclusive)."""

    models_between = db.session.query(Model).filter(Model.year >= start_year, Model.year < end_year).all()

    for model in models_between:
        print model
