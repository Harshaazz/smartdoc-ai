import pytesseract
from PIL import Image
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Pytesseract\tesseract.exe"
)

POPPLER_PATH = r"D:\Tools\poppler\Library\bin"


def extract_text_from_image(image_path):

    image = Image.open(image_path)

    text = pytesseract.image_to_string(image)

    return text.strip()


def extract_text_from_pdf(pdf_path):

    pages = convert_from_path(
        pdf_path,
        poppler_path=POPPLER_PATH
    )

    full_text = ""

    for page in pages:

        text = pytesseract.image_to_string(page)

        full_text += text + "\n"

    return full_text.strip()