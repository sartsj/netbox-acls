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
        views.ACLIngressRuleListView.as_view(),
        name="aclingressrule_list",
    ),
    path(
        "standard-rules/add/",
        views.ACLIngressRuleEditView.as_view(),
        name="aclingressrule_add",
    ),
    path(
        "standard-rules/delete/",
        views.ACLIngressRuleBulkDeleteView.as_view(),
        name="aclingressrule_bulk_delete",
    ),
    path(
        "standard-rules/<int:pk>/",
        views.ACLIngressRuleView.as_view(),
        name="aclingressrule",
    ),
    path(
        "standard-rules/<int:pk>/edit/",
        views.ACLIngressRuleEditView.as_view(),
        name="aclingressrule_edit",
    ),
    path(
        "standard-rules/<int:pk>/delete/",
        views.ACLIngressRuleDeleteView.as_view(),
        name="aclingressrule_delete",
    ),
    path(
        "standard-rules/<int:pk>/",
        include(get_model_urls("netbox_acls", "aclingressrule")),
    ),
    # Extended Access List Rules
    path(
        "extended-rules/",
        views.ACLEgressRuleListView.as_view(),
        name="aclegressrule_list",
    ),
    path(
        "extended-rules/add/",
        views.ACLEgressRuleEditView.as_view(),
        name="aclegressrule_add",
    ),
    path(
        "extended-rules/delete/",
        views.ACLEgressRuleBulkDeleteView.as_view(),
        name="aclegressrule_bulk_delete",
    ),
    path(
        "extended-rules/<int:pk>/",
        views.ACLEgressRuleView.as_view(),
        name="aclegressrule",
    ),
    path(
        "extended-rules/<int:pk>/edit/",
        views.ACLEgressRuleEditView.as_view(),
        name="aclegressrule_edit",
    ),
    path(
        "extended-rules/<int:pk>/delete/",
        views.ACLEgressRuleDeleteView.as_view(),
        name="aclegressrule_delete",
    ),
    path(
        "extended-rules/<int:pk>/",
        include(get_model_urls("netbox_acls", "aclegressrule")),
    ),
)
