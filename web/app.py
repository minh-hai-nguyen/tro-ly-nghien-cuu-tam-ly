# -*- coding: utf-8 -*-
"""
Trợ lý Nghiên cứu Tâm lý học — Web tĩnh (không đăng nhập)
RAG chatbot + Tổng hợp liên bài + Thư viện
"""
import os, sys, json
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
import chromadb
from sentence_transformers import SentenceTransformer

BASE_DIR = Path(__file__).parent.parent
RAG_DB = str(BASE_DIR / 'rag_db')
DOCS_DIR = Path(__file__).parent / 'docs'
COLLECTION = 'lo_au_v3'

SOURCE_MAP = {
    'fpubh-12-1232856.pdf': {'title': 'Hoa và cs. (2024) — Lo âu HS THPT Hà Nội', 'journal': 'Frontiers in Public Health', 'translation_pdf': 'DICH_Hoa_2024_Frontiers.pdf', 'translation_docx': 'DICH_Hoa_2024_Frontiers.docx', 'original_pdf': 'GOC_Hoa_2024_Frontiers.pdf', 'url': 'https://doi.org/10.3389/fpubh.2024.1232856'},
    'DICH_Hoa_2024_Frontiers_LoAu_THPT_HaNoi.md': {'title': 'Hoa và cs. (2024) — Lo âu HS THPT Hà Nội [Bản dịch]', 'journal': 'Frontiers in Public Health', 'translation_pdf': 'DICH_Hoa_2024_Frontiers.pdf', 'translation_docx': 'DICH_Hoa_2024_Frontiers.docx', 'url': 'https://doi.org/10.3389/fpubh.2024.1232856'},
    'PIIS2468266725000982.pdf': {'title': 'GBD 2021 ASEAN (2025) — 10 RLTT tại ASEAN', 'journal': 'Lancet Public Health', 'translation_pdf': 'DICH_GBD_ASEAN_2025.pdf', 'translation_docx': 'DICH_GBD_ASEAN_2025.docx', 'original_pdf': 'GOC_GBD_ASEAN_2025_Lancet.pdf', 'url': 'https://doi.org/10.1016/S2468-2667(25)00098-2'},
    'DICH_GBD_2021_ASEAN_Lancet_2025.md': {'title': 'GBD 2021 ASEAN (2025) [Bản dịch]', 'journal': 'Lancet Public Health', 'translation_pdf': 'DICH_GBD_ASEAN_2025.pdf', 'url': 'https://doi.org/10.1016/S2468-2667(25)00098-2'},
    'journal.pone.0316825.pdf': {'title': 'Zhameden và cs. (2025) — Can thiệp trường học LMIC', 'journal': 'PLOS ONE', 'translation_pdf': 'DICH_Zhameden_2025.pdf', 'translation_docx': 'DICH_Zhameden_2025.docx', 'original_pdf': 'GOC_Zhameden_2025_PLOSONE.pdf', 'url': 'https://doi.org/10.1371/journal.pone.0316825'},
    'DICH_Zhameden_2025_CanThiep_TruongHoc_LMIC.md': {'title': 'Zhameden và cs. (2025) [Bản dịch]', 'journal': 'PLOS ONE', 'translation_pdf': 'DICH_Zhameden_2025.pdf', 'url': 'https://doi.org/10.1371/journal.pone.0316825'},
    'Child Adoles Psych Nursing - 2025 - Anderson - Contributing Factors to the Rise in Adolescent Anxiety and Associated Mental.pdf': {'title': 'Anderson và cs. (2025) — Yếu tố gia tăng lo âu VTN', 'journal': 'J Child Adolesc Psychiatric Nursing', 'translation_docx': 'DICH_Anderson_2025.docx', 'url': 'https://doi.org/10.1111/jcap.70009'},
    'DICH_Anderson_2025_YeuTo_GiaTang_LoAu_VTN.md': {'title': 'Anderson và cs. (2025) [Bản dịch]', 'journal': 'J Child Adolesc Psychiatric Nursing', 'translation_docx': 'DICH_Anderson_2025.docx', 'url': 'https://doi.org/10.1111/jcap.70009'},
    'VNAMHS-Report_Eng_15-Feb-2023.pdf': {'title': 'V-NAMHS (2022) — SKTT VTN Việt Nam', 'journal': 'Viện XHH + UQ + Johns Hopkins', 'translation_pdf': 'DICH_VNAMHS_2022.pdf', 'translation_docx': 'DICH_VNAMHS_2022.docx', 'original_pdf': 'GOC_VNAMHS_2022.pdf', 'url': 'https://qcmhr.org/docman/reports/15-vnamhs-report-eng-15-feb-2023/file'},
    'DICH_VNAMHS_2022_DayDu.md': {'title': 'V-NAMHS (2022) [Bản dịch]', 'journal': 'Viện XHH', 'translation_pdf': 'DICH_VNAMHS_2022.pdf', 'url': 'https://qcmhr.org/docman/reports/15-vnamhs-report-eng-15-feb-2023/file'},
    'BAO_CAO_3_BAI_VIET_NAM.md': {'title': 'Báo cáo 3 bài Việt Nam', 'journal': 'Nội bộ'},
    'DATABASE_BAI_BAO_LO_AU.md': {'title': 'CSDL bài báo lo âu', 'journal': 'Nội bộ'},
    'Study on school-related factors impacting mental health and well-being of adolescents in Viet Nam.pdf': {'title': 'UNICEF (2022) — Yếu tố trường học VTN VN', 'journal': 'UNICEF', 'url': 'https://www.unicef.org/vietnam/reports/study-school-related-factors'},
}

app = FastAPI(title='Trợ lý NC Tâm lý học')

print('Loading RAG model...')
MODEL_NAME = os.environ.get('EMBEDDING_MODEL', 'all-MiniLM-L6-v2')
print(f'Loading model: {MODEL_NAME}')
model = SentenceTransformer(MODEL_NAME)
client = chromadb.PersistentClient(path=RAG_DB)
try:
    collection = client.get_collection(COLLECTION)
except:
    collection = client.get_or_create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})
print(f'RAG ready: {collection.count()} chunks')

app.mount('/static', StaticFiles(directory=str(Path(__file__).parent / 'static')), name='static')
app.mount('/docs', StaticFiles(directory=str(DOCS_DIR)), name='docs')

@app.get('/', response_class=HTMLResponse)
async def index():
    with open(Path(__file__).parent / 'static' / 'index.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.post('/api/query')
async def query(request: Request):
    data = await request.json()
    question = data.get('question', '').strip()
    if not question:
        return JSONResponse({'error': 'Empty'}, status_code=400)

    q_emb = model.encode([question]).tolist()
    results = collection.query(query_embeddings=q_emb, n_results=data.get('n_results', 5), include=['documents', 'metadatas', 'distances'])

    sources = []
    for doc_text, meta, dist in zip(results['documents'][0], results['metadatas'][0], results['distances'][0]):
        source_name = meta.get('source', '')
        info = SOURCE_MAP.get(source_name, {'title': source_name, 'journal': ''}).copy()
        relevance = max(0, (1 - dist) * 100)

        links = {}
        if 'translation_pdf' in info: links['translation_pdf'] = f'/docs/{info["translation_pdf"]}'
        if 'translation_docx' in info: links['translation_docx'] = f'/docs/{info["translation_docx"]}'
        if 'original_pdf' in info: links['original_pdf'] = f'/docs/{info["original_pdf"]}'
        if 'url' in info: links['original_url'] = info['url']

        page_ref = meta.get('page_ref', '')

        next_q = meta.get('next_question', '')

        sources.append({
            'text': doc_text[:600],
            'relevance': round(relevance, 1),
            'title': info.get('title', source_name),
            'journal': info.get('journal', ''),
            'links': links,
            'page_ref': page_ref,
            'next_question': next_q,
        })

    return JSONResponse({'question': question, 'sources': sources})

@app.get('/api/documents')
async def list_documents():
    docs = []
    for fname in sorted(os.listdir(DOCS_DIR)):
        if not fname.endswith(('.pdf', '.docx')): continue
        info = SOURCE_MAP.get(fname, {'title': fname, 'journal': ''})
        docs.append({'filename': fname, 'title': info.get('title', fname), 'journal': info.get('journal', ''), 'download': f'/docs/{fname}'})
    return JSONResponse(docs)

if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('PORT', 8000))
    uvicorn.run(app, host='0.0.0.0', port=port)
