# -*- coding: utf-8 -*-
"""Test RAG with 170 questions across 7 categories"""
import sys, io
try: sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
except: pass
import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
client = chromadb.PersistentClient(path='rag_db')
col = client.get_collection('lo_au_v3')

tests = {
    'VN': [
        ('Tỷ lệ lo âu ở học sinh THPT Hà Nội?','40,6'),('Lo âu học sinh Hà Nội sau COVID?','40,6'),
        ('Bao nhiêu phần trăm học sinh Hà Nội bị lo âu?','40,6'),('GAD-7 cho kết quả gì ở Hà Nội?','40,6'),
        ('Tỷ lệ rối loạn lo âu DSM-5 tại Việt Nam?','2,3'),('DISC-5 cho tỷ lệ lo âu bao nhiêu?','2,3'),
        ('V-NAMHS tìm thấy gì về lo âu?','21,7'),('Khảo sát quốc gia SKTT Việt Nam?','V-NAMHS'),
        ('Lo âu ở học sinh dân tộc thiểu số?','54,4'),('DTTS Lạng Sơn có tỷ lệ lo âu bao nhiêu?','54,4'),
        ('DASS-21 ở học sinh DTTS Việt Nam?','54,4'),('Trầm cảm ở học sinh DTTS Lạng Sơn?','59'),
        ('Lo âu ở VTN cơ sở bảo trợ xã hội Huế?','22,96'),('Chất lượng chăm sóc và SKTT VTN Huế?','Pham'),
        ('Lo âu ở học sinh TP.HCM?','50,3'),('Nghiên cứu đa trung tâm TP.HCM?','2.631'),
        ('Lo âu VTN Việt Nam trong COVID?','41,5'),('Lo âu VTN Việt Nam sau COVID?','25,4'),
        ('So sánh lo âu trước và sau COVID ở Việt Nam?','giảm'),('Hoàng Trung Học nghiên cứu gì?','8.473'),
        ('Phụ huynh Việt Nam nhận ra con bị lo âu?','5,1'),('Bao nhiêu VTN VN tiếp cận dịch vụ SKTT?','8,4'),
        ('ACEs ở học sinh dân tộc thiểu số VN?','48,9'),('Trải nghiệm bất lợi thời thơ ấu DTTS?','ACE'),
        ('Cronbach alpha của GAD-7 tại Việt Nam?','0,916'),('Điểm GAD-7 nam vs nữ ở Hà Nội?','1,74'),
    ],
    'Intl': [
        ('Trầm cảm ở thanh niên Philippines?','20,9'),('Philippines trầm cảm tăng gấp đôi?','9,6'),
        ('Tỷ lệ RLTT tại ASEAN?','11,9'),('ASEAN có bao nhiêu ca RLTT?','80,4'),
        ('Việt Nam thấp nhất ASEAN về RLTT?','10,1'),('Malaysia cao nhất ASEAN?','13,2'),
        ('DALYs do RLTT tại ASEAN?','11,2'),('Nhóm 10-14 tuổi ASEAN gánh nặng?','16,3'),
        ('Trầm cảm HS Trung Quốc Suzhou?','14,5'),('PHQ-9 ở HS Trung Quốc?','14,5'),
        ('SKTT VTN Nam Á?','81,6'),('LGBTQ+ trầm cảm Philippines?','32,3'),
        ('Nữ trầm cảm Philippines?','24,3'),('Nghèo và trầm cảm Philippines?','25,1'),
        ('Xu hướng RLTT ASEAN 1990-2021?','70'),('GBD 2021 tìm thấy gì ở ASEAN?','80,4'),
        ('Bác sĩ tâm thần ASEAN?','0,2'),('Kỳ thị SKTT tại Nam Á?','kỳ thị'),
        ('Zhu nghiên cứu gì?','Suzhou'),('Puyat nghiên cứu gì?','Filipino'),
    ],
    'Risk': [
        ('Giới tính ảnh hưởng lo âu?','nữ'),('Nữ giới lo âu cao hơn nam giới?','nữ'),
        ('Thiếu ngủ gây trầm cảm?','13,7'),('Ngủ dưới 5 giờ nguy cơ?','13,7'),
        ('Hoạt động ngoài trời bảo vệ SKTT?','ngoài trời'),
        ('Gia đình đơn thân và lo âu?','1,43'),('Gia đình tái hôn nguy cơ?','1,83'),
        ('Chăm sóc cảm xúc vs thể chất?','-0,40'),('Có người tâm sự giảm trầm cảm?','0,22'),
        ('ACEs và lo âu?','ACE'),('Áp lực học tập gây lo âu?','học tập'),
        ('Mạng xã hội và lo âu VTN?','mạng xã hội'),('Thế hệ Z lo âu cao nhất?','Gen Z'),
        ('Nghèo đói và trầm cảm?','nghèo'),('Bắt nạt gây lo âu?','bắt nạt'),
        ('Nhóm nào dễ bị tổn thương nhất?','DTTS'),
    ],
    'Method': [
        ('GAD-7 là gì?','GAD'),('DASS-21 là gì?','DASS'),('DISC-5 là gì?','DISC'),
        ('PHQ-9 là gì?','PHQ'),('CES-D là gì?','CES'),
        ('Sàng lọc khác chẩn đoán?','sàng lọc'),('So sánh sàng lọc và chẩn đoán lo âu VN?','2,3'),
        ('Tại sao tỷ lệ sàng lọc cao hơn chẩn đoán?','sàng lọc'),
        ('RCT là gì?','RCT'),('PRISMA là gì?','PRISMA'),('GRADE là gì?','GRADE'),
        ('Phương pháp hỗn hợp?','hỗn hợp'),('Nghiên cứu cắt ngang?','cắt ngang'),
    ],
    'Interv': [
        ('Can thiệp SKTT trường học?','trường học'),('CBT cho lo âu?','CBT'),
        ('Can thiệp tại LMIC?','LMIC'),('RCT trường học Việt Nam?','RCT'),
        ('Zhameden tìm bao nhiêu RCT?','6'),('Hiệu quả CBT cho trầm cảm?','3/4'),
        ('Hiệu quả CBT cho lo âu?','1/4'),('Anderson khuyến nghị gì?','đa tầng'),
        ('Theo dõi dài hạn can thiệp?','3 tháng'),('Chi phí-hiệu quả can thiệp?','chi phí'),
        ('Điều chỉnh văn hóa can thiệp?','văn hóa'),('Whole-school approach?','school'),
    ],
    'Service': [
        ('Tiếp cận dịch vụ SKTT VN?','8,4'),('Phụ huynh nhận ra con lo âu?','5,1'),
        ('Khoảng trống dịch vụ SKTT VN?','8,4'),('Mental health literacy VN?','hiểu biết'),
        ('Kỳ thị SKTT Việt Nam?','kỳ thị'),('Dịch vụ SKTT Philippines?','2%'),
        ('Chính sách SKTT ASEAN?','chính sách'),('UNICEF báo cáo gì về VN?','UNICEF'),
        ('Sàng lọc SKTT tại trường VN?','sàng lọc'),('Phòng ngừa SKTT VTN?','phòng ngừa'),
    ],
    'Gap': [
        ('Khoảng trống nghiên cứu lo âu VN?','RCT'),('Gap nghiên cứu SKTT Việt Nam?','gap'),
        ('Cần nghiên cứu gì thêm về lo âu HS?','RCT'),('RCT cần thiết tại VN?','RCT'),
        ('Nghiên cứu dọc SKTT VN?','dọc'),('Chuẩn hóa DISC-5 cho VN?','chuẩn hóa'),
        ('Mở rộng NC DTTS ngoài Lạng Sơn?','DTTS'),('NC giấc ngủ-lo âu tại VN?','giấc ngủ'),
        ('Đào tạo phụ huynh chăm sóc cảm xúc?','phụ huynh'),('NC chi phí-hiệu quả can thiệp VN?','chi phí'),
    ],
}

total_p = 0; total_f = 0; total_q = 0
fails = []

for cat, qs in tests.items():
    cp = 0; cf = 0
    for q, kw in qs:
        total_q += 1
        emb = model.encode([q]).tolist()
        r = col.query(query_embeddings=emb, n_results=3, include=['distances','documents'])
        all_text = ' '.join(r['documents'][0]).lower()
        top_rel = max(0, (1 - r['distances'][0][0]) * 100)
        found = kw.lower() in all_text
        ok = found and top_rel >= 45
        if ok:
            cp += 1; total_p += 1
        else:
            cf += 1; total_f += 1
            fails.append(f'  [{cat}] [{top_rel:.0f}%] {q[:50]} kw="{kw}" {"FOUND" if found else "MISS"}')

    t = cp + cf
    print(f'{cat:10s}: {cp:3d}/{t:3d} ({cp/t*100:5.1f}%)')

print(f'\nTOTAL: {total_p}/{total_q} PASS ({total_p/total_q*100:.1f}%)')
print(f'\nFAILED ({total_f}):')
for fl in fails[:20]:
    print(fl)
if len(fails) > 20:
    print(f'  ... +{len(fails)-20} more')
