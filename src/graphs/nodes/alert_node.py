import logging
from src.schemas.graph_state import PredictionState

logger = logging.getLogger(__name__)

class AlertNode:
    def __init__(self, alert_service):
        self.alert_service = alert_service

    def __call__(self, state: PredictionState) -> dict:
        if state.get("status") == "failed":
            return {}

        logger.info("Kích hoạt AlertNode tạo cảnh báo hệ thống.")
        try:
            alert_message = self.alert_service.generate_alert(
                state["risk_level"],
                state["confidence"]
            )
            return {
                "alert_message": alert_message,
            }
        except Exception as e:
            logger.error("Lỗi tạo alert message", exc_info=True)
            return {}