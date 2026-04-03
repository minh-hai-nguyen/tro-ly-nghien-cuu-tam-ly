# -*- coding: utf-8 -*-
"""Build FULL RAG with multilingual model (paraphrase-multilingual-MiniLM-L12-v2)
For server with enough RAM (>1GB). Includes ALL entries bilingual + Vietnam papers."""
import sys, io, os
try: sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
except: pass
import chromadb
from sentence_transformers import SentenceTransformer

MODEL_NAME = 'paraphrase-multilingual-MiniLM-L12-v2'
DB_PATH = 'rag_db_full'

print(f'Loading model: {MODEL_NAME}...')
model = SentenceTransformer(MODEL_NAME)
print('Model loaded.')

# Clean old DB
if os.path.exists(DB_PATH):
    import shutil
    shutil.rmtree(DB_PATH, ignore_errors=True)
    if os.path.exists(DB_PATH):
        # Windows lock workaround
        import time; time.sleep(1)
        shutil.rmtree(DB_PATH, ignore_errors=True)

client = chromadb.PersistentClient(path=DB_PATH)
col = client.create_collection('lo_au_full', metadata={"hnsw:space": "cosine"})

# ============================================================
# ENTRIES: Bilingual (English + Vietnamese) for maximum recall
# ============================================================
entries = [
    # --- VIETNAM PAPERS ---
    'Hoa 2024: Lo âu 40,6% ở 3.910 học sinh THPT Hà Nội Việt Nam sử dụng GAD-7 (Cronbach alpha=0,916). Nữ điểm TB 1,74 cao hơn nam 1,50 (p<0,01). Phỏng vấn sâu phát hiện áp lực thi cử, kỳ thị xã hội, kỳ vọng gia đình. Frontiers in Public Health Q1. // Hoa 2024: anxiety prevalence 40.6% among 3,910 high school students Hanoi Vietnam GAD-7 alpha=0.916. Female mean 1.74 vs male 1.50 (p<0.01). Exam pressure, social stigma, family expectations.',

    'V-NAMHS 2022: Khảo sát quốc gia đầu tiên về sức khỏe tâm thần thanh thiếu niên Việt Nam. 5.996 thanh thiếu niên 10-17 tuổi, 38 tỉnh. Chẩn đoán DISC-5/DSM-5. Vấn đề SKTT 21,7%, lo âu triệu chứng 18,6%, rối loạn lo âu chẩn đoán 2,3%, trầm cảm MDD 0,9%, bất kỳ rối loạn 3,3%. Chỉ 8,4% tiếp cận dịch vụ. Cha mẹ chỉ nhận ra 5,1%. // V-NAMHS 2022: first national survey 5,996 adolescents 10-17 years 38 provinces Vietnam. DISC-5/DSM-5 diagnostic. Mental health 21.7%, anxiety symptoms 18.6%, anxiety disorder 2.3%, MDD 0.9%, any disorder 3.3%. Only 8.4% accessed services. Parents recognized only 5.1%.',

    'Ngô Anh Vinh 2024: 845 học sinh dân tộc thiểu số nội trú tại Lạng Sơn Việt Nam. DASS-21. Lo âu 54,4%, trầm cảm 59,0%, căng thẳng 24,7%. Trải nghiệm bất lợi thời thơ ấu (ACEs) 48,9%. Mối quan hệ bạn bè kém liên quan đến lo âu. // Ngo Anh Vinh 2024: 845 ethnic minority boarding school students Lang Son Vietnam. DASS-21. Anxiety 54.4%, depression 59.0%, stress 24.7%. ACEs 48.9%. Poor friendship linked to anxiety.',

    'Phạm 2024: 273+273 thanh thiếu niên tại cơ sở hỗ trợ xã hội Huế Việt Nam. Chăm sóc cảm xúc beta=-0,40 cho lo âu (p<0,001) — yếu tố bảo vệ mạnh. Chăm sóc thể chất KHÔNG có ý nghĩa thống kê. Emotional care giảm lo âu mạnh, physical care không tác động. // Pham 2024: 273+273 adolescents social support facilities Hue Vietnam. Emotional care beta=-0.40 anxiety (p<0.001) — strong protective factor. Physical care NOT significant.',

    'Hoàng Trung Học 2025: 8.473 thanh thiếu niên 6 tỉnh Việt Nam. Trong COVID lo âu 41,5%, sau COVID giảm 25,4%. Yếu tố nguy cơ: quan hệ cha mẹ-con kém, sử dụng điện tử quá mức, giấc ngủ kém. // Hoang Trung Hoc 2025: 8,473 adolescents 6 provinces Vietnam. During COVID anxiety 41.5%, after 25.4%. Risk: poor parent-child, excessive electronics, poor sleep.',

    # --- INTERNATIONAL PAPERS ---
    'Jenkins 2023: 75 học sinh đa sắc tộc San Diego Hoa Kỳ. Lo âu 50,6% trầm cảm 44%. Nữ > nam p=0,002. Bạo lực giới, COVID, phân biệt đối xử. Phương pháp hỗn hợp PHQ-9A + GAD-10 + phỏng vấn dân tộc học. // Jenkins 2023: 75 multiethnic students San Diego. Anxiety 50.6% depression 44%. Female>male p=0.002. Gender violence COVID discrimination. Mixed methods.',

    'Saikia 2023: 360 học sinh Assam Ấn Độ. Lo âu 24,4%. NAM > NỮ 30% vs 18,9% P=0,049 — TRÁI NGƯỢC y văn quốc tế. Cha mẹ đơn thân, rượu, chơi game. Văn hóa bộ lạc Đông Bắc Ấn Độ. DASS-21 tiếng Assam. // Saikia 2023: 360 students Assam India. Anxiety 24.4%. MALE>FEMALE 30% vs 18.9% P=0.049 — OPPOSITE to international literature. Single parent, alcohol, gaming. Tribal culture Northeast India.',

    'Mandaknalli 2021: 450 học sinh Ấn Độ đô thị tự trị. Lo âu 24% (108/450) sử dụng GAD-7. Nữ 58,3% trong nhóm lo âu P=0,022. Thiếu hoạt động thể chất 78,7% nhóm lo âu. Hút thuốc 85,2% nhóm lo âu. // Mandaknalli 2021: 450 students India municipality. Anxiety 24% (108/450) GAD-7. Female 58.3% anxiety group P=0.022. No physical activity 78.7% anxiety group. Smoking 85.2% anxiety group.',

    'NSCH 2020: Khảo sát quốc gia Hoa Kỳ n=55.162. Lo âu được chẩn đoán 16,1%. Tăng 61% từ 2016-2023. Nữ 20,1% nam 12,3%. Khó kết bạn gấp 10 lần. Nghỉ học ≥11 ngày gấp 5 lần. 82,6% nhận điều trị nhưng 61% gặp khó khăn tiếp cận. // NSCH 2020: US national n=55,162. Anxiety 16.1% diagnosed. Increased 61% 2016-2023. Female 20.1% male 12.3%. 10x difficulty friends. 82.6% received treatment but 61% had access difficulties.',

    'Alharbi 2019: 1.245 học sinh Ả Rập Saudi Qassim. Lo âu 63,5% trầm cảm 74% ngưỡng thấp. Nữ > nam P<0,001. PHQ-9 + GAD-7. Nữ chiếm 71,3% nhóm lo âu nặng. PubMed indexed. // Alharbi 2019: 1,245 students Saudi Arabia Qassim. Anxiety 63.5% depression 74% low threshold. Female>male P<0.001. PHQ-9 + GAD-7. Female 71.3% severe anxiety group.',

    'Nakie 2022: 849 học sinh Ethiopia Tây Bắc. Lo âu 66,7% trầm cảm 41,4% căng thẳng 52,2%. Nhai khat AOR=5,595 hút thuốc AOR=4,777. Bệnh mãn tính AOR=2,099. Tiền sử BTTGD AOR=1,777. BMC Psychiatry Q1 — hồi quy đa biến AOR. // Nakie 2022: 849 students Northwest Ethiopia. Anxiety 66.7% depression 41.4% stress 52.2%. Khat AOR=5.595 smoking AOR=4.777. Chronic illness AOR=2.099. Family mental history AOR=1.777. BMC Q1 multivariate AOR.',

    'Chen 2023: 63.205 học sinh miền Tây Trung Quốc Tự Cống. Lo âu 13,9% trầm cảm 23%. Rối loạn giấc ngủ OR=6,99 — yếu tố mạnh nhất. Rối loạn chơi game OR=5,00. Bắt nạt thao túng xã hội OR=1,97. Nữ OR=1,55. BMC Psychiatry Q1. // Chen 2023: 63,205 students Western China Zigong. Anxiety 13.9% depression 23%. Sleep disorder OR=6.99 — strongest factor. Gaming disorder OR=5.00. Social manipulation bullying OR=1.97. Female OR=1.55. BMC Q1.',

    'Wen 2020: 900 học sinh THCS nông thôn Giang Tây Trung Quốc. Phân tích hồ sơ tiềm ẩn LPA 3 nhóm: lo âu nhẹ 19,2%, trung bình 56%, nặng 24,8%. Áp lực học tập rất cao OR=11,579 — yếu tố nguy cơ mạnh nhất. NỮ lo âu nặng gấp gần 4 lần nam (OR nam=0,262). Hỗ trợ SKTT trường OR=0,562 bảo vệ. // Wen 2020: 900 rural junior high students Jiangxi China. LPA 3 profiles: mild 19.2%, moderate 56%, severe 24.8%. Academic pressure OR=11.579 — strongest risk. FEMALE severe anxiety ~4x male (male OR=0.262). School MH support OR=0.562 protective.',

    'Qiu 2022: 2.079 học sinh THCS Hợp Phì Trung Quốc. Lo âu 13,4% trầm cảm 26%. Khả năng phục hồi thấp OR=6,74 cho trầm cảm, OR=2,80 lo âu. Nuôi dạy tiêu cực OR=2,01 lo âu. Nuôi dạy tích cực OR=0,32 bảo vệ. LPA 3 hồ sơ nuôi dạy. // Qiu 2022: 2,079 middle school Hefei China. Anxiety 13.4% depression 26%. Low resilience OR=6.74 depression, OR=2.80 anxiety. Negative parenting OR=2.01 anxiety. Positive parenting OR=0.32 protective.',

    'Xu 2021: 373.216 học sinh Trung Quốc Hà Nam — CỠ MẪU LỚN NHẤT TOÀN CẦU. Lo âu 9,89% GAD-7. NAM > NỮ 10,11% vs 9,66% — trái y văn. Nông thôn 11,33% > thành thị 8,77% OR=1,30. COVID-19 đỉnh dịch 02/2020. J Affect Disord Q1. // Xu 2021: 373,216 students China Henan LARGEST GLOBALLY. Anxiety 9.89% GAD-7. MALE>FEMALE 10.11% vs 9.66% — opposite literature. Rural 11.33% > urban 8.77% OR=1.30. COVID-19 peak Feb 2020. Q1.',

    'Bhardwaj 2020: 288 học sinh trường công Chandigarh Ấn Độ. Lo âu 81,9% CAO NHẤT — trầm cảm 64,9% căng thẳng 55,2%. DASS-21. Nữ lo âu nặng+cực nặng 63,7% vs nam 36,0% P<0,001. Đồng mắc rất cao OR=9,77-17,26. // Bhardwaj 2020: 288 government school Chandigarh India. Anxiety 81.9% HIGHEST — depression 64.9% stress 55.2%. DASS-21. Female severe+extreme 63.7% vs male 36.0% P<0.001. Comorbidity very high OR=9.77-17.26.',

    # --- REVIEWS & GLOBAL ---
    'GBD ASEAN 2025 Lancet: 10 nước ASEAN. 80,4 triệu ca, tăng 70% 1990-2021. Việt Nam 10,1%, Malaysia 13,2%. Tuổi 10-14: 16,3% DALYs. 11,2 triệu DALYs (8,54-14,3). // GBD ASEAN 2025 Lancet: 10 countries. 80.4 million cases, 70% increase 1990-2021. Vietnam 10.1%, Malaysia 13.2%. Age 10-14: 16.3% DALYs. 11.2M DALYs.',

    'Puyat 2025: Thanh thiếu niên Philippines trầm cảm tăng từ 9,6% (2013) lên 20,9% (2021). Nữ 24,3%, LGBTQ+ 32,3%, nghèo nhất 25,1%. n=30.127. Chỉ ~2% tiếp cận dịch vụ. // Puyat 2025: Filipino youth depression 9.6% to 20.9% (2013-2021). Female 24.3%, LGBTQ+ 32.3%, poorest 25.1%. n=30,127. Only ~2% accessed services.',

    'Zhu 2025 BMC Trung Quốc: 9.831 học sinh Tô Châu. Trầm cảm 14,5%+5,8%. Ngủ <5 giờ AOR=13,710 cho trầm cảm. Hoạt động ngoài trời 2-3 giờ AOR=0,557 bảo vệ. Cha mẹ đơn thân AOR=1,434. // Zhu 2025 BMC China: 9,831 students Suzhou. Depression 14.5%+5.8%. Sleep <5h AOR=13.710. Outdoor 2-3h AOR=0.557 protective. Single parent AOR=1.434.',

    'Mudunna 2025 Lancet SEA: Nam Á 8 nước. Tỷ lệ 1,5-81,6% dao động rất lớn. Kỳ thị là rào cản lớn nhất tiếp cận dịch vụ SKTT. // Mudunna 2025 Lancet SEA: South Asia 8 countries. Prevalence 1.5-81.6% wide range. Stigma biggest barrier to mental health services.',

    'Anderson 2025: Tổng quan 61 bài. 31,9% thanh thiếu niên lo âu. Gen Z cao nhất. 48/52 nghiên cứu áp lực học tập liên quan SKTT kém. // Anderson 2025: 61 articles review. 31.9% adolescents anxiety. Gen Z highest. 48/52 studies academic pressure linked poor mental health.',

    'Zhameden 2025: 6 RCTs nước thu nhập thấp-trung bình 1.587 học sinh. CBT hiệu quả 3/4 trầm cảm nhưng chỉ 1/4 lo âu. GRADE rất thấp. KHÔNG CÓ RCT từ Việt Nam. // Zhameden 2025: 6 RCTs LMIC 1,587 students. CBT 3/4 depression but 1/4 anxiety. GRADE very low. NO RCT from Vietnam.',

    # --- CROSS-STUDY SYNTHESIS ---
    'Khoảng cách sàng lọc vs chẩn đoán tại Việt Nam: GAD-7 cho 40,6% (Hoa), DASS-21 cho 54,4% (Ngo Anh Vinh), nhưng DISC-5 chẩn đoán chỉ 2,3% (V-NAMHS). Chênh lệch 17-24 lần. Phương pháp đo lường quyết định mạnh đến kết quả. // Screening vs diagnostic Vietnam: GAD-7 40.6%, DASS-21 54.4%, DISC-5 only 2.3%. Difference 17-24 times. Measurement method strongly determines results.',

    'Giới tính trong 11 bài: 8/11 nữ > nam (phù hợp y văn). Chỉ 2 ngoại lệ nam > nữ: Saikia 2023 (Ấn Độ bộ lạc) và Xu 2021 (Trung Quốc COVID). Wen 2020 thực tế nữ > nam (OR nam=0,262). V-NAMHS không khác biệt rõ. // Gender in 11 papers: 8/11 female>male (consistent literature). Only 2 exceptions male>female: Saikia 2023 (tribal India) and Xu 2021 (China COVID). Wen 2020 actually female>male (male OR=0.262).',

    'Giấc ngủ và lo âu: Ngủ <5 giờ AOR=13,71 cho trầm cảm (Zhu 2025). Rối loạn giấc ngủ OR=6,99 — yếu tố mạnh nhất (Chen 2023). Hoạt động ngoài trời 2-3 giờ bảo vệ AOR=0,557 (Zhu). Giấc ngủ là yếu tố có thể can thiệp được. // Sleep and anxiety: Sleep <5h AOR=13.71 depression (Zhu 2025). Sleep disorder OR=6.99 strongest factor (Chen 2023). Outdoor 2-3h protective AOR=0.557. Sleep is modifiable factor.',

    'Gia đình và sức khỏe tâm thần: Chăm sóc cảm xúc beta=-0,40 giảm lo âu mạnh (Pham 2024 Việt Nam). Chăm sóc thể chất KHÔNG có ý nghĩa. Nuôi dạy tích cực OR=0,30 trầm cảm OR=0,32 lo âu bảo vệ (Qiu 2022). Cha mẹ đơn thân AOR=1,43 (Zhu). Khả năng phục hồi thấp OR=6,74 (Qiu). // Family and mental health: Emotional care beta=-0.40 reduces anxiety strongly (Pham 2024 Vietnam). Physical care NOT significant. Positive parenting OR=0.30 depression OR=0.32 anxiety protective (Qiu 2022). Single parent AOR=1.43 (Zhu). Low resilience OR=6.74 (Qiu).',

    'Chăm sóc cảm xúc ảnh hưởng đến sức khỏe tâm thần: Nghiên cứu Pham 2024 tại Huế Việt Nam chứng minh chăm sóc cảm xúc (lắng nghe, chia sẻ, đồng cảm) có beta=-0,40 cho lo âu (p<0,001), giảm lo âu rất mạnh. Trong khi đó chăm sóc thể chất (ăn uống, quần áo, nhà ở) KHÔNG có ý nghĩa thống kê. Điều này gợi ý can thiệp nên tập trung vào hỗ trợ cảm xúc hơn là chỉ đáp ứng nhu cầu vật chất. Tương tự, Qiu 2022 tại Trung Quốc cho thấy nuôi dạy tích cực giảm 70% trầm cảm (OR=0,30) và 68% lo âu (OR=0,32). // Emotional care impact on mental health: Pham 2024 Hue Vietnam proved emotional care (listening, sharing, empathy) beta=-0.40 for anxiety (p<0.001), strongly reduces anxiety. Physical care (food, clothing, shelter) NOT significant. Suggests intervention should focus on emotional support rather than just material needs. Similarly, Qiu 2022 China: positive parenting reduces 70% depression (OR=0.30) and 68% anxiety (OR=0.32).',

    'Can thiệp tại trường: 0 RCT từ Việt Nam (Zhameden 2025). CBT hiệu quả cho trầm cảm 3/4 nhưng lo âu chỉ 1/4. GRADE rất thấp. Hỗ trợ SKTT trường giảm lo âu nặng OR=0,562 (Wen 2020). Cần NC can thiệp tại trường Việt Nam. // School interventions: 0 RCTs from Vietnam (Zhameden 2025). CBT effective depression 3/4 but anxiety only 1/4. GRADE very low. School MH support reduces severe anxiety OR=0.562 (Wen 2020). Need school intervention RCT in Vietnam.',

    'Khoảng cách dịch vụ SKTT: Việt Nam 8,4% tiếp cận (V-NAMHS). Philippines ~2% (Puyat). Hoa Kỳ 82,6% nhận điều trị (NSCH). Cha mẹ Việt Nam chỉ nhận ra 5,1% con có vấn đề. ASEAN bác sĩ tâm thần 0,2-4,3/100.000 dân. // Mental health service gap: Vietnam 8.4% access. Philippines ~2%. USA 82.6% received treatment. Vietnamese parents recognize only 5.1%. ASEAN psychiatrists 0.2-4.3/100K.',

    '5 khoảng trống NC hàng đầu Việt Nam: (1) RCT can thiệp tại trường (2) So sánh GAD-7 vs DISC-5 cùng mẫu (3) Nghiên cứu dọc hậu COVID (4) Mối quan hệ giấc ngủ-lo âu (5) Đào tạo kỹ năng phụ huynh. // Top 5 research gaps Vietnam: (1) School intervention RCT (2) GAD-7 vs DISC-5 same sample (3) Longitudinal post-COVID (4) Sleep-anxiety relationship (5) Parent skills training.',

    # --- TOOLS/SCALES ---
    'GAD-7: Thang đo Rối loạn Lo âu Tổng quát 7 mục, điểm 0-21. Nhẹ 5-9, trung bình 10-14, nặng 15-21. Spitzer 2006. Sàng lọc, không chẩn đoán. // GAD-7: Generalized Anxiety Disorder 7-item scale 0-21. Mild 5-9, moderate 10-14, severe 15-21. Spitzer 2006. Screening, not diagnostic.',

    'DASS-21: 21 mục đo trầm cảm lo âu căng thẳng. Lovibond 1995. Công cụ sàng lọc, cho tỷ lệ cao hơn chẩn đoán. Lo âu ≥8 dương tính. // DASS-21: 21 items depression anxiety stress. Lovibond 1995. Screening tool, higher rates than diagnostic. Anxiety ≥8 positive.',

    'DISC-5: Phỏng vấn chẩn đoán DSM-5 cho trẻ em. Tỷ lệ rối loạn lo âu 2,3% tại Việt Nam — thấp hơn nhiều so với sàng lọc 40-54%. // DISC-5: Diagnostic interview DSM-5 for children. Anxiety disorder 2.3% in Vietnam — much lower than screening 40-54%.',

    'PHQ-9: 9 mục sàng lọc trầm cảm 0-27. Spitzer 1999. Dựa trên DSM-IV. Nhẹ 5-9, trung bình 10-14, nặng vừa 15-19, nặng 20-27. // PHQ-9: 9-item depression screening 0-27. Spitzer 1999. Based on DSM-IV.',

    'MHT: Trắc nghiệm Sức khỏe Tâm thần 100 mục, 8 thang nội dung. Thang đo tiêu chuẩn hóa cho THCS Trung Quốc. Cronbach alpha 0,878. // MHT: Mental Health Test 100 items, 8 subscales. Standardized for Chinese junior high. Cronbach alpha 0.878.',

    'SAS: Thang đo Lo âu Tự đánh giá 20 mục, ngưỡng điểm 50. Zung 1971. // SAS: Self-rating Anxiety Scale 20 items, cut-off score 50. Zung 1971.',

    'CES-D: Thang đo Trầm cảm 20 mục, ngưỡng ≥20. Radloff 1977. // CES-D: Center for Epidemiologic Studies Depression Scale 20 items, cut-off ≥20. Radloff 1977.',

    # --- VIETNAMESE-ONLY FAQ entries (boost recall for Vietnamese queries) ---
    'Tỷ lệ lo âu ở học sinh Việt Nam: Hoa 2024 nghiên cứu 3.910 học sinh THPT Hà Nội cho thấy tỷ lệ lo âu là 40,6% (GAD-7). Ngo Anh Vinh 2024 tại Lạng Sơn dân tộc thiểu số cho thấy 54,4% (DASS-21). V-NAMHS 2022 chẩn đoán DISC-5 chỉ 2,3%. Hoàng Trung Học 2025: trong COVID 41,5%, sau COVID 25,4%.',

    'Sự khác biệt giới tính về lo âu ở thanh thiếu niên: Đa số nghiên cứu (8/11) cho thấy nữ có tỷ lệ lo âu cao hơn nam, phù hợp y văn quốc tế (McLean 2011). Chỉ có 2 ngoại lệ nam cao hơn nữ: Saikia 2023 tại Ấn Độ (30,0% vs 18,9%) và Xu 2021 tại Trung Quốc (10,11% vs 9,66% trong COVID-19). Wen 2020 thực tế nữ cao hơn nam (OR nam = 0,262).',

    'Yếu tố nguy cơ lo âu ở thanh thiếu niên: Giấc ngủ kém (Chen 2023 OR=6,99; Zhu 2025 AOR=13,71). Áp lực học tập (Wen 2020 OR=11,579). Chơi game (Chen OR=5,00). Bắt nạt (Chen OR=1,97). Cha mẹ đơn thân (Zhu AOR=1,43). Nuôi dạy tiêu cực (Qiu OR=2,01). Nhai khat (Nakie AOR=5,6). Hút thuốc (Nakie AOR=4,8).',

    'Yếu tố bảo vệ sức khỏe tâm thần thanh thiếu niên: Chăm sóc cảm xúc (Pham 2024 beta=-0,40). Nuôi dạy tích cực (Qiu 2022 OR=0,30 trầm cảm, OR=0,32 lo âu). Hoạt động ngoài trời 2-3 giờ (Zhu AOR=0,557). Hỗ trợ SKTT tại trường (Wen OR=0,562). Thành tích học tập tốt (Wen OR=0,377).',

    'Tổng quan các nước ASEAN về rối loạn tâm thần thanh thiếu niên: Theo GBD 2025 trên Lancet, 10 nước ASEAN có 80,4 triệu ca rối loạn tâm thần, tăng 70% từ 1990-2021. Việt Nam 10,1%, Malaysia 13,2%. Tuổi 10-14 chịu 16,3% DALYs. Tổng 11,2 triệu DALYs (8,54-14,3).',

    'Áp lực học tập và lo âu: Wen 2020 tại nông thôn Trung Quốc cho thấy áp lực học tập rất cao có OR=11,579 cho lo âu nặng — yếu tố nguy cơ mạnh nhất. Anderson 2025 tổng quan 61 bài: 48/52 nghiên cứu áp lực học tập liên quan sức khỏe tâm thần kém. Hoa 2024: phỏng vấn sâu tại Hà Nội phát hiện áp lực thi cử là nguồn lo âu hàng đầu.',
]

print(f'Total entries: {len(entries)}')

ids = [f'e{i}' for i in range(len(entries))]
metas = [{'source': 'full', 'type': 'bilingual', 'chunk_index': i} for i in range(len(entries))]

print('Encoding...')
embs = model.encode(entries, show_progress_bar=True).tolist()

print('Adding to ChromaDB...')
col.add(documents=entries, embeddings=embs, ids=ids, metadatas=metas)

db_size = os.path.getsize(f'{DB_PATH}/chroma.sqlite3') // 1024
print(f'\nFull RAG: {col.count()} entries, DB: {db_size}KB')

# ============================================================
# TEST
# ============================================================
tests = [
    ('lo âu học sinh Việt Nam', '40.6'),
    ('chẩn đoán DISC-5 Việt Nam', '2.3'),
    ('giấc ngủ trầm cảm nguy cơ', '13.7'),
    ('can thiệp trường học RCT Việt Nam', 'RCT'),
    ('khác biệt giới tính lo âu', 'female'),
    ('Philippines trầm cảm thanh thiếu niên', '20.9'),
    ('ASEAN rối loạn tâm thần', '80.4'),
    ('chăm sóc cảm xúc ảnh hưởng sức khỏe tâm thần', '-0.40'),
    ('GAD-7 thang đo lo âu', 'GAD'),
    ('tiếp cận dịch vụ sức khỏe tâm thần Việt Nam', '8.4'),
    ('nam cao hơn nữ lo âu', 'Saikia'),
    ('áp lực học tập lo âu Trung Quốc', '11.579'),
    ('nuôi dạy tích cực bảo vệ', '0.30'),
    ('dân tộc thiểu số lo âu Việt Nam', '54.4'),
    ('COVID-19 lo âu thanh thiếu niên', 'COVID'),
]

print('\n--- TEST ---')
passed = 0
for q, kw in tests:
    r = col.query(query_embeddings=model.encode([q]).tolist(), n_results=5, include=['documents', 'distances'])
    found = kw in ' '.join(r['documents'][0])
    rel = max(0, (1 - r['distances'][0][0]) * 100)
    ok = found and rel >= 50
    if ok: passed += 1
    print(f'{"PASS" if ok else "FAIL"} [{rel:.0f}%] {q[:40]:40s} kw={kw}: {"OK" if found else "NO"}')

print(f'\n{passed}/{len(tests)} = {passed/len(tests)*100:.0f}%')
print(f'\nDB path: {os.path.abspath(DB_PATH)}')
print(f'Model: {MODEL_NAME}')
