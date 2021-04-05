#!/usr/bin/env python

import logic_bank_utils.util as logic_bank_utils
import sqlalchemy.ext.declarative
from flask_sqlalchemy import SQLAlchemy
from logic_bank.logic_bank import LogicBank  # in logic_row, 'sqlalchemy.ext' has no 'declarative'
from logic_bank.exec_row_logic.logic_row import LogicRow
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from logic import rules_bank

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

# import payment_allocation.models as models  # just a guess

debug = Base # from sqlalchemy.ext.declarative import declarative_base;  Base = declarative_base()

db = SQLAlchemy()
models_base = db.Model
print(f'app - db IsA: {str(type(db))}'
      f'\napp - models_base IsA: {str(type(models_base))}\n')


class QueryDyn(QueryObjectType):
    class Meta:
        print("scheme: QueryDyn, db IsA: " + str(type(db)))              # prints:  <class 'flask_sqlalchemy.SQLAlchemy'>
        print("scheme: QueryDyn, db.Model IsA: " + str(type(db.Model)))  # prints:  <class 'flask_sqlalchemy.model.DefaultMeta'>
        """
        running example prints:
            extens: Query(Dyn), db IsA: <class 'flask_sqlalchemy.SQLAlchemy'>
            scheme: Query(Dyn), db IsA: <class 'flask_sqlalchemy.SQLAlchemy'>
            scheme: Query(Dyn), db.Model IsA: <class 'flask_sqlalchemy.model.DefaultMeta'>
            app - models: <module 'flask_app.models' from '/Users/val/dev/graph_ql/graphene-sqlalchemy-auto/example/flask_app/models.py'>
        """
        debug_db = db
        debug_model = db.Model
        declarative_base = db.Model   # Python Console says db.Model is <class 'sqlalchemy.ext.declarative.api.Model'>

        # exclude_models = ["User"]  # exclude models


class MutationDyn(MutationObjectType):
    class Meta:
        declarative_base = db.Model
        session = db_session  # mutate used
        # include_object = []  # you can use yourself mutation UserCreateMutation, UserUpdateMutation


""" fails...
AssertionError: MutationDyn fields must be a mapping (dict / OrderedDict) with field names as keys or a function which returns such a mapping.
"""
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
