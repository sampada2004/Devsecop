import os
import time
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import ollama
import pdfplumber
from PIL import Image
import pytesseract
import io

from Security.Decrypt import decrypt_file
from monitoring import monitor_rag_stage, monitor_llm, record_event, measure_query

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


@monitor_rag_stage(stage="ocr_extraction")
def extract_text_from_images_in_pdf(pdf_path):
    """Extract text from images inside PDF pages using pdfplumber + pytesseract OCR."""
    ocr_texts = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            
            images = page.images
            for img_index, img in enumerate(images):
               
                x0, y0, x1, y1 = img['x0'], img['y0'], img['x1'], img['y1']
                cropped_image = page.within_bbox((x0, y0, x1, y1)).to_image(resolution=300)
                pil_image = cropped_image.original
                text = pytesseract.image_to_string(pil_image)
                if text.strip():
                    ocr_texts.append(text.strip())
    
    record_event("pdf_ocr_processed", "success")
    return "\n".join(ocr_texts)

# Skip decryption for testing monitoring
# decrypt_file("data/circulars2.enc", "data/circulars2.pdf")

# Use a sample PDF if available, otherwise create a dummy one
import os
pdf_file_path = "data/circulars2.pdf"

# If the PDF doesn't exist, create a dummy one for testing
if not os.path.exists(pdf_file_path):
    os.makedirs(os.path.dirname(pdf_file_path), exist_ok=True)
    with open(pdf_file_path, 'w') as f:
        f.write("This is a dummy PDF for testing monitoring.")
    print(f"Created dummy file at {pdf_file_path} for testing")

ocr_text = extract_text_from_images_in_pdf(pdf_file_path)

loader = PyPDFLoader(pdf_file_path)
pages = loader.load()

if ocr_text.strip():
    from langchain.schema import Document
    pages.append(Document(page_content=ocr_text))

text_splitter = CharacterTextSplitter(chunk_size=1500, chunk_overlap=300)
docs = text_splitter.split_documents(pages)

model = SentenceTransformer("all-MiniLM-L6-v2")
texts = [doc.page_content for doc in docs]
embeddings = model.encode(texts)

dimension = embeddings[0].shape[0]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

@measure_query(query_type="rag_query")
def ask_question(query):
    # Embedding generation
    start_embedding_time = time.time()
    try:
        query_embedding = model.encode([query])
        record_event("embedding_generated", "success")
    except Exception as e:
        record_event("embedding_generated", "failure")
        raise e
    
    # Vector search
    start_search_time = time.time()
    try:
        D, I = index.search(np.array(query_embedding), k=4)
        search_time = time.time() - start_search_time
        record_event("vector_search_completed", "success")
    except Exception as e:
        record_event("vector_search_completed", "failure")
        raise e
    
    # Context preparation
    top_chunks = "\n".join([texts[i] for i in I[0]])
    
    prompt = f"""Answer the question based on the following content:
{top_chunks}

Question: {query}
Answer:"""
    
    # LLM generation
    try:
        start_llm_time = time.time()
        response = ollama.chat(model="mistral", messages=[
            {"role": "user", "content": prompt}
        ])
        llm_time = time.time() - start_llm_time
        record_event("llm_response_generated", "success")
        return response["message"]["content"]
    except Exception as e:
        record_event("llm_response_generated", "failure")
        raise e

if __name__ == "__main__":
    print("RAG system ready! Type a question (or 'exit' to quit):")
    while True:
        user_input = input(">>> ")
        if user_input.lower() in ['exit', 'quit']:
            break
        answer = ask_question(user_input)
        print("\n💬 Answer:", answer, "\n")
