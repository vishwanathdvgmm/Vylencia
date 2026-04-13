import yaml
from datasets import load_dataset

CONFIG_PATH = "training/configs/vylencia_lora_config.yaml"

print("Loading config...")
with open(CONFIG_PATH, "r") as f:
    cfg = yaml.safe_load(f)

print("Config OK")

print("Loading dataset...")
ds = load_dataset("json", data_files=cfg["data"]["path"], split="train")

print(f"Dataset loaded: {len(ds)} samples")

sample = ds[0]
assert "context" in sample
assert "response" in sample

print("Sample entry:")
print(sample)

print("Environment validation PASSED")
