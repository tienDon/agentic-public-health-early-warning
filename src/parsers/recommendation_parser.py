# src/parsers/recommendation_parser.py

class RecommendationParser:
    
    @staticmethod
    def parse(text: str) -> list:
        """
        Nhận vào text thô từ LLM, thực hiện bóc tách (parse) 
        và kiểm tra tính hợp lệ (validate).
        """
        if not text:
            return []
            
        lines = text.strip().split('\n')
        recommendations = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('-'):
                content = line.lstrip('- ').strip()
                if ':' in content:
                    priority, action = content.split(':', 1)
                    priority_clean = priority.strip().upper()
                    action_clean = action.strip()
                    
                    # Đoạn validate dữ liệu đầu vào
                    if priority_clean in ["HIGH", "MEDIUM", "LOW"] and action_clean:
                        recommendations.append({
                            "priority": priority_clean,
                            "action": action_clean
                        })
                        
        return recommendations