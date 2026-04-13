import torch
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
)
from peft import LoraConfig, get_peft_model
from trl import SFTTrainer
import yaml
import os

# -------------------------------------------------
# Load training config
# -------------------------------------------------
with open("training/configs/vylencia_lora_config.yaml", "r") as f:
    cfg = yaml.safe_load(f)

BASE_MODEL = "google/gemma-2-2b-it"
DATA_PATH = cfg["data"]["path"]

# -------------------------------------------------
# Load tokenizer & model (frozen base)
# -------------------------------------------------
tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, use_fast=False)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(
    BASE_MODEL,
    load_in_8bit=torch.cuda.is_available(),
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
    per_device_train_batch_size=cfg["training"]["batch_size"],
    gradient_accumulation_steps=cfg["training"]["gradient_accumulation"],
    num_train_epochs=cfg["training"]["epochs"],
    learning_rate=float(cfg["training"]["learning_rate"]),
    warmup_ratio=cfg["training"]["warmup_ratio"],
    fp16=cfg["training"]["fp16"],
    logging_dir="training/logs",
    logging_steps=10,
    save_strategy="epoch",
    report_to="none",
)

# -------------------------------------------------
# Trainer (instruction tuning)
# -------------------------------------------------
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    formatting_func=format_example,
    args=training_args,
)


# -------------------------------------------------
# Train (DO NOT RUN YET)
# -------------------------------------------------
if __name__ == "__main__":
    print("Training script...")
    trainer.train()
    trainer.model.save_pretrained("training/outputs/final_adapter")
    tokenizer.save_pretrained("training/outputs/final_adapter")