"""
Define the django models for this plugin.
"""

from django.apps import apps
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel

from ..choices import ACLProtocolChoices, ACLRuleActionChoices, ACLTypeChoices
from .fw_rule_lists import FirewallRuleList

__all__ = (
    "FWRule",
    "FWIngressRule",
    "FWEgressRule",
)


class FWRule(NetBoxModel):
    fw_rule_list = models.ForeignKey(
        on_delete=models.CASCADE,
        to=FirewallRuleList,
        verbose_name="Firewall Rule List"
    )
    index = models.PositiveIntegerField()
    remark = models.CharField(
        max_length=500,
        blank=True,
    )
    description = models.CharField(
        max_length=500,
        blank=True,
    )
    destination_ports = ArrayField(
        base_field=models.PositiveIntegerField(),
        blank=True,
        null=True,
        verbose_name="Destination Ports",
    )
    protocol = models.CharField(
        blank=True,
        choices=ACLProtocolChoices,
        max_length=30,
    )

    clone_fields = ("fw_rule_list", "destination_ports")

    def __str__(self):
        return f"{self.access_list}: Rule {self.index}"

    @classmethod
    def get_prerequisite_models(cls):
        return [FirewallRuleList]

    class Meta:
        """
        Define the common model properties:
          - as an abstract model
          - ordering
          - unique together
        """

        abstract = True
        ordering = ["fw_rule_list", "index"]
        unique_together = ["fw_rule_list", "index"]


class FWIngressRule(FWRule):

    source_prefix = models.CharField(
        max_length=100,
        blank=True,
    )

    def get_absolute_url(self):
        """
        The method is a Django convention; although not strictly required,
        it conveniently returns the absolute URL for any particular object.
        """
        return reverse("plugins:netbox_acls:fwingressrule", args=[self.pk])

    @classmethod
    def get_prerequisite_models(cls):
        return [FirewallRuleList]

    class Meta(FWRule.Meta):
        """
        Define the model properties adding to or overriding the inherited class:
          - default_related_name for any FK relationships
          - verbose name (for displaying in the GUI)
          - verbose name plural (for displaying in the GUI)
        """
        default_related_name = "ingressrules"
        verbose_name = "FW Ingress Rule"
        verbose_name_plural = "FW Ingress Rules"


class FWEgressRule(FWRule):

    destination_prefix = models.CharField(
        max_length=100,
        blank=True,
    )

    def get_absolute_url(self):
        """
        The method is a Django convention; although not strictly required,
        it conveniently returns the absolute URL for any particular object.
        """
        return reverse("plugins:netbox_acls:fwegressrule", args=[self.pk])

    def get_protocol_color(self):
        return ACLProtocolChoices.colors.get(self.protocol)

    @classmethod
    def get_prerequisite_models(cls):
        return [FirewallRuleList]

    class Meta(FWRule.Meta):
        """
        Define the model properties adding to or overriding the inherited class:
          - default_related_name for any FK relationships
          - verbose name (for displaying in the GUI)
          - verbose name plural (for displaying in the GUI)
        """

        default_related_name = "egressrules"
        verbose_name = "FW Egress Rule"
        verbose_name_plural = "FW Egress Rules"
