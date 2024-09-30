import pdfplumber

from oocana import Context
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def main(inputs: dict, context: Context):
  pdf_file_path = inputs["pdf_file"]
  docs: list[Document] = []

  with pdfplumber.open(pdf_file_path) as pdf_file:
    for page in pdf_file.pages:
      page_content = page.extract_text_simple()
      docs.append(Document(
        page_content=page_content,
      ))

  text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=500,
  )
  docs = text_splitter.split_documents(docs)

  return { "out": docs }
