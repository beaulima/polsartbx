import logging

from polsartbx.apps.create_session import create_session, create_session_subparser
from polsartbx.apps.create_polsar_signatures import create_polsar_signatures, create_polsar_signatures_subparser

def get_applications_table():
    return {
        "new": (create_session_subparser, create_session),
        "polsarsigs": (create_polsar_signatures_subparser, create_polsar_signatures)
    }


logger = logging.getLogger("polsartbx.apps")
