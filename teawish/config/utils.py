import os

from pydantic import BaseModel


class BaseFromEnvConfig(BaseModel):
    @classmethod
    def from_env(cls):
        return cls(**os.environ)


def split_string_from_env(env_var: str) -> list[str]:
    return env_var.split(',')


def env_to_abs_path(env_var: str) -> str:
    if not env_var:
        return env_var

    if os.path.isabs(env_var):
        return env_var
    else:
        return os.path.abspath(env_var)
