#!/usr/bin/env python

import logic_bank_utils.util as logic_bank_utils

(did_fix_path, sys_env_info) = \
    logic_bank_utils.add_python_path(project_dir="payment_allocation_graphene", my_file=__file__)
print("\n" + did_fix_path + "\n\n" + sys_env_info + "\n\n")

from payment_allocation.z_database import db_session, init_db
from payment_allocation.models import Customer, Order, Payment, PaymentAllocation

from flask import Flask
from payment_allocation.schema import schema

from flask_graphql import GraphQLView


app = Flask(__name__)
app.debug = True

as_packaged = False
if as_packaged:  # ala https://github.com/graphql-python/graphene-sqlalchemy/tree/master/examples/flask_sqlalchemy
    app.add_url_rule(
        "/graphql", view_func=GraphQLView.as_view("graphql", schema=schema, graphiql=True)
    )
else:  # from @yoursdearboy https://github.com/graphql-python/graphene-sqlalchemy/issues/30
    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
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
