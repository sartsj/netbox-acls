"""
Define the django models for this plugin.
"""

from django.apps import apps
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel

from ..choices import ACLProtocolChoices, ACLAssignmentDirectionChoices
from .access_lists import AccessList

__all__ = (
    "ACLRule",
    "ACLIngressRule",
    "ACLEgressRule",
)


class ACLRule(NetBoxModel):
    """
    Abstract model for ACL Rules.
    Inherrited by both ACLIngressRule and ACLEgressRule.
    """

    access_list = models.ForeignKey(
        on_delete=models.CASCADE,
        to=AccessList,
        verbose_name="Access List",
        related_name="rules",
    )
    description = models.CharField(
        max_length=500,
        #blank=True,
    )
    destination_ports = ArrayField(
        base_field=models.PositiveIntegerField(),
        blank=True,
        null=True,
        verbose_name="Destination Ports",
    )
    protocol = models.CharField(
        #blank=True,
        #null=True,
        choices=ACLProtocolChoices,
        max_length=30,
    )

    clone_fields = ("access_list", "destination_ports", "protocol")

    def __str__(self):
        return f"{self.access_list} Rule "

    @classmethod
    def get_prerequisite_models(cls):
        return [AccessList]

    class Meta:
        """
        Define the common model properties:
          - as an abstract model
          - ordering
          - unique together
        """

        abstract = True
        ordering = ["access_list", "destination_ports", "protocol"]
        unique_together = ["access_list", "destination_ports", "protocol"]


class ACLIngressRule(ACLRule):
    """
    Inherits ACLRule.
    Add ACLIngressRule specific field: source_prefix
    """

    access_list = models.ForeignKey(
        on_delete=models.CASCADE,
        to=AccessList,
        verbose_name="Ingress Access List",
        limit_choices_to={"type": ACLAssignmentDirectionChoices.DIRECTION_INGRESS},
        related_name="aclingressrules",
    )
    source_prefix = models.CharField(
        max_length=100,
        #blank=True,
        #null=True,
    )

    def get_absolute_url(self):
        """
        The method is a Django convention; although not strictly required,
        it conveniently returns the absolute URL for any particular object.
        """
        return reverse("plugins:netbox_acls:aclingressrule", args=[self.pk])

    @classmethod
    def get_prerequisite_models(cls):
        return [AccessList]

    class Meta(ACLRule.Meta):
        """
        Define the model properties adding to or overriding the inherited class:
          - default_related_name for any FK relationships
          - verbose name (for displaying in the GUI)
          - verbose name plural (for displaying in the GUI)
        """

        verbose_name = "ACL Ingress Rule"
        verbose_name_plural = "ACL Ingress Rules"


class ACLEgressRule(ACLRule):
    """
    Inherits ACLRule.
    Add ACLEgressRule specific field: destination_prefix
    """

    access_list = models.ForeignKey(
        on_delete=models.CASCADE,
        to=AccessList,
        verbose_name="Egress Access List",
        limit_choices_to={"type": ACLAssignmentDirectionChoices.DIRECTION_EGRESS},
        related_name="aclegressrules",
    )
    destination_prefix = models.CharField(
        max_length=100,
        #blank=True,
        #null=True,
    )


    def get_absolute_url(self):
        """
        The method is a Django convention; although not strictly required,
        it conveniently returns the absolute URL for any particular object.
        """
        return reverse("plugins:netbox_acls:aclegressrule", args=[self.pk])

    def get_protocol_color(self):
        return ACLProtocolChoices.colors.get(self.protocol)

    @classmethod
    def get_prerequisite_models(cls):
        return [AccessList]

    class Meta(ACLRule.Meta):
        """
        Define the model properties adding to or overriding the inherited class:
          - default_related_name for any FK relationships
          - verbose name (for displaying in the GUI)
          - verbose name plural (for displaying in the GUI)
        """

        verbose_name = "ACL Egress Rule"
        verbose_name_plural = "ACL Egress Rules"
