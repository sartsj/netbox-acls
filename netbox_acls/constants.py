"""
Constants for filters
"""
from django.db.models import Q

ACL_HOST_ASSIGNMENT_MODELS = Q(Q(app_label="dcim", model="devicerole"),)

ACL_INTERFACE_ASSIGNMENT_MODELS = Q(
    Q(app_label="dcim", model="interface") | Q(app_label="virtualization", model="vminterface"),
)
