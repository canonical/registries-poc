import uuid
from datetime import datetime
from typing import Optional

from src import schemas, db
from src.constants import EMPTY_CONFIG
from src.types import ConfigDict


def update_target_config(config: ConfigDict) -> None:
    db.update_target_config(config)


def get_target_config() -> schemas.Config:
    return db.get_target_config()


def register(
    ip_address: str, public_key_rsa: str, arch: str
) -> schemas.RegisterResponse:
    registration_uuid = uuid.uuid4()
    registered_at = int(datetime.now().timestamp())
    state = schemas.State(
        registered=registered_at,
        ip_address=ip_address,
        public_key_rsa=public_key_rsa,
        arch=arch,
        config=EMPTY_CONFIG.config,
    )
    db.create_state(registration_uuid, state)
    return schemas.RegisterResponse(
        uuid=registration_uuid,
        registered=registered_at,
        ip_address=ip_address,
        public_key_rsa=public_key_rsa,
        arch=arch,
    )


def is_registered(registration_uuid: uuid.UUID) -> bool:
    return db.is_registered(registration_uuid)


def poll(
    registration_uuid: uuid.UUID, config: ConfigDict
) -> Optional[schemas.PollResponse]:
    _update_state(registration_uuid, config)
    target_config = db.get_target_config()
    if not _is_config_matching_target(config, target_config.config):
        return schemas.PollResponse(config=target_config.config)
    return None


def _update_state(registration_uuid: uuid.UUID, config: ConfigDict) -> None:
    state = db.get_state(registration_uuid)
    state.config = config
    db.update_state(registration_uuid, state)


def _is_config_matching_target(config: ConfigDict, target: ConfigDict) -> bool:
    return config == target


def get_state(registration_uuid: uuid.UUID) -> schemas.State:
    return db.get_state(registration_uuid)
