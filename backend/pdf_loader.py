import fitz
from pathlib import Path


def extract_text_from_pdf(pdf_path):
    pdf_path = Path(pdf_path)

    document = fitz.open(pdf_path)

    pages = []

    for page_number, page in enumerate(document):
        text = page.get_text()

        if text.strip():
            pages.append({
                "page": page_number + 1,
                "text": text
            })

    document.close()

    return pages

if __name__ == "__main__":

    pdf_path = r"E:\StudyMate-AI\data\documents\Sql_learning.pdf"

    pages = extract_text_from_pdf(pdf_path)

    print(f"Total pages extracted: {len(pages)}")

    for page in pages[:2]:
        print("\n" + "=" * 60)
        print(f"PAGE {page['page']}")
        print("=" * 60)
        print(page["text"][:1000])