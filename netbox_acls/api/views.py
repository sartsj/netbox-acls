"""
Create views to handle the API logic.
A view set is a single class that can handle the view, add, change,
and delete operations which each require dedicated views under the UI.
"""

from django.db.models import Count
from netbox.api.viewsets import NetBoxModelViewSet

from .. import filtersets, models
from .serializers import (
    AccessListSerializer,
    ACLExtendedRuleSerializer,
    ACLInterfaceAssignmentSerializer,
    ACLStandardRuleSerializer,
    FirewallRuleListSerializer,
    FWInterfaceAssignmentSerializer,
    FWIngressRuleSerializer,
    FWEgressRuleSerializer,
)

__all__ = [
    "AccessListViewSet",
    "ACLStandardRuleViewSet",
    "ACLInterfaceAssignmentViewSet",
    "ACLExtendedRuleViewSet",
    "FirewallRuleListViewSet",
    "FWInterfaceAssignmentViewSet",
    "FWIngressRuleViewSet",
    "FWEgressRuleViewSet",
]


class AccessListViewSet(NetBoxModelViewSet):
    """
    Defines the view set for the django AccessList model & associates it to a view.
    """

    queryset = (
        models.AccessList.objects.prefetch_related("tags")
        .annotate(
            rule_count=Count("aclextendedrules") + Count("aclstandardrules"),
        )
        .prefetch_related("tags")
    )
    serializer_class = AccessListSerializer
    filterset_class = filtersets.AccessListFilterSet


class ACLInterfaceAssignmentViewSet(NetBoxModelViewSet):
    """
    Defines the view set for the django ACLInterfaceAssignment model & associates it to a view.
    """

    queryset = models.ACLInterfaceAssignment.objects.prefetch_related(
        "access_list",
        "tags",
    )
    serializer_class = ACLInterfaceAssignmentSerializer
    filterset_class = filtersets.ACLInterfaceAssignmentFilterSet


class ACLStandardRuleViewSet(NetBoxModelViewSet):
    """
    Defines the view set for the django ACLStandardRule model & associates it to a view.
    """

    queryset = models.ACLStandardRule.objects.prefetch_related(
        "access_list",
        "tags",
    )
    serializer_class = ACLStandardRuleSerializer
    filterset_class = filtersets.ACLStandardRuleFilterSet


class ACLExtendedRuleViewSet(NetBoxModelViewSet):
    """
    Defines the view set for the django ACLExtendedRule model & associates it to a view.
    """

    queryset = models.ACLExtendedRule.objects.prefetch_related(
        "access_list",
        "tags",
    )
    serializer_class = ACLExtendedRuleSerializer
    filterset_class = filtersets.ACLExtendedRuleFilterSet


class FirewallRuleListViewSet(NetBoxModelViewSet):
    """
    Defines the view set for the django FirewallRuleList model & associates it to a view.
    """

    queryset = (
        models.FirewallRuleList.objects.prefetch_related("tags")
        .annotate(
            rule_count=Count("fwingressrules") + Count("fwegressrules"),
        )
        .prefetch_related("tags")
    )
    serializer_class = FirewallRuleListSerializer
    filterset_class = filtersets.FirewallRuleListFilterSet


class FWInterfaceAssignmentViewSet(NetBoxModelViewSet):
    """
    Defines the view set for the django FWInterfaceAssignment model & associates it to a view.
    """

    queryset = models.FWInterfaceAssignment.objects.prefetch_related(
        "fw_rule_list",
        "tags",
    )
    serializer_class = FWInterfaceAssignmentSerializer
    filterset_class = filtersets.FWInterfaceAssignmentFilterSet


class FWIngressRuleViewSet(NetBoxModelViewSet):
    """
    Defines the view set for the django FWIngressRule model & associates it to a view.
    """

    queryset = models.FWIngressRule.objects.prefetch_related(
        "fw_rule_list",
        "tags",
    )
    serializer_class = FWIngressRuleSerializer
    filterset_class = filtersets.FWIngressRuleFilterSet


class FWEgressRuleViewSet(NetBoxModelViewSet):
    """
    Defines the view set for the django FWEgressRule model & associates it to a view.
    """

    queryset = models.FWEgressRule.objects.prefetch_related(
        "fw_rule_list",
        "tags",
    )
    serializer_class = FWEgressRuleSerializer
    filterset_class = filtersets.FWEgressRuleFilterSet
