import os
from typing import Optional

from snap_http.http import get, SnapdHttpException


def get_registry_value(name: str, *, fields: Optional[list[str]] = None) -> dict:
    """Get the registry values (or a subset)."""
    query_params = {}
    if fields:
        query_params["fields"] = ",".join(fields)

    try:
        account_id = os.environ["ACCOUNT_ID"]
        response = get(
            f"/registry/{account_id}/network/{name}",
            query_params=query_params,
        )
        return response.result
    except SnapdHttpException:
        # the registry is empty
        return {}
