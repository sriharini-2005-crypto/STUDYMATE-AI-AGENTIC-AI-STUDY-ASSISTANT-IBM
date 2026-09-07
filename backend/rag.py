from search import search
from memory import ConversationMemory
import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:3b"


# Create conversation memory
memory = ConversationMemory()


def generate_answer(question, top_k=3):

    # -----------------------------------------
    # 1. Search relevant study material
    # -----------------------------------------
    results = search(question, top_k=top_k)

    context_parts = []

    for i, result in enumerate(results):

        context_parts.append(
            f"[Source {i + 1} - Page {result['page']}]\n"
            f"{result['text']}"
        )

    context = "\n\n".join(context_parts)


    # -----------------------------------------
    # 2. Get previous conversation
    # -----------------------------------------
    history = memory.get_formatted_history()

    if not history:
        history = "No previous conversation."


    # -----------------------------------------
    # 3. Create prompt
    # -----------------------------------------
    prompt = f"""
You are StudyMate AI, an intelligent learning assistant.

Answer the student's question using ONLY the information
provided in the study material.

You may use the previous conversation to understand
the student's current question.

If the answer cannot be found in the study material, say:

"I couldn't find this information in the provided study material."

Explain the answer clearly and simply.

----------------------------------------
PREVIOUS CONVERSATION
----------------------------------------

{history}

----------------------------------------
STUDY MATERIAL
----------------------------------------

{context}

----------------------------------------
CURRENT STUDENT QUESTION
----------------------------------------

{question}

----------------------------------------
ANSWER
----------------------------------------
"""


    # -----------------------------------------
    # 4. Send prompt to Ollama
    # -----------------------------------------
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )

    response.raise_for_status()

    answer = response.json()["response"]


    # -----------------------------------------
    # 5. Save conversation to memory
    # -----------------------------------------
    memory.add_message(
        "student",
        question
    )

    memory.add_message(
        "studymate",
        answer
    )


    return answer, results


# -----------------------------------------
# Interactive Chat
# -----------------------------------------

if __name__ == "__main__":

    print("=" * 70)
    print("STUDYMATE AI")
    print("Conversation Memory Enabled")
    print("=" * 70)

    print("\nType 'exit' to stop.\n")

    while True:

        question = input("You: ").strip()

        if question.lower() in ["exit", "quit"]:
            print("\nStudyMate AI: Goodbye! 👋")
            break

        if not question:
            continue

        print("\nStudyMate AI: Thinking...\n")

        answer, results = generate_answer(question)

        print("-" * 70)
        print(answer)
        print("-" * 70)

        print("\nSources:")

        for result in results:
            print(f"- Page {result['page']}")

        print()