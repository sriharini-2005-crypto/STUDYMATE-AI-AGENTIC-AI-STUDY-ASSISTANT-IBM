from search import search
from rag import generate_answer


# --------------------------------------------------
# TOOL 1: SEARCH STUDY MATERIAL
# --------------------------------------------------

def search_study_material(query, top_k=3):

    results = search(query, top_k=top_k)

    formatted_results = []

    for result in results:

        formatted_results.append({
            "page": result["page"],
            "text": result["text"],
            "distance": result["distance"]
        })

    return formatted_results


# --------------------------------------------------
# TOOL 2: GENERATE QUIZ
# --------------------------------------------------

def generate_quiz(topic, number_of_questions=5):

    results = search_study_material(topic, top_k=5)

    context = "\n\n".join(
        result["text"]
        for result in results
    )

    prompt = f"""
You are StudyMate AI, an educational assistant.

Create a quiz based ONLY on the study material below.

Topic:
{topic}

Number of questions:
{number_of_questions}

Study Material:
{context}

Generate {number_of_questions} multiple-choice questions.

For each question provide:

Question:
A)
B)
C)
D)

Correct Answer:
Explanation:

Make the questions useful for a college student.
Include a mixture of easy, medium, and difficult questions.
Do not invent information that is not present in the study material.
"""

    answer = generate_answer(prompt)

    return answer


# --------------------------------------------------
# TEST THE TOOLS
# --------------------------------------------------

if __name__ == "__main__":

    print("=" * 70)
    print("STUDYMATE AI - QUIZ GENERATOR")
    print("=" * 70)

    topic = "SQL joins"

    quiz = generate_quiz(topic, 5)

    print("\n")
    print(quiz)



# --------------------------------------------------
# TOOL 3: CREATE STUDY PLAN
# --------------------------------------------------

def create_study_plan(topic, days=7):

    results = search_study_material(topic, top_k=8)

    context = "\n\n".join(
        result["text"]
        for result in results
    )

    prompt = f"""
You are StudyMate AI, an educational study planner.

Create a {days}-day study plan for:

Topic:
{topic}

Use ONLY the study material provided below.

Study Material:
{context}

Create a practical {days}-day learning plan.

For each day provide:

Day:
Topic:
What to Learn:
Practice Task:

Make the difficulty gradually increase.

The final day should include revision and a mock test.

Do not introduce topics that are completely unrelated
to the provided study material.
"""

    answer = generate_answer(prompt)

    return answer

# --------------------------------------------------
# TEST THE TOOLS
# --------------------------------------------------

if __name__ == "__main__":

    print("=" * 70)
    print("STUDYMATE AI - STUDY PLAN GENERATOR")
    print("=" * 70)

    plan = create_study_plan("SQL", 7)

    print("\n")
    print(plan)