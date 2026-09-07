from tools import search_study_material
from tools import generate_quiz
from tools import create_study_plan


def route_request(message):

    message_lower = message.lower()

    # ----------------------------------------
    # QUIZ
    # ----------------------------------------

    if any(word in message_lower for word in [
        "quiz",
        "questions",
        "mcq",
        "test me"
    ]):

        return "quiz"


    # ----------------------------------------
    # STUDY PLAN
    # ----------------------------------------

    if any(word in message_lower for word in [
        "study plan",
        "learning plan",
        "schedule",
        "study schedule"
    ]):

        return "study_plan"


    # ----------------------------------------
    # DEFAULT → SEARCH
    # ----------------------------------------

    return "search"


def execute_request(message):

    tool = route_request(message)

    print(f"\nSelected Tool: {tool}")

    # ----------------------------------------
    # SEARCH
    # ----------------------------------------

    if tool == "search":

        results = search_study_material(
            message,
            top_k=3
        )

        return results


    # ----------------------------------------
    # QUIZ
    # ----------------------------------------

    elif tool == "quiz":

        return generate_quiz(
            message,
            5
        )


    # ----------------------------------------
    # STUDY PLAN
    # ----------------------------------------

    elif tool == "study_plan":

        return create_study_plan(
            message,
            7
        )


if __name__ == "__main__":

    print("=" * 70)
    print("STUDYMATE AI - TOOL ROUTER")
    print("=" * 70)


    test_messages = [

        "What is INNER JOIN?",

        "Give me 5 SQL questions",

        "Create a 7 day SQL study plan"

    ]


    for message in test_messages:

        print("\n" + "-" * 70)

        print("Student:")
        print(message)

        result = execute_request(message)

        print("\nResult:")

        if isinstance(result, list):

            for i, item in enumerate(result):

                print(f"\nResult {i + 1}")
                print(f"Page: {item['page']}")
                print(item["text"][:300])

        else:

            print(result[:1500])