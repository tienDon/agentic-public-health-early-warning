import joblib
import numpy as np
from features.missing_feature_checker import (
    MissingFeatureChecker
)
class RiskPredictor:
    def __init__(self, bundle_path):
        """
        Load toàn bộ bundle và khởi tạo các thông tin cần thiết.
        """
        bundle = joblib.load(bundle_path)

        self.lgb_model = bundle["lgb_model"]
        self.xgb_model = bundle.get("xgb_model")
        self.features = bundle["features"]
        self.feature_schema = bundle["feature_schema"]
        
        self.version = bundle.get("version", "unknown")
        self.target = bundle.get("target", None)

    def health_check(self):
        """Kiểm tra tình trạng sức khỏe của mô hình."""
        return {
            "status":
                "healthy"
                if self.lgb_model is not None
                else "unhealthy",

            "version": self.version,

            "feature_count":
                len(self.features),

            "ensemble":
                self.xgb_model is not None
            }

    def validate_features(self, X):

        report = (
            MissingFeatureChecker.check(
                X.columns,
                self.features
            )
        )

        if not report["valid"]:

            raise ValueError(
                f"Missing features: "
                f"{report['missing']}"
            )

        if report["extra"]:

            print(
                f"Warning: Extra features ignored: "
                f"{report['extra']}"
            )

        return True

    def validate_schema(self, X):

        for col in self.features:

            if col not in X.columns:
                raise ValueError(
                    f"Missing feature: {col}"
                )

            if not np.issubdtype(
                X[col].dtype,
                np.number
            ):
                raise ValueError(
                    f"{col} must be numeric"
                )

        return True

    def validate_missing_values(self, X):
        missing_count = X.isnull().sum().sum()
        if missing_count > 0:
            raise ValueError(f"Input contains {missing_count} missing values")
        return True

    def reorder_features(self, X):
        return X[self.features]

    def _run_preprocessing_pipeline(self, X):
        """Gom nhóm các bước kiểm tra đầu vào."""
        self.validate_features(X)
        self.validate_schema(X)
        self.validate_missing_values(X)
        return self.reorder_features(X)

    def classify_risk(self, score):
        if score < 30: return "LOW"
        elif score < 60: return "MEDIUM"
        return "HIGH"

    def calculate_confidence(self, pred_lgb, pred_xgb):
        if pred_xgb is None: return 1.0
        diff = abs(pred_lgb - pred_xgb)
        return round(float(max(0, 1 - (diff / 100))), 3)

    def predict(self, X):
        X = self._run_preprocessing_pipeline(X)
        
        pred_lgb_log = self.lgb_model.predict(X)
        if self.xgb_model:
            pred_xgb_log = self.xgb_model.predict(X)
            pred_log = (pred_lgb_log + pred_xgb_log) / 2
        else:
            pred_log = pred_lgb_log

        pred_real = np.clip(np.expm1(pred_log), 0, 100)
        return pred_real

    def predict_with_metadata(self, X):
        # Tiền xử lý tập trung
        X_processed = self._run_preprocessing_pipeline(X)

        pred_lgb_log = self.lgb_model.predict(X_processed)
        model_used = "lightgbm"
        pred_xgb_log = None

        if self.xgb_model:
            pred_xgb_log = self.xgb_model.predict(X_processed)
            pred_log = (pred_lgb_log + pred_xgb_log) / 2
            model_used = "ensemble"
        else:
            pred_log = pred_lgb_log

        score = float(np.clip(np.expm1(pred_log[0]), 0, 100))
        
        # Tính confidence
        confidence = self.calculate_confidence(
            np.expm1(pred_lgb_log[0]),
            np.expm1(pred_xgb_log[0]) if pred_xgb_log is not None else None
        )

        return {
            "risk_score": round(score, 2),
            "risk_level": self.classify_risk(score),
            "confidence": confidence,
            "model_used": model_used,
            "model_version": self.version
        }

    def get_model_info(self):

        return {
            "version": self.version,
            "target": self.target,
            "feature_count": len(self.features),
            "ensemble": self.xgb_model is not None
        }
    def get_required_features(self):
        return self.features    



