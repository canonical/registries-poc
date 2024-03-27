import os
from typing import Any, Optional

from snap_http.http import get, put, SnapdHttpException


def get_aspect(name: str, *, fields: Optional[list[str]] = None) -> dict:
    """Get the aspect values (or a subset)."""
    query_params = {}
    if fields:
        query_params["fields"] = ",".join(fields)

    try:
        account_id = os.environ["ACCOUNT_ID"]
        response = get(
            f"/aspects/{account_id}/aspects-poc/{name}",
            query_params=query_params,
        )
        return response.result
    except SnapdHttpException:
        # the aspect is empty
        return {}


def set_aspect(
    name: str,
    value: dict[str, Any],
) -> None:
    """Set the aspect values."""
    account_id = os.environ["ACCOUNT_ID"]
    put(
        f"/aspects/{account_id}/aspects-poc/{name}",
        value,
    )


def unset_aspect(name: str, *, fields: Optional[list[str]] = None) -> None:
    """Unset an aspect (or a subset)."""
    if fields is None:
        fields = [*get_aspect(name).keys()]

    try:
        set_aspect(name, dict.fromkeys(fields, None))
    except SnapdHttpException:
        # the aspect does not exist
        # removing non-existent aspects will cause errors
        pass
