from graphene import ObjectType
from netbox.graphql.fields import ObjectField, ObjectListField

from .types import *


class Query(ObjectType):
    """
    Defines the queries available to this plugin via the graphql api.
    """

    access_list = ObjectField(AccessListType)
    access_list_list = ObjectListField(AccessListType)

    acl_egress_rule = ObjectField(ACLEgressRuleType)
    acl_egress_rule_list = ObjectListField(ACLEgressRuleType)

    acl_ingress_rule = ObjectField(ACLIngressRuleType)
    acl_ingress_rule_list = ObjectListField(ACLIngressRuleType)


schema = Query
