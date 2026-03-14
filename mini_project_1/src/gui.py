# gui.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QListWidget, 
    QListWidgetItem, QAbstractItemView, QLineEdit, QPushButton, 
    QTextEdit, QSpacerItem, QSizePolicy, QShortcut
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence

from models.model_linear import (ALL_GENRES, recommend_movies)

class MovieRecommenderGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎬 Hệ Thống Gợi Ý Phim")
        self.setGeometry(200, 200, 700, 600) # Mở rộng bề ngang một chút cho giống tỷ lệ ảnh
        
        # Áp dụng StyleSheet tối giản giống thiết kế trong ảnh
        self.setStyleSheet("""
            QWidget {
                font-family: Arial, sans-serif;
                font-size: 24px;
                color: #000000;
                background-color: #ffffff;
            }
            QLabel {
                margin-bottom: 2px;
                font-weight: bold;
            }
            QPushButton {
                background-color: #3bb2fe; 
                color: white;
                border: 1px solid #2a8cc8;
                padding: 8px 0px;
                font-size: 24px;    
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2a8cc8;
            }
            QLineEdit, QListWidget, QTextEdit {
                border: 1px solid #767676;
                background-color: #ffffff;
                padding: 4px;
            }
            QListWidget::item:selected {
                background-color: #3bb2fe;
                color: white;
            }
        """)

        # Layout chính của toàn bộ cửa sổ (Xếp dọc)
        main_layout = QVBoxLayout()
        main_layout.setSpacing(20) # Khoảng cách giữa các khu vực
        main_layout.setContentsMargins(30, 30, 30, 30) # Căn lề ngoài

        # ==========================================
        # 1. KHU VỰC PHÍA TRÊN (Chia 2 cột ngang)
        # ==========================================
        top_h_layout = QHBoxLayout()
        top_h_layout.setSpacing(40) 

        # --- Cột trái: Thể loại ---
        left_v_layout = QVBoxLayout()
        left_v_layout.addWidget(QLabel("Thể loại:"))
        
        self.genre_list = QListWidget()
        self.genre_list.setSelectionMode(QAbstractItemView.MultiSelection)
        for g in ALL_GENRES:
            item = QListWidgetItem(g)
            self.genre_list.addItem(item)
            
        left_v_layout.addWidget(self.genre_list)
        
        top_h_layout.addLayout(left_v_layout, stretch=2)

        # --- Cột phải: Năm phát hành & Top-K ---
        right_v_layout = QVBoxLayout()
        right_v_layout.setSpacing(40)
        
        # Ô nhập Năm
        year_layout = QVBoxLayout()
        year_layout.addWidget(QLabel("Năm phát hành:"))
        self.fav_year_input = QLineEdit()
        year_layout.addWidget(self.fav_year_input)
        right_v_layout.addLayout(year_layout)
        
        # Ô nhập Top-K
        top_k_layout = QVBoxLayout()
        top_k_layout.addWidget(QLabel("Top-K:"))
        self.top_k_input = QLineEdit()
        self.top_k_input.setText("5")
        top_k_layout.addWidget(self.top_k_input)
        right_v_layout.addLayout(top_k_layout)
        
        # Đẩy các ô nhập liệu lên trên cùng của cột phải
        right_v_layout.addStretch()
        
        # Thêm cột phải vào layout ngang trên cùng (stretch=1)
        top_h_layout.addLayout(right_v_layout, stretch=1)

        # Thêm toàn bộ khu vực phía trên vào layout chính
        main_layout.addLayout(top_h_layout)

        # ==========================================
        # 2. KHU VỰC GIỮA (Nút Gợi Ý)
        # ==========================================
        btn_layout = QHBoxLayout()
        
        self.recommend_btn = QPushButton("Gợi ý")
        self.recommend_btn.setFixedSize(260, 60) 
        self.recommend_btn.setCursor(Qt.PointingHandCursor)

        self.recommend_btn.clicked.connect(self.on_recommend)

        self.shortcut_return = QShortcut(QKeySequence("Return"), self)
        self.shortcut_return.activated.connect(self.on_recommend)
        self.shortcut_enter = QShortcut(QKeySequence("Enter"), self)
        self.shortcut_enter.activated.connect(self.on_recommend)
        
        # Dùng khoảng trống 2 bên để căn giữa nút bấm
        btn_layout.addStretch()
        btn_layout.addWidget(self.recommend_btn)
        btn_layout.addStretch()
        
        main_layout.addLayout(btn_layout)

        # ==========================================
        # 3. KHU VỰC PHÍA DƯỚI (Kết quả)
        # ==========================================
        bottom_v_layout = QVBoxLayout()
        bottom_v_layout.addWidget(QLabel("Kết quả:"))
        
        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        bottom_v_layout.addWidget(self.result_area)
        
        main_layout.addLayout(bottom_v_layout)

        # Áp dụng layout chính cho Window
        self.setLayout(main_layout)

        # Kết nối sự kiện nút bấm
        self.recommend_btn.clicked.connect(self.on_recommend)

    # Logic xử lý gọi hàm gợi ý
    def on_recommend(self):
        fav_genres = [item.text() for item in self.genre_list.selectedItems()]
        fav_year_text = self.fav_year_input.text().strip()
        fav_year = int(fav_year_text) if fav_year_text.isdigit() else None
        top_k_text = self.top_k_input.text().strip()
        top_k = int(top_k_text) if top_k_text.isdigit() else 5

        self.result_area.clear()
        
        try:
            recs = recommend_movies(fav_genres, fav_year, top_k)
            result_str = "\n".join([f"{i+1}. {row['title']} (Điểm: {row['final_score']:.2f})"
                                    for i,row in recs.iterrows()])
            if not result_str:
                self.result_area.setText("Không tìm thấy bộ phim nào phù hợp.")
            else:
                self.result_area.setText(result_str)
        except Exception as e:
            self.result_area.setText(f"Đã xảy ra lỗi: {str(e)}")