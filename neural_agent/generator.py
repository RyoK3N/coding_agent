"""Generate source code from parsed architecture."""

from pathlib import Path
from typing import List

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from .architecture import Architecture

DEFAULT_TRAINING_PROMPT = """
You are a senior ML engineer. Generate a Keras model implementation for the given architecture.
Architecture: {architecture}
Return Python code only.
"""

DEFAULT_DATA_PROMPT = """
You are a senior ML engineer. Write Python code to create a data pipeline for image data with shape {input_shape}. Include preprocessing, train/validation split and batching with TensorFlow datasets.
"""


class CodeGenerator:
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.llm = ChatOpenAI(model_name=model, openai_api_key=api_key)

    def _generate(self, prompt: str) -> str:
        template = ChatPromptTemplate.from_template("{prompt}")
        chain = template | self.llm
        return chain.invoke({"prompt": prompt}).content

    def generate_model(self, arch: Architecture) -> str:
        return self._generate(DEFAULT_TRAINING_PROMPT.format(architecture=arch.json()))

    def generate_data_pipeline(self, input_shape: str) -> str:
        return self._generate(DEFAULT_DATA_PROMPT.format(input_shape=input_shape))

    def generate_training(self, arch: Architecture) -> str:
        prompt = (
            "You are a senior ML engineer. Write a Python training loop for the architecture including compiling, training and validation. Use TensorFlow/Keras APIs."
        )
        return self._generate(prompt)

    def write_files(self, arch: Architecture, output_dir: Path, input_shape: str) -> List[Path]:
        output_dir.mkdir(parents=True, exist_ok=True)
        files = []
        model_code = self.generate_model(arch)
        model_path = output_dir / "model.py"
        model_path.write_text(model_code)
        files.append(model_path)

        data_code = self.generate_data_pipeline(input_shape)
        data_path = output_dir / "data.py"
        data_path.write_text(data_code)
        files.append(data_path)

        train_code = self.generate_training(arch)
        train_path = output_dir / "train.py"
        train_path.write_text(train_code)
        files.append(train_path)
        return files
