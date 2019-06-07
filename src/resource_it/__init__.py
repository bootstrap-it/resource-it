

from urllib.parse import urlparse
from pipe_it import pipe

import log_it
log = log_it.logger(__name__)

from pathlib import Path

url_resolving_ctx = {
    "cwd": Path.cwd(),
    "home": Path.home(),
}

def resource(url, **data):
    url = url.format(**url_resolving_ctx)
    res_url = ResourceUrl.from_str(url)
    res_cls = RESOURCES_CATALOG[res_url.scheme]
    res = res_cls(res_url)
    if data:
        res | ensure(data)
    return res

@pipe
def ensure(res, data={}):
    if not res.exists:
        res.create(**data)
        log.info(f"CREATE: {res.url}")
    else:
        diff = res.diff(data)
        if diff:
            log.info(f"UPDATE: {res.url}\n\tdiff: {diff}")
            res.update(**diff)
        else:
            log.debug(f"{res.url} is already up-to-date")
    return res

from resource_it.base import Resource, ResourceUrl, ResourceNotFoundError
from resource_it.filesystem import File, Dir
from resource_it.consul import Consul_KV
from resource_it.git import Repo

RESOURCES_CATALOG = {
    "git-local": Repo,
    "file": File,
    "dir": Dir,
    "consul-kv": Consul_KV,
}
