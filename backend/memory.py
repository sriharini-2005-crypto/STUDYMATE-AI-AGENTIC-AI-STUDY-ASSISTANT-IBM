class ConversationMemory:

    def __init__(self):
        self.history = []

    def add_message(self, role, message):
        self.history.append({
            "role": role,
            "message": message
        })

    def get_history(self):
        return self.history

    def get_formatted_history(self):
        formatted = []

        for item in self.history:
            formatted.append(
                f"{item['role'].upper()}: {item['message']}"
            )

        return "\n".join(formatted)

    def clear(self):
        self.history = []