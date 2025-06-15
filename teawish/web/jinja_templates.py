import datetime
from typing import Any

from fastapi.datastructures import URL
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from jinja2 import pass_context

from teawish.config import WebConfig


def get_templates(web_config: WebConfig) -> Jinja2Templates:
    templates = Jinja2Templates(
        directory=web_config.templates_dir,
    )
    register_filters(templates, web_config)
    return templates


def register_filters(templates: Jinja2Templates, web_config: WebConfig):
    templates.env.globals['now'] = datetime.datetime.now
    templates.env.filters['format_date'] = lambda dt: dt.strftime('%H:%M %d.%m.%Y')
    templates.env.globals['discord_link'] = web_config.discord_link
    templates.env.globals['url_for'] = urlx_for
    templates.env.globals['world_map_address'] = web_config.world_map_address


@pass_context
def urlx_for(context: dict, name: str, **path_params: Any) -> URL:
    request: Request = context['request']
    http_url = request.url_for(name, **path_params)
    if scheme := request.headers.get('x-forwarded-proto'):
        return http_url.replace(scheme=scheme)
    return http_url
