Python
import streamlit as st
import google.generativeai as genai
import docx

st.set_page_config(page_title="App Soạn Giáo Án Mầm Non", layout="wide")

st.title("🏫 Trợ Lý Soạn Giáo Án Mầm Non Thông Minh")
st.caption("Tự động hóa soạn giáo án chuẩn theo khung chương trình nhà trường")

# Thanh cấu hình bên trái
with st.sidebar:
    st.header("⚙️ Cấu Hình")
    api_key = st.text_input("Nhập Gemini API Key:", type="password")
    st.markdown("---")
    st.write("📁 **Tài liệu nhà trường (Upload để AI học):**")
    uploaded_files = st.file_uploader(
        "Tải lên Kế hoạch năm, Quy định, Giáo án mẫu (.txt hoặc .docx)", 
        accept_multiple_files=True
    )

# Form nhập liệu
col1, col2 = st.columns(2)
with col1:
    do_tuoi = st.selectbox("Chọn độ tuổi:", ["Nhà trẻ (24-36 tháng)", "Mẫu giáo bé (3-4 tuổi)", "Mẫu giáo nhỡ (4-5 tuổi)", "Mẫu giáo lớn (5-6 tuổi)"])
    linh_vuc = st.selectbox("Lĩnh vực phát triển:", ["Phát triển Thể chất", "Phát triển Nhận thức", "Phát triển Ngôn ngữ", "Phát triển Tình cảm & Kỹ năng xã hội", "Phát triển Thẩm mỹ"])
with col2:
    chu_de = st.text_input("Chủ đề / Tuần:", "Bản thân - Tuần 1")
    ten_bai = st.text_input("Tên hoạt động:", "Vẽ chân dung cô giáo")

yeu_cau_them = st.text_area("Yêu cầu bổ sung:", "Tích hợp trò chơi gây hứng thú, tăng cường hoạt động nhóm...")

# Xử lý tạo giáo án
if st.button("🚀 Soạn Giáo Án Ngay", type="primary"):
    if not api_key:
        st.error("Vui lòng nhập API Key ở thanh cấu hình bên trái!")
    elif not ten_bai:
        st.warning("Vui lòng nhập tên hoạt động!")
    else:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')

        context_data = ""
        if uploaded_files:
            for file in uploaded_files:
                context_data += f"\n--- TÀI LIỆU TRƯỜNG ({file.name}) ---\n" + file.read().decode("utf-8", errors="ignore")

        prompt = f"""
        Bạn là một giáo viên mầm non giàu kinh nghiệm. Hãy soạn một giáo án chi tiết theo đúng cấu trúc tiêu chuẩn.
        
        TÀI LIỆU THAM CHIẾU CỦA TRƯỜNG:
        {context_data}

        THÔNG TIN BÀI SOẠN:
        - Độ tuổi: {do_tuoi}
        - Lĩnh vực: {linh_vuc}
        - Chủ đề: {chu_de}
        - Tên bài dạy: {ten_bai}
        - Yêu cầu thêm: {yeu_cau_them}

        YÊU CẦU ĐẦU RA:
        Soạn giáo án đầy đủ 3 phần: Mục tiêu (Kiến thức, Kỹ năng, Thái độ), Chuẩn bị, Tiến trình hoạt động (Mở đầu -> Nội dung chính -> Kết thúc). Bám sát độ tuổi và định dạng tài liệu mẫu.
        """

        with st.spinner("AI đang soạn bài, cô/thầy chờ chút nhé..."):
            try:
                response = model.generate_content(prompt)
                st.success("Soạn giáo án thành công!")
                st.markdown(response.text)

                doc = docx.Document()
                doc.add_heading(f"GIÁO ÁN: {ten_bai.upper()}", 0)
                doc.add_paragraph(response.text)
                doc.save("Giao_An.docx")

                with open("Giao_An.docx", "rb") as file:
                    st.download_button(
                        label="📄 Tải Giáo Án File Word (.docx)",
                        data=file,
                        file_name=f"Giao_An_{ten_bai}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
            except Exception as e:
                st.error(f"Có lỗi xảy ra: {str(e)}")
