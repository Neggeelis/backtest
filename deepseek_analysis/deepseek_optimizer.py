from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import pandas as pd

MODEL_NAME = "deepseek-ai/deepseek-v3-base"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

class DeepSeekOptimizer:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME, trust_remote_code=True, torch_dtype=torch.float32, device_map="auto"
        ).to(DEVICE)

    def optimize_strategy(self, df: pd.DataFrame):
        """AI analizē datus un atgriež strukturētu stratēģiju (BUY, SELL, HOLD)."""
        input_text = "Analyze market data and return structured JSON with trading signals:\n" + df.to_string()
        inputs = self.tokenizer(input_text, return_tensors="pt").to(DEVICE)
        outputs = self.model.generate(**inputs, max_length=512)

        ai_decision = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        strategy_dict = {"signal": 0, "comment": ai_decision}
        if "BUY" in ai_decision:
            strategy_dict["signal"] = 1
        elif "SELL" in ai_decision:
            strategy_dict["signal"] = -1

        return strategy_dict
