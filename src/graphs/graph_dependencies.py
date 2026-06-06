# src/graphs/graph_dependencies.py
import logging
from pathlib import Path
from src.models.predictor import RiskPredictor
from src.features.feature_validator import FeatureValidator
from src.services.alert_service import AlertService
from src.services.shap_explanation_service import ShapExplanationService
from src.agents.explanation_agent import ExplanationAgent
from src.agents.recommendation_agent import RecommendationAgent

from src.graphs.nodes import (
    PredictNode, 
    ShapNode, 
    AlertNode, 
    RecommendationNode, 
    ExplanationNode
)
from src.graphs.prediction_graph import PredictionGraph

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "artifacts" / "ensemble_bundle.joblib"
logger = logging.getLogger(__name__)

# --- BỘ NHỚ ĐỆM TOÀN CỤC CHỈ LƯU TRỮ ĐỒ THỊ VÀ PREDICTOR THÔ ---
_compiled_graph = None
_shared_predictor = None  # Lưu trữ predictor để chia sẻ cho các endpoint metadata

def get_prediction_graph():
    """
    Singleton Factory: Khởi tạo tất cả các dependencies, nodes 
    và compile đồ thị LangGraph chỉ một lần duy nhất (Lazy Loading).
    """
    global _compiled_graph, _shared_predictor

    if _compiled_graph is None:
        logger.info("Initializing Graph Dependencies and compiling LangGraph pipeline...")
        try:
            # 1. Khởi tạo các Core Services & ML Models nặng
            _shared_predictor = RiskPredictor(MODEL_PATH)
            
            validator = FeatureValidator(
                expected_features=_shared_predictor.features,
                feature_schema=_shared_predictor.feature_schema
            )
            
            alert_service = AlertService()
            
            shap_service = ShapExplanationService(
                model=_shared_predictor.get_primary_model(),
                feature_names=_shared_predictor.features
            )
            
            # 2. Khởi tạo LLM Agents
            explanation_agent = ExplanationAgent()
            recommendation_agent = RecommendationAgent()
            
            # 3. Khởi tạo hệ thống Nodes hạt nhân độc lập
            predict_node = PredictNode(_shared_predictor, validator)
            shap_node = ShapNode(shap_service, _shared_predictor)
            alert_node = AlertNode(alert_service)
            explanation_node = ExplanationNode(explanation_agent)
            recommendation_node = RecommendationNode(recommendation_agent)
            
            # 4. Khởi tạo Wrapper chứa cấu trúc đồ thị
            prediction_pipeline = PredictionGraph(
                predict_node,
                shap_node,
                alert_node,
                explanation_node,
                recommendation_node
            )
            
            _compiled_graph = prediction_pipeline.graph
            logger.info("LangGraph pipeline compiled successfully.")
            
        except Exception as e:
            logger.critical("Failed to initialize and compile Prediction LangGraph!", exc_info=True)
            raise e

    return _compiled_graph


def get_shared_predictor() -> RiskPredictor:
    """
    Hàm bổ trợ giúp bốc nhanh thực thể predictor ra ngoài 
    mà không cần lội ngược dòng vào cấu trúc đồ thị LangGraph phức tạp.
    """
    global _shared_predictor
    if _shared_predictor is None:
        # Nếu chưa chạy qua get_prediction_graph thì trigger chạy để khởi tạo
        get_prediction_graph()
    return _shared_predictor