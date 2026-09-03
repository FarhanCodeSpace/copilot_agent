"""Reusable action-selection and execution framework for agentic workflows."""

from basic_agent import get_genai_response


class AgentFramework:
    """Choose and execute one configured action for a user prompt."""

    REQUIRED_ACTION_KEYS = {
        "action_name",
        "action_description",
        "action_function",
        "require_permission",
    }

    def __init__(
        self,
        actions,
        *,
        developer_prompt_elements=None,
        response_client=get_genai_response,
        approval_handler=None,
    ):
        self.actions = self._validate_actions(actions)
        self._actions_by_name = {action["action_name"]: action for action in self.actions}
        self.developer_prompt_elements = dict(developer_prompt_elements or {})
        self.response_client = response_client
        self.approval_handler = approval_handler or self._console_approval

    @classmethod
    def _validate_actions(cls, actions):
        validated_actions = list(actions)
        action_names = set()

        for action in validated_actions:
            missing_keys = cls.REQUIRED_ACTION_KEYS - action.keys()
            if missing_keys:
                raise ValueError(
                    f"Action is missing required keys: {sorted(missing_keys)}"
                )

            action_name = action["action_name"]
            if not isinstance(action_name, str) or not action_name.strip():
                raise ValueError("action_name must be a non-empty string")
            if action_name in action_names:
                raise ValueError(f"Duplicate action_name: {action_name}")
            if not callable(action["action_function"]):
                raise TypeError(f"action_function for {action_name} must be callable")
            if not isinstance(action["require_permission"], bool):
                raise TypeError(f"require_permission for {action_name} must be a bool")

            action_names.add(action_name)

        if not validated_actions:
            raise ValueError("At least one action is required")
        return validated_actions

    def build_developer_prompt(self):
        elements = self.developer_prompt_elements
        sections = []

        if elements.get("role"):
            sections.append(str(elements["role"]))
        if elements.get("objective"):
            sections.append(f"Objective:\n{elements['objective']}")
        if elements.get("instructions"):
            sections.append(self._format_value("Instructions", elements["instructions"]))

        action_lines = [
            f"- {action['action_name']}: {action['action_description']}"
            for action in self.actions
        ]
        sections.append(
            "Available actions:\n"
            + "\n".join(action_lines)
        )

        output_format = elements.get(
            "output_format",
            "Respond with ONLY the action name. Do not include any explanation.",
        )
        sections.append(self._format_value("Output format", output_format))

        if elements.get("additional_context"):
            sections.append(
                self._format_value("Additional context", elements["additional_context"])
            )

        return "\n\n".join(sections)

    @staticmethod
    def _format_value(title, value):
        if isinstance(value, (list, tuple)):
            value = "\n".join(f"- {item}" for item in value)
        return f"{title}:\n{value}"

    def make_decision(self, user_prompt):
        response = self.response_client(self.build_developer_prompt(), user_prompt)
        return response.strip().splitlines()[0].strip()

    def execute_decision(self, decision, *args, **kwargs):
        action_name = decision.strip()
        action = self._actions_by_name.get(action_name)
        if action is None:
            raise ValueError(f"Unknown action selected by agent: {action_name}")

        if action["require_permission"] and not self.approval_handler(action):
            return None

        return action["action_function"](*args, **kwargs)

    def run(self, user_prompt, *args, **kwargs):
        decision = self.make_decision(user_prompt)
        return self.execute_decision(decision, *args, **kwargs)

    @staticmethod
    def _console_approval(action):
        answer = input(
            f"Allow the agent to execute {action['action_name']}? (Y/n): "
        )
        return answer.strip().lower() in {"", "y", "yes"}