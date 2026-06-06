# src/services/graph_inference_service.py
from src.schemas.graph_state import create_initial_state
from src.graphs.graph_dependencies import get_prediction_graph, get_shared_predictor

class GraphInferenceService:

    def __init__(self):
        self.graph = get_prediction_graph()
        # Lưu reference của predictor vào đây để API Router gọi được trực tiếp!
        self.predictor = get_shared_predictor()

    def predict(self, input_data: dict) -> dict:
        state = create_initial_state(input_data=input_data)
        return self.graph.invoke(state)

    async def predict_batch(self, batch_data: list[dict]) -> list[dict]:
        initial_states = [create_initial_state(input_data=item) for item in batch_data]
        config = {"max_concurrency": 2} # Giới hạn concurrency chống lỗi nghẽn Groq/Gemini 429
        results = await self.graph.abatch(initial_states, config=config)
        return results