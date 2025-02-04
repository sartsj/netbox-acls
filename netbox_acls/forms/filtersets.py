"""
Defines each django model's GUI filter/search options.
"""

from dcim.models import Device, Interface, Region, Site, SiteGroup, VirtualChassis
from django import forms
from ipam.models import Prefix
from netbox.forms import NetBoxModelFilterSetForm
from utilities.forms.fields import (
    DynamicModelChoiceField,
    DynamicModelMultipleChoiceField,
    TagFilterField,
)
from utilities.forms.utils import add_blank_choice
from virtualization.models import VirtualMachine, VMInterface

from ..choices import (
    ACLAssignmentDirectionChoices,
    ACLProtocolChoices,
)
from ..models import (
    AccessList,
    ACLEgressRule,
    ACLInterfaceAssignment,
    ACLIngressRule,
)

__all__ = (
    "AccessListFilterForm",
    "ACLInterfaceAssignmentFilterForm",
    "ACLIngressRuleFilterForm",
    "ACLEgressRuleFilterForm",
)


class AccessListFilterForm(NetBoxModelFilterSetForm):
    """
    GUI filter form to search the django AccessList model.
    """

    model = AccessList
    region = DynamicModelChoiceField(
        queryset=Region.objects.all(),
        required=False,
    )
    site_group = DynamicModelChoiceField(
        queryset=SiteGroup.objects.all(),
        required=False,
        label="Site Group",
    )
    site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        required=False,
        query_params={"region_id": "$region", "group_id": "$site_group"},
    )
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        query_params={
            "region_id": "$region",
            "group_id": "$site_group",
            "site_id": "$site",
        },
        required=False,
    )
    virtual_machine = DynamicModelChoiceField(
        queryset=VirtualMachine.objects.all(),
        required=False,
    )
    virtual_chassis = DynamicModelChoiceField(
        queryset=VirtualChassis.objects.all(),
        required=False,
    )
    type = forms.ChoiceField(
        choices=add_blank_choice(ACLAssignmentDirectionChoices),
        required=False,
    )
    tag = TagFilterField(model)

    fieldsets = (
        (None, ("q", "tag")),
        (
            "Host Details",
            (
                "region",
                "site_group",
                "site",
                "device",
                "virtual_chassis",
                "virtual_machine",
            ),
        ),
        ("ACL Details", ("type",)),
    )


class ACLInterfaceAssignmentFilterForm(NetBoxModelFilterSetForm):
    """
    GUI filter form to search the django AccessList model.
    """

    model = ACLInterfaceAssignment
    region = DynamicModelChoiceField(
        queryset=Region.objects.all(),
        required=False,
    )
    site_group = DynamicModelChoiceField(
        queryset=SiteGroup.objects.all(),
        required=False,
        label="Site Group",
    )
    site = DynamicModelChoiceField(
        queryset=Site.objects.all(),
        required=False,
        query_params={"region_id": "$region", "group_id": "$site_group"},
    )
    device = DynamicModelChoiceField(
        queryset=Device.objects.all(),
        query_params={
            "region_id": "$region",
            "group_id": "$site_group",
            "site_id": "$site",
        },
        required=False,
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
        label="Virtual Machine",
    )
    vminterface = DynamicModelChoiceField(
        queryset=VMInterface.objects.all(),
        required=False,
        query_params={
            "virtual_machine_id": "$virtual_machine",
        },
        label="Interface",
    )
    access_list = DynamicModelChoiceField(
        queryset=AccessList.objects.all(),
        query_params={
            "assigned_object": "$device",
        },
        label="Access List",
    )
    tag = TagFilterField(model)

    # fieldsets = (
    #    (None, ('q', 'tag')),
    #    ('Host Details', ('region', 'site_group', 'site', 'device')),
    #    ('ACL Details', ('type')),
    # )


class ACLIngressRuleFilterForm(NetBoxModelFilterSetForm):
    """
    GUI filter form to search the django ACLIngressRule model.
    """

    model = ACLIngressRule
    tag = TagFilterField(model)
    access_list = DynamicModelMultipleChoiceField(
        queryset=AccessList.objects.all(),
        required=False,
    )
    source_prefix = DynamicModelMultipleChoiceField(
        queryset=Prefix.objects.all(),
        required=False,
        label="Source Prefix",
    )
    fieldsets = (
        (None, ("q", "tag")),
        ("Rule Details", ("access_list", "source_prefix")),
    )


class ACLEgressRuleFilterForm(NetBoxModelFilterSetForm):
    """
    GUI filter form to search the django ACLEgressRule model.
    """

    model = ACLEgressRule
    tag = TagFilterField(model)
    access_list = DynamicModelMultipleChoiceField(
        queryset=AccessList.objects.all(),
        required=False,
    )
    source_prefix = DynamicModelMultipleChoiceField(
        queryset=Prefix.objects.all(),
        required=False,
        label="Source Prefix",
    )
    destination_prefix = DynamicModelMultipleChoiceField(
        queryset=Prefix.objects.all(),
        required=False,
        label="Destination Prefix",
    )
    protocol = forms.ChoiceField(
        choices=add_blank_choice(ACLProtocolChoices),
        required=False,
    )

    fieldsets = (
        (None, ("q", "tag")),
        (
            "Rule Details",
            (
                "access_list",
                "destination_prefix",
                "protocol",
            ),
        ),
    )
