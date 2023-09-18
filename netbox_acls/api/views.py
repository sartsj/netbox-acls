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
    ACLEgressRuleSerializer,
    ACLInterfaceAssignmentSerializer,
    ACLIngressRuleSerializer,
)

__all__ = [
    "AccessListViewSet",
    "ACLIngressRuleViewSet",
    "ACLInterfaceAssignmentViewSet",
    "ACLEgressRuleViewSet",
]


class AccessListViewSet(NetBoxModelViewSet):
    """
    Defines the view set for the django AccessList model & associates it to a view.
    """

    queryset = (
        models.AccessList.objects.prefetch_related("tags")
        .annotate(
            rule_count=Count("aclegressrules") + Count("aclingressrules"),
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


class ACLIngressRuleViewSet(NetBoxModelViewSet):
    """
    Defines the view set for the django ACLIngressRule model & associates it to a view.
    """

    queryset = models.ACLIngressRule.objects.prefetch_related(
        "access_list",
        "tags",
    )
    serializer_class = ACLIngressRuleSerializer
    filterset_class = filtersets.ACLIngressRuleFilterSet


class ACLEgressRuleViewSet(NetBoxModelViewSet):
    """
    Defines the view set for the django ACLEgressRule model & associates it to a view.
    """

    queryset = models.ACLEgressRule.objects.prefetch_related(
        "access_list",
        "tags",
    )
    serializer_class = ACLEgressRuleSerializer
    filterset_class = filtersets.ACLEgressRuleFilterSet
