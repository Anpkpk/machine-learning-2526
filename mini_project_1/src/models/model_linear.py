import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error

import re

from config.config import (MOVIES_PATH, RATINGS_PATH)

# -------------------------------
# Load MovieLens 1M dataset
# -------------------------------
ratings = pd.read_csv(
    RATINGS_PATH,
    sep="::",
    engine="python",
    names=["userId","movieId","rating","timestamp"],
    encoding="latin-1"
)

movies = pd.read_csv(
    MOVIES_PATH,
    sep="::",
    engine="python",
    names=["movieId","title","genres"],
    encoding="latin-1"
)

# Extract year
def extract_year(title):
    m = re.search(r"\((\d{4})\)", title)
    if m:
        return int(m.group(1))
    else:
        return 0

movies["year"] = movies["title"].apply(extract_year)

# Genre one-hot
movies["genres"] = movies["genres"].str.split("|")
ALL_GENRES = sorted(list(set(g for row in movies["genres"] for g in row)))
for g in ALL_GENRES:
    movies[g] = movies["genres"].apply(lambda x: 1 if g in x else 0)
    
genre_cols = list(ALL_GENRES)

# Merge rating + features
data = ratings.merge(movies, on="movieId")

# scale year
scaler = MinMaxScaler()
data["year_scaled"] = scaler.fit_transform(data["year"].values.reshape(-1,1))
movies["year_scaled"] = scaler.transform(movies["year"].values.reshape(-1,1))

feature_cols = genre_cols + ["year_scaled"]

X = data[feature_cols].values
y = data["rating"].values


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Linear Regression
model_linear = LinearRegression()
model_linear.fit(X_train, y_train)

# Test
y_pred_linear = model_linear.predict(X_test)

# Tính RMSE
rmse = np.sqrt(mean_squared_error(y_test, y_pred_linear))
print(f"Linear Regression RMSE: {rmse:.4f}")

# -------------------------------
# Build user profile (genres + year)
# -------------------------------
def build_user_profile(fav_genres=[], fav_year=None):
    # vector genres
    genre_vector = np.zeros(len(genre_cols))
    for i,g in enumerate(genre_cols):
        if g in fav_genres:
            genre_vector[i] = 1.0
    if len(fav_genres) > 0:
        genre_vector = genre_vector / genre_vector.max()
    
    # vector year
    if fav_year is not None:
        year_vector = np.array([scaler.transform([[fav_year]])[0,0]])
    else:
        year_vector = np.array([0.0])
    
    user_vector = np.concatenate([genre_vector, year_vector])
    return user_vector

def recommend_movies(fav_genres=[], fav_year=None, top_k=5, alpha=0.8):
    """
    alpha (0 -> 1): Trọng số ưu tiên độ tương đồng với sở thích người dùng.
    - alpha cao (VD: 0.8): Rất ưu tiên phim đúng thể loại/năm người dùng chọn.
    - alpha thấp (VD: 0.2): Ưu tiên phim có rating chung cao (từ mô hình LR).
    """
    
    # 1. Build user vector và định dạng lại thành ma trận 2D (1, n_features) cho hàm cosine_similarity
    user_vector = build_user_profile(fav_genres, fav_year).reshape(1, -1) 
    
    # 2. Lấy features của tất cả phim
    X_movies = movies[feature_cols].to_numpy()  
    
    # 3. Tính độ tương đồng giữa "Sở thích" và "Đặc trưng phim" (Giá trị từ 0 đến 1)
    similarity_scores = cosine_similarity(user_vector, X_movies)[0]
    
    # 4. Dự đoán điểm chất lượng chung của phim từ mô hình Linear Regression
    lr_scores = model_linear.predict(X_movies)
    
    # 5. Chuẩn hóa lr_scores về khoảng [0, 1] để dễ dàng cộng gộp với similarity_scores
    # Giả sử rating trong dataset MovieLens từ 1 đến 5
    lr_scores_normalized = (lr_scores - 1) / 4.0 
    
    # 6. Tính điểm cuối cùng (Kết hợp cá nhân hóa và chất lượng chung)
    final_scores = (alpha * similarity_scores) + ((1 - alpha) * lr_scores_normalized)
    
    # 7. Tạo DataFrame kết quả
    recs = pd.DataFrame({
        "title": movies["title"],
        "similarity": similarity_scores, 
        "lr_prediction": lr_scores,     
        "final_score": final_scores
    })
    
    # 8. Sắp xếp theo final_score giảm dần và trả về Top-K
    recs_sorted = recs.sort_values("final_score", ascending=False).head(top_k)
    return recs_sorted
