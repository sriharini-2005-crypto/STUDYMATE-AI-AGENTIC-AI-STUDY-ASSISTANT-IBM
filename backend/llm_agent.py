from ollama import chat

from tools import (
    search_study_material,
    generate_quiz,
    create_study_plan
)


class StudyMateAgent:

    def __init__(self):

        self.model = "llama3.2"

        self.tools = {
            "search": search_study_material,
            "quiz": generate_quiz,
            "study_plan": create_study_plan
        }

    def decide_tool(self, message):

        prompt = f"""
You are the tool-selection system for StudyMate AI.

Choose exactly ONE tool.

Available tools:

1. search
   Use for questions about study material, explanations,
   definitions, examples, or factual questions.

2. quiz
   Use when the student wants questions, MCQs, a quiz,
   or wants to be tested.

3. study_plan
   Use when the student asks for a study plan,
   learning schedule, revision plan, or timetable.

Student message:
{message}

Return ONLY one of these:

search
quiz
study_plan
"""

        response = chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        tool = response["message"]["content"].strip().lower()

        # Safety fallback
        if tool not in self.tools:
            tool = "search"

        return tool

    def run(self, message):

        tool_name = self.decide_tool(message)

        print(f"\nAgent selected: {tool_name}")

        if tool_name == "search":

            return search_study_material(
                message,
                top_k=3
            )

        elif tool_name == "quiz":

            return generate_quiz(
                message,
                number_of_questions=5
            )

        elif tool_name == "study_plan":

            return create_study_plan(
                message,
                days=7
            )


if __name__ == "__main__":

    agent = StudyMateAgent()

    print("=" * 70)
    print("STUDYMATE AI - LLM AGENT")
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