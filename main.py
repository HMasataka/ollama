#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "langchain-core>=1.2.14",
#     "langchain-ollama>=1.0.1",
#     "langgraph>=1.0.9",
# ]
# ///
"""ai - カレントディレクトリで動くAIアシスタント"""
import os
import subprocess

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent

WORK_DIR = os.getcwd()


@tool
def write_file(path: str, content: str) -> str:
    """指定パスにファイルを書き出す"""
    full = os.path.join(WORK_DIR, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(content)
    return f"Wrote {len(content)} bytes to {full}"


@tool
def read_file(path: str) -> str:
    """指定パスのファイルを読み取る"""
    full = os.path.join(WORK_DIR, path)
    with open(full, "r") as f:
        return f.read()


@tool
def list_files(directory: str = ".") -> str:
    """ディレクトリ内のファイル一覧を返す"""
    full = os.path.join(WORK_DIR, directory)
    entries = []
    for entry in sorted(os.listdir(full)):
        entry_path = os.path.join(full, entry)
        marker = "/" if os.path.isdir(entry_path) else ""
        entries.append(f"{entry}{marker}")
    return "\n".join(entries)


@tool
def run_command(command: str) -> str:
    """シェルコマンドを実行する"""
    result = subprocess.run(
        command,
        shell=True,
        cwd=WORK_DIR,
        capture_output=True,
        text=True,
        timeout=30,
    )
    output = (result.stdout + result.stderr).strip()
    return output if output else "(no output)"


def main():
    llm = ChatOllama(model="qwen3", temperature=0)
    agent = create_react_agent(
        model=llm,
        tools=[write_file, read_file, list_files, run_command],
        prompt=f"あなたはファイル操作アシスタントです。作業ディレクトリは {WORK_DIR} です。"
        "ファイルパスは相対パスで扱ってください。",
    )

    print(f"AI Assistant ({WORK_DIR})")
    print("Type 'exit' to quit.\n")

    history = []

    while True:
        try:
            user_input = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if user_input.strip() in ("quit", "exit"):
            break

        if not user_input.strip():
            continue

        history.append(HumanMessage(content=user_input))
        result = agent.invoke({"messages": history})
        history = result["messages"]
        print(f"AI: {history[-1].content}\n")


if __name__ == "__main__":
    main()
