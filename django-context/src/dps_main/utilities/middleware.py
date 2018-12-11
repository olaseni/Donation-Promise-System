#
"""
DPS Middlewares
"""

from .actions import ActionHelper


class DPSActionsMiddleWare(object):
    """
    This middleware class establishes a way to inject the user based actions infrastructure into the request.
    This provides a consistent and ubiquitous way to access actions
    """

    def __init__(self, get_response) -> None:
        """
        Stores the get_response callable for subsequent retrieval
        """
        self.get_response = get_response

    def __call__(self, request):
        # associate the action helper with the request
        request.action_helper = ActionHelper(request.user)

        response = self.get_response(request)

        # chain next middleware
        return response
