"""
Defines the business logic for the plugin.
Specifically, all the various interactions with a client.
"""

from dcim.models import Device, Interface, VirtualChassis
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
    "ACLIngressRuleView",
    "ACLIngressRuleListView",
    "ACLIngressRuleEditView",
    "ACLIngressRuleDeleteView",
    "ACLIngressRuleBulkDeleteView",
    "ACLEgressRuleView",
    "ACLEgressRuleListView",
    "ACLEgressRuleEditView",
    "ACLEgressRuleDeleteView",
    "ACLEgressRuleBulkDeleteView",
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

        if instance.type == choices.ACLAssignmentDirectionChoices.DIRECTION_EGRESS:
            table = tables.ACLEgressRuleTable(instance.aclegressrules.all())
        elif instance.type == choices.ACLAssignmentDirectionChoices.DIRECTION_INGRESS:
            table = tables.ACLIngressRuleTable(instance.aclingressrules.all())
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
        rule_count=Count("aclegressrules") + Count("aclingressrules"),
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
            rule_count=Count("aclegressrules") + Count("aclingressrules"),
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
# ACLIngressRule views
#


@register_model_view(models.ACLIngressRule)
class ACLIngressRuleView(generic.ObjectView):
    """
    Defines the view for the ACLIngressRule django model.
    """

    queryset = models.ACLIngressRule.objects.prefetch_related(
        "access_list",
        "tags",
    )


class ACLIngressRuleListView(generic.ObjectListView):
    """
    Defines the list view for the ACLIngressRule django model.
    """

    queryset = models.ACLIngressRule.objects.prefetch_related(
        "access_list",
        "tags",
    )
    table = tables.ACLIngressRuleTable
    filterset = filtersets.ACLIngressRuleFilterSet
    filterset_form = forms.ACLIngressRuleFilterForm


@register_model_view(models.ACLIngressRule, "edit")
class ACLIngressRuleEditView(generic.ObjectEditView):
    """
    Defines the edit view for the ACLIngressRule django model.
    """

    queryset = models.ACLIngressRule.objects.prefetch_related(
        "access_list",
        "tags",
    )
    form = forms.ACLIngressRuleForm

    def get_extra_addanother_params(self, request):
        """
        Returns a dictionary of additional parameters to be passed to the "Add Another" button.
        """

        return {
            "access_list": request.GET.get("access_list") or request.POST.get("access_list"),
        }


@register_model_view(models.ACLIngressRule, "delete")
class ACLIngressRuleDeleteView(generic.ObjectDeleteView):
    """
    Defines delete view for the ACLIngressRules django model.
    """

    queryset = models.ACLIngressRule.objects.prefetch_related(
        "access_list",
        "tags",
    )


class ACLIngressRuleBulkDeleteView(generic.BulkDeleteView):
    queryset = models.ACLIngressRule.objects.prefetch_related(
        "access_list",
        "tags",
    )
    filterset = filtersets.ACLIngressRuleFilterSet
    table = tables.ACLIngressRuleTable


#
# ACLEgressRule views
#


@register_model_view(models.ACLEgressRule)
class ACLEgressRuleView(generic.ObjectView):
    """
    Defines the view for the ACLEgressRule django model.
    """

    queryset = models.ACLEgressRule.objects.prefetch_related(
        "access_list",
        "tags",
    )


class ACLEgressRuleListView(generic.ObjectListView):
    """
    Defines the list view for the ACLEgressRule django model.
    """

    queryset = models.ACLEgressRule.objects.prefetch_related(
        "access_list",
        "tags",
    )
    table = tables.ACLEgressRuleTable
    filterset = filtersets.ACLEgressRuleFilterSet
    filterset_form = forms.ACLEgressRuleFilterForm


@register_model_view(models.ACLEgressRule, "edit")
class ACLEgressRuleEditView(generic.ObjectEditView):
    """
    Defines the edit view for the ACLEgressRule django model.
    """

    queryset = models.ACLEgressRule.objects.prefetch_related(
        "access_list",
        "tags",
    )
    form = forms.ACLEgressRuleForm

    def get_extra_addanother_params(self, request):
        """
        Returns a dictionary of additional parameters to be passed to the "Add Another" button.
        """

        return {
            "access_list": request.GET.get("access_list") or request.POST.get("access_list"),
        }


@register_model_view(models.ACLEgressRule, "delete")
class ACLEgressRuleDeleteView(generic.ObjectDeleteView):
    """
    Defines delete view for the ACLEgressRules django model.
    """

    queryset = models.ACLEgressRule.objects.prefetch_related(
        "access_list",
        "tags",
    )


class ACLEgressRuleBulkDeleteView(generic.BulkDeleteView):
    queryset = models.ACLEgressRule.objects.prefetch_related(
        "access_list",
        "tags",
    )
    filterset = filtersets.ACLEgressRuleFilterSet
    table = tables.ACLEgressRuleTable
