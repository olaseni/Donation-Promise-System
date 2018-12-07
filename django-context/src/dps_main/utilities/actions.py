from dps_main.models import Cause


def create_cause():
    return Cause.objects.create()


def list_causes():
    return [0]


def list_available_causes():
    return []


def get_cause():
    return None


def update_cause():
    pass


def delete_cause():
    pass


def add_promise_to_cause():
    pass


def list_promises():
    return []


def get_promise():
    return None


def update_promise():
    pass


def delete_promise():
    pass


def list_promises_by_cause():
    return []


def get_promise_for_cause():
    return []


def get_all_causes_promised():
    return []
