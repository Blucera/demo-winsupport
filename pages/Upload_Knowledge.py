from uuid import uuid4

import streamlit as st

from core import is_domain_allowed
from core.documentParser.exceptions.invalidFileType import InvalidFileType
from core.documentParser.pdfParser import PDFParser
from core.embedding_manager import chunk_text, EmbeddingManager

if not is_domain_allowed():
    st.error("This app is not allowed on this domain.")
    st.stop()

# ------ CONFIG -------
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100
COLLECTION_NAME = "docs"

st.header("Upload")
st.caption("Upload PDF to train the AI on your personal data.")

message_placeholder = st.empty()

file_upload = st.file_uploader("Upload PDF(s)", type="pdf")

if file_upload:
    parser = PDFParser()
    try:
        # ----- GETTING TEXT FROM UPLOADED DOC -----
        text = parser.load_document(file_upload)

        print("PDF EXTRACTED TEXT")
        print(text)

        # ----- SPLITTING IN CHUNKS -------
        chunks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)
        print("TEXT CHUNKS")
        print(chunks)

        # ----- PASSING CHUNKS TO EMBEDDING MANAGER ------
        emb_mgr = EmbeddingManager(collection_name=COLLECTION_NAME)
        doc_id = str(uuid4()) + file_upload.name.replace(".pdf", "")
        ids = emb_mgr.upsert_chunks(doc_id, chunks)

        message_placeholder.success("PDF Loaded Successfully!")

    except InvalidFileType as e:
        message_placeholder.error(str(e))
