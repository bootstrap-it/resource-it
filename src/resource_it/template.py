from datetime import timedelta, date
def datetime_format(value, format="%Y-%m-%d"):
    return value.strftime(format)

import yaml
def from_yaml(value):
    return yaml.safe_load(value)

from jinja2 import Environment
jinja_env = Environment(
    line_statement_prefix="#",
    line_comment_prefix="##",
)

jinja_env.filters["datetime_format"] = datetime_format
jinja_env.filters["from_yaml"] = from_yaml

from faker import Faker
faker = Faker()
faker.seed(1000)

additional_ctx: dict = None

import log_it
log = log_it.logger(__name__)

from pipe_it import pipe

@pipe
def jinja(items, ctx={}):
    for it in items:
        jinja_template = jinja_env.from_string(it)
        yield jinja_template.render({
            **ctx,
            "fake": faker,
            "date": date,
            "timedelta": timedelta,
        })
