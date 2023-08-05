
from typing import List
import uuid
from datetime import datetime, timedelta
from pytz import UTC

from arxiv.users import auth, domain
from arxiv.base.globals import get_application_config


def get_system_token(name: str, scopes: List[str]) -> str:
    start = datetime.now(tz=UTC)
    end = start + timedelta(seconds=36000)
    session = domain.Session(
        session_id=str(uuid.uuid4()),
        start_time=datetime.now(), end_time=end,
        user=domain.System(name),
        authorizations=domain.Authorizations(scopes=scopes)
    )
    return auth.tokens.encode(session, get_application_config()['JWT_SECRET'])


def get_compiler_scopes(resource: str) -> List[str]:
    """Get minimal auth scopes necessary for compilation integration."""
    return [auth.scopes.READ_COMPILE.for_resource(resource),
            auth.scopes.CREATE_COMPILE.for_resource(resource)]
