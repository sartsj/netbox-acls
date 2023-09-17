"""
Creates API endpoint URLs for the plugin.
"""

from netbox.api.routers import NetBoxRouter

from . import views

app_name = "netbox_acls"

router = NetBoxRouter()
router.register("access-lists", views.AccessListViewSet)
router.register("interface-assignments", views.ACLInterfaceAssignmentViewSet)
router.register("standard-acl-rules", views.ACLStandardRuleViewSet)
router.register("extended-acl-rules", views.ACLExtendedRuleViewSet)
router.register("fw-rule-lists", views.FirewallRuleListViewSet)
router.register("fw-interface-assignments", views.FWInterfaceAssignmentViewSet)
router.register("fw-ingress-rules", views.FWIngressRuleViewSet)
router.register("fw-egress-rules", views.FWEgressRuleViewSet)

urlpatterns = router.urls
