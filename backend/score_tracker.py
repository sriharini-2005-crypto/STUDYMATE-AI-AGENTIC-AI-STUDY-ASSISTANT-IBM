import json
import os


SCORE_FILE = "quiz_scores.json"


class QuizScoreTracker:

    def __init__(self):

        if os.path.exists(SCORE_FILE):

            with open(SCORE_FILE, "r") as file:
                self.scores = json.load(file)

        else:

            self.scores = []


    def add_score(self, topic, score, total):

        percentage = (score / total) * 100

        record = {
            "topic": topic,
            "score": score,
            "total": total,
            "percentage": round(percentage, 2)
        }

        self.scores.append(record)

        self._save()

        return record


    def get_scores(self):

        return self.scores


    def get_weak_topics(self, threshold=60):

        weak_topics = []

        for record in self.scores:

            if record["percentage"] < threshold:

                weak_topics.append(record)

        return weak_topics


    def _save(self):

        with open(SCORE_FILE, "w") as file:

            json.dump(
                self.scores,
                file,
                indent=4
            )


if __name__ == "__main__":

    tracker = QuizScoreTracker()

    result = tracker.add_score(
        "SQL Joins",
        7,
        10
    )

    print("=" * 60)
    print("QUIZ SCORE TRACKER")
    print("=" * 60)

    print("\nLatest Score:")
    print(result)

    print("\nAll Scores:")

    for score in tracker.get_scores():

        print(score)

    print("\nWeak Topics:")

    weak_topics = tracker.get_weak_topics()

    for topic in weak_topics:

        print(topic)