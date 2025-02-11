from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Izvēlamies DeepSeek AI modeli
MODEL_NAME = "deepseek-ai/deepseek-coder-6.7b-base"

try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(MODEL_NAME, trust_remote_code=True, torch_dtype=torch.bfloat16).cuda()

    print("✅ DeepSeek AI ir veiksmīgi ielādēts!")

except Exception as e:
    print("❌ Kļūda DeepSeek AI ielādē:", e)
