"""
Defines the business logic for the plugin.
Specifically, all the various interactions with a client.
"""

from dcim.models import Device, Interface, VirtualChassis, DeviceRole
from django.db.models import Count
from netbox.views import generic
from utilities.views import ViewTab, register_model_view
from virtualization.models import VirtualMachine, VMInterface

from . import choices, filtersets, forms, models, tables

__all__ = (
    "AccessListView",
    "AccessListListView",
    "AccessListEditView",
    "AccessListDeleteView",
    "AccessListBulkDeleteView",
    "ACLInterfaceAssignmentView",
    "ACLInterfaceAssignmentListView",
    "ACLInterfaceAssignmentEditView",
    "ACLInterfaceAssignmentDeleteView",
    "ACLInterfaceAssignmentBulkDeleteView",
    "ACLStandardRuleView",
    "ACLStandardRuleListView",
    "ACLStandardRuleEditView",
    "ACLStandardRuleDeleteView",
    "ACLStandardRuleBulkDeleteView",
    "ACLExtendedRuleView",
    "ACLExtendedRuleListView",
    "ACLExtendedRuleEditView",
    "ACLExtendedRuleDeleteView",
    "ACLExtendedRuleBulkDeleteView",
    "FirewallRuleListView",
    "FirewallRuleListListView",
    "FirewallRuleListEditView",
    "FirewallRuleListDeleteView",
    "FirewallRuleListBulkDeleteView",
    "FWInterfaceAssignmentView",
    "FWInterfaceAssignmentListView",
    "FWInterfaceAssignmentEditView",
    "FWInterfaceAssignmentDeleteView",
    "FWInterfaceAssignmentBulkDeleteView",
    "FWIngressRuleView",
    "FWIngressRuleListView",
    "FWIngressRuleEditView",
    "FWIngressRuleDeleteView",
    "FWIngressRuleBulkDeleteView",
    "FWEgressRuleView",
    "FWEgressRuleListView",
    "FWEgressRuleEditView",
    "FWEgressRuleDeleteView",
    "FWEgressRuleBulkDeleteView",
)


#
# AccessList views
#


@register_model_view(models.AccessList)
class AccessListView(generic.ObjectView):
    """
    Defines the view for the AccessLists django model.
    """

    queryset = models.AccessList.objects.prefetch_related("tags")

    def get_extra_context(self, request, instance):
        """
        Depending on the Access List type, the list view will return
        the required ACL Rule using the previous defined tables in tables.py.
        """

        if instance.type == choices.ACLTypeChoices.TYPE_EXTENDED:
            table = tables.ACLExtendedRuleTable(instance.aclextendedrules.all())
        elif instance.type == choices.ACLTypeChoices.TYPE_STANDARD:
            table = tables.ACLStandardRuleTable(instance.aclstandardrules.all())
        else:
            table = None

        if table:
            table.columns.hide("access_list")
            table.configure(request)

            return {
                "rules_table": table,
            }
        return {}


class AccessListListView(generic.ObjectListView):
    """
    Defines the list view for the AccessLists django model.
    """

    queryset = models.AccessList.objects.annotate(
        rule_count=Count("aclextendedrules") + Count("aclstandardrules"),
    ).prefetch_related("tags")
    table = tables.AccessListTable
    filterset = filtersets.AccessListFilterSet
    filterset_form = forms.AccessListFilterForm


@register_model_view(models.AccessList, "edit")
class AccessListEditView(generic.ObjectEditView):
    """
    Defines the edit view for the AccessLists django model.
    """

    queryset = models.AccessList.objects.prefetch_related("tags")
    form = forms.AccessListForm
    template_name = "netbox_acls/accesslist_edit.html"


@register_model_view(models.AccessList, "delete")
class AccessListDeleteView(generic.ObjectDeleteView):
    """
    Defines delete view for the AccessLists django model.
    """

    queryset = models.AccessList.objects.prefetch_related("tags")


class AccessListBulkDeleteView(generic.BulkDeleteView):
    queryset = models.AccessList.objects.prefetch_related("tags")
    filterset = filtersets.AccessListFilterSet
    table = tables.AccessListTable


class AccessListChildView(generic.ObjectChildrenView):
    """
    Defines the child view for the AccessLists model.
    """

    child_model = models.AccessList
    table = tables.AccessListTable
    filterset = filtersets.AccessListFilterSet
    template_name = "inc/view_tab.html"

    def get_extra_context(self, request, instance):
        return {
            "table_config": self.table.__name__,
            "model_type": self.queryset.model._meta.verbose_name.replace(" ", "_"),
            "add_url": "plugins:netbox_acls:accesslist_add",
        }

    def prep_table_data(self, request, queryset, parent):
        return queryset.annotate(
            rule_count=Count("aclextendedrules") + Count("aclstandardrules"),
        )


@register_model_view(Device, "access_lists")
class DeviceAccessListView(AccessListChildView):
    queryset = Device.objects.prefetch_related("tags")
    tab = ViewTab(
        label="Access Lists",
        badge=lambda obj: models.AccessList.objects.filter(device=obj).count(),
        permission="netbox_acls.view_accesslist",
    )

    def get_children(self, request, parent):
        return self.child_model.objects.restrict(request.user, "view").filter(
            device=parent,
        )


@register_model_view(VirtualChassis, "access_lists")
class VirtualChassisAccessListView(AccessListChildView):
    queryset = VirtualChassis.objects.prefetch_related("tags")
    tab = ViewTab(
        label="Access Lists",
        badge=lambda obj: models.AccessList.objects.filter(virtual_chassis=obj).count(),
        permission="netbox_acls.view_accesslist",
    )

    def get_children(self, request, parent):
        return self.child_model.objects.restrict(request.user, "view").filter(
            virtual_chassis=parent,
        )


@register_model_view(VirtualMachine, "access_lists")
class VirtualMachineAccessListView(AccessListChildView):
    queryset = VirtualMachine.objects.prefetch_related("tags")
    tab = ViewTab(
        label="Access Lists",
        badge=lambda obj: models.AccessList.objects.filter(virtual_machine=obj).count(),
        permission="netbox_acls.view_accesslist",
    )

    def get_children(self, request, parent):
        return self.child_model.objects.restrict(request.user, "view").filter(
            virtual_machine=parent,
        )


#
# ACLInterfaceAssignment views
#


@register_model_view(models.ACLInterfaceAssignment)
class ACLInterfaceAssignmentView(generic.ObjectView):
    """
    Defines the view for the ACLInterfaceAssignments django model.
    """

    queryset = models.ACLInterfaceAssignment.objects.prefetch_related(
        "access_list",
        "tags",
    )


class ACLInterfaceAssignmentListView(generic.ObjectListView):
    """
    Defines the list view for the ACLInterfaceAssignments django model.
    """

    queryset = models.ACLInterfaceAssignment.objects.prefetch_related(
        "access_list",
        "tags",
    )
    table = tables.ACLInterfaceAssignmentTable
    filterset = filtersets.ACLInterfaceAssignmentFilterSet
    filterset_form = forms.ACLInterfaceAssignmentFilterForm


@register_model_view(models.ACLInterfaceAssignment, "edit")
class ACLInterfaceAssignmentEditView(generic.ObjectEditView):
    """
    Defines the edit view for the ACLInterfaceAssignments django model.
    """

    queryset = models.ACLInterfaceAssignment.objects.prefetch_related(
        "access_list",
        "tags",
    )
    form = forms.ACLInterfaceAssignmentForm
    template_name = "netbox_acls/aclinterfaceassignment_edit.html"

    def get_extra_addanother_params(self, request):
        """
        Returns a dictionary of additional parameters to be passed to the "Add Another" button.
        """

        return {
            "access_list": request.GET.get("access_list") or request.POST.get("access_list"),
            "direction": request.GET.get("direction") or request.POST.get("direction"),
        }


@register_model_view(models.ACLInterfaceAssignment, "delete")
class ACLInterfaceAssignmentDeleteView(generic.ObjectDeleteView):
    """
    Defines delete view for the ACLInterfaceAssignments django model.
    """

    queryset = models.ACLInterfaceAssignment.objects.prefetch_related(
        "access_list",
        "tags",
    )


class ACLInterfaceAssignmentBulkDeleteView(generic.BulkDeleteView):
    queryset = models.ACLInterfaceAssignment.objects.prefetch_related(
        "access_list",
        "tags",
    )
    filterset = filtersets.ACLInterfaceAssignmentFilterSet
    table = tables.ACLInterfaceAssignmentTable


class ACLInterfaceAssignmentChildView(generic.ObjectChildrenView):
    """
    Defines the child view for the ACLInterfaceAssignments model.
    """

    child_model = models.ACLInterfaceAssignment
    table = tables.ACLInterfaceAssignmentTable
    filterset = filtersets.ACLInterfaceAssignmentFilterSet
    template_name = "inc/view_tab.html"

    def get_extra_context(self, request, instance):
        return {
            "table_config": self.table.__name__,
            "model_type": self.queryset.model._meta.verbose_name.replace(" ", "_"),
            "add_url": "plugins:netbox_acls:aclinterfaceassignment_add",
        }


@register_model_view(Interface, "acl_interface_assignments")
class InterfaceACLInterfaceAssignmentView(ACLInterfaceAssignmentChildView):
    queryset = Interface.objects.prefetch_related("device", "tags")
    tab = ViewTab(
        label="ACL Interface Assignments",
        badge=lambda obj: models.ACLInterfaceAssignment.objects.filter(
            interface=obj,
        ).count(),
        permission="netbox_acls.view_aclinterfaceassignment",
    )

    def get_children(self, request, parent):
        return self.child_model.objects.restrict(request.user, "view").filter(
            interface=parent,
        )


@register_model_view(VMInterface, "acl_interface_assignments")
class VirtualMachineInterfaceACLInterfaceAssignmentView(
    ACLInterfaceAssignmentChildView,
):
    queryset = VMInterface.objects.prefetch_related("virtual_machine", "tags")
    tab = ViewTab(
        label="ACL Interface Assignments",
        badge=lambda obj: models.ACLInterfaceAssignment.objects.filter(
            vminterface=obj,
        ).count(),
        permission="netbox_acls.view_aclinterfaceassignment",
    )

    def get_children(self, request, parent):
        return self.child_model.objects.restrict(request.user, "view").filter(
            vminterface=parent,
        )


#
# ACLStandardRule views
#


@register_model_view(models.ACLStandardRule)
class ACLStandardRuleView(generic.ObjectView):
    """
    Defines the view for the ACLStandardRule django model.
    """

    queryset = models.ACLStandardRule.objects.prefetch_related(
        "access_list",
        "tags",
    )


class ACLStandardRuleListView(generic.ObjectListView):
    """
    Defines the list view for the ACLStandardRule django model.
    """

    queryset = models.ACLStandardRule.objects.prefetch_related(
        "access_list",
        "tags",
    )
    table = tables.ACLStandardRuleTable
    filterset = filtersets.ACLStandardRuleFilterSet
    filterset_form = forms.ACLStandardRuleFilterForm


@register_model_view(models.ACLStandardRule, "edit")
class ACLStandardRuleEditView(generic.ObjectEditView):
    """
    Defines the edit view for the ACLStandardRule django model.
    """

    queryset = models.ACLStandardRule.objects.prefetch_related(
        "access_list",
        "tags",
    )
    form = forms.ACLStandardRuleForm

    def get_extra_addanother_params(self, request):
        """
        Returns a dictionary of additional parameters to be passed to the "Add Another" button.
        """

        return {
            "access_list": request.GET.get("access_list") or request.POST.get("access_list"),
        }


@register_model_view(models.ACLStandardRule, "delete")
class ACLStandardRuleDeleteView(generic.ObjectDeleteView):
    """
    Defines delete view for the ACLStandardRules django model.
    """

    queryset = models.ACLStandardRule.objects.prefetch_related(
        "access_list",
        "tags",
    )


class ACLStandardRuleBulkDeleteView(generic.BulkDeleteView):
    queryset = models.ACLStandardRule.objects.prefetch_related(
        "access_list",
        "tags",
    )
    filterset = filtersets.ACLStandardRuleFilterSet
    table = tables.ACLStandardRuleTable


#
# ACLExtendedRule views
#


@register_model_view(models.ACLExtendedRule)
class ACLExtendedRuleView(generic.ObjectView):
    """
    Defines the view for the ACLExtendedRule django model.
    """

    queryset = models.ACLExtendedRule.objects.prefetch_related(
        "access_list",
        "tags",
    )


class ACLExtendedRuleListView(generic.ObjectListView):
    """
    Defines the list view for the ACLExtendedRule django model.
    """

    queryset = models.ACLExtendedRule.objects.prefetch_related(
        "access_list",
        "tags",
    )
    table = tables.ACLExtendedRuleTable
    filterset = filtersets.ACLExtendedRuleFilterSet
    filterset_form = forms.ACLExtendedRuleFilterForm


@register_model_view(models.ACLExtendedRule, "edit")
class ACLExtendedRuleEditView(generic.ObjectEditView):
    """
    Defines the edit view for the ACLExtendedRule django model.
    """

    queryset = models.ACLExtendedRule.objects.prefetch_related(
        "access_list",
        "tags",
    )
    form = forms.ACLExtendedRuleForm

    def get_extra_addanother_params(self, request):
        """
        Returns a dictionary of additional parameters to be passed to the "Add Another" button.
        """

        return {
            "access_list": request.GET.get("access_list") or request.POST.get("access_list"),
        }


@register_model_view(models.ACLExtendedRule, "delete")
class ACLExtendedRuleDeleteView(generic.ObjectDeleteView):
    """
    Defines delete view for the ACLExtendedRules django model.
    """

    queryset = models.ACLExtendedRule.objects.prefetch_related(
        "access_list",
        "tags",
    )


class ACLExtendedRuleBulkDeleteView(generic.BulkDeleteView):
    queryset = models.ACLExtendedRule.objects.prefetch_related(
        "access_list",
        "tags",
    )
    filterset = filtersets.ACLExtendedRuleFilterSet
    table = tables.ACLExtendedRuleTable


#
# FirewallRuleList views
#


@register_model_view(models.FirewallRuleList)
class FirewallRuleListView(generic.ObjectView):
    """
    Defines the view for the FirewallRuleList django model.
    """

    queryset = models.FirewallRuleList.objects.prefetch_related("tags")

    def get_extra_context(self, request, instance):
        """
        Depending on the Access List type, the list view will return
        the required ACL Rule using the previous defined tables in tables.py.
        """

        table_ingress = tables.FWIngressRuleTable(instance.fwingressrules.all())
        table_egress = tables.FWIngressRuleTable(instance.fwegressrules.all())

        if table_ingress and table_egress:
            table_ingress.columns.hide("fw_rule_list")
            table_ingress.configure(request)

            table_egress.columns.hide("fw_rule_list")
            table_egress.configure(request)

            return {
                "ingress_table": table_ingress,
                "egress_table": table_egress,
            }
        
        return {}


class FirewallRuleListListView(generic.ObjectListView):
    """
    Defines the list view for the FirewallRuleList django model.
    """

    queryset = models.FirewallRuleList.objects.annotate(
        rule_count=Count("fwingressrules") + Count("fwegressrules"),
    ).prefetch_related("tags")
    table = tables.FirewallRuleListTable
    filterset = filtersets.FirewallRuleListFilterSet
    filterset_form = forms.FirewallRuleListFilterForm


@register_model_view(models.FirewallRuleList, "edit")
class FirewallRuleListEditView(generic.ObjectEditView):
    """
    Defines the edit view for the FirewallRuleList django model.
    """

    queryset = models.FirewallRuleList.objects.prefetch_related("tags")
    form = forms.FirewallRuleListForm
    template_name = "netbox_acls/fwrulelist_edit.html"


@register_model_view(models.FirewallRuleList, "delete")
class FirewallRuleListDeleteView(generic.ObjectDeleteView):
    """
    Defines delete view for the FirewallRuleList django model.
    """

    queryset = models.FirewallRuleList.objects.prefetch_related("tags")


class FirewallRuleListBulkDeleteView(generic.BulkDeleteView):
    queryset = models.FirewallRuleList.objects.prefetch_related("tags")
    filterset = filtersets.FirewallRuleListFilterSet
    table = tables.FirewallRuleListTable


class FirewallRuleListChildView(generic.ObjectChildrenView):
    """
    Defines the child view for the FirewallRuleList model.
    """

    child_model = models.FirewallRuleList
    table = tables.FirewallRuleListTable
    filterset = filtersets.FirewallRuleListFilterSet
    template_name = "inc/view_tab.html"

    def get_extra_context(self, request, instance):
        return {
            "table_config": self.table.__name__,
            "model_type": self.queryset.model._meta.verbose_name.replace(" ", "_"),
            "add_url": "plugins:netbox_acls:fwrulelist_add",
        }

    def prep_table_data(self, request, queryset, parent):
        return queryset.annotate(
            rule_count=Count("fwingressrules") + Count("fwegressrules"),
        )


# @register_model_view(Device, "fw_rule_lists")
# class DeviceFirewallRuleListView(FirewallRuleListChildView):
#     queryset = Device.objects.prefetch_related("tags")
#     tab = ViewTab(
#         label="Access Lists",
#         badge=lambda obj: models.FirewallRuleList.objects.filter(device=obj).count(),
#         permission="netbox_acls.view_accesslist",
#     )

#     def get_children(self, request, parent):
#         return self.child_model.objects.restrict(request.user, "view").filter(
#             device=parent,
#         )


# @register_model_view(VirtualChassis, "fw_rule_lists")
# class VirtualChassisFirewallRuleListView(FirewallRuleListChildView):
#     queryset = VirtualChassis.objects.prefetch_related("tags")
#     tab = ViewTab(
#         label="Access Lists",
#         badge=lambda obj: models.FirewallRuleList.objects.filter(virtual_chassis=obj).count(),
#         permission="netbox_acls.view_accesslist",
#     )

#     def get_children(self, request, parent):
#         return self.child_model.objects.restrict(request.user, "view").filter(
#             virtual_chassis=parent,
#         )


# @register_model_view(VirtualMachine, "fw_rule_lists")
# class VirtualMachineFirewallRuleListView(FirewallRuleListChildView):
#     queryset = VirtualMachine.objects.prefetch_related("tags")
#     tab = ViewTab(
#         label="Access Lists",
#         badge=lambda obj: models.FirewallRuleList.objects.filter(virtual_machine=obj).count(),
#         permission="netbox_acls.view_accesslist",
#     )

#     def get_children(self, request, parent):
#         return self.child_model.objects.restrict(request.user, "view").filter(
#             virtual_machine=parent,
#         )


#
# FWInterfaceAssignment views
#


@register_model_view(models.FWInterfaceAssignment)
class FWInterfaceAssignmentView(generic.ObjectView):
    """
    Defines the view for the FWInterfaceAssignment django model.
    """

    queryset = models.FWInterfaceAssignment.objects.prefetch_related(
        "fw_rule_list",
        "tags",
    )


class FWInterfaceAssignmentListView(generic.ObjectListView):
    """
    Defines the list view for the FWInterfaceAssignments django model.
    """

    queryset = models.FWInterfaceAssignment.objects.prefetch_related(
        "fw_rule_list",
        "tags",
    )
    table = tables.FWInterfaceAssignmentTable
    filterset = filtersets.FWInterfaceAssignmentFilterSet
    filterset_form = forms.FWInterfaceAssignmentFilterForm


@register_model_view(models.FWInterfaceAssignment, "edit")
class FWInterfaceAssignmentEditView(generic.ObjectEditView):
    """
    Defines the edit view for the FWInterfaceAssignments django model.
    """

    queryset = models.FWInterfaceAssignment.objects.prefetch_related(
        "fw_rule_list",
        "tags",
    )
    form = forms.FWInterfaceAssignmentForm
    template_name = "netbox_acls/fwinterfaceassignment_edit.html"

    def get_extra_addanother_params(self, request):
        """
        Returns a dictionary of additional parameters to be passed to the "Add Another" button.
        """

        return {
            "fw_rule_list": request.GET.get("fw_rule_list") or request.POST.get("fw_rule_list"),
        }


@register_model_view(models.FWInterfaceAssignment, "delete")
class FWInterfaceAssignmentDeleteView(generic.ObjectDeleteView):
    """
    Defines delete view for the FWInterfaceAssignments django model.
    """

    queryset = models.FWInterfaceAssignment.objects.prefetch_related(
        "fw_rule_list",
        "tags",
    )


class FWInterfaceAssignmentBulkDeleteView(generic.BulkDeleteView):
    queryset = models.FWInterfaceAssignment.objects.prefetch_related(
        "fw_rule_list",
        "tags",
    )
    filterset = filtersets.FWInterfaceAssignmentFilterSet
    table = tables.FWInterfaceAssignmentTable


class FWInterfaceAssignmentChildView(generic.ObjectChildrenView):
    """
    Defines the child view for the FWInterfaceAssignments model.
    """

    child_model = models.FWInterfaceAssignment
    table = tables.FWInterfaceAssignmentTable
    filterset = filtersets.FWInterfaceAssignmentFilterSet
    template_name = "inc/view_tab.html"

    def get_extra_context(self, request, instance):
        return {
            "table_config": self.table.__name__,
            "model_type": self.queryset.model._meta.verbose_name.replace(" ", "_"),
            "add_url": "plugins:netbox_acls:fwinterfaceassignment_add",
        }


@register_model_view(Interface, "fw_interface_assignments")
class InterfaceFWInterfaceAssignmentView(FWInterfaceAssignmentChildView):
    queryset = Interface.objects.prefetch_related("device", "tags")
    tab = ViewTab(
        label="FW Interface Assignments",
        badge=lambda obj: models.FWInterfaceAssignment.objects.filter(
            interface=obj,
        ).count(),
        permission="netbox_acls.view_fwinterfaceassignment",
    )

    def get_children(self, request, parent):
        return self.child_model.objects.restrict(request.user, "view").filter(
            interface=parent,
        )


@register_model_view(VMInterface, "fw_interface_assignments")
class VirtualMachineInterfaceFWInterfaceAssignmentView(
    FWInterfaceAssignmentChildView,
):
    queryset = VMInterface.objects.prefetch_related("virtual_machine", "tags")
    tab = ViewTab(
        label="fw Interface Assignments",
        badge=lambda obj: models.FWInterfaceAssignment.objects.filter(
            vminterface=obj,
        ).count(),
        permission="netbox_acls.view_aclinterfaceassignment",
    )

    def get_children(self, request, parent):
        return self.child_model.objects.restrict(request.user, "view").filter(
            vminterface=parent,
        )


#
# FWIngressRule views
#


@register_model_view(models.FWIngressRule)
class FWIngressRuleView(generic.ObjectView):
    """
    Defines the view for the FWIngressRule django model.
    """

    queryset = models.FWIngressRule.objects.prefetch_related(
        "fw_rule_list",
        "tags",
    )


class FWIngressRuleListView(generic.ObjectListView):
    """
    Defines the list view for the FWIngressRule django model.
    """

    queryset = models.FWIngressRule.objects.prefetch_related(
        "fw_rule_list",
        "tags",
    )
    table = tables.FWIngressRuleTable
    filterset = filtersets.FWIngressRuleFilterSet
    filterset_form = forms.FWIngressRuleFilterForm


@register_model_view(models.FWIngressRule, "edit")
class FWIngressRuleEditView(generic.ObjectEditView):
    """
    Defines the edit view for the FWIngressRule django model.
    """

    queryset = models.FWIngressRule.objects.prefetch_related(
        "fw_rule_list",
        "tags",
    )
    form = forms.FWIngressRuleForm

    def get_extra_addanother_params(self, request):
        """
        Returns a dictionary of additional parameters to be passed to the "Add Another" button.
        """

        return {
            "fw_rule_list": request.GET.get("fw_rule_list") or request.POST.get("fw_rule_list"),
        }


@register_model_view(models.FWIngressRule, "delete")
class FWIngressRuleDeleteView(generic.ObjectDeleteView):
    """
    Defines delete view for the FWIngressRules django model.
    """

    queryset = models.FWIngressRule.objects.prefetch_related(
        "fw_rule_list",
        "tags",
    )


class FWIngressRuleBulkDeleteView(generic.BulkDeleteView):
    queryset = models.FWIngressRule.objects.prefetch_related(
        "fw_rule_list",
        "tags",
    )
    filterset = filtersets.FWIngressRuleFilterSet
    table = tables.FWIngressRuleTable


#
# FWEgressRule views
#


@register_model_view(models.FWEgressRule)
class FWEgressRuleView(generic.ObjectView):
    """
    Defines the view for the FWEgressRule django model.
    """

    queryset = models.FWEgressRule.objects.prefetch_related(
        "fw_rule_list",
        "tags",
    )


class FWEgressRuleListView(generic.ObjectListView):
    """
    Defines the list view for the FWEgressRule django model.
    """

    queryset = models.FWEgressRule.objects.prefetch_related(
        "fw_rule_list",
        "tags",
    )
    table = tables.FWEgressRuleTable
    filterset = filtersets.FWEgressRuleFilterSet
    filterset_form = forms.FWEgressRuleFilterForm


@register_model_view(models.FWEgressRule, "edit")
class FWEgressRuleEditView(generic.ObjectEditView):
    """
    Defines the edit view for the FWEgressRule django model.
    """

    queryset = models.FWEgressRule.objects.prefetch_related(
        "fw_rule_list",
        "tags",
    )
    form = forms.FWEgressRuleForm

    def get_extra_addanother_params(self, request):
        """
        Returns a dictionary of additional parameters to be passed to the "Add Another" button.
        """

        return {
            "fw_rule_list": request.GET.get("fw_rule_list") or request.POST.get("fw_rule_list"),
        }


@register_model_view(models.FWEgressRule, "delete")
class FWEgressRuleDeleteView(generic.ObjectDeleteView):
    """
    Defines delete view for the FWEgressRules django model.
    """

    queryset = models.FWEgressRule.objects.prefetch_related(
        "fw_rule_list",
        "tags",
    )


class FWEgressRuleBulkDeleteView(generic.BulkDeleteView):
    queryset = models.FWEgressRule.objects.prefetch_related(
        "fw_rule_list",
        "tags",
    )
    filterset = filtersets.FWEgressRuleFilterSet
    table = tables.FWEgressRuleTable
