from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_NAME = "deepseek-ai/deepseek-coder"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

class DeepSeekCodeOptimizer:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME, trust_remote_code=True, torch_dtype=torch.float32
        ).to(DEVICE)

    def refactor_strategy(self, strategy_code):
        """
        AI analizē un optimizē kodu, lai sasniegtu 65%+ win rate
        """
        input_text = f"Optimize this trading strategy code to achieve 65%+ win rate:\n{strategy_code}"
        inputs = self.tokenizer(input_text, return_tensors="pt").to(DEVICE)
        outputs = self.model.generate(**inputs, max_length=512)

        optimized_code = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return optimized_code
