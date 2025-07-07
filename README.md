# Coding Agent

This repository contains a prototype coding agent for generating neural network code from architecture descriptions. The agent uses **LangChain**, **OpenAI** and **Pydantic** to parse architecture files and produce boilerplate code for data pipelines, model definitions and training scripts.

## Usage

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Place an `architecture.txt` file describing your model.
3. Run the agent:
   ```bash
   python -m neural_agent.main architecture.txt --api-key YOUR_OPENAI_API_KEY
   ```
   Generated code will be placed in the `generated/` directory by default.

The provided `architecture.txt` is an example architecture used for testing.
