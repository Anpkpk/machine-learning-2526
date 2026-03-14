# Hệ Thống Gợi Ý Phim Hybrid (Movie Recommendation System)

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

Hệ thống tính toán **điểm số cuối cùng (Final Score)** cho mỗi bộ phim dựa trên công thức lai:

### 1. Content-Based (Độ tương đồng)
- Tạo một **user_vector** dựa trên **Thể loại** và **Năm** mà người dùng chọn.
- Tính toán **cosine_similarity** giữa `user_vector` và `movie_vector` của tất cả các phim trong cơ sở dữ liệu.

### 2. Linear Regression (Chất lượng dự đoán)
- Mô hình hồi quy tuyến tính được huấn luyện trên tập dữ liệu đánh giá (**ratings**) để dự đoán điểm trung bình mà cộng đồng sẽ dành cho một bộ phim dựa trên đặc trưng của nó.
$$
\text{Rating}_{\text{pred}} = \beta_0 + \beta_1 \cdot \text{Genre}_1 + \beta_2 \cdot \text{Genre}_2 + \dots + \beta_k \cdot \text{Genre}_k + \beta_{\text{year}} \cdot \text{Year}_{\text{scaled}}
$$

### 3. Kết hợp (Hybrid)
- Điểm số cuối cùng được tính bằng công thức:
$$
\text{Final\_Score} = (\alpha \times \text{Similarity}) + ((1 - \alpha) \times \text{Normalized\_LR\_Score})
$$

- Trong đó, **α** là trọng số ưu tiên tính cá nhân hóa.

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

