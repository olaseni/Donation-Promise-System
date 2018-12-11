from django import template

from dps_main.utilities.actions import ActionHelper

register = template.Library()


@register.simple_tag(takes_context=True)
def action_helper_ping(context):
    """
    Pings the action helper
    """
    return ActionHelper(context.get('user')).ping()
