"""Simple console chatbot powered by OpenRouter."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path


DEVELOPER_MESSAGE = (
	"You are a concise, helpful console chatbot. Keep replies short unless the user asks for details. "
	"Ask clarifying questions when needed, and maintain context across the conversation."
)

DEFAULT_MODEL = os.getenv("OPENROUTER_MODEL", "moonshotai/kimi-k3")
DEFAULT_MAX_TOKENS = int(os.getenv("OPENROUTER_MAX_TOKENS", "256"))
OPENAI_COMPAT_CHAT_URL = "https://openrouter.ai/api/v1/chat/completions"


def load_dotenv_file(path: str = ".env") -> None:
	env_path = Path(path)
	if not env_path.exists():
		return

	for raw_line in env_path.read_text(encoding="utf-8").splitlines():
		line = raw_line.strip()
		if not line or line.startswith("#") or "=" not in line:
			continue

		key, value = line.split("=", 1)
		os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def get_api_key() -> str:
	load_dotenv_file()

	api_key = os.getenv("OPENROUTER_API_KEY")
	if not api_key:
		raise SystemExit(
			"OPENROUTER_API_KEY is not set. Add it to your environment or .env file before running this script."
		)
	return api_key


def build_messages(history: list[dict[str, object]], user_message: str) -> list[dict[str, object]]:
	return history[-12:] + [
		{
			"role": "user",
			"content": user_message,
		}
	]


def extract_text(response_json: dict[str, object]) -> str:
	choices = response_json.get("choices", [])
	if not isinstance(choices, list) or not choices:
		raise RuntimeError(f"No text response returned by OpenRouter: {response_json}")

	first_choice = choices[0]
	if not isinstance(first_choice, dict):
		raise RuntimeError(f"No text response returned by OpenRouter: {response_json}")

	message = first_choice.get("message", {})
	if not isinstance(message, dict):
		raise RuntimeError(f"No text response returned by OpenRouter: {response_json}")

	content = message.get("content", "")
	if isinstance(content, str) and content.strip():
		return content.strip()

	raise RuntimeError(f"No text response returned by OpenRouter: {response_json}")


def send_response(api_key: str, model_name: str, messages: list[dict[str, object]]) -> str:
	payload = {
		"model": model_name,
		"max_tokens": DEFAULT_MAX_TOKENS,
		"messages": [
			{"role": "system", "content": DEVELOPER_MESSAGE},
			*messages,
		],
	}
	request = urllib.request.Request(
		OPENAI_COMPAT_CHAT_URL,
		data=json.dumps(payload).encode("utf-8"),
		headers={
			"Authorization": f"Bearer {api_key}",
			"HTTP-Referer": os.getenv("OPENROUTER_HTTP_REFERER", "http://localhost"),
			"X-OpenRouter-Title": os.getenv("OPENROUTER_TITLE", "Console Chatbot"),
			"Content-Type": "application/json",
			"Accept": "application/json",
		},
		method="POST",
	)

	try:
		with urllib.request.urlopen(request, timeout=60) as response:
			response_json = json.loads(response.read().decode("utf-8"))
	except urllib.error.HTTPError as exc:
		error_body = exc.read().decode("utf-8", errors="replace")
		raise RuntimeError(f"OpenRouter API request failed ({exc.code}): {error_body}") from exc
	except urllib.error.URLError as exc:
		raise RuntimeError(f"Network error calling OpenRouter API: {exc.reason}") from exc

	return extract_text(response_json)


def run_chat() -> None:
	api_key = get_api_key()
	model_name = os.getenv("OPENROUTER_MODEL", DEFAULT_MODEL)
	history: list[dict[str, object]] = []

	print("OpenRouter chatbot ready. Type 'exit' or 'quit' to stop.")

	while True:
		try:
			user_message = input("You: ").strip()
		except (EOFError, KeyboardInterrupt):
			print("\nGoodbye.")
			return

		if not user_message:
			continue

		if user_message.lower() in {"exit", "quit"}:
			print("Goodbye.")
			return

		messages = build_messages(history, user_message)

		try:
			reply_text = send_response(api_key, model_name, messages)
		except Exception as exc:
			print(f"Error: {exc}")
			continue

		history.append({"role": "user", "content": user_message})
		history.append({"role": "assistant", "content": reply_text})
		print(f"Bot: {reply_text}")


if __name__ == "__main__":
	run_chat()
