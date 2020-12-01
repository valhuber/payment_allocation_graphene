Example: Graphene + SQLAlchemy + LogicBank
==========================================

This example project demos integration between:

* [Graphene-SQLAlchemy](https://github.com/graphql-python/graphene-sqlalchemy)
and 
* [LogicBank](https://github.com/valhuber/LogicBank)

It is an adaption of [this example](https://github.com/graphql-python/graphene-sqlalchemy/tree/master/examples/flask_sqlalchemy).

See the [LogicBank Wiki](https://github.com/valhuber/LogicBank/wiki/Sample-Project---Allocation) for an overview of the ```payment_allocation``` application.

Getting started
---------------

First you'll need to get the source of the project. Do this by cloning the
whole Graphene-SQLAlchemy repository:

```bash
# Get the example project code
git clone https://github.com/valhuber/payment_allocation_graphene.git
```

It is good idea (but not required) to create a virtual environment
for this project. We'll do this using
[virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
to keep things simple,
but you may also find something like
[virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/)
to be useful:

```bash
# Create a virtualenv in which we can install the dependencies
cd payment_allocation_graphene
virtualenv venv
source venv/bin/activate
```

Now we can install our dependencies:

```bash
pip install -r requirements.txt
```

Verify LogicBank
----------------

```bash
cd payment_allocation/tests
python add_payment.py
```

Explore Graphene
----------------
***WIP*** - not running

Now the following command will setup the database, and start the server:

```bash
chmod +x app.py
./app.py
```


Now head on over to
[http://127.0.0.1:5000/graphql](http://127.0.0.1:5000/graphql)
and run some queries; samples below.

This fails with ```Request' object has no attribute 'get'```

Mentioned in this [stack overflow](https://github.com/graphql-python/graphene-sqlalchemy/issues/130),
which links to [this](https://github.com/graphql-python/graphene-sqlalchemy/issues/286)

```
{
  allCustomers(sort: [ID_ASC]) {
    edges {
      node {
        Id
        Balance
      }
    }
  }
}
```

```
{
  allCustomers {
    edges {
      node {
        Id
        Balance
        OrderList {
          CustomerID
          AmountTotal
        }
      }
    }
  }
}
```
