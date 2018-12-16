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
            """
            Ingest some vars from request context
            """
            self.user = request.user
            self.action_helper = request.action_helper
            self.resolver = request.resolver_match
            self.url_name = self.resolver.url_name
            self.is_make_promise = self.url_name == 'make_promise'
            self.kwargs = self.resolver.kwargs or {}
            self.pk = self.kwargs.get('pk')

        def get_promise_on_cause(self, cause_id) -> Promise:
            """
            Retrieve the promise on the cause belonging to current user
            :param cause_id: int
            :return: Promise
            """
            try:
                return self.action_helper.get_promise_for_cause(cause_id).get()
            except Promise.DoesNotExist:
                pass

        @property
        def promise_for_context_cause(self) -> Promise:
            """
            Get the promise associated with the cause
            """
            if self.is_make_promise and self.pk:
                return self.get_promise_on_cause(self.pk)

        @property
        def can_promise_for_context_cause(self) -> bool:
            """
            User can make a promise for the current cause
            """
            return not isinstance(self.promise_for_context_cause, Promise)

        @AttrLookup
        def can_promise(self, cause):
            """
            Retrieves a cause on an arbitrary cause
            """
            return not isinstance(self.get_promise_on_cause(cause.id if isinstance(cause, Cause) else cause), Promise)

    return {'factotum': Factotum()}
