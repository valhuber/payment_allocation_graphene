#!/usr/bin/env python

import logic_bank_utils.util as logic_bank_utils
import sqlalchemy

(did_fix_path, sys_env_info) = \
    logic_bank_utils.add_python_path(project_dir="payment_allocation_graphene", my_file=__file__)
print("\n" + did_fix_path + "\n\n" + sys_env_info + "\n\n")

from payment_allocation.database import db_session, init_db, Base
from payment_allocation.models import Customer, Order, Payment, PaymentAllocation

from flask import Flask
from payment_allocation.schema import schema

from flask_graphql import GraphQLView

from graphene_sqlalchemy_auto import QueryObjectType, MutationObjectType

app = Flask(__name__)
app.debug = True

import graphene
from sqlalchemy.orm import sessionmaker
"""
Base = declarative_base()
Session = sessionmaker()

is app.config.update... required?
see https://github.com/goodking-bq/graphene-sqlalchemy-auto/blob/master/example/flask_app/app.py
"""

import payment_allocation.models as models  # just a guess

debug = Base # from sqlalchemy.ext.declarative import declarative_base;  Base = declarative_base()

class QueryDyn(QueryObjectType):
    class Meta:  # console run fails with: AttributeError: type object 'Base' has no attribute 'registry'
        print("QueryDyn, Base IsA: " + str(type(Base)))  # prints:  <class 'sqlalchemy.ext.declarative.api.DeclarativeMeta'>
        declarative_base = Base   # Python Console says Base is <class 'sqlalchemy.ext.declarative.api.Base'>
        # exclude_models = ["User"]  # exclude models

class MutationDyn(MutationObjectType):
    class Meta:
        declarative_base = Base
        session = db_session  # mutate used
        # include_object = []  # you can use yourself mutation UserCreateMutation, UserUpdateMutation

# fails: AssertionError: MutationDyn fields must be a mapping (dict / OrderedDict) with field names as keys or a function which returns such a mapping.
# mutation_dyn = MutationDyn()
dynamic_schema = graphene.Schema(query=QueryDyn, mutation=MutationDyn)
app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view(
        'graphql',
        schema=dynamic_schema,
        graphiql=True,
        get_context=lambda: {'session': db_session}
    ),
)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    init_db()
    print("DB Init Complete")
    app.run()
