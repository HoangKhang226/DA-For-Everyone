# Chat With Data – Data Analysis Chatbot

**Chat With Your Data** là một ứng dụng **chatbot phân tích dữ liệu** được xây dựng bằng **Streamlit + LangChain Agent**.  
Người dùng có thể:

- Upload file **CSV**
- Đặt câu hỏi bằng **ngôn ngữ tự nhiên**
- Chatbot sẽ tự động:
  - Phân tích dữ liệu
  - Sinh và thực thi **code Python trên DataFrame**
  - Vẽ **biểu đồ phù hợp**
  - Trả lời dựa trên **kết quả thực thi code** (data-driven)

---

##  Mục tiêu Project
- Xây dựng chatbot **phân tích dữ liệu tự động**
- Áp dụng **LLM Agent** cho Data Analysis
- Mọi câu trả lời dựa trên **kết quả code** và **nội dung dataset**

---

##  Cách Chatbot Hoạt Động

1. Người dùng upload file **CSV**.
2. Dữ liệu được load vào `DataFrame df`.
3. Người dùng nhập câu hỏi bằng **ngôn ngữ tự nhiên**.
4. LLM Agent:
   - Phân tích yêu cầu
   - Sinh code Python để xử lý dữ liệu
   - Thực thi code bằng `python_repl_ast`
   - Vẽ **biểu đồ phù hợp**
5. Chatbot trả về:
   - Nhận xét
   - Biểu đồ
   - Code đã chạy
   - Kết quả dữ liệu (`DataFrame` / `Series`)

> ⚠️ Chatbot **không được trả lời nếu chưa chạy code**.

Ngoài ra người dùng có thể upload thêm nội dung của dataset thông qua các file docx, txt, pdf
---

##  Quy Trình Phân Tích (Agent Logic)

### 1️. Khám phá dữ liệu
- `df.info()`
- `df.describe()`

### 2️. Xử lý & tính toán
- `groupby`
- Lọc dữ liệu
- Tính tổng, tỷ lệ, thống kê

### 3️. Trực quan hóa
- Tự động chọn biểu đồ: `Bar`, `Line`, `Pie`, `Boxplot`
- Luôn vẽ **ít nhất 1 biểu đồ**
- Biểu đồ hiển thị trực tiếp trên Streamlit

---

##  Công Nghệ Sử Dụng
- Python
- Streamlit
- Pandas
- Matplotlib
- Seaborn
- LangChain (Pandas DataFrame Agent)

---

##  Cách Chạy Project

### 1️. Clone repository
git clone https://github.com/HoangKhang226/DA-For-Everyone.git
cd DA-For-Everyone
### 2️. Cài thư viện
bash
Sao chép mã
pip install -r requirements.txt
### 3️. Thiết lập biến môi trường
Tạo file .env:

ini
Sao chép mã
GOOGLE_API_KEY=your_api_key_here
### 4️. Chạy ứng dụng
bash
Sao chép mã
streamlit run Chat_With_Your_Data.py
💡 Tính Năng Nổi Bật
Chat với dữ liệu CSV

Tự sinh & thực thi code Pandas

Hiển thị:

Câu trả lời

Code đã chạy

Bảng dữ liệu

Biểu đồ

Lưu lịch sử chat trong session

👤 Author
Hoàng Khang – Data Science Student
GitHub: https://github.com/HoangKhang226
