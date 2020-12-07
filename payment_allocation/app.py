#!/usr/bin/env python

import logic_bank_utils.util as logic_bank_utils

(did_fix_path, sys_env_info) = \
    logic_bank_utils.add_python_path(project_dir="payment_allocation_graphene", my_file=__file__)
print("\n" + did_fix_path + "\n\n" + sys_env_info + "\n\n")

from payment_allocation.database import db_session, init_db, Base
from payment_allocation.models import Customer, Order, Payment, PaymentAllocation

from flask import Flask
from payment_allocation.schema import schema

from flask_graphql import GraphQLView


app = Flask(__name__)
app.debug = True

strategy = "dear_boy"  # seeking update, using "goodking_bq"  -- fails per readme
if strategy == "like_example":  # ala https://github.com/graphql-python/graphene-sqlalchemy/tree/master/examples/flask_sqlalchemy
    app.add_url_rule(
        "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
    )
elif strategy == "dear_boy":  # from @yoursdearboy https://github.com/graphql-python/graphene-sqlalchemy/issues/30
    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            graphiql=True,
            get_context=lambda: {'session': db_session}
        ),
    )
elif strategy == "goodking_bq":  # from @yoursdearboy https://github.com/graphql-python/graphene-sqlalchemy/issues/30
    from graphene_sqlalchemy_auto import QueryObjectType, MutationObjectType
    from sqlalchemy.ext.declarative import declarative_base
    import graphene
    from sqlalchemy.orm import sessionmaker
    """
    Base = declarative_base()
    Session = sessionmaker()
    """


    class Query(QueryObjectType):
        class Meta:
            declarative_base = Base
            exclude_models = ["User"]  # exclude models

    class Mutation(MutationObjectType):
        class Meta:
            declarative_base = Base
            session = db_session  # mutate used

            include_object = []  # you can use yourself mutation UserCreateMutation, UserUpdateMutation

    dynamic_schema = graphene.Schema(query=Query, mutation=Mutation)
    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=dynamic_schema,
            graphiql=True,
            get_context=lambda: {'session': db_session}
        ),
    )
else:
    raise Exception("no such strategy")

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    init_db()
    print("DB Init Complete")
    app.run()
