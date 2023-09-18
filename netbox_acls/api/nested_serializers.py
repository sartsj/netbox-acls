"""
Serializers control the translation of client data to and from Python objects,
while Django itself handles the database abstraction.
"""

from netbox.api.serializers import WritableNestedSerializer
from rest_framework import serializers

from ..models import (
    AccessList,
    ACLEgressRule,
    ACLInterfaceAssignment,
    ACLIngressRule,
)

__all__ = [
    "NestedAccessListSerializer",
    "NestedACLInterfaceAssignmentSerializer",
    "NestedACLIngressRuleSerializer",
    "NestedACLEgressRuleSerializer",
]


class NestedAccessListSerializer(WritableNestedSerializer):
    """
    Defines the nested serializer for the django AccessList model & associates it to a view.
    """

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_acls-api:accesslist-detail",
    )

    class Meta:
        """
        Associates the django model ACLIngressRule & fields to the nested serializer.
        """

        model = AccessList
        fields = ("id", "url", "display", "name")


class NestedACLInterfaceAssignmentSerializer(WritableNestedSerializer):
    """
    Defines the nested serializer for the django ACLInterfaceAssignment model & associates it to a view.
    """

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_acls-api:aclinterfaceassignment-detail",
    )

    class Meta:
        """
        Associates the django model ACLInterfaceAssignment & fields to the nested serializer.
        """

        model = ACLInterfaceAssignment
        fields = ("id", "url", "display", "access_list")


class NestedACLIngressRuleSerializer(WritableNestedSerializer):
    """
    Defines the nested serializer for the django ACLIngressRule model & associates it to a view.
    """

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_acls-api:aclingressrule-detail",
    )

    class Meta:
        """
        Associates the django model ACLIngressRule & fields to the nested serializer.
        """

        model = ACLIngressRule
        fields = ("id", "url", "display", "index")


class NestedACLEgressRuleSerializer(WritableNestedSerializer):
    """
    Defines the nested serializer for the django ACLEgressRule model & associates it to a view.
    """

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_acls-api:aclegressrule-detail",
    )

    class Meta:
        """
        Associates the django model ACLEgressRule & fields to the nested serializer.
        """

        model = ACLEgressRule
        fields = ("id", "url", "display", "index")
