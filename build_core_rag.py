# -*- coding: utf-8 -*-
"""Build core bilingual RAG for Render (all-MiniLM-L6-v2, fits 512MB)"""
import sys, io, os
try: sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
except: pass
import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path='rag_db')

for c in client.list_collections():
    client.delete_collection(c.name)

col = client.create_collection('lo_au_v3', metadata={"hnsw:space": "cosine"})

core = [
    'Hoa 2024: anxiety prevalence 40.6% among 3,910 high school students in Hanoi Vietnam using GAD-7 (alpha=0.916). Female mean 1.74 vs male 1.50 (p<0.01). Qualitative interviews found exam pressure, social stigma, family expectations.',
    'V-NAMHS 2022: national survey 5,996 adolescents 10-17 years 38 provinces Vietnam. DISC-5/DSM-5 diagnostic. Mental health problems 21.7%, anxiety 18.6%, anxiety disorder 2.3%, MDD 0.9%, any disorder 3.3%. Only 8.4% accessed services.',
    'Ngo Anh Vinh 2024: 845 ethnic minority boarding school students Lang Son Vietnam. DASS-21. Anxiety 54.4%, depression 59.0%, stress 24.7%. ACEs 48.9%. Poor friendship linked to anxiety.',
    'Pham 2024: 273+273 adolescents social support facilities Hue Vietnam. Emotional care beta=-0.40 for anxiety (p<0.001). Physical care NOT significant.',
    'Hoang Trung Hoc 2025: 8,473 adolescents 6 provinces Vietnam. During COVID anxiety 41.5%, after 25.4%. Risk: poor parent-child, excessive electronics, poor sleep.',
    'GBD ASEAN 2025 Lancet: 10 ASEAN countries. 80.4 million cases, 70% increase 1990-2021. Vietnam 10.1%, Malaysia 13.2%. Age 10-14: 16.3% DALYs. 11.2M DALYs (8.54-14.3).',
    'Puyat 2025: Filipino youth depression 9.6% (2013) to 20.9% (2021). Female 24.3%, LGBTQ+ 32.3%, poorest 25.1%. n=30,127.',
    'Zhu 2025 BMC China: 9,831 students Suzhou. Depression 14.5%+5.8%. Sleep <5h AOR=13.710. Outdoor 2-3h AOR=0.557. Single parent AOR=1.434.',
    'Mudunna 2025 Lancet SEA: South Asia 8 countries. Prevalence 1.5-81.6%. Stigma biggest barrier.',
    'Anderson 2025: 61 articles review. 31.9% adolescents anxiety. Gen Z highest. 48/52 studies academic pressure linked poor mental health.',
    'Zhameden 2025: 6 RCTs LMIC 1,587 students. CBT 3/4 depression but 1/4 anxiety. GRADE very low. NO RCT from Vietnam.',
    'Jenkins 2023: 75 multiethnic students San Diego. Anxiety 50.6% depression 44%. Female>male p=0.002. Gender violence COVID discrimination.',
    'Saikia 2023: 360 students Assam India. Anxiety 24.4%. Male>female 30% vs 18.9% opposite to literature. Single parent alcohol gaming.',
    'NSCH 2020: US national n=55,162. Anxiety 16.1% diagnosed. Increased 61% 2016-2023. Female 20.1% male 12.3%. 10x difficulty friends.',
    'Alharbi 2019: 1,245 students Saudi Arabia. Anxiety 63.5% depression 74% low threshold. Female>male P<0.001.',
    'Nakie 2022: 849 students Ethiopia. Anxiety 66.7% depression 41.4% stress 52.2%. Khat AOR=5.6 smoking AOR=4.8. BMC Q1.',
    'Chen 2023: 63,205 students Western China. Anxiety 13.9% depression 23%. Bullying sleep gaming risks. BMC Q1.',
    'Wen 2020: 900 rural China. LPA 3 profiles. Severe anxiety 24.78%. Male>female. School support protective.',
    'Qiu 2022: 2,079 Chinese middle school. Anxiety 13.4% depression 26%. Negative parenting OR=2.01. Low resilience OR=6.74.',
    'Xu 2021: 373,216 students China LARGEST GLOBALLY. Anxiety 9.89%. Male>female. Rural 12.80%. COVID worry risk. J Affect Disord Q1.',
    'Bhardwaj 2020: 288 government school India. Anxiety 73.3% HIGHEST. Depression 64.9% stress 74.7%. Low SES.',
    'Screening vs diagnostic Vietnam: GAD-7 40.6%, DASS-21 54.4%, DISC-5 only 2.3%. Difference 17-24 times.',
    'Gender: 8/18 female>male. 3 exceptions male>female: Saikia Wen Xu. V-NAMHS no difference.',
    'Sleep: AOR=13.71 for <5h sleep depression (Zhu China). Outdoor 2-3h protective AOR=0.557.',
    'Family: emotional care beta=-0.40 (Pham VN). Confidant OR=0.22 (Dong China). Single parent AOR=1.43.',
    'Interventions: 0 RCTs Vietnam. CBT 3/4 depression 1/4 anxiety. GRADE very low. Need school RCT VN.',
    'Service gap: Vietnam 8.4% access. Philippines 2%. Parents 5.1% recognize. ASEAN psychiatrists 0.2-4.3/100K.',
    'Top gaps Vietnam: (1) school RCT (2) GAD-7 vs DISC-5 same sample (3) longitudinal COVID (4) sleep-anxiety (5) parent training.',
    'GAD-7: 7-item anxiety screening 0-21. Mild 5-9 moderate 10-14 severe 15-21. Spitzer 2006.',
    'DASS-21: 21 items depression anxiety stress. Lovibond 1995. Screening tool higher rates than diagnostic.',
    'DISC-5: diagnostic interview DSM-5 criteria. Prevalence 2.3% vs screening 40-54%. Much lower.',
    'PHQ-9: 9-item depression screening 0-27. Spitzer 1999.',
]

ids = [f'c{i}' for i in range(len(core))]
metas = [{'source': 'core', 'type': 'core', 'page_ref': 'summary', 'chunk_index': i} for i in range(len(core))]
embs = model.encode(core).tolist()
col.add(documents=core, embeddings=embs, ids=ids, metadatas=metas)

print(f'Core RAG: {col.count()} entries, DB: {os.path.getsize("rag_db/chroma.sqlite3")//1024}KB')

# Test
tests = [
    ('anxiety Vietnam students','40.6'), ('DISC-5 diagnosis Vietnam','2.3'),
    ('sleep depression risk','13.7'), ('school intervention RCT Vietnam','RCT'),
    ('gender difference anxiety','female'), ('Philippines depression','20.9'),
    ('ASEAN mental disorders','80.4'), ('emotional care mental health','-0.40'),
    ('GAD-7 scale','GAD'), ('service access Vietnam','8.4'),
]
p = 0
for q, kw in tests:
    r = col.query(query_embeddings=model.encode([q]).tolist(), n_results=3, include=['documents','distances'])
    found = kw in ' '.join(r['documents'][0])
    rel = max(0,(1-r['distances'][0][0])*100)
    ok = found and rel >= 50
    if ok: p += 1
    print(f'{"PASS" if ok else "FAIL"} [{rel:.0f}%] {q[:35]:35s} kw={kw}: {"OK" if found else "NO"}')
print(f'\n{p}/{len(tests)} = {p/len(tests)*100:.0f}%')
