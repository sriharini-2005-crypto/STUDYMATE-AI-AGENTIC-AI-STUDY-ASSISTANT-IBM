from pdf_loader import extract_text_from_pdf
from chunker import create_chunks

from sentence_transformers import SentenceTransformer
import faiss
import pickle
from pathlib import Path


# ==========================================
# PROJECT PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

PDF_PATH = BASE_DIR / "data" / "documents" / "Sql_learning.pdf"

PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================
# 1. LOAD PDF
# ==========================================

print("Loading PDF...")

pages = extract_text_from_pdf(PDF_PATH)

print(f"Total pages: {len(pages)}")


# ==========================================
# 2. CREATE CHUNKS
# ==========================================

print("Creating chunks...")

chunks = create_chunks(pages)

print(f"Total chunks: {len(chunks)}")


# ==========================================
# 3. LOAD EMBEDDING MODEL
# ==========================================

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded.")


# ==========================================
# 4. CREATE EMBEDDINGS
# ==========================================

texts = [chunk["text"] for chunk in chunks]

print("Creating embeddings...")

embeddings = model.encode(
    texts,
    convert_to_numpy=True,
    show_progress_bar=True
)

print(f"Embedding shape: {embeddings.shape}")


# ==========================================
# 5. CREATE FAISS INDEX
# ==========================================

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(embeddings)

print(f"Vectors stored in FAISS: {index.ntotal}")


# ==========================================
# 6. SAVE FAISS INDEX
# ==========================================

index_path = PROCESSED_DIR / "sql_index.faiss"

faiss.write_index(
    index,
    str(index_path)
)


# ==========================================
# 7. SAVE CHUNKS
# ==========================================

chunks_path = PROCESSED_DIR / "chunks.pkl"

with open(chunks_path, "wb") as f:
    pickle.dump(chunks, f)


# ==========================================
# 8. VERIFY FILES
# ==========================================

print()
print("==========================================")
print("FILES SAVED")
print("==========================================")

print(f"FAISS index : {index_path}")
print(f"Chunks      : {chunks_path}")

print()
print("FAISS exists :", index_path.exists())
print("Chunks exists:", chunks_path.exists())
print()
print("Vector store created successfully!")