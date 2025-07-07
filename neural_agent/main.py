"""CLI entrypoint for the code generation agent."""

import argparse
from pathlib import Path
import os

from .agent import CodeGenAgent


def main():
    parser = argparse.ArgumentParser(description="Generate code from architecture description")
    parser.add_argument("arch", type=Path, help="Path to architecture.txt")
    parser.add_argument("--output", type=Path, default=Path("generated"), help="Output directory")
    parser.add_argument("--api-key", type=str, default=None, help="OpenAI API key")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OpenAI API key required. Pass via --api-key or OPENAI_API_KEY env var")

    agent = CodeGenAgent(api_key=api_key)
    files = agent.run(args.arch, args.output)
    print("Generated files:")
    for f in files:
        print(" -", f)

if __name__ == "__main__":
    main()
