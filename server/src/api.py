import uuid

from fastapi import APIRouter, HTTPException
from starlette.responses import Response

from src import schemas, logic
from src.schemas import PollResponse

router = APIRouter()


@router.put(
    "/target-config/",
    response_model=schemas.Config,
    responses={200: {"description": "Updated target configuration"}},
)
async def update_target_config(config: schemas.Config) -> schemas.Config:
    logic.update_target_config(config.config)
    return config


@router.get(
    "/target-config/",
    response_model=schemas.Config,
    responses={200: {"description": "Returned target configuration"}},
)
async def get_target_config() -> schemas.Config:
    rsp = logic.get_target_config()
    return rsp


@router.post(
    "/register/",
    response_model=schemas.RegisterResponse,
    responses={200: {"description": "Registered agent"}},
)
async def register(
    register_request: schemas.RegisterRequest,
) -> schemas.RegisterResponse:
    rsp = logic.register(**register_request.model_dump())
    return rsp


@router.post(
    "/poll/",
    response_model=schemas.PollResponse,
    responses={
        200: {"description": "Polled with agent configuration not matching target"},
        204: {"description": "Polled with agent configuration matching target"},
        400: {"description": "Agent not registered", "model": schemas.ErrorResponse},
    },
)
async def poll(poll_request: schemas.PollRequest) -> PollResponse | Response:
    if not logic.is_registered(poll_request.uuid):
        raise HTTPException(status_code=400, detail="Agent not registered")
    rsp = logic.poll(poll_request.uuid, poll_request.config)
    if rsp is None:
        return Response(status_code=204)
    return rsp


@router.get(
    "/state/{registration_uuid}/",
    response_model=schemas.State,
    responses={
        200: {"description": "Returned agent state"},
        400: {
            "description": "Agent registration not found",
            "model": schemas.ErrorResponse,
        },
    },
)
async def get_state(registration_uuid: uuid.UUID) -> schemas.State:
    if not logic.is_registered(registration_uuid):
        raise HTTPException(status_code=400, detail="Agent registration not found")
    rsp = logic.get_state(registration_uuid)
    return rsp
