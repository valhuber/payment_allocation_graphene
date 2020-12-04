from decimal import Decimal

import logic_bank_utils.util as logic_bank_utils

(did_fix_path, sys_env_info) = \
    logic_bank_utils.add_python_path(project_dir="payment_allocation_graphene", my_file=__file__)
print("\n" + did_fix_path + "\n\n" + sys_env_info + "\n\n")


def setup_db():
    """ copy db/database-gold.sqlite3 over db/database.sqlite3"""
    import os
    from shutil import copyfile
    from logic_bank.util import prt

    print("\n" + prt("restoring database-gold\n"))

    basedir = os.path.abspath(os.path.dirname(__file__))
    basedir = os.path.dirname(basedir)

    print("\n********************************\n"
          "  IMPORTANT - create database.sqlite3 from database-gold.sqlite3 in " + basedir + "/payment_allocation/db/\n" +
          "            - from -- " + prt("") +
          "\n********************************")

    db_loc = os.path.join(basedir, "database.sqlite3")
    db_source = os.path.join(basedir, "database-gold.sqlite3")
    copyfile(src=db_source, dst=db_loc)


setup_db()

import payment_allocation.models as models
from logic_bank.exec_row_logic.logic_row import LogicRow
from logic_bank.util import row_prt, prt
from payment_allocation.logic import session  # opens db, activates logic listener <--

"""
Test calling GraphQL (server must be running).
"""

query = """
{
  allCustomers {
    edges {
      node {
        Id
        Balance
        OrderList {
          edges {
            node {
              CustomerId
              AmountTotal
            }
          }
        }
      }
    }
  }
}
"""

import requests
import json

url = 'http://127.0.0.1:5000/graphql'
r = requests.post(url, json={'query': query})
print(r.status_code)
print(r.text)

