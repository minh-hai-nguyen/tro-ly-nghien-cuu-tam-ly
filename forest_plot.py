# -*- coding: utf-8 -*-
"""
Forest Plot — So sánh tỷ lệ lo âu/trầm cảm giữa các nghiên cứu
Dữ liệu từ 10 bài đã dịch
"""
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'DejaVu Sans'
import numpy as np

# ============================================================
# PLOT 1: Tỷ lệ lo âu theo quốc gia (sàng lọc)
# ============================================================
studies_anxiety = [
    # (label, prevalence%, CI_low, CI_high, tool, n)
    ('VN Hà Nội — Hoa 2024\n(GAD-7, n=3.910)', 40.6, 38.5, 42.7, 'GAD-7'),
    ('VN DTTS — Ngô 2024\n(DASS-21, n=845)', 54.4, 51.0, 57.8, 'DASS-21'),
    ('VN quốc gia — V-NAMHS\n(DISC-5 chẩn đoán, n=5.996)', 2.3, 1.5, 3.1, 'DISC-5'),
    ('VN quốc gia — V-NAMHS\n(vấn đề SKTT, n=5.996)', 18.6, 16.8, 20.4, 'DISC-5'),
    ('TQ Suzhou — Zhu 2025\n(PHQ-9 trầm cảm, n=9.831)', 20.3, 19.1, 21.5, 'PHQ-9'),
    ('Philippines — Puyat 2025\n(CES-D trầm cảm, n=10.949)', 20.9, 19.9, 21.9, 'CES-D'),
    ('ASEAN — GBD 2025\n(mô hình, dân số)', 11.9, 10.9, 12.9, 'GBD'),
    ('ASEAN VN — GBD 2025\n(mô hình, dân số)', 10.1, 9.1, 11.3, 'GBD'),
]

fig, ax = plt.subplots(figsize=(12, 7))

y_pos = np.arange(len(studies_anxiety))
colors = []
for s in studies_anxiety:
    if 'DISC-5' in s[4] and 'chẩn đoán' in s[0]:
        colors.append('#c62828')  # red for diagnostic
    elif 'DISC-5' in s[4]:
        colors.append('#e65100')  # orange for subthreshold
    elif 'GBD' in s[4]:
        colors.append('#1565c0')  # blue for GBD model
    else:
        colors.append('#2e7d32')  # green for screening

for i, (label, prev, ci_lo, ci_hi, tool) in enumerate(studies_anxiety):
    ax.errorbar(prev, i, xerr=[[prev-ci_lo], [ci_hi-prev]],
                fmt='D', markersize=8, color=colors[i], capsize=5, capthick=2, linewidth=2)

ax.set_yticks(y_pos)
ax.set_yticklabels([s[0] for s in studies_anxiety], fontsize=9)
ax.set_xlabel('Tỷ lệ (%)', fontsize=12)
ax.set_title('Forest Plot: Tỷ lệ lo âu/trầm cảm ở VTN theo quốc gia và công cụ đo', fontsize=13, fontweight='bold')
ax.axvline(x=20, color='gray', linestyle='--', alpha=0.5, label='Mức 20%')
ax.axvline(x=40, color='gray', linestyle=':', alpha=0.5, label='Mức 40%')
ax.invert_yaxis()
ax.grid(axis='x', alpha=0.3)

# Legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#2e7d32', label='Sàng lọc (GAD-7, DASS-21, CES-D, PHQ-9)'),
    Patch(facecolor='#e65100', label='Vấn đề SKTT (DISC-5 subthreshold)'),
    Patch(facecolor='#c62828', label='Chẩn đoán (DISC-5/DSM-5)'),
    Patch(facecolor='#1565c0', label='Mô hình GBD'),
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=8)

plt.tight_layout()
plt.savefig('forest_plot_prevalence.png', dpi=200, bbox_inches='tight')
print('Saved: forest_plot_prevalence.png')

# ============================================================
# PLOT 2: Yếu tố nguy cơ/bảo vệ (AOR/β)
# ============================================================
fig2, ax2 = plt.subplots(figsize=(12, 8))

risk_factors = [
    # (label, AOR/OR, CI_low, CI_high, type)
    ('Ngủ < 5h → trầm cảm\n(Zhu 2025, TQ)', 13.71, 8.66, 21.71, 'risk'),
    ('Ngủ 5-6h → trầm cảm\n(Zhu 2025, TQ)', 7.29, 5.32, 10.00, 'risk'),
    ('Ngủ 6-7h → trầm cảm\n(Zhu 2025, TQ)', 2.68, 2.02, 3.55, 'risk'),
    ('Gia đình tái hôn\n(Zhu 2025, TQ)', 1.84, 1.32, 2.55, 'risk'),
    ('Cả 2 cha mẹ vắng\n(Zhu 2025, TQ)', 1.71, 1.29, 2.27, 'risk'),
    ('Gia đình đơn thân\n(Zhu 2025, TQ)', 1.43, 1.13, 1.81, 'risk'),
    ('HS THPT vs THCS\n(Zhu 2025, TQ)', 1.41, 1.16, 1.71, 'risk'),
    ('Nữ vs Nam (Philippines)\n(Puyat 2025)', 1.41, 1.30, 1.53, 'risk'),
    ('AOR = 1 (không ảnh hưởng)', 1.00, 1.00, 1.00, 'ref'),
    ('Nam giới (bảo vệ)\n(Zhu 2025, TQ)', 0.80, 0.72, 0.90, 'protect'),
    ('Ngoài trời 1-2h\n(Zhu 2025, TQ)', 0.66, 0.53, 0.81, 'protect'),
    ('Ngoài trời 2-3h\n(Zhu 2025, TQ)', 0.56, 0.41, 0.76, 'protect'),
]

y2 = np.arange(len(risk_factors))
for i, (label, aor, ci_lo, ci_hi, typ) in enumerate(risk_factors):
    color = '#c62828' if typ == 'risk' else '#2e7d32' if typ == 'protect' else '#757575'
    marker = 's' if typ == 'ref' else 'D'
    ax2.errorbar(aor, i, xerr=[[aor-ci_lo], [ci_hi-aor]],
                fmt=marker, markersize=8, color=color, capsize=4, capthick=1.5, linewidth=1.5)

ax2.set_yticks(y2)
ax2.set_yticklabels([s[0] for s in risk_factors], fontsize=9)
ax2.set_xlabel('AOR (Adjusted Odds Ratio)', fontsize=12)
ax2.set_title('Forest Plot: Yếu tố nguy cơ và bảo vệ (AOR) — Tổng hợp liên bài', fontsize=13, fontweight='bold')
ax2.axvline(x=1.0, color='black', linestyle='-', linewidth=1.5, label='AOR = 1')
ax2.set_xscale('log')
ax2.set_xlim(0.3, 25)
ax2.invert_yaxis()
ax2.grid(axis='x', alpha=0.3)

legend2 = [
    Patch(facecolor='#c62828', label='Yếu tố nguy cơ (AOR > 1)'),
    Patch(facecolor='#2e7d32', label='Yếu tố bảo vệ (AOR < 1)'),
    Patch(facecolor='#757575', label='Mức tham chiếu (AOR = 1)'),
]
ax2.legend(handles=legend2, loc='lower right', fontsize=8)

plt.tight_layout()
plt.savefig('forest_plot_risk_factors.png', dpi=200, bbox_inches='tight')
print('Saved: forest_plot_risk_factors.png')

# ============================================================
# PLOT 3: Xu hướng thời gian
# ============================================================
fig3, ax3 = plt.subplots(figsize=(10, 6))

# Philippines trend
years_ph = [2013, 2021]
prev_ph = [9.6, 20.9]
ax3.plot(years_ph, prev_ph, 'o-', color='#1565c0', linewidth=2, markersize=8, label='Philippines trầm cảm (Puyat 2025)')

# Vietnam during/after COVID
years_vn = [2021, 2023]
prev_vn_anx = [41.5, 25.4]
ax3.plot(years_vn, prev_vn_anx, 's-', color='#c62828', linewidth=2, markersize=8, label='Việt Nam lo âu (Hoàng TH 2025)')

prev_vn_dep = [34.2, 20.1]
ax3.plot(years_vn, prev_vn_dep, 's--', color='#e65100', linewidth=2, markersize=8, label='Việt Nam trầm cảm (Hoàng TH 2025)')

# China stable
years_cn = [2019, 2023]
prev_cn = [20.3, 20.3]
ax3.plot(years_cn, prev_cn, '^-', color='#2e7d32', linewidth=2, markersize=8, label='Trung Quốc trầm cảm (Zhu 2025)')

# Hoa 2024 single point
ax3.plot(2021, 40.6, 'D', color='#6a1b9a', markersize=10, label='VN Hà Nội lo âu GAD-7 (Hoa 2024)')

ax3.set_xlabel('Năm', fontsize=12)
ax3.set_ylabel('Tỷ lệ (%)', fontsize=12)
ax3.set_title('Xu hướng lo âu/trầm cảm ở VTN theo thời gian', fontsize=13, fontweight='bold')
ax3.legend(fontsize=8, loc='upper left')
ax3.grid(alpha=0.3)
ax3.set_xlim(2012, 2024)
ax3.set_ylim(0, 50)

plt.tight_layout()
plt.savefig('forest_plot_trends.png', dpi=200, bbox_inches='tight')
print('Saved: forest_plot_trends.png')

print('All 3 plots saved OK')
