"""Parser for architecture.txt files."""

import re
from pathlib import Path
from typing import List

from .architecture import Architecture, Layer


_LAYER_HEADER_RE = re.compile(r"Layer (\d+): (.+) \((.+)\)")
_PARAM_RE = re.compile(r"- ([\w\s]+): (.+)")


def parse_architecture(path: Path) -> Architecture:
    text = path.read_text()
    lines = text.splitlines()

    layers: List[Layer] = []
    connections: List[str] = []
    total_layers = 0

    current_layer: dict | None = None
    for line in lines:
        if line.startswith("Total layers"):
            total_layers = int(line.split(":")[1].strip())
        m = _LAYER_HEADER_RE.match(line)
        if m:
            if current_layer:
                layers.append(Layer(**current_layer))
            idx, name, layer_type = m.groups()
            current_layer = {
                "name": name.strip(),
                "type": layer_type.strip(),
                "params": {},
            }
            continue
        p = _PARAM_RE.search(line)
        if p and current_layer:
            key, value = p.groups()
            current_layer["params"][key.strip()] = value.strip()
        if line.startswith("* "):
            connections.append(line[2:].strip())

    if current_layer:
        layers.append(Layer(**current_layer))

    return Architecture(total_layers=total_layers, layers=layers, connections=connections)
