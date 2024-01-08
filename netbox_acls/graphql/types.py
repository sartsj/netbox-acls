"""
Define the object types and queries availble via the graphql api.
"""

from netbox.graphql.types import NetBoxObjectType

from .. import filtersets, models

__all__ = (
    "AccessListType",
    "ACLInterfaceAssignmentType",
    "ACLEgressRuleType",
    "ACLIngressRuleType",
)


class AccessListType(NetBoxObjectType):
    """
    Defines the object type for the django model AccessList.
    """

    class Meta:
        """
        Associates the filterset, fields, and model for the django model AccessList.
        """

        model = models.AccessList
        fields = "__all__"
        filterset_class = filtersets.AccessListFilterSet


class ACLInterfaceAssignmentType(NetBoxObjectType):
    """
    Defines the object type for the django model AccessList.
    """

    class Meta:
        """
        Associates the filterset, fields, and model for the django model ACLInterfaceAssignment.
        """

        model = models.ACLInterfaceAssignment
        fields = "__all__"
        filterset_class = filtersets.ACLInterfaceAssignmentFilterSet


class ACLEgressRuleType(NetBoxObjectType):
    """
    Defines the object type for the django model ACLEgressRule.
    """

    class Meta:
        """
        Associates the filterset, fields, and model for the django model ACLEgressRule.
        """

        model = models.ACLEgressRule
        fields = "__all__"
        filterset_class = filtersets.ACLEgressRuleFilterSet


class ACLIngressRuleType(NetBoxObjectType):
    """
    Defines the object type for the django model ACLIngressRule.
    """

    class Meta:
        """
        Associates the filterset, fields, and model for the django model ACLIngressRule.
        """

        model = models.ACLIngressRule
        fields = "__all__"
        filterset_class = filtersets.ACLIngressRuleFilterSet
