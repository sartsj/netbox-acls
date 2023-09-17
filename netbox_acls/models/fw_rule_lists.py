"""
Define the django models for this plugin.
"""

from dcim.models import Interface, DeviceRole
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from netbox.models import NetBoxModel
from virtualization.models import VMInterface

#from ..choices import ACLActionChoices, ACLAssignmentDirectionChoices, ACLTypeChoices
from ..constants import ACL_INTERFACE_ASSIGNMENT_MODELS

__all__ = (
    "FirewallRuleList",
    "FWInterfaceAssignment",
)


alphanumeric_plus = RegexValidator(
    r"^[a-zA-Z0-9-_]+$",
    "Only alphanumeric, hyphens, and underscores characters are allowed.",
)


class FirewallRuleList(NetBoxModel):
    """
    Model defintion for Access Lists.
    """

    name = models.CharField(
        max_length=500,
        validators=[alphanumeric_plus],
    )
    assigned_object_type = models.ForeignKey(
        to=ContentType,
        limit_choices_to=models.Q(app_label="dcim", model="device_role"),
        on_delete=models.PROTECT,
    )
    assigned_object_id = models.PositiveBigIntegerField()
    assigned_object = GenericForeignKey(
        ct_field="assigned_object_type",
        fk_field="assigned_object_id",
    )
    comments = models.TextField(
        blank=True,
    )
    clone_fields = ()

    class Meta:
        unique_together = ["assigned_object_type", "assigned_object_id", "name"]
        ordering = ["assigned_object_type", "assigned_object_id", "name"]
        verbose_name = "Firewall Rule List"
        verbose_name_plural = "Firewall Rule Lists"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        The method is a Django convention; although not strictly required,
        it conveniently returns the absolute URL for any particular object.
        """
        return reverse("plugins:netbox_acls:fwrulelist", args=[self.pk])


class FWInterfaceAssignment(NetBoxModel):
    """
    Model defintion for Access Lists associations with other Host interfaces:
      - VM interfaces
      - device interface
      - tbd on more
    """

    fw_rule_list = models.ForeignKey(
        on_delete=models.CASCADE,
        to=FirewallRuleList,
        verbose_name="FW Rule List",
    )
    assigned_object_type = models.ForeignKey(
        to=ContentType,
        limit_choices_to=ACL_INTERFACE_ASSIGNMENT_MODELS,
        on_delete=models.PROTECT,
    )
    assigned_object_id = models.PositiveBigIntegerField()
    assigned_object = GenericForeignKey(
        ct_field="assigned_object_type",
        fk_field="assigned_object_id",
    )
    comments = models.TextField(
        blank=True,
    )

    clone_fields = ("fw_rule_list")

    class Meta:
        unique_together = [
            "fw_rule_list",
            "assigned_object_type",
            "assigned_object_id",
        ]
        ordering = [
            "assigned_object_type",
            "assigned_object_id",
            "fw_rule_list",
            "interface",
        ]
        verbose_name = "FW Interface Assignment"
        verbose_name_plural = "FW Interface Assignments"

    def get_absolute_url(self):
        """
        The method is a Django convention; although not strictly required,
        it conveniently returns the absolute URL for any particular object.
        """
        return reverse(
            "plugins:netbox_acls:fwinterfaceassignment",
            args=[self.pk],
        )

    @classmethod
    def get_prerequisite_models(cls):
        return [FirewallRuleList]


GenericRelation(
    to=FWInterfaceAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="interface",
).contribute_to_class(Interface, "fwrulelistassignments")

GenericRelation(
    to=FWInterfaceAssignment,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="vminterface",
).contribute_to_class(VMInterface, "fwrulelistassignments")

GenericRelation(
    to=FirewallRuleList,
    content_type_field="assigned_object_type",
    object_id_field="assigned_object_id",
    related_query_name="devicerole",
).contribute_to_class(DeviceRole, "fwrulelists")
