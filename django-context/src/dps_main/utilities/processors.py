from dps_main.models import Cause, Promise
from .attributelookup import AttrLookup


def get_factotum(request):
    """
    Demonstrates a good use of template tags and context processors
    """

    class Factotum(object):
        """
        This is a bit counter-intuitive seeing as `request` is already available in templates, but I will
        go with it for demonstration purposes
        """

        def __init__(self):
            self.user = request.user
            self.action_helper = request.action_helper

        @AttrLookup
        def can_promise(self, cause):
            promise = None
            try:
                promise = self.action_helper.get_promise_for_cause(cause.id if isinstance(cause, Cause) else cause)
            except Promise.DoesNotExist:
                pass
            return not isinstance(promise, Promise)

    return {'factotum': Factotum()}
