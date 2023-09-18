"""
Filters enable users to request only a specific subset of objects matching a query;
when filtering the sites list by status or region, for instance.
"""
import django_filters
from dcim.models import DeviceRole, Interface
from netbox.filtersets import NetBoxModelFilterSet
from virtualization.models import VMInterface

from .models import AccessList, ACLEgressRule, ACLInterfaceAssignment, ACLIngressRule

__all__ = (
    "AccessListFilterSet",
    "ACLIngressRuleFilterSet",
    "ACLInterfaceAssignmentFilterSet",
    "ACLEgressRuleFilterSet",
)


class AccessListFilterSet(NetBoxModelFilterSet):
    """
    Define the filter set for the django model AccessList.
    """

    device_role = django_filters.ModelMultipleChoiceFilter(
        field_name="device_role__name",
        queryset=DeviceRole.objects.all(),
        to_field_name="name",
        label="Device Role (name)",
    )
    device_role_id = django_filters.ModelMultipleChoiceFilter(
        field_name="device_role",
        queryset=DeviceRole.objects.all(),
        label="Device Role (ID)",
    )

    class Meta:
        """
        Associates the django model AccessList & fields to the filter set.
        """

        model = AccessList
        fields = (
            "id",
            "name",
            "device_role",
            "device_role_id",
            "type",
            "default_action",
            "comments",
        )

    def search(self, queryset, name, value):
        """
        Override the default search behavior for the django model.
        """
        return queryset.filter(description__icontains=value)


class ACLInterfaceAssignmentFilterSet(NetBoxModelFilterSet):
    """
    Define the filter set for the django model ACLInterfaceAssignment.
    """

    interface = django_filters.ModelMultipleChoiceFilter(
        field_name="interface__name",
        queryset=Interface.objects.all(),
        to_field_name="name",
        label="Interface (name)",
    )
    interface_id = django_filters.ModelMultipleChoiceFilter(
        field_name="interface",
        queryset=Interface.objects.all(),
        label="Interface (ID)",
    )
    vminterface = django_filters.ModelMultipleChoiceFilter(
        field_name="vminterface__name",
        queryset=VMInterface.objects.all(),
        to_field_name="name",
        label="VM Interface (name)",
    )
    vminterface_id = django_filters.ModelMultipleChoiceFilter(
        field_name="vminterface",
        queryset=VMInterface.objects.all(),
        label="VM Interface (ID)",
    )

    class Meta:
        """
        Associates the django model ACLInterfaceAssignment & fields to the filter set.
        """

        model = ACLInterfaceAssignment
        fields = (
            "id",
            "access_list",
            "interface",
            "interface_id",
            "vminterface",
            "vminterface_id",
        )

    def search(self, queryset, name, value):
        """
        Override the default search behavior for the django model.
        """
        return queryset.filter(description__icontains=value)


class ACLIngressRuleFilterSet(NetBoxModelFilterSet):
    """
    Define the filter set for the django model ACLIngressRule.
    """

    class Meta:
        """
        Associates the django model ACLIngressRule & fields to the filter set.
        """

        model = ACLIngressRule
        fields = ("id", "access_list", "index", "action", "source_prefix", "protocol")

    def search(self, queryset, name, value):
        """
        Override the default search behavior for the django model.
        """
        return queryset.filter(description__icontains=value)


class ACLEgressRuleFilterSet(NetBoxModelFilterSet):
    """
    Define the filter set for the django model ACLEgressRule.
    """

    class Meta:
        """
        Associates the django model ACLEgressRule & fields to the filter set.
        """

        model = ACLEgressRule
        fields = ("id", "access_list", "index", "action", "destination_prefix", "protocol")

    def search(self, queryset, name, value):
        """
        Override the default search behavior for the django model.
        """
        return queryset.filter(description__icontains=value)
