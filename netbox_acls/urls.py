"""
Map Views to URLs.
"""

from django.urls import include, path
from utilities.urls import get_model_urls

from . import views

urlpatterns = (
    # Access Lists
    path("access-lists/", views.AccessListListView.as_view(), name="accesslist_list"),
    path(
        "access-lists/add/",
        views.AccessListEditView.as_view(),
        name="accesslist_add",
    ),
    # path('access-lists/edit/', views.AccessListBulkEditView.as_view(), name='accesslist_bulk_edit'),
    path(
        "access-lists/delete/",
        views.AccessListBulkDeleteView.as_view(),
        name="accesslist_bulk_delete",
    ),
    path("access-lists/<int:pk>/", views.AccessListView.as_view(), name="accesslist"),
    path(
        "access-lists/<int:pk>/edit/",
        views.AccessListEditView.as_view(),
        name="accesslist_edit",
    ),
    path(
        "access-lists/<int:pk>/delete/",
        views.AccessListDeleteView.as_view(),
        name="accesslist_delete",
    ),
    path(
        "access-lists/<int:pk>/",
        include(get_model_urls("netbox_acls", "accesslist")),
    ),
    # Access List Interface Assignments
    path(
        "interface-assignments/",
        views.ACLInterfaceAssignmentListView.as_view(),
        name="aclinterfaceassignment_list",
    ),
    path(
        "interface-assignments/add/",
        views.ACLInterfaceAssignmentEditView.as_view(),
        name="aclinterfaceassignment_add",
    ),
    # path(
    #    "interface-assignments/edit/",
    #    views.ACLInterfaceAssignmentBulkEditView.as_view(),
    #    name="aclinterfaceassignment_bulk_edit"
    # ),
    path(
        "interface-assignments/delete/",
        views.ACLInterfaceAssignmentBulkDeleteView.as_view(),
        name="aclinterfaceassignment_bulk_delete",
    ),
    path(
        "interface-assignments/<int:pk>/",
        views.ACLInterfaceAssignmentView.as_view(),
        name="aclinterfaceassignment",
    ),
    path(
        "interface-assignments/<int:pk>/edit/",
        views.ACLInterfaceAssignmentEditView.as_view(),
        name="aclinterfaceassignment_edit",
    ),
    path(
        "interface-assignments/<int:pk>/delete/",
        views.ACLInterfaceAssignmentDeleteView.as_view(),
        name="aclinterfaceassignment_delete",
    ),
    path(
        "interface-assignments/<int:pk>/",
        include(get_model_urls("netbox_acls", "aclinterfaceassignment")),
    ),
    # Standard Access List Rules
    path(
        "standard-rules/",
        views.ACLStandardRuleListView.as_view(),
        name="aclstandardrule_list",
    ),
    path(
        "standard-rules/add/",
        views.ACLStandardRuleEditView.as_view(),
        name="aclstandardrule_add",
    ),
    path(
        "standard-rules/delete/",
        views.ACLStandardRuleBulkDeleteView.as_view(),
        name="aclstandardrule_bulk_delete",
    ),
    path(
        "standard-rules/<int:pk>/",
        views.ACLStandardRuleView.as_view(),
        name="aclstandardrule",
    ),
    path(
        "standard-rules/<int:pk>/edit/",
        views.ACLStandardRuleEditView.as_view(),
        name="aclstandardrule_edit",
    ),
    path(
        "standard-rules/<int:pk>/delete/",
        views.ACLStandardRuleDeleteView.as_view(),
        name="aclstandardrule_delete",
    ),
    path(
        "standard-rules/<int:pk>/",
        include(get_model_urls("netbox_acls", "aclstandardrule")),
    ),
    # Extended Access List Rules
    path(
        "extended-rules/",
        views.ACLExtendedRuleListView.as_view(),
        name="aclextendedrule_list",
    ),
    path(
        "extended-rules/add/",
        views.ACLExtendedRuleEditView.as_view(),
        name="aclextendedrule_add",
    ),
    path(
        "extended-rules/delete/",
        views.ACLExtendedRuleBulkDeleteView.as_view(),
        name="aclextendedrule_bulk_delete",
    ),
    path(
        "extended-rules/<int:pk>/",
        views.ACLExtendedRuleView.as_view(),
        name="aclextendedrule",
    ),
    path(
        "extended-rules/<int:pk>/edit/",
        views.ACLExtendedRuleEditView.as_view(),
        name="aclextendedrule_edit",
    ),
    path(
        "extended-rules/<int:pk>/delete/",
        views.ACLExtendedRuleDeleteView.as_view(),
        name="aclextendedrule_delete",
    ),
    path(
        "extended-rules/<int:pk>/",
        include(get_model_urls("netbox_acls", "aclextendedrule")),
    ),

    # Firewall Rule Lists
    path("fwrule-lists/", views.FirewallRuleListListView.as_view(), name="fwrulelist_list"),
    path(
        "fwrule-lists/add/",
        views.FirewallRuleListEditView.as_view(),
        name="fwrulelist_add",
    ),
    # path('fwrule-lists/edit/', views.FirewallRuleListBulkEditView.as_view(), name='fwrulelist_bulk_edit'),
    path(
        "fwrule-lists/delete/",
        views.FirewallRuleListBulkDeleteView.as_view(),
        name="fwrulelist_bulk_delete",
    ),
    path("fwrule-lists/<int:pk>/", views.FirewallRuleListView.as_view(), name="fwrulelist"),
    path(
        "fwrule-lists/<int:pk>/edit/",
        views.FirewallRuleListEditView.as_view(),
        name="fwrulelist_edit",
    ),
    path(
        "fwrule-lists/<int:pk>/delete/",
        views.FirewallRuleListDeleteView.as_view(),
        name="fwrulelist_delete",
    ),
    path(
        "fwrule-lists/<int:pk>/",
        include(get_model_urls("netbox_acls", "fwrulelist")),
    ),
    # FW Rule Interface Assignments
    path(
        "fw-interface-assignments/",
        views.FWInterfaceAssignmentListView.as_view(),
        name="fwinterfaceassignment_list",
    ),
    path(
        "fw-interface-assignments/add/",
        views.FWInterfaceAssignmentEditView.as_view(),
        name="fwinterfaceassignment_add",
    ),
    # path(
    #    "fw-interface-assignments/edit/",
    #    views.FWInterfaceAssignmentBulkEditView.as_view(),
    #    name="fwinterfaceassignment_bulk_edit"
    # ),
    path(
        "fw-interface-assignments/delete/",
        views.FWInterfaceAssignmentBulkDeleteView.as_view(),
        name="fwinterfaceassignment_bulk_delete",
    ),
    path(
        "fw-interface-assignments/<int:pk>/",
        views.FWInterfaceAssignmentView.as_view(),
        name="fwinterfaceassignment",
    ),
    path(
        "fw-interface-assignments/<int:pk>/edit/",
        views.FWInterfaceAssignmentEditView.as_view(),
        name="fwinterfaceassignment_edit",
    ),
    path(
        "fw-interface-assignments/<int:pk>/delete/",
        views.FWInterfaceAssignmentDeleteView.as_view(),
        name="fwinterfaceassignment_delete",
    ),
    path(
        "fw-interface-assignments/<int:pk>/",
        include(get_model_urls("netbox_acls", "fwinterfaceassignment")),
    ),
    # FW Ingress Rules
    path(
        "fw-ingress-rules/",
        views.FWIngressRuleListView.as_view(),
        name="fwingressrule_list",
    ),
    path(
        "fw-ingress-rules/add/",
        views.FWIngressRuleEditView.as_view(),
        name="fwingressrule_add",
    ),
    path(
        "fw-ingress-rules/delete/",
        views.FWIngressRuleBulkDeleteView.as_view(),
        name="fwingressrule_bulk_delete",
    ),
    path(
        "fw-ingress-rules/<int:pk>/",
        views.FWIngressRuleView.as_view(),
        name="fwingressrule",
    ),
    path(
        "fw-ingress-rules/<int:pk>/edit/",
        views.FWIngressRuleEditView.as_view(),
        name="fwingressrule_edit",
    ),
    path(
        "fw-ingress-rules/<int:pk>/delete/",
        views.FWIngressRuleDeleteView.as_view(),
        name="fwingressrule_delete",
    ),
    path(
        "fw-ingress-rules/<int:pk>/",
        include(get_model_urls("netbox_acls", "fwingressrule")),
    ),
    # FW Egress Rules
    path(
        "fw-egress-rules/",
        views.FWEgressRuleListView.as_view(),
        name="fwegressrule_list",
    ),
    path(
        "fw-egress-rules/add/",
        views.FWEgressRuleEditView.as_view(),
        name="fwegressrule_add",
    ),
    path(
        "fw-egress-rules/delete/",
        views.FWEgressRuleBulkDeleteView.as_view(),
        name="fwegressrule_bulk_delete",
    ),
    path(
        "fw-egress-rules/<int:pk>/",
        views.FWEgressRuleView.as_view(),
        name="fwegressrule",
    ),
    path(
        "fw-egress-rules/<int:pk>/edit/",
        views.FWEgressRuleEditView.as_view(),
        name="fwegressrule_edit",
    ),
    path(
        "fw-egress-rules/<int:pk>/delete/",
        views.FWEgressRuleDeleteView.as_view(),
        name="fwegressrule_delete",
    ),
    path(
        "fw-egress-rules/<int:pk>/",
        include(get_model_urls("netbox_acls", "fwegressrule")),
    ),
)
