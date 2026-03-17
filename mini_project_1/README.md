# Hệ Thống Gợi Ý Phim (Movie Recommendation System)

Đây là một ứng dụng Desktop (GUI) gợi ý phim được xây dựng bằng Python. Hệ thống sử dụng Mô hình Hồi quy tuyến tính - Linear Regression để đưa ra các đề xuất phim cá nhân hóa dựa trên sở thích về thể loại và năm phát hành của người dùng.

## Tính năng chính

* **Giao diện trực quan:** Giao diện người dùng đơn giản được xây dựng bằng PyQt5.
* **Tùy chỉnh sở thích:** Cho phép người dùng chọn nhiều thể loại phim yêu thích cùng lúc và năm phát hành mong muốn.
* **Tùy chọn Top-K:** Người dùng có thể tùy chỉnh số lượng phim muốn hệ thống gợi ý (ví dụ: Top 10, Top 20).

## Công nghệ sử dụng

* **Ngôn ngữ:** Python 3.x
* **Giao diện (GUI):** PyQt5
* **Xử lý dữ liệu & Học máy:** `pandas`, `numpy`, `scikit-learn`
* **Dataset:** [MovieLens 1M Dataset](https://grouplens.org/datasets/movielens/1m/)

## Nguyên lý hoạt động (Thuật toán Hybrid)

Hệ thống tính toán **điểm số cuối cùng (Final Score)** cho mỗi bộ phim dựa trên điểm số mà cộng đồng đánh giá:

### 1. Sử dụng hồi quy tuyến tính (Linear Regression) để dự đoán chất lượng
- Mô hình học mối quan hệ giữa đặc trưng của phim (thể loại, năm phát hành) và điểm đánh giá (rating) từ các người dùng trong tập dữ liệu.

- Mô hình hồi quy tuyến tính được huấn luyện trên tập dữ liệu đánh giá (**ratings**) để dự đoán điểm trung bình mà cộng đồng sẽ dành cho một bộ phim dựa trên đặc trưng của nó.
```math
\text{Rating}_{\text{pred}} = \beta_0 + \beta_1 \cdot \text{Genre}_1 + \beta_2 \cdot \text{Genre}_2 + \dots + \beta_k \cdot \text{Genre}_k + \beta_{\text{year}} \cdot \text{Year}_{\text{scaled}}
```
- **Rating** được chuẩn hóa trên thang 5.  

- Mục đích: Tìm ra những thể loại hoặc thời kỳ phim nào thường được đánh giá cao. Ví dụ: Phim Drama năm 1990 có xu hướng được rate cao. Mô hình này đóng vai trò như một bộ lọc chất lượng.

### 2. Phân tích độ tương đồng nội dung bằng Cosine Similarity
- Người dùng và Phim đều được biểu diễn dưới dạng các vector số học trong cùng một không gian đặc trưng (bao gồm các cột one-hot của Thể loại và giá trị scale của Năm).

- Cosine Similarity sẽ đo góc giữa hai vector này. Góc càng nhỏ (Cosine tiến về 1), bộ phim đó càng sát với cấu hình sở thích mà người dùng đã nhập.

### 3. Kết hợp
- Kết hợp hai chỉ số trên bằng một siêu tham số α (từ 0 đến 1) để cân bằng giữa "sở thích cá nhân" và "độ hay chung của phim".
- Điểm số cuối cùng được tính bằng công thức:
```math
\text{Final\_Score} = (\alpha \times \text{Similarity}) + ((1 - \alpha) \times \text{Normalized\_LR\_Score})
```

- Trong đó, **α** là trọng số ưu tiên tính cá nhân hóa (đang sử dụng **α=0.8**).
    * Nếu α = 1: Hệ thống chỉ quan tâm phim có đúng thể loại/năm không, bỏ qua hoàn toàn việc phim đó hay hay dở.

    * Nếu α = 0: Hệ thống phớt lờ sở thích người dùng, chỉ gợi ý các phim có rating chung cao nhất (Top Trending).

## Hướng dẫn Cài đặt & Sử dụng
### 1. Chuẩn bị môi trường
Cài đặt các thư viện cần thiết:
```
pip install -r src/requirement.txt
```

### 2. Khởi chạy ứng dụng
```
python src/main.py
```

