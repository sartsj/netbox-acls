"""
Define the plugin menu buttons & the plugin navigation bar enteries.
"""

from django.conf import settings
from extras.plugins import PluginMenu, PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices

plugin_settings = settings.PLUGINS_CONFIG["netbox_acls"]

#
# Define plugin menu buttons
#
menu_buttons = (
    PluginMenuItem(
        link="plugins:netbox_acls:accesslist_list",
        link_text="Access Lists",
        permissions=["netbox_acls.view_accesslist"],
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_acls:accesslist_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["netbox_acls.add_accesslist"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_acls:aclstandardrule_list",
        link_text="Standard Rules",
        permissions=["netbox_acls.view_aclstandardrule"],
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_acls:aclstandardrule_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["netbox_acls.add_aclstandardrule"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_acls:aclextendedrule_list",
        link_text="Extended Rules",
        permissions=["netbox_acls.view_aclextendedrule"],
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_acls:aclextendedrule_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["netbox_acls.add_aclextendedrule"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_acls:aclinterfaceassignment_list",
        link_text="Interface Assignments",
        permissions=["netbox_acls.view_aclinterfaceassignment"],
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_acls:aclinterfaceassignment_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["netbox_acls.add_aclinterfaceassignment"],
            ),
        ),
    ),
)

if plugin_settings.get("top_level_menu"):
    menu = PluginMenu(
        label="Access Lists",
        groups=(("ACLs", menu_buttons),),
        icon_class="mdi mdi-lock",
    )
else:
    menu_items = menu_buttons


fwmenu_buttons = (
    PluginMenuItem(
        link="plugins:netbox_acls:fwrulelist_list",
        link_text="Firewall Rule Lists",
        permissions=["netbox_acls.view_fwrulelist"],
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_acls:fwrulelist_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["netbox_acls.add_fwrulelist"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_acls:fwingressrule_list",
        link_text="FW Ingress Rules",
        permissions=["netbox_acls.view_fwingressrule"],
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_acls:fwingressrule_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["netbox_acls.add_fwingressrule"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_acls:fwegressrule_list",
        link_text="FW Egress Rules",
        permissions=["netbox_acls.view_fwegressrule"],
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_acls:fwegressrule_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["netbox_acls.add_fwegressrule"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_acls:fwinterfaceassignment_list",
        link_text="FW Interface Assignments",
        permissions=["netbox_acls.view_fwinterfaceassignment"],
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_acls:aclinterfaceassignment_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["netbox_acls.add_aclinterfaceassignment"],
            ),
        ),
    ),
)


if plugin_settings.get("top_level_menu"):
    menu = PluginMenu(
        label="Firewall Rule Lists",
        groups=(("FWLs", fwmenu_buttons),),
        icon_class="mdi mdi-lock",
    )
else:
    menu_items = menu_buttons
