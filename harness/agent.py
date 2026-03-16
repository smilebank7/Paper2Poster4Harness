import os
import subprocess
import tempfile


class HarnessAgent:
    """Drop-in replacement for CAMEL ChatAgent.
    Routes AI calls through Claude Code CLI (subscription-based, no API key needed).
    """

    def __init__(
        self,
        system_message="",
        model=None,
        message_window_size=None,
        token_limit=None,
    ):
        self.system_message = system_message
        self.conversation = []
        self.model = model
        self.message_window_size = message_window_size
        self.token_limit = token_limit

    def reset(self):
        self.conversation = []

    def step(self, prompt_or_message):
        from harness.response import HarnessBaseMessage, HarnessResponse

        if isinstance(prompt_or_message, str):
            content = prompt_or_message
        elif isinstance(prompt_or_message, HarnessBaseMessage):
            content = prompt_or_message.content
        elif hasattr(prompt_or_message, "content"):
            content = prompt_or_message.content
        else:
            content = str(prompt_or_message)

        full_prompt = self._build_prompt(content)
        response_text = self._call_claude(full_prompt)

        self.conversation.append({"role": "user", "content": content})
        self.conversation.append({"role": "assistant", "content": response_text})

        if (
            self.message_window_size
            and len(self.conversation) > self.message_window_size * 2
        ):
            self.conversation = self.conversation[-(self.message_window_size * 2) :]

        input_tokens = len(full_prompt) // 4
        output_tokens = len(response_text) // 4
        return HarnessResponse(response_text, input_tokens, output_tokens)

    def _build_prompt(self, user_content):
        parts = []
        if self.system_message:
            parts.append(
                f"[System Instructions]\n{self.system_message}\n[End System Instructions]\n"
            )
        window = self.message_window_size or 10
        recent = self.conversation[-(window * 2) :] if self.conversation else []
        for msg in recent:
            role = "User" if msg["role"] == "user" else "Assistant"
            parts.append(f"[{role}]\n{msg['content']}\n")
        parts.append(f"[User]\n{user_content}")
        return "\n".join(parts)

    def _call_claude(self, prompt):
        """Call Claude via CLI subprocess."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write(prompt)
            prompt_file = f.name

        try:
            # Try piping to claude CLI
            cmd = (
                f'cat "{prompt_file}" | claude -p --output-format text --no-input '
                "2>/dev/null"
            )
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=600,
            )

            if result.returncode != 0 or not result.stdout.strip():
                # Fallback: direct argument (truncated if needed)
                cmd_alt = [
                    "claude",
                    "-p",
                    prompt[:50000],
                    "--output-format",
                    "text",
                    "--no-input",
                ]
                result = subprocess.run(
                    cmd_alt,
                    capture_output=True,
                    text=True,
                    timeout=600,
                )

            response = result.stdout.strip()
            if not response:
                raise RuntimeError(
                    f"Empty response from Claude CLI. stderr: {result.stderr}"
                )
            return response
        except FileNotFoundError as e:
            raise RuntimeError(
                "Claude CLI ('claude') not found. Install:\n"
                "  npm install -g @anthropic-ai/claude-code\n"
                "Or OpenCode: https://github.com/opencode-ai/opencode"
            ) from e
        except subprocess.TimeoutExpired as e:
            raise RuntimeError("Claude CLI timed out after 600 seconds") from e
        finally:
            os.unlink(prompt_file)
