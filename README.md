# Example: Graphene + SQLAlchemy + LogicBank

This example project explores integration between:

* [Graphene-SQLAlchemy](https://github.com/graphql-python/graphene-sqlalchemy)
and 
* [LogicBank](https://github.com/valhuber/LogicBank)

It is an adaption of [the graphene flask example](https://github.com/graphql-python/graphene-sqlalchemy/tree/master/examples/flask_sqlalchemy).

See the [LogicBank Wiki](https://github.com/valhuber/LogicBank/wiki/Sample-Project---Allocation) for an overview of the ```payment_allocation``` application.

-----------------

> This is a **work in progress** to explore GraphQL, and Logic Bank integration.
> 
> Hello World, to confirm basic read, write with rules.

-----------------

## Background
**GraphQL** (as I understand it) moves API definition from 
the server team to the consumers,
who clearly better understand their requirements.  Clear
specifications can reduce traffic, in either size and or
number of messages.  The focus is on **efficient retrieval
and organizational independence.**

**Logic Base** can reduce update logic coding (a signficant
part of any database app) by 40X, by using
spreadsheet-like rules plus Python for extensibility.  The
focus is on **update agility.**

Both are based on SQLAlchemy.  This project explores using
Graphene for retrieval, and Logic Base for mutation logic.

## Install

```bash
git clone https://github.com/valhuber/payment_allocation_graphene.git

# Create a virtualenv in which we can install the dependencies
cd payment_allocation_graphene
virtualenv venv
source venv/bin/activate

# install dependencies
pip install -r requirements.txt
```

Here is failing pip freeze:
```bash
aniso8601==7.0.0
certifi==2020.12.5
chardet==4.0.0
click==7.1.2
Flask==1.1.2
Flask-GraphQL==2.0.1
Flask-SQLAlchemy==2.4.4
graphene==2.1.8
graphene-sqlalchemy==2.3.0
graphql-core==2.3.2
graphql-relay==2.0.1
graphql-server-core==1.2.0
idna==2.10
itsdangerous==1.1.0
Jinja2==2.11.3
logicbank==0.9.6
logicbankutils==0.6.0
MarkupSafe==1.1.1
promise==2.3
python-dateutil==2.8.1
requests==2.25.1
Rx==1.6.1
singledispatch==3.6.1
six==1.15.0
SQLAlchemy==1.3.20
SQLAlchemy-Utils==0.36.8
urllib3==1.26.4
Werkzeug==1.0.1
```

vs. working pip freeze from graphene-sqlalchemy-auto
```bash
aniso8601==7.0.0
click==7.1.2
Flask==1.1.2
Flask-GraphQL==2.0.1
Flask-SQLAlchemy==2.4.4
graphene==2.1.8
graphene-sqlalchemy==2.3.0
graphql-core==2.3.2
graphql-relay==2.0.1
graphql-server-core==1.2.0
itsdangerous==1.1.0
Jinja2==2.11.2
MarkupSafe==1.1.1
promise==2.3
Rx==1.6.1
singledispatch==3.4.0.3
six==1.15.0
SQLAlchemy==1.3.20
Werkzeug==1.0.1
```

### Verify LogicBank


```bash
cd payment_allocation/tests
python add_payment.py

# console log should end with:
..Customer[ALFKI] {Correct adjusted Customer Result} Id: ALFKI, CompanyName: Alfreds Futterkiste, Balance:  [16.00-->] -984.00, CreditLimit: 2000.00  row@: 0x107e19730 - 2021-04-03 20:52:28,174 - logic_logger - DEBUG

add_payment, ran to completion

```

## Run Mutation Test

This fails, per the log below:

```bash
cd payment_allocation
export PYTHONPATH="/Users/val/dev/graph_ql/payment_allocation_graphene/"
python app.py
```


### Fails to create schema

On 4/3, ```pip install graphene-sqlalchemy_auto -U```.

Now failing with:
```
(venv) val@Vals-MacBook-Pro-16 payment_allocation % export PYTHONPATH="/Users/val/dev/graph_ql/payment_allocation_graphene/"
(venv) val@Vals-MacBook-Pro-16 payment_allocation % python app.py                                                           

logic/__init__.py#<module>(): BEGIN - setup logging, connect to db, register listeners


Validate Rule BankAbstractRule Bank[0x102709d30] (loaded 2021-04-05 07:58:14.607281)
Mapped Class[Customer] rules:
  Derive Customer.Balance as Sum(Order.AmountOwed Where None)
Mapped Class[Order] rules:
  Derive Order.AmountOwed as Formula (1): Rule.formula(derive=Order.AmountOwed, as_expressi [...]
  Derive Order.AmountPaid as Sum(PaymentAllocation.AmountAllocated Where None)
Mapped Class[PaymentAllocation] rules:
  Derive PaymentAllocation.AmountAllocated as Formula (1): Rule.formula(derive=PaymentAllocation.AmountAlloc [...]
Mapped Class[Payment] rules:
  RowEvent Function: <function allocate_payment at 0x1023c05e0> 

logic/__init__.py#<module>(): END - connected, session created, listeners registered


logic/__init__.py#<module>(): BEGIN - setup logging, connect to db, register listeners


Validate Rule BankAbstractRule Bank[0x102709d30] (loaded 2021-04-05 07:58:14.692094)
Mapped Class[Customer] rules:
  Derive Customer.Balance as Sum(Order.AmountOwed Where None)
Mapped Class[Order] rules:
  Derive Order.AmountOwed as Formula (1): Rule.formula(derive=Order.AmountOwed, as_expressi [...]
  Derive Order.AmountPaid as Sum(PaymentAllocation.AmountAllocated Where None)
Mapped Class[PaymentAllocation] rules:
  Derive PaymentAllocation.AmountAllocated as Formula (1): Rule.formula(derive=PaymentAllocation.AmountAlloc [...]
Mapped Class[Payment] rules:
  RowEvent Function: <function allocate_payment at 0x1023c05e0> 

logic/__init__.py#<module>(): END - connected, session created, listeners registered


NOT Fixing path (default PyCharm, set in VSC Launch Config)

**************** add_python_path BEGIN          calling file: app.py

Run Environment info...

Current Working Directory: /Users/val/dev/graph_ql/payment_allocation_graphene/payment_allocation

sys.path: (Python imports)
/Users/val/dev/graph_ql/payment_allocation_graphene/payment_allocation
/Users/val/dev/graph_ql/payment_allocation_graphene
/Users/val/.pyenv/versions/3.8.6/lib/python38.zip
/Users/val/.pyenv/versions/3.8.6/lib/python3.8
/Users/val/.pyenv/versions/3.8.6/lib/python3.8/lib-dynload
/Users/val/dev/graph_ql/payment_allocation_graphene/venv/lib/python3.8/site-packages

From: app.py

Using Python: 3.8.6 (default, Oct 27 2020, 21:11:31) 
[Clang 12.0.0 (clang-1200.0.32.27)]

At: 2021-04-05 07:58:14.723091

fix path: NOT Fixing path (default PyCharm, set in VSC Launch Config)

**************** add_python_path END


app - db IsA: <class 'flask_sqlalchemy.SQLAlchemy'>
app - models_base IsA: <class 'flask_sqlalchemy.model.DefaultMeta'>

scheme: QueryDyn, db IsA: <class 'flask_sqlalchemy.SQLAlchemy'>
scheme: QueryDyn, db.Model IsA: <class 'flask_sqlalchemy.model.DefaultMeta'>
Traceback (most recent call last):
  File "app.py", line 77, in <module>
    dynamic_schema = graphene.Schema(query=QueryDyn, mutation=MutationDyn)
  File "/Users/val/dev/graph_ql/payment_allocation_graphene/venv/lib/python3.8/site-packages/graphene/types/schema.py", line 78, in __init__
    self.build_typemap()
  File "/Users/val/dev/graph_ql/payment_allocation_graphene/venv/lib/python3.8/site-packages/graphene/types/schema.py", line 167, in build_typemap
    self._type_map = TypeMap(
  File "/Users/val/dev/graph_ql/payment_allocation_graphene/venv/lib/python3.8/site-packages/graphene/types/typemap.py", line 80, in __init__
    super(TypeMap, self).__init__(types)
  File "/Users/val/dev/graph_ql/payment_allocation_graphene/venv/lib/python3.8/site-packages/graphql/type/typemap.py", line 31, in __init__
    self.update(reduce(self.reducer, types, OrderedDict()))  # type: ignore
  File "/Users/val/dev/graph_ql/payment_allocation_graphene/venv/lib/python3.8/site-packages/graphene/types/typemap.py", line 88, in reducer
    return self.graphene_reducer(map, type)
  File "/Users/val/dev/graph_ql/payment_allocation_graphene/venv/lib/python3.8/site-packages/graphene/types/typemap.py", line 117, in graphene_reducer
    return GraphQLTypeMap.reducer(map, internal_type)
  File "/Users/val/dev/graph_ql/payment_allocation_graphene/venv/lib/python3.8/site-packages/graphql/type/typemap.py", line 109, in reducer
    field_map = type_.fields
  File "/Users/val/dev/graph_ql/payment_allocation_graphene/venv/lib/python3.8/site-packages/graphql/pyutils/cached_property.py", line 22, in __get__
    value = obj.__dict__[self.func.__name__] = self.func(obj)
  File "/Users/val/dev/graph_ql/payment_allocation_graphene/venv/lib/python3.8/site-packages/graphql/type/definition.py", line 198, in fields
    return define_field_map(self, self._fields)
  File "/Users/val/dev/graph_ql/payment_allocation_graphene/venv/lib/python3.8/site-packages/graphql/type/definition.py", line 214, in define_field_map
    assert isinstance(field_map, Mapping) and len(field_map) > 0, (
AssertionError: MutationDyn fields must be a mapping (dict / OrderedDict) with field names as keys or a function which returns such a mapping.
(venv) val@Vals-MacBook-Pro-16 payment_allocation % 

```

--------
# Ignore the rest...


#### Retrieval Example
The purpose of these is just to run, and return data.

###### Single Type
Open your browser to
[http://127.0.0.1:5000/graphql](http://127.0.0.1:5000/graphql)
and paste in the request below:

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


###### Multi-type
Using your command line:
```
cd tests
python test_get.py
```
Or, open your browser to
[http://127.0.0.1:5000/graphql](http://127.0.0.1:5000/graphql)
and paste in the request below:

```
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
```

<figure><img src="payment_allocation/images/multi-type.png" width="800"></figure>


#### Update Example - WIP
This fails: ```Schema is not configured for mutations```.

Such configuration appears to be [quite code intensive](https://docs.graphene-python.org/en/latest/types/mutations/),
but possibly can create from model (statically or dynamically).  There's
[also this](https://graphql.org/graphql-js/mutations-and-input-types/).

There appears to be some
[promising work](https://github.com/goodking-bq/graphene-sqlalchemy-auto) in
this area, anxious to try this out.  First try, however, resulted in:
```
Traceback (most recent call last):
  File "/Users/val/dev/graph_ql/payment_allocation_graphene/payment_allocation/app.py", line 59, in <module>
    dynamic_schema = graphene.Schema(query=Query, mutation=Mutation)
  File "/Users/val/dev/graph_ql/payment_allocation_graphene/venv/lib/python3.8/site-packages/graphene/types/schema.py", line 78, in __init__
    self.build_typemap()
  File "/Users/val/dev/graph_ql/payment_allocation_graphene/venv/lib/python3.8/site-packages/graphene/types/schema.py", line 167, in build_typemap
    self._type_map = TypeMap(
  File "/Users/val/dev/graph_ql/payment_allocation_graphene/venv/lib/python3.8/site-packages/graphene/types/typemap.py", line 80, in __init__
    super(TypeMap, self).__init__(types)
  File "/Users/val/dev/graph_ql/payment_allocation_graphene/venv/lib/python3.8/site-packages/graphql/type/typemap.py", line 31, in __init__
    self.update(reduce(self.reducer, types, OrderedDict()))  # type: ignore
  File "/Users/val/dev/graph_ql/payment_allocation_graphene/venv/lib/python3.8/site-packages/graphene/types/typemap.py", line 88, in reducer
    return self.graphene_reducer(map, type)
  File "/Users/val/dev/graph_ql/payment_allocation_graphene/venv/lib/python3.8/site-packages/graphene/types/typemap.py", line 117, in graphene_reducer
    return GraphQLTypeMap.reducer(map, internal_type)
  File "/Users/val/dev/graph_ql/payment_allocation_graphene/venv/lib/python3.8/site-packages/graphql/type/typemap.py", line 109, in reducer
    field_map = type_.fields
  File "/Users/val/dev/graph_ql/payment_allocation_graphene/venv/lib/python3.8/site-packages/graphql/pyutils/cached_property.py", line 22, in __get__
    value = obj.__dict__[self.func.__name__] = self.func(obj)
  File "/Users/val/dev/graph_ql/payment_allocation_graphene/venv/lib/python3.8/site-packages/graphql/type/definition.py", line 198, in fields
    return define_field_map(self, self._fields)
  File "/Users/val/dev/graph_ql/payment_allocation_graphene/venv/lib/python3.8/site-packages/graphql/type/definition.py", line 214, in define_field_map
    assert isinstance(field_map, Mapping) and len(field_map) > 0, (
AssertionError: Mutation fields must be a mapping (dict / OrderedDict) with field names as keys or a function which returns such a mapping.

Process finished with exit code 1

```

```
mutation {
  customerCreate
    ( input:
        {
            Id: "ADDED",
            CompanyName: "Added, Inc",
            Balance: 0,
            CreditLimit: 0
        }
    )
    { customer {
      id
    }
  }
}
```


## Resolved Issue
Patterning the code after [this example](https://github.com/graphql-python/graphene-sqlalchemy/tree/master/examples/flask_sqlalchemy),
gets **fail** with ```Request' object has no attribute 'get'```.

Mentioned in this [stack overflow](https://github.com/graphql-python/graphene-sqlalchemy/issues/130),
which links to [this](https://github.com/graphql-python/graphene-sqlalchemy/issues/286).

Also tried [this](https://github.com/graphql-python/graphene-sqlalchemy/issues/30)
(see app.py), but still fails.

But, the [suggestion here](https://github.com/graphql-python/graphene-sqlalchemy/issues/30)
worked, using @yoursdearboy's lambda (thankyou! see ```app.py```):

```
app.add_url_rule(
  '/graphql',
  view_func=GraphQLView.as_view(
    'graphql',
    schema=schema,
    graphiql=True,
    get_context=lambda: {'session': db.session}
  )
)
``` 
