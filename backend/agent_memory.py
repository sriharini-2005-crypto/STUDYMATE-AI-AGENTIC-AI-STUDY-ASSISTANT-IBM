from memory import ConversationMemory
from llm_agent import StudyMateAgent


class StudyMateAgentWithMemory:

    def __init__(self):

        self.agent = StudyMateAgent()
        self.memory = ConversationMemory()

    def chat(self, message):

        # Get previous conversation
        history = self.memory.get_formatted_history()

        # Add previous context to the current message
        if history:

            enhanced_message = f"""
Previous conversation:

{history}

Current student message:

{message}
"""

        else:

            enhanced_message = message

        # Run agent
        response = self.agent.run(enhanced_message)

        # Convert search results to readable text
        if isinstance(response, list):

            answer = "\n\n".join(
                result["text"]
                for result in response
            )

        else:

            answer = response

        # Save conversation
        self.memory.add_message(
            "student",
            message
        )

        self.memory.add_message(
            "assistant",
            answer
        )

        return answer


if __name__ == "__main__":

    agent = StudyMateAgentWithMemory()

    print("=" * 70)
    print("STUDYMATE AI - AGENT + MEMORY")
    print("=" * 70)

    while True:

        message = input("\nStudent: ")

        if message.lower() in ["exit", "quit"]:

            print("Agent stopped.")
            break

        answer = agent.chat(message)

        print("\nStudyMate:")
        print(answer)