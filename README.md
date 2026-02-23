# ollama-agent

LangChain + Ollama で動くローカルAIアシスタント。
カレントディレクトリで起動すると、そのディレクトリを作業対象としてチャット・ファイル操作・コマンド実行ができる。

## 必要なもの

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- [Ollama](https://ollama.com/) (起動済み)
- Qwen3 モデル (`ollama pull qwen3`)

## セットアップ

```bash
uv sync
```

## 使い方

```bash
# カレントディレクトリで起動
uv run main.py

# 任意のディレクトリで起動
cp main.py ~/.local/bin/ai
```

```text
AI Assistant (/Users/you/projects/my-app)
Type 'exit' to quit.

You: ファイル一覧を見せて
AI: src/ package.json README.md ...

You: hello worldをhello.txtに書いて
AI: hello.txtにhello worldを書き出しました。
```

## 利用可能なツール

| ツール        | 機能               |
| ------------- | ------------------ |
| `write_file`  | ファイル書き出し   |
| `read_file`   | ファイル読み取り   |
| `list_files`  | ディレクトリ一覧   |
| `run_command` | シェルコマンド実行 |

ツールが不要な質問には通常のチャットで回答する。

## モデルの変更

`main.py` の `ChatOllama(model="qwen3")` を変更する。

```python
# Llama
llm = ChatOllama(model="llama3.1")

# Gemma
llm = ChatOllama(model="gemma2")
```

## 技術スタック

- [LangChain](https://www.langchain.com/) - LLM統合フレームワーク
- [LangGraph](https://langchain-ai.github.io/langgraph/) - エージェントワークフロー
- [Ollama](https://ollama.com/) - ローカルLLM実行環境
