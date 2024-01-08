"""
Defines the various choices to be used by the models, forms, and other plugin specifics.
"""

from utilities.choices import ChoiceSet

__all__ = (
    "ACLAssignmentDirectionChoices",
    "ACLProtocolChoices",
    "ACLProtocolChoices",
)


class ACLAssignmentDirectionChoices(ChoiceSet):
    """
    Defines the direction of the application of the ACL on an associated interface.
    """

    DIRECTION_INGRESS = "ingress"
    DIRECTION_EGRESS = "egress"

    CHOICES = [
        (DIRECTION_INGRESS, "Ingress", "blue"),
        (DIRECTION_EGRESS, "Egress", "purple"),
    ]


class ACLProtocolChoices(ChoiceSet):
    """
    Defines the choices availble for the Access Lists plugin specific to ACL Rule protocol.
    """

    PROTOCOL_ICMP = "icmp"
    PROTOCOL_TCP = "tcp"
    PROTOCOL_UDP = "udp"

    CHOICES = [
        (PROTOCOL_ICMP, "ICMP", "purple"),
        (PROTOCOL_TCP, "TCP", "blue"),
        (PROTOCOL_UDP, "UDP", "orange"),
    ]
