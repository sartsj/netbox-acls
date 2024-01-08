"""
Creates API endpoint URLs for the plugin.
"""

from netbox.api.routers import NetBoxRouter

from . import views

app_name = "netbox_acls"

router = NetBoxRouter()
router.register("access-lists", views.AccessListViewSet)
router.register("interface-assignments", views.ACLInterfaceAssignmentViewSet)
router.register("standard-acl-rules", views.ACLIngressRuleViewSet)
router.register("extended-acl-rules", views.ACLEgressRuleViewSet)

urlpatterns = router.urls
