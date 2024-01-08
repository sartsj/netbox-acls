"""
Serializers control the translation of client data to and from Python objects,
while Django itself handles the database abstraction.
"""

from django.contrib.contenttypes.models import ContentType
from drf_spectacular.utils import extend_schema_field
from ipam.api.serializers import NestedPrefixSerializer
from netbox.api.fields import ContentTypeField
from netbox.api.serializers import NetBoxModelSerializer
from netbox.constants import NESTED_SERIALIZER_PREFIX
from rest_framework import serializers
from utilities.api import get_serializer_for_model

from ..constants import ACL_HOST_ASSIGNMENT_MODELS, ACL_INTERFACE_ASSIGNMENT_MODELS
from ..models import (
    AccessList,
    ACLEgressRule,
    ACLInterfaceAssignment,
    ACLIngressRule,
)
from .nested_serializers import NestedAccessListSerializer

__all__ = [
    "AccessListSerializer",
    "ACLInterfaceAssignmentSerializer",
    "ACLIngressRuleSerializer",
    "ACLEgressRuleSerializer",
]

# Sets a standard error message for ACL rules no associated to an ACL of the same type.
error_message_acl_type = "Provided parent Access List is not of right type."


class AccessListSerializer(NetBoxModelSerializer):
    """
    Defines the serializer for the django AccessList model & associates it to a view.
    """

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_acls-api:accesslist-detail",
    )
    rule_count = serializers.IntegerField(read_only=True)
    assigned_object_type = ContentTypeField(
        queryset=ContentType.objects.filter(ACL_HOST_ASSIGNMENT_MODELS),
    )
    assigned_object = serializers.SerializerMethodField(read_only=True)

    class Meta:
        """
        Associates the django model AccessList & fields to the serializer.
        """

        model = AccessList
        fields = (
            "id",
            "url",
            "display",
            "name",
            "assigned_object_type",
            "assigned_object_id",
            "assigned_object",
            "type",
            "comments",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
            "rule_count",
        )

    @extend_schema_field(serializers.DictField())
    def get_assigned_object(self, obj):
        serializer = get_serializer_for_model(
            obj.assigned_object,
            prefix=NESTED_SERIALIZER_PREFIX,
        )
        context = {"request": self.context["request"]}
        return serializer(obj.assigned_object, context=context).data

    def validate(self, data):
        """
        Validates api inputs before processing:
          - Check that the GFK object is valid.
          - Check if Access List has no existing rules before change the Access List's type.
        """
        error_message = {}

        # Check if Access List has no existing rules before change the Access List's type.
        if self.instance and self.instance.type != data.get("type") and self.instance.rule_count > 0:
            error_message["type"] = [
                "This ACL has ACL rules associated, CANNOT change ACL type.",
            ]

        if error_message:
            raise serializers.ValidationError(error_message)

        return super().validate(data)


class ACLInterfaceAssignmentSerializer(NetBoxModelSerializer):
    """
    Defines the serializer for the django ACLInterfaceAssignment model & associates it to a view.
    """

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_acls-api:aclinterfaceassignment-detail",
    )
    access_list = NestedAccessListSerializer()
    assigned_object_type = ContentTypeField(
        queryset=ContentType.objects.filter(ACL_INTERFACE_ASSIGNMENT_MODELS),
    )
    assigned_object = serializers.SerializerMethodField(read_only=True)

    class Meta:
        """
        Associates the django model ACLInterfaceAssignment & fields to the serializer.
        """

        model = ACLInterfaceAssignment
        fields = (
            "id",
            "url",
            "access_list",
            "assigned_object_type",
            "assigned_object_id",
            "assigned_object",
            "comments",
            "tags",
            "custom_fields",
            "created",
            "last_updated",
        )

    @extend_schema_field(serializers.DictField())
    def get_assigned_object(self, obj):
        serializer = get_serializer_for_model(
            obj.assigned_object,
            prefix=NESTED_SERIALIZER_PREFIX,
        )
        context = {"request": self.context["request"]}
        return serializer(obj.assigned_object, context=context).data

    def validate(self, data):
        """
        Validate the AccessList django model's inputs before allowing it to update the instance.
          - Check that the GFK object is valid.
          - Check that the associated interface's parent host has the selected ACL defined.
        """
        error_message = {}
        acl_host = data["access_list"].assigned_object

        if data["assigned_object_type"].model == "interface":
            interface_host = data["assigned_object_type"].get_object_for_this_type(id=data["assigned_object_id"]).device
        elif data["assigned_object_type"].model == "vminterface":
            interface_host = data["assigned_object_type"].get_object_for_this_type(id=data["assigned_object_id"]).virtual_machine
        else:
            interface_host = None
        # Check that the associated interface's parent host has the selected ACL defined.
        if acl_host != interface_host:
            error_acl_not_assigned_to_host = "Access List not present on the selected interface's host."
            error_message["access_list"] = [error_acl_not_assigned_to_host]
            error_message["assigned_object_id"] = [error_acl_not_assigned_to_host]

        if error_message:
            raise serializers.ValidationError(error_message)

        return super().validate(data)


class ACLIngressRuleSerializer(NetBoxModelSerializer):
    """
    Defines the serializer for the django ACLIngressRule model & associates it to a view.
    """

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_acls-api:aclingressrule-detail",
    )
    access_list = NestedAccessListSerializer()

    class Meta:
        """
        Associates the django model ACLIngressRule & fields to the serializer.
        """

        model = ACLIngressRule
        fields = (
            "id",
            "url",
            "display",
            "access_list",
            "tags",
            "description",
            "created",
            "custom_fields",
            "last_updated",
            "source_prefix",
            "protocol",
        )

    def validate(self, data):
        """
        Validate the ACLIngressRule django model's inputs before allowing it to update the instance:
          - Check if protocol set to something other than icmp, but no destination ports set.
          - Check if protocol set to icmp, but ports are set.
        """
        error_message = {}

        # Check if protocol set to something other than icmp, but no destination ports set.
        if data.get("protocol") != 'icmp':
            if not data.get("destination_ports"):
                error_message["destination_ports"] = [
                    "Protocol is set to TCP or UDP, Destination Ports MUST be set.",
                ]
        # Check if protocol set to icmp, but ports are set.
        else:
            if data.get("destination_ports"):
                error_message["destination_ports"] = [
                    "Protocol is set to ICMP, Destination Ports CANNOT be set.",
                ]

        if error_message:
            raise serializers.ValidationError(error_message)

        return super().validate(data)


class ACLEgressRuleSerializer(NetBoxModelSerializer):
    """
    Defines the serializer for the django ACLEgressRule model & associates it to a view.
    """

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_acls-api:aclegressrule-detail",
    )
    access_list = NestedAccessListSerializer()

    class Meta:
        """
        Associates the django model ACLEgressRule & fields to the serializer.
        """

        model = ACLEgressRule
        fields = (
            "id",
            "url",
            "display",
            "access_list",
            "tags",
            "description",
            "created",
            "custom_fields",
            "last_updated",
            "destination_prefix",
            "destination_ports",
            "protocol",
        )

    def validate(self, data):
        """
        Validate the ACLEgressRule django model's inputs before allowing it to update the instance:
          - Check if protocol set to something other than icmp, but no destination ports set.
          - Check if protocol set to icmp, but ports are set.
        """
        error_message = {}

        # Check if protocol set to something other than icmp, but no destination ports set.
        if data.get("protocol") != 'icmp':
            if not data.get("destination_ports"):
                error_message["destination_ports"] = [
                    "Protocol is set to TCP or UDP, Destination Ports MUST be set.",
                ]
        # Check if protocol set to icmp, but ports are set.
        else:
            if data.get("destination_ports"):
                error_message["destination_ports"] = [
                    "Protocol is set to ICMP, Destination Ports CANNOT be set.",
                ]

        if error_message:
            raise serializers.ValidationError(error_message)

        return super().validate(data)
