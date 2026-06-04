climate-health-early-warning/
├── .venv/                      # Thư mục môi trường ảo (uv tự tạo)
├── data/                       # NƠI CHỨA DATA (Quản lý tập trung)
│   ├── raw/                    # <--- Ném 3 file vừa tải từ Kaggle vào đây
│   └── processed/              # Nơi lưu data sau khi bạn đã clean hoặc trích xuất feature
├── notebooks/                  # Nơi chứa các file Jupyter Notebook để test/EDA
│   └── 01_data_exploration.ipynb
├── src/                        # Mã nguồn chính của dự án (viết dạng module)
│   ├── __init__.py
│   ├── predictor.py            # Code train model dự báo (XGBoost/LSTM)
│   ├── agents.py               # Code định nghĩa LangGraph Agents
│   └── utils.py                # Các hàm bổ trợ (load data, custom log...)
├── pyproject.toml              # File config của uv
├── requirements.txt            # Danh sách thư viện
└── README.md                   # Hướng dẫn chạy dự án