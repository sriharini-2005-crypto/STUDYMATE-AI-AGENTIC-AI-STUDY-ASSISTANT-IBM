import faiss
import pickle
from sentence_transformers import SentenceTransformer
from pathlib import Path


# ==========================================
# PROJECT PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

PROCESSED_DIR = BASE_DIR / "data" / "processed"

INDEX_PATH = PROCESSED_DIR / "sql_index.faiss"
CHUNKS_PATH = PROCESSED_DIR / "chunks.pkl"


# ==========================================
# LOAD FAISS INDEX
# ==========================================

print("Loading FAISS index...")

index = faiss.read_index(str(INDEX_PATH))

print(f"Vectors loaded: {index.ntotal}")


# ==========================================
# LOAD CHUNKS
# ==========================================

print("Loading chunks...")

with open(CHUNKS_PATH, "rb") as f:
    chunks = pickle.load(f)

print(f"Chunks loaded: {len(chunks)}")


# ==========================================
# LOAD EMBEDDING MODEL
# ==========================================

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded.")


# ==========================================
# SEARCH FUNCTION
# ==========================================

def search(query, top_k=3):

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    )

    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for distance, index_id in zip(distances[0], indices[0]):

        results.append({
            "page": chunks[index_id]["page"],
            "text": chunks[index_id]["text"],
            "distance": float(distance)
        })

    return results


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    query = "What does COUNT(*) do?"

    print()
    print("=" * 70)
    print("QUESTION")
    print("=" * 70)
    print(query)

    results = search(query, top_k=3)

    for i, result in enumerate(results):

        print()
        print("-" * 70)
        print(f"RESULT {i + 1}")
        print(f"PAGE: {result['page']}")
        print(f"DISTANCE: {result['distance']}")
        print("-" * 70)

        print(result["text"])