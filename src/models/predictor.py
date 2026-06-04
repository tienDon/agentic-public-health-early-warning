import joblib
import numpy as np

class RiskPredictor:
    def __init__(self, bundle_path):
        bundle = joblib.load(bundle_path)
        self.lgb_model = bundle["lgb_model"]
        self.xgb_model = bundle.get("xgb_model")
        self.features = bundle["features"]
        self.feature_schema = bundle["feature_schema"]
        self.version = bundle.get("version", "unknown")
        self.target = bundle.get("target", None)

    def health_check(self):
        return {
            "status": "healthy" if self.lgb_model is not None else "unhealthy",
            "version": self.version,
            "feature_count": len(self.features),
            "ensemble": self.xgb_model is not None
        }

    def get_required_features(self):
        return self.features

    def reorder_features(self, X):
        return X[self.features]
        
    def get_primary_model(self):
        """Trả về mô hình chính để dùng cho XAI (SHAP)"""
        return self.lgb_model

    def predict(self, X):
        """Chỉ thực hiện dự báo toán học thuần túy"""
        X_clean = self.reorder_features(X)
        
        pred_lgb_log = self.lgb_model.predict(X_clean)
        pred_xgb_log = None

        if self.xgb_model:
            pred_xgb_log = self.xgb_model.predict(X_clean)
            pred_log = (pred_lgb_log + pred_xgb_log) / 2
        else:
            pred_log = pred_lgb_log

        # Inverse log và clip
        pred_real = np.clip(np.expm1(pred_log), 0, 100)
        
        # Trả về cả kết quả raw để InferenceService tự tính confidence
        return {
            "score": float(pred_real[0]),
            "pred_lgb_raw": float(np.expm1(pred_lgb_log[0])),
            "pred_xgb_raw": float(np.expm1(pred_xgb_log[0])) if self.xgb_model else None,
            "model_used": "ensemble" if self.xgb_model else "lightgbm"
        }

    def get_model_info(self):
        return {
            "version": self.version,
            "target": self.target,
            "feature_count": len(self.features),
            "ensemble": self.xgb_model is not None
        }


