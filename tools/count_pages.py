
from pathlib import Path
import csv
import hashlib
from pypdf import PdfReader

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
MANIFEST = PROJECT_ROOT / "data" / "manifest.csv"

def sha256_file(file_path):
    """Calculate SHA-256 hash to identify duplicate files."""
    digest = hashlib.sha256()

    with file_path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def main():
    if not RAW_DIR.exists():
        print(f"Error: Folder not found: {RAW_DIR}")
        return

    pdf_files = sorted(RAW_DIR.rglob("*.pdf"))

    if not pdf_files:
        print("No PDF files found in data/raw/")
        return

    MANIFEST.parent.mkdir(parents=True, exist_ok=True)

    total_pages = 0
    seen_hashes = set()

    with MANIFEST.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow([
            "file",
            "relative_path",
            "pages",
            "bytes",
            "sha256",
            "duplicate",
            "status",
            "error"
        ])

        for pdf_path in pdf_files:
            relative_path = pdf_path.relative_to(PROJECT_ROOT)
            file_hash = sha256_file(pdf_path)
            duplicate = file_hash in seen_hashes
            seen_hashes.add(file_hash)

            try:
                reader = PdfReader(str(pdf_path), strict=False)

                if reader.is_encrypted:
                    raise ValueError("Encrypted PDF")

                pages = len(reader.pages)
                total_pages += pages

                writer.writerow([
                    pdf_path.name,
                    str(relative_path),
                    pages,
                    pdf_path.stat().st_size,
                    file_hash,
                    duplicate,
                    "OK",
                    ""
                ])

                print(f"{relative_path}: {pages} pages"
                      f"{' [DUPLICATE]' if duplicate else ''}")

            except Exception as error:
                writer.writerow([
                    pdf_path.name,
                    str(relative_path),
                    0,
                    pdf_path.stat().st_size,
                    file_hash,
                    duplicate,
                    "ERROR",
                    str(error)
                ])

                print(f"ERROR: {relative_path}: {error}")

    print("\n--- DATASET SUMMARY ---")
    print(f"PDF files found: {len(pdf_files)}")
    print(f"Total pages in readable PDFs: {total_pages}")
    print(f"Manifest saved to: {MANIFEST}")


if __name__ == "__main__":
    main()
