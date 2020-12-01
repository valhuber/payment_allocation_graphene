from payment_allocation.models import Customer as CustomerModel
from payment_allocation.models import Order as OrderModel
from payment_allocation.models import Payment as PaymentModel
from payment_allocation.models import PaymentAllocation as PaymentAllocationModel

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField, SQLAlchemyObjectType


class Customer(SQLAlchemyObjectType):
    class Meta:
        model = CustomerModel
        interfaces = (relay.Node, )


class Order(SQLAlchemyObjectType):
    class Meta:
        model = OrderModel
        interfaces = (relay.Node, )


class Payment(SQLAlchemyObjectType):
    class Meta:
        model = PaymentModel
        interfaces = (relay.Node, )


class Order(SQLAlchemyObjectType):
    class Meta:
        model = OrderModel
        interfaces = (relay.Node, )


class PaymentAllocation(SQLAlchemyObjectType):
    class Meta:
        model = PaymentAllocationModel
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    # Allow only single column sorting
    all_customers = SQLAlchemyConnectionField(
        Customer.connection, sort=Customer.sort_argument())
    # Allows sorting over multiple columns, by default over the primary key
    all_payments = SQLAlchemyConnectionField(Payment.connection)
    # Disable sorting over this field
    all_payment_allocations = SQLAlchemyConnectionField(PaymentAllocation.connection, sort=None)


schema = graphene.Schema(query=Query)
