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

# The datatype returned from that query is a object (in this case, a Brand object).


# 2. In your own words, what is an association table, and what type of
# relationship (many to one, many to many, one to one, etc.) does an
# association table manage?

# An association table is a table that "glues" together two tables, but does not
# hold any meaningful data of its own. It manages a many to many relationship. 


# -------------------------------------------------------------------
# Part 3: SQLAlchemy Queries


# Get the brand with the ``id`` of "ram."
q1 = db.session.query(Brand).filter_by(brand_id='ram').one()

# Get all models with the name "Corvette" and the brand_id "che."
q2 = db.session.query(Model).filter_by(name='Corvette', brand_id='che').all()

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
q7 = Brand.query.filter((Brand.discontinued != None)|(Brand.founded < 1950)).all()

# Get any model whose brand_id is not "for."
q8 = Brand.query.filter(Brand.brand_id != 'for').all()



# -------------------------------------------------------------------
# Part 4: Write Functions


def get_model_info(year):
    """Takes in a year and prints out each model name, brand name, and brand
    headquarters for that year using only ONE database query."""

    models = db.session.query(Model).filter_by(year=year).all()

    for model in models:
        model_name = model.name
        brand_name = model.brand.name
        headquarters = model.brand.headquarters

        print "Model name: %s, Brand name: %s, Headquarters: %s" % (model_name, 
                                                    brand_name, headquarters)


def get_brands_summary():
    """Prints out each brand name and each model name with year for that brand
    using only ONE database query."""

    brands = Brand.query.options(db.joinedload('models')).all()

    brands_and_models = {}

    for brand in brands:
        brand_name = brand.name
        brands_and_models[brand_name] = []
        for model in brand.models:
            model_name = model.name
            year = model.year
            brands_and_models[brand_name].append((model_name, year))

    for brand, cars in brands_and_models.items():
        print '%s:\n' %(brand)
        for model in cars:
            print "Model: %s | Year:%s" % (model[0], model[1])
        print




def search_brands_by_name(mystr):
    """Returns all Brand objects corresponding to brands whose names include
    the given string."""

    return Brand.query.filter(Brand.name.like('%'+mystr+'%')).all()


def get_models_between(start_year, end_year):
    """Returns all Model objects corresponding to models made between
    start_year (inclusive) and end_year (exclusive)."""

    return Model.query.filter(Model.year >= start_year, Model.year < end_year).all()

