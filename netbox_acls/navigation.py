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
        link="plugins:netbox_acls:aclingressrule_list",
        link_text="Ingress Rules",
        permissions=["netbox_acls.view_aclingressrule"],
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_acls:aclingressrule_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["netbox_acls.add_aclingressrule"],
            ),
            PluginMenuButton(
                link="plugins:netbox_acls:aclingressrule_import",
                title="Import",
                icon_class="mdi mdi-upload",
                color=ButtonColorChoices.CYAN,
                permissions=["netbox_acls.add_aclingressrule"],
            ),
        ),
    ),
    PluginMenuItem(
        link="plugins:netbox_acls:aclegressrule_list",
        link_text="Egress Rules",
        permissions=["netbox_acls.view_aclegressrule"],
        buttons=(
            PluginMenuButton(
                link="plugins:netbox_acls:aclegressrule_add",
                title="Add",
                icon_class="mdi mdi-plus-thick",
                color=ButtonColorChoices.GREEN,
                permissions=["netbox_acls.add_aclegressrule"],
            ),
            PluginMenuButton(
                link="plugins:netbox_acls:aclegressrule_import",
                title="Import",
                icon_class="mdi mdi-upload",
                color=ButtonColorChoices.CYAN,
                permissions=["netbox_acls.add_aclegressrule"],
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
