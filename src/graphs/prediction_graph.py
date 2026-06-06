from src.graphs.nodes import (
    PredictNode, 
    ShapNode, 
    AlertNode, 
    RecommendationNode, 
    ExplanationNode
    )

# Phác thảo cách kết nối trong file prediction_graph.py sắp tới:
from langgraph.graph import StateGraph, START, END
from src.schemas.graph_state import PredictionState

class PredictionGraph:

    def __init__(
        self,
        predict_node,
        shap_node,
        alert_node,
        explanation_node,
        recommendation_node
    ):
        self.predict_node = predict_node
        self.shap_node = shap_node
        self.alert_node = alert_node
        self.explanation_node = explanation_node
        self.recommendation_node = recommendation_node

        self.graph = self._build()

    def _build(self):

        builder = StateGraph(PredictionState)

        builder.add_node("predict", self.predict_node)

        builder.add_node("shap", self.shap_node)

        builder.add_node("alert", self.alert_node)

        builder.add_node("explanation", self.explanation_node)

        builder.add_node("recommendation", self.recommendation_node)

        builder.add_edge(START, "predict")

        builder.add_edge("predict", "shap")

        builder.add_edge("shap", "alert")

        builder.add_edge("alert", "explanation")

        builder.add_edge("explanation", "recommendation")

        builder.add_edge("recommendation", END)

        return builder.compile()
    
    def invoke(self, state: PredictionState) -> PredictionState:
        return self.graph.invoke(state)