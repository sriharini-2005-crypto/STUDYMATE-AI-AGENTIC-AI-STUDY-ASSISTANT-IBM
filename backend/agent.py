from tools import (
    search_study_material,
    generate_quiz,
    create_study_plan
)


# --------------------------------------------------
# AGENT
# --------------------------------------------------

class StudyMateAgent:

    def __init__(self):

        self.tools = {
            "search": search_study_material,
            "quiz": generate_quiz,
            "study_plan": create_study_plan
        }


    # --------------------------------------------------
    # DECIDE WHICH TOOL TO USE
    # --------------------------------------------------

    def decide_tool(self, message):

        message_lower = message.lower()

        if any(word in message_lower for word in [
            "quiz",
            "mcq",
            "test me",
            "questions"
        ]):

            return "quiz"


        if any(word in message_lower for word in [
            "study plan",
            "learning plan",
            "study schedule",
            "schedule"
        ]):

            return "study_plan"


        return "search"


    # --------------------------------------------------
    # EXECUTE TOOL
    # --------------------------------------------------

    def run(self, message):

        tool_name = self.decide_tool(message)

        print(f"\nAgent selected: {tool_name}")

        if tool_name == "search":

            result = self.tools["search"](
                message,
                top_k=3
            )

            return result


        elif tool_name == "quiz":

            result = self.tools["quiz"](
                message,
                number_of_questions=5
            )

            return result


        elif tool_name == "study_plan":

            result = self.tools["study_plan"](
                message,
                days=7
            )

            return result


# --------------------------------------------------
# TEST AGENT
# --------------------------------------------------

if __name__ == "__main__":

    agent = StudyMateAgent()

    print("=" * 70)
    print("STUDYMATE AI AGENT")
    print("=" * 70)


    while True:

        message = input("\nStudent: ")

        if message.lower() in ["exit", "quit"]:

            print("Agent stopped.")

            break


        result = agent.run(message)

        print("\nStudyMate:")

        if isinstance(result, list):

            for i, item in enumerate(result):

                print(f"\nResult {i + 1}")
                print(f"Page: {item['page']}")
                print(item["text"][:500])

        else:

            print(result)