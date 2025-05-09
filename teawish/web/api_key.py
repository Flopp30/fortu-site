from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from fastapi.security import APIKeyCookie
from starlette.status import HTTP_403_FORBIDDEN


class TemplateAPIKeyCookie(APIKeyCookie):
    @staticmethod
    def check_api_key(api_key: Optional[str], auto_error: bool) -> Optional[str]:
        if not auto_error:
            return api_key

        if not api_key:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
            )

        try:
            UUID(api_key)
        except ValueError:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
            )

        return api_key
