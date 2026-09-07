from pdf_loader import extract_text_from_pdf


def create_chunks(pages, chunk_size=1000, overlap=200):

    chunks = []

    for page in pages:

        text = page["text"]

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk_text = text[start:end]

            chunks.append({
                "page": page["page"],
                "text": chunk_text
            })

            start = end - overlap

    return chunks


if __name__ == "__main__":

    pdf_path = r"E:\StudyMate-AI\data\documents\Sql_learning.pdf"

    pages = extract_text_from_pdf(pdf_path)

    chunks = create_chunks(pages)

    print(f"Total pages: {len(pages)}")
    print(f"Total chunks created: {len(chunks)}")

    for i, chunk in enumerate(chunks[:3]):

        print("\n" + "=" * 60)
        print(f"CHUNK {i + 1}")
        print(f"PAGE: {chunk['page']}")
        print("=" * 60)

        print(chunk["text"])