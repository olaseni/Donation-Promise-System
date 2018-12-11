#


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

    return {'factotum': Factotum()}
