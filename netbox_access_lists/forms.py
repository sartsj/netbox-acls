from django import forms

from extras.models import Tag
from ipam.models import Prefix
from netbox.forms import NetBoxModelForm, NetBoxModelFilterSetForm
from utilities.forms import CommentField, DynamicModelChoiceField, DynamicModelMultipleChoiceField, StaticSelectMultiple, TagFilterField
from .models import AccessList, AccessListExtendedRule, AccessListActionChoices, AccessListProtocolChoices, AccessListTypeChoices, AccessListStandardRule


class AccessListForm(NetBoxModelForm):
    comments = CommentField()
    tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False
    )

    class Meta:
        model = AccessList
        fields = ('name', 'device', 'type', 'default_action', 'comments', 'tags')


class AccessListFilterForm(NetBoxModelFilterSetForm):
    model = AccessList
    type = forms.MultipleChoiceField(
        choices=AccessListTypeChoices,
        required=False,
        widget=StaticSelectMultiple()
    )
    default_action = forms.MultipleChoiceField(
        choices=AccessListActionChoices,
        required=False,
        widget=StaticSelectMultiple()
    )
    tag = TagFilterField(model)


class AccessListStandardRuleForm(NetBoxModelForm):
    access_list = DynamicModelChoiceField(
        queryset=AccessList.objects.all(),
        query_params={
            'type': 'standard'
        }
    )
    tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False
    )
    source_prefix = DynamicModelChoiceField(
        queryset=Prefix.objects.all(),
        required=False
    )


    class Meta:
        model = AccessListStandardRule
        fields = (
            'access_list', 'index', 'remark', 'action', 'tags', 'source_prefix',
        )


class AccessListStandardRuleFilterForm(NetBoxModelFilterSetForm):
    model = AccessListStandardRule
    access_list = forms.ModelMultipleChoiceField(
        queryset=AccessList.objects.all(),
        required=False,
        widget=StaticSelectMultiple()
    )
    index = forms.IntegerField(
        required=False
    )
    tag = TagFilterField(model)
    action = forms.MultipleChoiceField(
        choices=AccessListActionChoices,
        required=False,
        widget=StaticSelectMultiple()
    )


class AccessListExtendedRuleForm(NetBoxModelForm):
    access_list = DynamicModelChoiceField(
        queryset=AccessList.objects.all(),
        query_params={
            'type': 'extended'
        }
    )
    tags = DynamicModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False
    )
    source_prefix = DynamicModelChoiceField(
        queryset=Prefix.objects.all(),
        required=False
    )
    destination_prefix = DynamicModelChoiceField(
        queryset=Prefix.objects.all(),
        required=False
    )


    class Meta:
        model = AccessListExtendedRule
        fields = (
            'access_list', 'index', 'remark', 'action', 'tags', 'source_prefix',
            'source_ports', 'destination_prefix', 'destination_ports', 'protocol'
        )


class AccessListExtendedRuleFilterForm(NetBoxModelFilterSetForm):
    model = AccessListExtendedRule
    access_list = forms.ModelMultipleChoiceField(
        queryset=AccessList.objects.all(),
        required=False,
        widget=StaticSelectMultiple()
    )
    index = forms.IntegerField(
        required=False
    )
    tag = TagFilterField(model)
    action = forms.MultipleChoiceField(
        choices=AccessListActionChoices,
        required=False,
        widget=StaticSelectMultiple()
    )
    protocol = forms.MultipleChoiceField(
        choices=AccessListProtocolChoices,
        required=False,
        widget=StaticSelectMultiple()
    )
