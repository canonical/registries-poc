import os
from typing import Optional

from snap_http.http import get, SnapdHttpException


def get_aspect(name: str, *, fields: Optional[list[str]] = None) -> dict:
    """Get the aspect values (or a subset)."""
    query_params = {}
    if fields:
        query_params["fields"] = ",".join(fields)

    try:
        account_id = os.environ["ACCOUNT_ID"]
        response = get(
            f"/aspects/{account_id}/aspects-poc-v2/{name}",
            query_params=query_params,
        )
        return response.result
    except SnapdHttpException:
        # the aspect is empty
        return {}
