import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware

log = logging.getLogger(__name__)


class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        log.info(f'Request: {request.url.path} finished in {duration:.4f} seconds')
        return response
