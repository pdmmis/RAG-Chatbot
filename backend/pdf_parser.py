from pathlib import Path
from pydantic import BaseModel
import fitz
MAX_SIZE_MB = 10
class ParsedPDF(BaseModel):
    file_name: str
    pages: int
    text: str
def parse_pdf(file_path: Path) -> ParsedPDF:
    if not file_path.exists() or not file_path.is_file():
        raise FileNotFoundError(f"File {file_path} does not exist.")
    if file_path.stat().st_size > MAX_SIZE_MB * 1024 * 1024:
        raise ValueError(f"File size exceeds the maximum limit of {MAX_SIZE_MB} MB.")
    doc = fitz.open(file_path)
    text = ""
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        text += page.get_text()
    parsed_pdf = ParsedPDF(
        file_name=file_path.name,
        pages=doc.page_count,
        text=text
    )
    return parsed_pdf