"""
Serializers control the translation of client data to and from Python objects,
while Django itself handles the database abstraction.
"""

from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
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
    ACLExtendedRule,
    ACLInterfaceAssignment,
    ACLStandardRule,
    FirewallRuleList,
    FWEgressRule,
    FWIngressRule,
    FWInterfaceAssignment,
)
from .nested_serializers import NestedAccessListSerializer, NestedFirewallRuleListSerializer

__all__ = [
    "AccessListSerializer",
    "ACLInterfaceAssignmentSerializer",
    "ACLStandardRuleSerializer",
    "ACLExtendedRuleSerializer",
    "FirewallRuleListSerializer",
    "FWEgressRuleSerializer",
    "FWIngressRuleSerializer",
    "FWInterfaceAssignmentSerializer",
]

# Sets a standard error message for ACL rules with an action of remark, but no remark set.
error_message_no_remark = "Action is set to remark, you MUST add a remark."
# Sets a standard error message for ACL rules with an action of remark, but no source_prefix is set.
error_message_action_remark_source_prefix_set = "Action is set to remark, Source Prefix CANNOT be set."
# Sets a standard error message for ACL rules with an action not set to remark, but no remark is set.
error_message_remark_without_action_remark = "CANNOT set remark unless action is set to remark."
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
            "default_action",
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
            "direction",
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


class ACLStandardRuleSerializer(NetBoxModelSerializer):
    """
    Defines the serializer for the django ACLStandardRule model & associates it to a view.
    """

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_acls-api:aclstandardrule-detail",
    )
    access_list = NestedAccessListSerializer()

    class Meta:
        """
        Associates the django model ACLStandardRule & fields to the serializer.
        """

        model = ACLStandardRule
        fields = (
            "id",
            "url",
            "display",
            "access_list",
            "index",
            "action",
            "tags",
            "description",
            "remark",
            "created",
            "custom_fields",
            "last_updated",
            "source_prefix",
        )

    def validate(self, data):
        """
        Validate the ACLStandardRule django model's inputs before allowing it to update the instance:
          - Check if action set to remark, but no remark set.
          - Check if action set to remark, but source_prefix set.
        """
        error_message = {}

        # Check if action set to remark, but no remark set.
        if data.get("action") == "remark" and data.get("remark") is None:
            error_message["remark"] = [error_message_no_remark]
        # Check if action set to remark, but source_prefix set.
        if data.get("source_prefix"):
            error_message["source_prefix"] = [
                error_message_action_remark_source_prefix_set,
            ]

        if error_message:
            raise serializers.ValidationError(error_message)

        return super().validate(data)


class ACLExtendedRuleSerializer(NetBoxModelSerializer):
    """
    Defines the serializer for the django ACLExtendedRule model & associates it to a view.
    """

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_acls-api:aclextendedrule-detail",
    )
    access_list = NestedAccessListSerializer()

    class Meta:
        """
        Associates the django model ACLExtendedRule & fields to the serializer.
        """

        model = ACLExtendedRule
        fields = (
            "id",
            "url",
            "display",
            "access_list",
            "index",
            "action",
            "tags",
            "description",
            "created",
            "custom_fields",
            "last_updated",
            "source_prefix",
            "source_ports",
            "destination_prefix",
            "destination_ports",
            "protocol",
            "remark",
        )

    def validate(self, data):
        """
        Validate the ACLExtendedRule django model's inputs before allowing it to update the instance:
          - Check if action set to remark, but no remark set.
          - Check if action set to remark, but source_prefix set.
          - Check if action set to remark, but source_ports set.
          - Check if action set to remark, but destination_prefix set.
          - Check if action set to remark, but destination_ports set.
          - Check if action set to remark, but protocol set.
          - Check if action set to remark, but protocol set.
        """
        error_message = {}

        # Check if action set to remark, but no remark set.
        if data.get("action") == "remark" and data.get("remark") is None:
            error_message["remark"] = [error_message_no_remark]
        # Check if action set to remark, but source_prefix set.
        if data.get("source_prefix"):
            error_message["source_prefix"] = [
                error_message_action_remark_source_prefix_set,
            ]
        # Check if action set to remark, but source_ports set.
        if data.get("source_ports"):
            error_message["source_ports"] = [
                "Action is set to remark, Source Ports CANNOT be set.",
            ]
        # Check if action set to remark, but destination_prefix set.
        if data.get("destination_prefix"):
            error_message["destination_prefix"] = [
                "Action is set to remark, Destination Prefix CANNOT be set.",
            ]
        # Check if action set to remark, but destination_ports set.
        if data.get("destination_ports"):
            error_message["destination_ports"] = [
                "Action is set to remark, Destination Ports CANNOT be set.",
            ]
        # Check if action set to remark, but protocol set.
        if data.get("protocol"):
            error_message["protocol"] = [
                "Action is set to remark, Protocol CANNOT be set.",
            ]

        if error_message:
            raise serializers.ValidationError(error_message)

        return super().validate(data)


class FirewallRuleListSerializer(NetBoxModelSerializer):
    """
    Defines the serializer for the django FirewallRuleList model & associates it to a view.
    """

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_acls-api:fwrulelist-detail",
    )
    rule_count = serializers.IntegerField(read_only=True)
    assigned_object_type = ContentTypeField(
        queryset=ContentType.objects.filter(Q(app_label="dcim", model="device_role")),
    )
    assigned_object = serializers.SerializerMethodField(read_only=True)

    class Meta:
        """
        Associates the django model FWRuleList & fields to the serializer.
        """

        model = FirewallRuleList
        fields = (
            "id",
            "url",
            "display",
            "name",
            "assigned_object_type",
            "assigned_object_id",
            "assigned_object",
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
        """
        error_message = {}

        if error_message:
            raise serializers.ValidationError(error_message)

        return super().validate(data)


class FWInterfaceAssignmentSerializer(NetBoxModelSerializer):
    """
    Defines the serializer for the django FWInterfaceAssignment model & associates it to a view.
    """

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_acls-api:fwinterfaceassignment-detail",
    )
    fw_rule_list = NestedFirewallRuleListSerializer()
    assigned_object_type = ContentTypeField(
        queryset=ContentType.objects.filter(ACL_INTERFACE_ASSIGNMENT_MODELS),
    )
    assigned_object = serializers.SerializerMethodField(read_only=True)

    class Meta:
        """
        Associates the django model FWInterfaceAssignment & fields to the serializer.
        """

        model = FWInterfaceAssignment
        fields = (
            "id",
            "url",
            "fw_rule_list",
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
        """
        error_message = {}

        if error_message:
            raise serializers.ValidationError(error_message)

        return super().validate(data)


class FWIngressRuleSerializer(NetBoxModelSerializer):
    """
    Defines the serializer for the django FWIngressRule model & associates it to a view.
    """

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_acls-api:fwingressrule-detail",
    )
    fw_rule_list = NestedFirewallRuleListSerializer()

    class Meta:
        """
        Associates the django model FWIngressRule & fields to the serializer.
        """

        model = FWIngressRule
        fields = (
            "id",
            "url",
            "display",
            "fw_rule_list",
            "index",
            "tags",
            "description",
            "created",
            "custom_fields",
            "last_updated",
            "source_prefix",
            "destination_ports",
            "protocol",
        )

    def validate(self, data):
        """
        Validate the ACLStandardRule django model's inputs before allowing it to update the instance:

        """
        error_message = {}

        if error_message:
            raise serializers.ValidationError(error_message)

        return super().validate(data)


class FWEgressRuleSerializer(NetBoxModelSerializer):
    """
    Defines the serializer for the django FWEgressRule model & associates it to a view.
    """

    url = serializers.HyperlinkedIdentityField(
        view_name="plugins-api:netbox_acls-api:fwegressrule-detail",
    )
    fw_rule_list = NestedFirewallRuleListSerializer()

    class Meta:
        """
        Associates the django model FWEgressRule & fields to the serializer.
        """

        model = FWEgressRule
        fields = (
            "id",
            "url",
            "display",
            "access_list",
            "index",
            "action",
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
        Validate the FWEgressRule django model's inputs before allowing it to update the instance:

        """
        error_message = {}

        if error_message:
            raise serializers.ValidationError(error_message)

        return super().validate(data)
