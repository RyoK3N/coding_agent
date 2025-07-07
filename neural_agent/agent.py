"""High level agent orchestrating parsing and generation."""

from pathlib import Path
from typing import List

from .architecture import Architecture
from .parser import parse_architecture
from .generator import CodeGenerator


class CodeGenAgent:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def run(self, arch_file: Path, output_dir: Path) -> List[Path]:
        arch = parse_architecture(arch_file)
        input_shape = self._infer_input_shape(arch)
        generator = CodeGenerator(api_key=self.api_key)
        return generator.write_files(arch, output_dir, input_shape)

    def _infer_input_shape(self, arch: Architecture) -> str:
        for layer in arch.layers:
            if "Input shape" in layer.params:
                return layer.params["Input shape"]
        return "(224, 224, 3)"
