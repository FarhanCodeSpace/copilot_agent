# OpenRouter Agent Examples

Small Python examples for building console agents with [OpenRouter](https://openrouter.ai/). The repository progresses from a single model request to structured output, conversational context, email classification, and a reusable action framework.

## What is included

| File                            | Purpose                                                                                       |
| ------------------------------- | --------------------------------------------------------------------------------------------- |
| `response_demo.py`              | Minimal request that asks the model a question and prints the response.                       |
| `basic_agent.py`                | Shared OpenRouter request helper used by several examples.                                    |
| `conversation_demo.py`          | Interactive chatbot that keeps recent conversation history.                                   |
| `structured_outputs.py`         | Example of requesting a Pydantic-shaped response.                                             |
| `email_agent.py`                | Simple email classification flow with mock actions.                                           |
| `agentic_framework.py`          | Reusable framework for selecting and executing configured actions, including approval checks. |
| `email_agent_framework_demo.py` | Email agent built on `AgentFramework`, with a permission check before deletion.               |

The examples print or simulate actions locally. They do not connect to a real mailbox or send, label, delete, or mark messages in an external email service.

## Requirements

- Python 3.10 or newer
- An [OpenRouter](https://openrouter.ai/) API key
- Internet access for API requests

Install the Python dependencies:

```bash
python -m pip install python-dotenv requests pydantic
```

## Configuration

Create a local `.env` file in the project directory:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
OPENROUTER_MODEL=moonshotai/kimi-k3
OPENROUTER_MAX_TOKENS=256
```

`OPENROUTER_MODEL` and `OPENROUTER_MAX_TOKENS` are optional. The examples use the model shown above and `256` tokens by default.

Keep `.env` private. Never commit an API key; if a key has been exposed, revoke it in OpenRouter and create a replacement.

## Run an example

Run commands from the repository directory:

```bash
python response_demo.py
python conversation_demo.py
python email_agent.py
python email_agent_framework_demo.py
```

`conversation_demo.py`, `email_agent.py`, and `email_agent_framework_demo.py` are interactive. Follow the prompts and type `exit` or `quit` in the chatbot to stop it. `structured_outputs.py` and `response_demo.py` execute immediately when run.

## Framework usage

`AgentFramework` accepts a list of actions. Each action has:

- `action_name`: the exact name the model must return
- `action_description`: guidance shown to the model
- `action_function`: the Python callable to execute
- `require_permission`: whether approval is required first

The framework separates decision-making from execution, validates action definitions, and rejects unknown model decisions. Inject `response_client` and `approval_handler` when testing without making network requests or reading console input.

## Notes

These scripts are learning examples rather than a production agent implementation. Before using an agent with real data or side effects, add authentication safeguards, input validation, structured error handling, tests, logging, and explicit user confirmation for destructive operations.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
