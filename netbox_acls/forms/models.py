"""
Defines each django model's GUI form to add or edit objects for each django model.
"""

from dcim.models import Device, Interface, VirtualChassis, DeviceRole
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.utils.safestring import mark_safe
from ipam.models import Prefix
from netbox.forms import NetBoxModelForm
from utilities.forms.fields import CommentField, DynamicModelChoiceField
from virtualization.models import (
    Cluster,
    ClusterGroup,
    ClusterType,
    VirtualMachine,
    VMInterface,
)

from ..choices import ACLAssignmentDirectionChoices
from ..models import (
    AccessList,
    ACLEgressRule,
    ACLInterfaceAssignment,
    ACLIngressRule,
)

__all__ = (
    "AccessListForm",
    "ACLInterfaceAssignmentForm",
    "ACLIngressRuleForm",
    "ACLEgressRuleForm",
)

# Sets a standard mark_safe help_text value to be used by the various classes
help_text_acl_rule_logic = mark_safe(
    "<b>*Note:</b> CANNOT be set if action is set to remark.",
)
# Sets a standard help_text value to be used by the various classes for acl action
help_text_acl_action = "Action the rule will take (remark, deny, or allow)."
# Sets a standard help_text value to be used by the various classes for acl index
help_text_acl_rule_index = "Determines the order of the rule in the ACL processing. AKA Sequence Number."

# Sets a standard error message for ACL rules with an action of remark, but no remark set.
error_message_no_remark = "Action is set to remark, you MUST add a remark."
# Sets a standard error message for ACL rules with an action of remark, but no source_prefix is set.
error_message_action_remark_source_prefix_set = "Action is set to remark, Source Prefix CANNOT be set."
# Sets a standard error message for ACL rules with an action not set to remark, but no remark is set.
error_message_remark_without_action_remark = "CANNOT set remark unless action is set to remark."


class AccessListForm(NetBoxModelForm):
    """
    GUI form to add or edit an AccessList.
    Requires a device, a name, a type, and a default_action.
    """

    # Device Role selector
    device_role = DynamicModelChoiceField(
        queryset=DeviceRole.objects.all(),
        required=True,
    )

    comments = CommentField()

    class Meta:
        model = AccessList
        fields = (
            "device_role",
            "name",
            "type",
            "default_action",
            "comments",
            "tags",
        )
        help_texts = {
            "default_action": "The default behavior of the ACL.",
            "name": "The name uniqueness per device is case insensitive.",
            "type": mark_safe(
                "<b>*Note:</b> CANNOT be changed if ACL Rules are assoicated to this Access List.",
            ),
        }

    def __init__(self, *args, **kwargs):
        # Initialize helper selectors
        instance = kwargs.get("instance")
        initial = kwargs.get("initial", {}).copy()
        if instance:
            if isinstance(instance.assigned_object, DeviceRole):
                initial["device_role"] = instance.assigned_object

        kwargs["initial"] = initial
        super().__init__(*args, **kwargs)

    def clean(self):
        """
        Validates form inputs before submitting:
          - Check if more than one host type selected.
          - Check if no hosts selected.
          - Check if duplicate entry. (Because of GFK.)
          - Check if Access List has no existing rules before change the Access List's type.
        """
        #cleaned_data = super().clean()
        error_message = {}
        if self.errors.get("name"):
            return self.cleaned_data
        name = self.cleaned_data.get("name")
        acl_type = self.cleaned_data.get("type")
        device_role = self.cleaned_data.get("device_role")

        # Check if no role selected.
        if not device_role:
            raise forms.ValidationError(
                "Access Lists must be assigned to a device, virtual chassis or virtual machine.",
            )

        # Check if Access List has no existing rules before change the Access List's type.
        if self.instance.pk and (
            (acl_type == ACLAssignmentDirectionChoices.DIRECTION_EGRESS and self.instance.aclingressrules.exists())
            or (acl_type == ACLAssignmentDirectionChoices.DIRECTION_INGRESS and self.instance.aclegressrules.exists())
        ):
            error_message["type"] = [
                "This ACL has ACL rules associated, CANNOT change ACL type.",
            ]

        if error_message:
            raise forms.ValidationError(error_message)

        return self.cleaned_data

    def save(self, *args, **kwargs):
        # Set assigned object
        self.instance.assigned_object = (self.cleaned_data.get("device_role"))

        return super().save(*args, **kwargs)


class ACLInterfaceAssignmentForm(NetBoxModelForm):
    """
    GUI form to add or edit ACL Host Object assignments
    Requires an access_list, a name, a type, and a default_action.
    """

    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        required=False,
        # query_params={
        # Need to pass ACL device to it
        # },
    )
    interface = DynamicModelChoiceField(
        queryset=Interface.objects.all(),
        required=False,
        query_params={
            "device_id": "$device",
        },
    )
    virtual_machine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
        # query_params={
        # Need to pass ACL device to it
        # },
        label="Virtual Machine",
    )
    vminterface = DynamicModelChoiceField(
        queryset=VMInterface.objects.all(),
        required=False,
        query_params={
            "virtual_machine_id": "$virtual_machine",
        },
        label="VM Interface",
    )
    # virtual_chassis = DynamicModelChoiceField(
    #    queryset=VirtualChassis.objects.all(),
    #    required=False,
    #    label='Virtual Chassis',
    # )
    access_list = DynamicModelChoiceField(
        queryset=AccessList.objects.all(),
        # query_params={
        #    'assigned_object': '$device',
        #    'assigned_object': '$virtual_machine',
        # },
        label="Access List",
    )
    comments = CommentField()

    def __init__(self, *args, **kwargs):
        # Initialize helper selectors
        instance = kwargs.get("instance")
        initial = kwargs.get("initial", {}).copy()
        if instance:
            if type(instance.assigned_object) is Interface:
                initial["interface"] = instance.assigned_object
                initial["device"] = "device"
            elif type(instance.assigned_object) is VMInterface:
                initial["vminterface"] = instance.assigned_object
                initial["virtual_machine"] = "virtual_machine"
        kwargs["initial"] = initial

        super().__init__(*args, **kwargs)

    class Meta:
        model = ACLInterfaceAssignment
        fields = (
            "access_list",
            "device",
            "interface",
            "virtual_machine",
            "vminterface",
            "comments",
            "tags",
        )
        help_texts = {
        }

    def clean(self):
        """
        Validates form inputs before submitting:
          - Check if both interface and vminterface are set.
          - Check if neither interface nor vminterface are set.
          - Check that an interface's parent device/virtual_machine is assigned to the Access List.
          - Check that an interface's parent device/virtual_machine is assigned to the Access List.
          - Check for duplicate entry. (Because of GFK)
        """
        #cleaned_data = super().clean()
        error_message = {}
        # access_list = self.cleaned_data.get("access_list")
        # interface = self.cleaned_data.get("interface")
        # vminterface = self.cleaned_data.get("vminterface")

        if error_message:
            raise forms.ValidationError(error_message)
        return self.cleaned_data

    def save(self, *args, **kwargs):
        # Set assigned object
        self.instance.assigned_object = self.cleaned_data.get(
            "interface",
        ) or self.cleaned_data.get("vminterface")
        return super().save(*args, **kwargs)


class ACLIngressRuleForm(NetBoxModelForm):
    """
    GUI form to add or edit Standard Access List.
    Requires an access_list, an index, and ACL rule type.
    See the clean function for logic on other field requirements.
    """

    access_list = DynamicModelChoiceField(
        queryset=AccessList.objects.all(),
        query_params={
            "type": ACLAssignmentDirectionChoices.DIRECTION_INGRESS,
        },
        help_text=mark_safe(
            "<b>*Note:</b> This field will only display Ingress ACLs.",
        ),
        label="Access List",
    )

    fieldsets = (
        ("Access List Details", ("access_list", "description", "tags")),
        ("Rule Definition", ("index", "action", "remark", "source_prefix", "destination_ports", "protocol")),
    )

    class Meta:
        model = ACLIngressRule
        fields = (
            "access_list",
            "index",
            "action",
            "remark",
            "source_prefix",
            "destination_ports", 
            "protocol",
            "tags",
            "description",
        )
        help_texts = {
            "index": help_text_acl_rule_index,
            "action": help_text_acl_action,
            "remark": mark_safe(
                "<b>*Note:</b> CANNOT be set if source prefix OR action is set.",
            ),
        }

    def clean(self):
        """
        Validates form inputs before submitting:
          - Check if action set to remark, but no remark set.
          - Check if action set to remark, but source_prefix set.
          - Check remark set, but action not set to remark.
        """
        #cleaned_data = super().clean()
        error_message = {}

        # No need to check for unique_together since there is no usage of GFK

        if self.cleaned_data.get("action") == "remark":
            # Check if action set to remark, but no remark set.
            if not self.cleaned_data.get("remark"):
                error_message["remark"] = [error_message_no_remark]
            # Check if action set to remark, but source_prefix set.
            if self.cleaned_data.get("source_prefix"):
                error_message["source_prefix"] = [
                    error_message_action_remark_source_prefix_set,
                ]
        # Check remark set, but action not set to remark.
        elif self.cleaned_data.get("remark"):
            error_message["remark"] = [error_message_remark_without_action_remark]

        if error_message:
            raise forms.ValidationError(error_message)
        return self.cleaned_data


class ACLEgressRuleForm(NetBoxModelForm):
    """
    GUI form to add or edit Extended Access List.
    Requires an access_list, an index, and ACL rule type.
    See the clean function for logic on other field requirements.
    """

    access_list = DynamicModelChoiceField(
        queryset=AccessList.objects.all(),
        query_params={
            "type": ACLAssignmentDirectionChoices.DIRECTION_EGRESS,
        },
        help_text=mark_safe(
            "<b>*Note:</b> This field will only display Extended ACLs.",
        ),
        label="Access List",
    )

    fieldsets = (
        ("Access List Details", ("access_list", "description", "tags")),
        (
            "Rule Definition",
            (
                "index",
                "action",
                "remark",
                "destination_prefix",
                "destination_ports",
                "protocol",
            ),
        ),
    )

    class Meta:
        model = ACLEgressRule
        fields = (
            "access_list",
            "index",
            "action",
            "remark",
            "destination_prefix",
            "destination_ports",
            "protocol",
            "tags",
            "description",
        )
        help_texts = {
            "action": help_text_acl_action,
            "destination_ports": help_text_acl_rule_logic,
            "index": help_text_acl_rule_index,
            "protocol": help_text_acl_rule_logic,
            "remark": mark_safe(
                "<b>*Note:</b> CANNOT be set if action is not set to remark.",
            ),
        }

    def clean(self):
        """
        Validates form inputs before submitting:
          - Check if action set to remark, but no remark set.
          - Check if action set to remark, but destination_prefix set.
          - Check if action set to remark, but destination_ports set.
          - Check if action set to remark, but destination_ports set.
          - Check if action set to remark, but protocol set.
          - Check remark set, but action not set to remark.
        """
        #cleaned_data = super().clean()
        error_message = {}

        # No need to check for unique_together since there is no usage of GFK

        if self.cleaned_data.get("action") == "remark":
            # Check if action set to remark, but no remark set.
            if not self.cleaned_data.get("remark"):
                error_message["remark"] = [error_message_no_remark]
            # Check if action set to remark, but destination_prefix set.
            if self.cleaned_data.get("destination_prefix"):
                error_message["destination_prefix"] = [
                    "Action is set to remark, Destination Prefix CANNOT be set.",
                ]
            # Check if action set to remark, but destination_ports set.
            if self.cleaned_data.get("destination_ports"):
                error_message["destination_ports"] = [
                    "Action is set to remark, Destination Ports CANNOT be set.",
                ]
            # Check if action set to remark, but protocol set.
            if self.cleaned_data.get("protocol"):
                error_message["protocol"] = [
                    "Action is set to remark, Protocol CANNOT be set.",
                ]
        # Check if action not set to remark, but remark set.
        elif self.cleaned_data.get("remark"):
            error_message["remark"] = [error_message_remark_without_action_remark]

        if error_message:
            raise forms.ValidationError(error_message)
        return self.cleaned_data
