import streamlit as st
from datetime import datetime
import pytz

# --- CẤU HÌNH TRANG ---
st.set_page_config(page_title="Báo Bài Pro UI", layout="wide")

# --- CSS NÂNG CẤP GIAO DIỆN (LUXURY DARK) ---
st.markdown("""
    <style>
    /* Nền gradient tối sâu thẳm */
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #020617 100%);
        color: #f8fafc;
    }
    
    /* Làm đẹp tiêu đề */
    .main-title {
        font-size: 45px;
        font-weight: 800;
        background: -webkit-linear-gradient(#3b82f6, #2dd4bf);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }

    /* Hiệu ứng Glassmorphism cho các thẻ nhập liệu */
    div[data-testid="stExpander"], .stTextInput input, .stTextArea textarea {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px);
        border-radius: 12px !important;
        color: #e2e8f0 !important;
    }

    /* Tùy chỉnh nút bấm môn học */
    div.stButton > button {
        border-radius: 12px;
        height: 3.8em;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        border: none !important;
    }
    
    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.3);
        filter: brightness(1.2);
    }

    /* Nút Xóa (X) tinh tế hơn */
    button[key*="del_"] {
        background-color: rgba(239, 68, 68, 0.2) !important;
        color: #ef4444 !important;
        border: 1px solid rgba(239, 68, 68, 0.4) !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- XỬ LÝ THỜI GIAN ---
def get_vietnam_date():
    tz = pytz.timezone('Asia/Ho_Chi_Minh')
    now = datetime.now(tz)
    days = ["Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy", "Chủ Nhật"]
    return f"{days[now.weekday()]} • {now.strftime('%d/%m/%Y')}"

# --- QUẢN LÝ DỮ LIỆU ---
if 'list_mon' not in st.session_state:
    st.session_state.list_mon = []

# Bảng màu Gradient hiện đại (Soft Neon)
all_subjects = {
    "Toán": "#3b82f6", "Văn": "#f43f5e", "Anh": "#10b981",
    "Lý": "#f59e0b", "Hóa": "#8b5cf6", "Sinh": "#14b8a6",
    "Sử": "#f97316", "Địa": "#64748b"
}

# --- GIAO DIỆN ---
st.markdown('<p class="main-title">BÁO BÀI</p>', unsafe_allow_html=True)
st.markdown(f'<p style="color: #94a3b8; font-size: 18px;">{get_vietnam_date()}</p>', unsafe_allow_html=True)

col1, col2 = st.columns([1.4, 2], gap="large")

with col1:
    st.write(" ")
    st.markdown("##### 📚 DANH MỤC MÔN HỌC")
    
    c1, c2 = st.columns(2)
    sub_items = list(all_subjects.items())
    
    for i, (sub, color) in enumerate(sub_items):
        target_col = c1 if i % 2 == 0 else c2
        
        # Inject CSS màu sắc hiện đại cho từng nút
        st.markdown(f"""
            <style>
            button[key="{sub}"] {{
                background: linear-gradient(135deg, {color}dd 0%, {color} 100%) !important;
                color: white !important;
                box-shadow: 0 4px 15px {color}44 !important;
            }}
            </style>
        """, unsafe_allow_html=True)
        
        if target_col.button(sub, key=sub, use_container_width=True):
            if sub not in st.session_state.list_mon:
                st.session_state.list_mon.append(sub)
    
    st.markdown("---")
    # Nút Lưu ý & Môn khác
    if st.button("📝 THÊM LƯU Ý", use_container_width=True):
        if "Lưu ý" not in st.session_state.list_mon:
            st.session_state.list_mon.append("Lưu ý")
            st.rerun()

    other = st.text_input("➕ Môn khác:", placeholder="Nhập tên môn...")
    if st.button("XÁC NHẬN THÊM", use_container_width=True):
        if other and other not in st.session_state.list_mon:
            st.session_state.list_mon.append(other)
            st.rerun()

with col2:
    st.write(" ")
    st.markdown("##### 📝 NỘI DUNG CHI TIẾT")
    content_dict = {}
    
    if not st.session_state.list_mon:
        st.markdown("""
            <div style="padding: 20px; border-radius: 12px; border: 1px dashed #334155; text-align: center; color: #64748b;">
                Chưa có môn nào được chọn.<br>Vui lòng chọn môn ở danh mục bên trái.
            </div>
        """, unsafe_allow_html=True)
    
    for mon in st.session_state.list_mon:
        with st.container():
            r_col1, r_col2 = st.columns([7, 1])
            with r_col1:
                if mon == "Lưu ý":
                    content_dict[mon] = st.text_area("Ghi chú quan trọng:", key="in_luu_y", height=100)
                else:
                    content_dict[mon] = st.text_input(f"Bài tập {mon}:", key=f"in_{mon}")
            with r_col2:
                st.write(" ")
                if st.button("✕", key=f"del_{mon}"):
                    st.session_state.list_mon.remove(mon)
                    st.rerun()

    if st.session_state.list_mon:
        st.markdown("---")
        # --- XUẤT PROMPT ---
        prompt_output = f" BÁO BÀI {get_vietnam_date().upper()}\n"
        prompt_output += "━━━━━━━━━━━━━━━━━━━━\n"
        
        ds_mon = [m for m in st.session_state.list_mon if m != "Lưu ý"]
        for mon in ds_mon:
            msg = content_dict.get(mon, "").strip()
            prompt_output += f"• {mon}: {msg if msg else 'Không có'}\n"
        
        if "Lưu ý" in st.session_state.list_mon:
            ghi_chu = content_dict.get("Lưu ý", "").strip()
            if ghi_chu:
                prompt_output += f"\n⚠️ LƯU Ý: {ghi_chu}\n"
        
        st.markdown("##### 🚀 KẾT QUẢ")
        st.code(prompt_output, language="text")
        
        if st.button("🗑️ LÀM MỚI TẤT CẢ", type="primary", use_container_width=True):
            st.session_state.list_mon = []
            st.rerun()