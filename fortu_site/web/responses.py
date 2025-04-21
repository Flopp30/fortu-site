import dataclasses as dc


@dc.dataclass
class SimpleResponse:
    message: str = 'OK'
