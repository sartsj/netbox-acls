import django_tables2 as tables

from netbox.tables import NetBoxTable, columns, ChoiceFieldColumn
from .models import AccessList, AccessListExtendedRule, AccessListStandardRule


class AccessListTable(NetBoxTable):
    name = tables.Column(
        linkify=True
    )
    device = tables.Column(
        linkify=True
    )
    type = ChoiceFieldColumn()
    default_action = ChoiceFieldColumn()
    rule_count = tables.Column(
        verbose_name='Rule Count'
    )
    tags = columns.TagColumn(
        url_name='plugins:netbox_access_lists:accesslist_list'
    )

    class Meta(NetBoxTable.Meta):
        model = AccessList
        fields = ('pk', 'id', 'name', 'device', 'type', 'rule_count', 'default_action', 'comments', 'actions', 'tags')
        default_columns = ('name', 'device', 'type', 'rule_count', 'default_action', 'tags')


class AccessListStandardRuleTable(NetBoxTable):
    access_list = tables.Column(
        linkify=True
    )
    index = tables.Column(
        linkify=True
    )
    action = ChoiceFieldColumn()
    tags = columns.TagColumn(
        url_name='plugins:netbox_access_lists:accessliststandardrule_list'
    )
    class Meta(NetBoxTable.Meta):
        model = AccessListStandardRule
        fields = (
            'pk', 'id', 'access_list', 'index', 'action', 'actions', 'remark', 'tags'
        )
        default_columns = (
            'access_list', 'index', 'action', 'actions', 'remark', 'tags'
        )


class AccessListExtendedRuleTable(NetBoxTable):
    access_list = tables.Column(
        linkify=True
    )
    index = tables.Column(
        linkify=True
    )
    action = ChoiceFieldColumn()
    tags = columns.TagColumn(
        url_name='plugins:netbox_access_lists:accesslistextendedrule_list'
    )
    protocol = ChoiceFieldColumn()

    class Meta(NetBoxTable.Meta):
        model = AccessListExtendedRule
        fields = (
            'pk', 'id', 'access_list', 'index', 'action', 'actions', 'remark', 'tags',
            'source_prefix', 'source_ports', 'destination_prefix', 'destination_ports', 'protocol'
        )
        default_columns = (
            'access_list', 'index', 'action', 'actions', 'remark', 'tags',
            'source_prefix', 'source_ports', 'destination_prefix', 'destination_ports', 'protocol'
        )
