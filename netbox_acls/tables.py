"""
Define the object lists / table view for each of the plugin models.
"""

import django_tables2 as tables
from netbox.tables import ChoiceFieldColumn, NetBoxTable, columns

from .models import AccessList, ACLEgressRule, ACLInterfaceAssignment, ACLIngressRule

__all__ = (
    "AccessListTable",
    "ACLInterfaceAssignmentTable",
    "ACLIngressRuleTable",
    "ACLEgressRuleTable",
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
        verbose_name="Assigned Role",
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
            "host",
            "assigned_object",
            "tags",
        )
        default_columns = (
            "id",
            "access_list",
            "host",
            "assigned_object",
            "tags",
        )


class ACLIngressRuleTable(NetBoxTable):
    """
    Defines the table view for the ACLIngressRule model.
    """

    access_list = tables.Column(
        linkify=True,
    )
    index = tables.Column(
        linkify=True,
    )
    action = ChoiceFieldColumn()
    tags = columns.TagColumn(
        url_name="plugins:netbox_acls:aclingressrule_list",
    )

    class Meta(NetBoxTable.Meta):
        model = ACLIngressRule
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


class ACLEgressRuleTable(NetBoxTable):
    """
    Defines the table view for the ACLEgressRule model.
    """

    access_list = tables.Column(
        linkify=True,
    )
    index = tables.Column(
        linkify=True,
    )
    action = ChoiceFieldColumn()
    tags = columns.TagColumn(
        url_name="plugins:netbox_acls:aclegressrule_list",
    )
    protocol = ChoiceFieldColumn()

    class Meta(NetBoxTable.Meta):
        model = ACLEgressRule
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
