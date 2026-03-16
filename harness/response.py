class HarnessResponse:
    def __init__(self, text, input_tokens=0, output_tokens=0):
        self.msgs = [HarnessMessage(text)]
        self.info = {
            "usage": {
                "prompt_tokens": input_tokens,
                "completion_tokens": output_tokens,
            }
        }


class HarnessMessage:
    def __init__(self, content):
        self.content = content


class HarnessBaseMessage:
    def __init__(self, role_name="User", content="", image_list=None):
        self.role_name = role_name
        self.content = content
        self.image_list = image_list or []

    @staticmethod
    def make_user_message(role_name="User", content="", image_list=None):
        return HarnessBaseMessage(
            role_name=role_name,
            content=content,
            image_list=image_list,
        )
