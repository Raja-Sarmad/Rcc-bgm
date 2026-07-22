from pypdf import PdfReader
import os

pdf_files = [
    r"i:\talha rcc mogul\rcc\Rcc-bgm\Content_pdf\RCC-BGM_About_Us_SEO_Content_2_Pages_Expanded.pdf",
    r"i:\talha rcc mogul\rcc\Rcc-bgm\Content_pdf\RCC-BGM_BGM_Division_SEO_Content_3_Pages.pdf",
    r"i:\talha rcc mogul\rcc\Rcc-bgm\Content_pdf\RCC-BGM_Contact_Page_SEO_Content_3_Pages.pdf",
    r"i:\talha rcc mogul\rcc\Rcc-bgm\Content_pdf\RCC-BGM_Industries_SEO_Content_2_Pages.pdf",
    r"i:\talha rcc mogul\rcc\Rcc-bgm\Content_pdf\RCC-BGM_Locations_Hub_SEO_Content_3_Pages.pdf",
    r"i:\talha rcc mogul\rcc\Rcc-bgm\Content_pdf\RCC-BGM_Why_RCC-BGM_SEO_Content_2_Pages_Expanded.pdf",
    r"i:\talha rcc mogul\rcc\Rcc-bgm\RCC-BGM_Complete_Remaining_Website_Pages_SEO_Content.pdf"
]

for pdf_path in pdf_files:
    if os.path.exists(pdf_path):
        print(f"\n{'='*80}\nFILE: {os.path.basename(pdf_path)}\n{'='*80}\n")
        reader = PdfReader(pdf_path)
        for page_num, page in enumerate(reader.pages, 1):
            text = page.extract_text()
            print(f"--- PAGE {page_num} ---\n{text}\n")
    else:
        print(f"File not found: {pdf_path}")
