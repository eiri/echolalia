import json
import logging
import os
import re
from typing import Any

from faker import Faker


class Generator:
    """Generate fake data documents from a template or item list."""

    def __init__(
        self,
        template: str | None = None,
        items: dict[str, str] | list[str] | None = None,
    ) -> None:
        if template is None and items is None:
            raise ValueError('missing required arguments "template" or "items"')
        self.log = logging.getLogger(__name__)
        self.fake = Faker()
        if template is None:
            tpl = self.create_template(items)  # type: ignore[arg-type]
        else:
            tpl = self.read_template(template)
        self.set_template(tpl)

    def generate(self, count: int) -> list[dict[str, Any]]:
        return [self.doc() for _ in range(count)]

    def normalize_to_json_type(self, value: Any) -> Any:
        known_types = (list, dict, str, int, float, bool, type(None))
        if not isinstance(value, known_types):
            value = str(value)
        return value

    def do_postprocess(self, value: Any, pplist: list) -> str:
        value = str(value)
        for pp in pplist:
            if isinstance(pp, dict):
                attr = pp["attr"]
                args = [value, *pp["args"]]
            else:
                attr = pp
                args = [value]
            if not hasattr(str, attr):
                continue
            fun = getattr(str, attr)
            value = fun(*args)
        return value

    def parse_attr(self, string: str) -> tuple[str, list[str]]:
        attrs = re.findall(r"{(\w+)}", string)
        if attrs:
            return (string, attrs)
        return (f"{{{string}}}", [string])

    def preprocess_value(self, tpl: Any) -> Any:
        if isinstance(tpl, str):
            frmt, attr = self.parse_attr(tpl)
            return {"frmt": frmt, "attr": attr, "args": ()}
        if isinstance(tpl, dict):
            if "attr" in tpl:
                if not isinstance(tpl["attr"], list):
                    frmt, attr = self.parse_attr(tpl["attr"])
                    tpl["attr"] = attr
                    if "frmt" not in tpl:
                        tpl["frmt"] = frmt
                else:
                    if "frmt" not in tpl:
                        tpl["frmt"] = " ".join(f"{{{a}}}" for a in tpl["attr"])
                tpl.setdefault("args", ())
                if "postprocess" in tpl and not isinstance(tpl["postprocess"], list):
                    tpl["postprocess"] = [tpl["postprocess"]]
                return tpl
            return self.preprocess_template(tpl)
        return [self.preprocess_value(v) for v in tpl]

    def preprocess_template(self, tpl: dict) -> dict:
        return {key: self.preprocess_value(value) for key, value in tpl.items()}

    def set_template(self, template: dict) -> None:
        self.template = self.preprocess_template(template)

    def read_template(self, template: str) -> dict:
        if not os.path.isfile(template):
            raise ValueError(f"Can't find template file {template}")
        self.log.debug("Reading template %s", template)
        with open(template) as fh:
            return json.load(fh)

    def create_template(self, items: dict[str, str] | list[str]) -> dict:
        self.log.debug("Creating template for %d item(s)", len(items))
        if isinstance(items, list):
            return {item: item for item in items}
        return dict(items)

    def generate_value(self, tpl: Any) -> Any:
        if isinstance(tpl, list):
            return [self.generate_value(v) for v in tpl]
        if "attr" in tpl:
            frmt: str = tpl["frmt"]
            args: tuple = tpl["args"]
            values: dict[str, Any] = {}
            for attr in tpl["attr"]:
                if not hasattr(self.fake, attr):
                    raise ValueError(f"Unknown fake method {attr}")
                values[attr] = getattr(self.fake, attr)(*args)
            first_value = next(iter(values.values()))
            if len(values) > 1 or isinstance(first_value, str):
                value = frmt.format(**values)
            else:
                value = first_value
        else:
            value = self.doc(tpl)
        value = self.normalize_to_json_type(value)
        if isinstance(tpl, dict) and "postprocess" in tpl:
            value = self.do_postprocess(value, tpl["postprocess"])
        return value

    def doc(self, tpl: dict | None = None) -> dict[str, Any]:
        items = (self.template if tpl is None else tpl).items()
        result = {key: self.generate_value(value) for key, value in items}
        if tpl is None:
            self.log.debug("Generated doc %s", result)
        return result
