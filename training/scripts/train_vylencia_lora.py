import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
)
from transformers import BitsAndBytesConfig
from peft import LoraConfig, get_peft_model
from transformers.utils import quantization_config
from trl import SFTTrainer
import yaml
import os

# -------------------------------------------------
# Load training config
# -------------------------------------------------
with open("training/configs/vylencia_lora_config.yaml", "r") as f:
    cfg = yaml.safe_load(f)

BASE_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
DATA_PATH = cfg["data"]["path"]

# -------------------------------------------------
# Load tokenizer & model (frozen base)
# -------------------------------------------------
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, use_fast=False)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

bnb_config = BitsAndBytesConfig(load_in_8bit=True)

model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    quantization_config=bnb_config,
    device_map="auto",
)

model.gradient_checkpointing_enable()
model.config.use_cache = False

# -------------------------------------------------
# Apply LoRA
# -------------------------------------------------
lora_cfg = LoraConfig(
    r=cfg["lora"]["r"],
    lora_alpha=cfg["lora"]["alpha"],
    lora_dropout=cfg["lora"]["dropout"],
    target_modules=cfg["lora"]["target_modules"],
    bias="none",
    task_type="CAUSAL_LM",
)

model = get_peft_model(model, lora_cfg)

# -------------------------------------------------
# Load dataset
# -------------------------------------------------
dataset = load_dataset(
    "json",
    data_files=DATA_PATH,
    split="train"
)

def format_example(example):
    text = f"""### Instruction:
{example['context']}
    
### Response:
{example['response']}"""

    return text + tokenizer.eos_token

# -------------------------------------------------
# Training arguments
# -------------------------------------------------
training_args = TrainingArguments(
    output_dir="training/outputs",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    num_train_epochs=1,
    max_steps=50,
    learning_rate=2e-4,
    fp16=True,
    logging_dir="training/logs",
    logging_steps=5,
    save_strategy="no",
    report_to="none",
)

# -------------------------------------------------
# Trainer (instruction tuning)
# -------------------------------------------------
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    formatting_func=format_example,
    args=training_args,
    processing_class=tokenizer,
)


# -------------------------------------------------
# Train (DO NOT RUN YET)
# -------------------------------------------------
if __name__ == "__main__":
    print("Training script...")
    trainer.train()
    trainer.model.save_pretrained("training/outputs/final_adapter")
    tokenizer.save_pretrained("training/outputs/final_adapter")