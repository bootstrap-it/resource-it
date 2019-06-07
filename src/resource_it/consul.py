from consul import Consul

from typing import Any, Union, Mapping
from dataclasses import dataclass
from resource_it import Resource, ResourceNotFoundError
import cfg_it

import log_it
log = log_it.logger(__name__)

@cfg_it.props
class cfg:
    consul_host: str = "localhost"

class Consul_KV(Resource):

    @dataclass
    class meta_cls:
        key: str
        consul: Any

    @dataclass
    class data_cls:
        value: Union[str, Mapping] = ""

    def init(self):
        consul_host = self.url.netloc or cfg.consul_host

        self.meta = Consul_KV.meta_cls(
            key=self.url.path.lstrip("/"),
            consul=Consul(host=consul_host),
        )

    def create(self, **data):
        log.debug(f"consul-kv: create '{self.meta.key}'")
        self.meta.consul.kv.put(self.meta.key, data["value"])

    def read(self):
        req_index, req_obj = self.meta.consul.kv.get(self.meta.key)
        try:
            self.data = Consul_KV.data_cls(
                value=req_obj["Value"].decode("utf-8"),
            )
        except Exception as e:
            raise ResourceNotFoundError

    def update(self, **data):
        log.debug(f"consul-kv: update '{self.meta.key}'")
        self.meta.consul.kv.put(self.meta.key, data["value"])

    def delete(self):
        raise NotImplementedError(f"ConsulKV: delete")
