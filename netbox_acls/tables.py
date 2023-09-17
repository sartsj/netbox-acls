"""
Define the object lists / table view for each of the plugin models.
"""

import django_tables2 as tables
from netbox.tables import ChoiceFieldColumn, NetBoxTable, columns

from .models import AccessList, ACLExtendedRule, ACLInterfaceAssignment, ACLStandardRule, FirewallRuleList, FWInterfaceAssignment, FWIngressRule, FWEgressRule

__all__ = (
    "AccessListTable",
    "ACLInterfaceAssignmentTable",
    "ACLStandardRuleTable",
    "ACLExtendedRuleTable",
    "FirewallRuleListTable",
    "FWInterfaceAssignmentTable",
    "FWIngressRuleTable",
    "FWEgressRuleTable",
)


COL_HOST_ASSIGNMENT = """
    {% if record.assigned_object.device %}
    <a href="{{ record.assigned_object.device.get_absolute_url }}">{{ record.assigned_object.device|placeholder }}</a>
    {% else %}
    <a href="{{ record.assigned_object.virtual_machine.get_absolute_url }}">{{ record.assigned_object.virtual_machine|placeholder }}</a>
    {% endif %}
 """


class AccessListTable(NetBoxTable):
    """
    Defines the table view for the AccessList model.
    """

    pk = columns.ToggleColumn()
    id = tables.Column(
        linkify=True,
    )
    assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name="Assigned Host",
    )
    name = tables.Column(
        linkify=True,
    )
    device = tables.Column(
        linkify=True,
    )
    type = ChoiceFieldColumn()
    default_action = ChoiceFieldColumn()
    rule_count = tables.Column(
        verbose_name="Rule Count",
    )
    tags = columns.TagColumn(
        url_name="plugins:netbox_acls:accesslist_list",
    )

    class Meta(NetBoxTable.Meta):
        model = AccessList
        fields = (
            "pk",
            "id",
            "name",
            "assigned_object",
            "type",
            "rule_count",
            "default_action",
            "comments",
            "actions",
            "tags",
        )
        default_columns = (
            "name",
            "assigned_object",
            "type",
            "rule_count",
            "default_action",
            "tags",
        )


class ACLInterfaceAssignmentTable(NetBoxTable):
    """
    Defines the table view for the AccessList model.
    """

    pk = columns.ToggleColumn()
    id = tables.Column(
        linkify=True,
    )
    access_list = tables.Column(
        linkify=True,
    )
    direction = ChoiceFieldColumn()
    host = tables.TemplateColumn(
        template_code=COL_HOST_ASSIGNMENT,
    )
    assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name="Assigned Interface",
    )
    tags = columns.TagColumn(
        url_name="plugins:netbox_acls:aclinterfaceassignment_list",
    )

    class Meta(NetBoxTable.Meta):
        model = ACLInterfaceAssignment
        fields = (
            "pk",
            "id",
            "access_list",
            "direction",
            "host",
            "assigned_object",
            "tags",
        )
        default_columns = (
            "id",
            "access_list",
            "direction",
            "host",
            "assigned_object",
            "tags",
        )


class ACLStandardRuleTable(NetBoxTable):
    """
    Defines the table view for the ACLStandardRule model.
    """

    access_list = tables.Column(
        linkify=True,
    )
    index = tables.Column(
        linkify=True,
    )
    action = ChoiceFieldColumn()
    tags = columns.TagColumn(
        url_name="plugins:netbox_acls:aclstandardrule_list",
    )

    class Meta(NetBoxTable.Meta):
        model = ACLStandardRule
        fields = (
            "pk",
            "id",
            "access_list",
            "index",
            "action",
            "actions",
            "remark",
            "tags",
            "description",
            "source_prefix",
        )
        default_columns = (
            "access_list",
            "index",
            "action",
            "actions",
            "remark",
            "source_prefix",
            "tags",
        )


class ACLExtendedRuleTable(NetBoxTable):
    """
    Defines the table view for the ACLExtendedRule model.
    """

    access_list = tables.Column(
        linkify=True,
    )
    index = tables.Column(
        linkify=True,
    )
    action = ChoiceFieldColumn()
    tags = columns.TagColumn(
        url_name="plugins:netbox_acls:aclextendedrule_list",
    )
    protocol = ChoiceFieldColumn()

    class Meta(NetBoxTable.Meta):
        model = ACLExtendedRule
        fields = (
            "pk",
            "id",
            "access_list",
            "index",
            "action",
            "actions",
            "remark",
            "tags",
            "description",
            "source_prefix",
            "source_ports",
            "destination_prefix",
            "destination_ports",
            "protocol",
        )
        default_columns = (
            "access_list",
            "index",
            "action",
            "actions",
            "remark",
            "tags",
            "source_prefix",
            "source_ports",
            "destination_prefix",
            "destination_ports",
            "protocol",
        )


class FirewallRuleListTable(NetBoxTable):
    """
    Defines the table view for the FirewallRuleList model.
    """

    pk = columns.ToggleColumn()
    id = tables.Column(
        linkify=True,
    )
    assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name="Assigned Device Role",
    )
    name = tables.Column(
        linkify=True,
    )
    device_role = tables.Column(
        linkify=True,
    )
    rule_count = tables.Column(
        verbose_name="Rule Count",
    )
    tags = columns.TagColumn(
        url_name="plugins:netbox_acls:fwrulelist_list",
    )

    class Meta(NetBoxTable.Meta):
        model = FirewallRuleList
        fields = (
            "pk",
            "id",
            "name",
            "assigned_object",
            "rule_count",
            "comments",
            "tags",
        )
        default_columns = (
            "name",
            "assigned_object",
            "rule_count",
            "tags",
        )


class FWInterfaceAssignmentTable(NetBoxTable):
    """
    Defines the table view for the FWInterfaceAssignment model.
    """

    pk = columns.ToggleColumn()
    id = tables.Column(
        linkify=True,
    )
    fw_rule_list = tables.Column(
        linkify=True,
    )
    direction = ChoiceFieldColumn()
    assigned_object = tables.Column(
        linkify=True,
        orderable=False,
        verbose_name="Assigned Interface",
    )
    tags = columns.TagColumn(
        url_name="plugins:netbox_acls:fwinterfaceassignment_list",
    )

    class Meta(NetBoxTable.Meta):
        model = ACLInterfaceAssignment
        fields = (
            "pk",
            "id",
            "fw_rule_list",
            "assigned_object",
            "tags",
        )
        default_columns = (
            "id",
            "fw_rule_list",
            "assigned_object",
            "tags",
        )


class FWIngressRuleTable(NetBoxTable):
    """
    Defines the table view for the FWIngressRule model.
    """

    fw_rule_list = tables.Column(
        linkify=True,
    )
    index = tables.Column(
        linkify=True,
    )
    tags = columns.TagColumn(
        url_name="plugins:netbox_acls:fwingressrule_list",
    )
    protocol = ChoiceFieldColumn()

    class Meta(NetBoxTable.Meta):
        model = FWIngressRule
        fields = (
            "pk",
            "id",
            "fw_rule_list",
            "index",
            "tags",
            "description",
            "source_prefix",
            "destination_ports",
            "protocol",
        )
        default_columns = (
            "fw_rule_list",
            "index",
            "source_prefix",
            "destination_ports",
            "protocol",
            "tags",
        )


class FWEgressRuleTable(NetBoxTable):
    """
    Defines the table view for the FWEgressRule model.
    """

    fw_rule_list = tables.Column(
        linkify=True,
    )
    index = tables.Column(
        linkify=True,
    )
    tags = columns.TagColumn(
        url_name="plugins:netbox_acls:fwegressrule_list",
    )
    protocol = ChoiceFieldColumn()

    class Meta(NetBoxTable.Meta):
        model = FWEgressRule
        fields = (
            "pk",
            "id",
            "fw_rule_list",
            "index",
            "tags",
            "description",
            "destination_prefix",
            "destination_ports",
            "protocol",
        )
        default_columns = (
            "fw_rule_list",
            "index",
            "tags",
            "destination_prefix",
            "destination_ports",
            "protocol",
        )
