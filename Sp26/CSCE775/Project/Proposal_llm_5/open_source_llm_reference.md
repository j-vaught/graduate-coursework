# Open-Source / Open-Weight LLM Reference Guide
**Last Updated:** February 2026
**Author:** J.C. Vaught

A comprehensive reference of all major open-source and open-weight LLM families, their available sizes, base model availability, licensing, and links.

---

## Table of Contents
1. [Models with Full Size Coverage (1-2B, 7-8B, 12-15B)](#tier-1-full-size-coverage)
2. [Major Model Families (Partial Coverage)](#tier-2-major-families-partial-coverage)
3. [MoE / Large-Scale Only Models](#tier-3-moe--large-scale-only)
4. [Specialized / Research Models](#tier-4-specialized--research)
5. [Quick Comparison Table](#quick-comparison-table)

---

## Tier 1: Full Size Coverage

These families provide base (pretrained, non-instruct) models across all three target tiers (~1-2B, ~7-8B, ~12-15B), making them suitable for controlled scaling experiments.

### Qwen3 (Alibaba Cloud)
- **Developer:** Qwen Team, Alibaba Cloud
- **Release:** April 2025
- **Architecture:** Dense Transformer (+ MoE variants)
- **License:** Apache 2.0
- **Training Data:** 36 trillion tokens, 119 languages
- **Context Length:** 32,768 tokens (base models)

| Size | Model ID | Parameters | HuggingFace |
|------|----------|------------|-------------|
| 0.6B | `Qwen/Qwen3-0.6B-Base` | 0.6B | https://huggingface.co/Qwen/Qwen3-0.6B-Base |
| 1.7B | `Qwen/Qwen3-1.7B-Base` | 1.7B | https://huggingface.co/Qwen/Qwen3-1.7B-Base |
| 4B | `Qwen/Qwen3-4B-Base` | 4B | https://huggingface.co/Qwen/Qwen3-4B-Base |
| 8B | `Qwen/Qwen3-8B-Base` | 8B | https://huggingface.co/Qwen/Qwen3-8B-Base |
| 14B | `Qwen/Qwen3-14B-Base` | 14.8B (13.2B non-embedding) | https://huggingface.co/Qwen/Qwen3-14B-Base |
| 32B | `Qwen/Qwen3-32B-Base` | 32B | https://huggingface.co/Qwen/Qwen3-32B-Base |
| 30B-A3B (MoE) | `Qwen/Qwen3-30B-A3B` | 30B total / 3B active | https://huggingface.co/Qwen/Qwen3-30B-A3B |
| 235B-A22B (MoE) | `Qwen/Qwen3-235B-A22B` | 235B total / 22B active | https://huggingface.co/Qwen/Qwen3-235B-A22B |

- **Website:** https://qwenlm.github.io/blog/qwen3/
- **GitHub:** https://github.com/QwenLM/Qwen3
- **Also released:** Qwen3.5 (late 2025), Qwen3-Coder-480B-A35B

---

### Qwen 2.5 (Alibaba Cloud)
- **Developer:** Qwen Team, Alibaba Cloud
- **Release:** September 2024
- **Architecture:** Dense Transformer
- **License:** Apache 2.0 (0.5B, 1.5B, 7B, 14B, 32B); Qwen License (3B, 72B)
- **Training Data:** 18 trillion tokens
- **Context Length:** 128K tokens

| Size | Model ID | HuggingFace |
|------|----------|-------------|
| 0.5B | `Qwen/Qwen2.5-0.5B` | https://huggingface.co/Qwen/Qwen2.5-0.5B |
| 1.5B | `Qwen/Qwen2.5-1.5B` | https://huggingface.co/Qwen/Qwen2.5-1.5B |
| 3B | `Qwen/Qwen2.5-3B` | https://huggingface.co/Qwen/Qwen2.5-3B |
| 7B | `Qwen/Qwen2.5-7B` | https://huggingface.co/Qwen/Qwen2.5-7B |
| 14B | `Qwen/Qwen2.5-14B` | https://huggingface.co/Qwen/Qwen2.5-14B |
| 32B | `Qwen/Qwen2.5-32B` | https://huggingface.co/Qwen/Qwen2.5-32B |
| 72B | `Qwen/Qwen2.5-72B` | https://huggingface.co/Qwen/Qwen2.5-72B |

- **Website:** https://qwenlm.github.io/blog/qwen2.5/
- **GitHub:** https://github.com/QwenLM/Qwen2.5
- **Also available:** Qwen2.5-Coder, Qwen2.5-Math (specialized variants)

---

### OLMo 2 (Allen Institute for AI)
- **Developer:** AI2 (Allen Institute for AI)
- **Release:** January 2025 (OLMo 2), November 2025 (OLMo 3)
- **Architecture:** Dense Transformer
- **License:** Apache 2.0 (fully open: weights, training data, training code, intermediate checkpoints)
- **Training Data:** Dolma dataset (fully open)
- **Context Length:** 4,096 tokens (base)

| Size | Model ID | HuggingFace |
|------|----------|-------------|
| 1B | `allenai/OLMo-2-0425-1B` | https://huggingface.co/allenai/OLMo-2-0425-1B |
| 7B | `allenai/OLMo-2-1124-7B` | https://huggingface.co/allenai/OLMo-2-1124-7B |
| 13B | `allenai/OLMo-2-1124-13B` | https://huggingface.co/allenai/OLMo-2-1124-13B |
| 32B | `allenai/OLMo-2-0325-32B` | https://huggingface.co/allenai/OLMo-2-0325-32B |

- **Website:** https://allenai.org/olmo
- **GitHub:** https://github.com/allenai/OLMo
- **Note:** Gold standard for research reproducibility. Full training data (Dolma), training code, evaluation code, and 500+ intermediate checkpoints all open.

---

### Pythia (EleutherAI)
- **Developer:** EleutherAI
- **Release:** 2023
- **Architecture:** Dense Transformer (GPT-NeoX based)
- **License:** Apache 2.0
- **Training Data:** The Pile, 300B tokens (dated by current standards)
- **Context Length:** 2,048 tokens

| Size | Model ID | HuggingFace |
|------|----------|-------------|
| 14M | `EleutherAI/pythia-14m` | https://huggingface.co/EleutherAI/pythia-14m |
| 31M | `EleutherAI/pythia-31m` | https://huggingface.co/EleutherAI/pythia-31m |
| 70M | `EleutherAI/pythia-70m` | https://huggingface.co/EleutherAI/pythia-70m |
| 160M | `EleutherAI/pythia-160m` | https://huggingface.co/EleutherAI/pythia-160m |
| 410M | `EleutherAI/pythia-410m` | https://huggingface.co/EleutherAI/pythia-410m |
| 1B | `EleutherAI/pythia-1b` | https://huggingface.co/EleutherAI/pythia-1b |
| 1.4B | `EleutherAI/pythia-1.4b` | https://huggingface.co/EleutherAI/pythia-1.4b |
| 2.8B | `EleutherAI/pythia-2.8b` | https://huggingface.co/EleutherAI/pythia-2.8b |
| 6.9B | `EleutherAI/pythia-6.9b` | https://huggingface.co/EleutherAI/pythia-6.9b |
| 12B | `EleutherAI/pythia-12b` | https://huggingface.co/EleutherAI/pythia-12b |

- **Website:** https://www.eleuther.ai/
- **GitHub:** https://github.com/EleutherAI/pythia
- **Note:** 154 intermediate checkpoints per model. Designed for interpretability and training dynamics research. Deduplicated variants also available (suffix `-deduped`).

---

### TeleChat (China Telecom)
- **Developer:** China Telecom / TeleAI
- **Release:** 2024
- **Architecture:** Dense Transformer
- **License:** TeleChat Community License (custom, commercial use requires application)

| Size | Model ID | HuggingFace |
|------|----------|-------------|
| 1B | `Tele-AI/TeleChat-1B` | https://huggingface.co/Tele-AI/TeleChat-1B |
| 7B | `Tele-AI/telechat-7B` | https://huggingface.co/Tele-AI/telechat-7B |
| 12B | `Tele-AI/TeleChat-12B` | https://huggingface.co/Tele-AI/TeleChat-12B |

- **Note:** Chinese/English bilingual focus. Restrictive license limits broader use.

---

## Tier 2: Major Families (Partial Coverage)

These are high-quality model families that are missing one of the three target size tiers.

### Gemma 3 (Google DeepMind)
- **Developer:** Google DeepMind
- **Release:** March 2025
- **Architecture:** Dense Transformer
- **License:** Gemma Terms of Use (custom, allows commercial use with restrictions)
- **Context Length:** 128K tokens (4B+), 32K tokens (270M, 1B)
- **Missing:** No 7-8B model (gap between 4B and 12B)

| Size | Model ID | HuggingFace |
|------|----------|-------------|
| 270M | `google/gemma-3-270m-pt` | https://huggingface.co/google/gemma-3-270m-pt |
| 1B | `google/gemma-3-1b-pt` | https://huggingface.co/google/gemma-3-1b-pt |
| 4B | `google/gemma-3-4b-pt` | https://huggingface.co/google/gemma-3-4b-pt |
| 12B | `google/gemma-3-12b-pt` | https://huggingface.co/google/gemma-3-12b-pt |
| 27B | `google/gemma-3-27b-pt` | https://huggingface.co/google/gemma-3-27b-pt |

- **Website:** https://ai.google.dev/gemma/docs/core
- **Note:** Multimodal (image + text) at 4B+. Base models use `-pt` suffix (pretrained).

---

### Meta Llama 3.1 / 3.2 / 3.3
- **Developer:** Meta
- **Release:** July 2024 (3.1), September 2024 (3.2), December 2024 (3.3)
- **Architecture:** Dense Transformer
- **License:** Llama 3.x Community License (permissive for <700M MAU)
- **Missing:** No 12-15B model. Llama 3.2 (1B/3B) is a different architecture from 3.1 (8B).

| Version | Size | Model ID | HuggingFace |
|---------|------|----------|-------------|
| 3.2 | 1B | `meta-llama/Llama-3.2-1B` | https://huggingface.co/meta-llama/Llama-3.2-1B |
| 3.2 | 3B | `meta-llama/Llama-3.2-3B` | https://huggingface.co/meta-llama/Llama-3.2-3B |
| 3.1 | 8B | `meta-llama/Llama-3.1-8B` | https://huggingface.co/meta-llama/Llama-3.1-8B |
| 3.1 | 70B | `meta-llama/Llama-3.1-70B` | https://huggingface.co/meta-llama/Llama-3.1-70B |
| 3.1 | 405B | `meta-llama/Llama-3.1-405B` | https://huggingface.co/meta-llama/Llama-3.1-405B |
| 3.3 | 70B | `meta-llama/Llama-3.3-70B` | https://huggingface.co/meta-llama/Llama-3.3-70B |

- **Website:** https://www.llama.com/
- **GitHub:** https://github.com/meta-llama/llama

---

### Ministral 3 (Mistral AI)
- **Developer:** Mistral AI
- **Release:** December 2025
- **Architecture:** Dense Transformer
- **License:** Apache 2.0
- **Missing:** Smallest is 3B (no 1-2B)

| Size | Model ID | HuggingFace |
|------|----------|-------------|
| 3B | `mistralai/Ministral-3-3B-Base-2512` | https://huggingface.co/mistralai/Ministral-3-3B-Base-2512 |
| 8B | `mistralai/Ministral-3-8B-Base-2512` | https://huggingface.co/mistralai/Ministral-3-8B-Base-2512 |
| 14B | `mistralai/Ministral-3-14B-Base-2512` | https://huggingface.co/mistralai/Ministral-3-14B-Base-2512 |

- **Website:** https://mistral.ai/
- **Also available:** Mistral Small 3 (24B), Mistral Large 3 (675B MoE)

---

### Falcon 3 (TII)
- **Developer:** Technology Innovation Institute (UAE)
- **Release:** December 2024
- **Architecture:** Dense Transformer
- **License:** TII Falcon License (permissive, royalty-free)
- **Missing:** Largest dense model is 10B (below 12-15B tier)

| Size | Model ID | HuggingFace |
|------|----------|-------------|
| 1B | `tiiuae/Falcon3-1B-Base` | https://huggingface.co/tiiuae/Falcon3-1B-Base |
| 3B | `tiiuae/Falcon3-3B-Base` | https://huggingface.co/tiiuae/Falcon3-3B-Base |
| 7B | `tiiuae/Falcon3-7B-Base` | https://huggingface.co/tiiuae/Falcon3-7B-Base |
| 10B | `tiiuae/Falcon3-10B-Base` | https://huggingface.co/tiiuae/Falcon3-10B-Base |

- **Website:** https://falconllm.tii.ae/
- **GitHub:** https://huggingface.co/tiiuae

---

### Falcon-H1 (TII)
- **Developer:** Technology Innovation Institute (UAE)
- **Release:** May 2025
- **Architecture:** Hybrid SSM-Transformer (Mamba2 + Attention)
- **License:** TII Falcon License
- **Missing:** No 12-15B (jumps from 7B to 34B)

| Size | Model ID | HuggingFace |
|------|----------|-------------|
| 0.5B | `tiiuae/Falcon-H1-0.5B-Base` | https://huggingface.co/tiiuae/Falcon-H1-0.5B-Base |
| 1.5B | `tiiuae/Falcon-H1-1.5B-Base` | https://huggingface.co/tiiuae/Falcon-H1-1.5B-Base |
| 1.5B-deep | `tiiuae/Falcon-H1-1.5B-Deep-Base` | https://huggingface.co/tiiuae/Falcon-H1-1.5B-Deep-Base |
| 3B | `tiiuae/Falcon-H1-3B-Base` | https://huggingface.co/tiiuae/Falcon-H1-3B-Base |
| 7B | `tiiuae/Falcon-H1-7B-Base` | https://huggingface.co/tiiuae/Falcon-H1-7B-Base |
| 34B | `tiiuae/Falcon-H1-34B-Base` | https://huggingface.co/tiiuae/Falcon-H1-34B-Base |

- **Note:** Hybrid architecture (not pure Transformer). Interesting for architecture comparison studies.

---

### IBM Granite 3.x / 4.0
- **Developer:** IBM
- **Release:** 2024-2025 (rolling)
- **Architecture:** Dense + Hybrid (SSM-Transformer) + MoE variants
- **License:** Apache 2.0
- **Missing:** No 12-15B dense model

| Version | Size | Model ID | Architecture | HuggingFace |
|---------|------|----------|-------------|-------------|
| 3.0 | 2B | `ibm-granite/granite-3.0-2b-base` | Dense | https://huggingface.co/ibm-granite/granite-3.0-2b-base |
| 3.1 | 8B | `ibm-granite/granite-3.1-8b-base` | Dense | https://huggingface.co/ibm-granite/granite-3.1-8b-base |
| 4.0 | 1B | `ibm-granite/granite-4.0-h-1b-base` | Hybrid | https://huggingface.co/ibm-granite/granite-4.0-h-1b-base |
| 4.0 | 3B | `ibm-granite/granite-4.0-h-3b-base` | Hybrid | https://huggingface.co/ibm-granite/granite-4.0-h-3b-base |
| 4.0 | 7B MoE | `ibm-granite/granite-4.0-tiny-preview` | MoE (7B/1B active) | https://huggingface.co/ibm-granite/granite-4.0-tiny-preview |

- **Website:** https://www.ibm.com/granite
- **GitHub:** https://github.com/ibm-granite

---

### InternLM 2.5 (Shanghai AI Lab)
- **Developer:** Shanghai AI Lab / InternLM Team
- **Release:** 2024-2025
- **Architecture:** Dense Transformer
- **License:** Apache 2.0 (code); custom license (weights)
- **Missing:** 20B overshoots the 12-15B tier

| Size | Model ID | HuggingFace |
|------|----------|-------------|
| 1.8B | `internlm/internlm2_5-1_8b` | https://huggingface.co/internlm/internlm2_5-1_8b |
| 7B | `internlm/internlm2_5-7b` | https://huggingface.co/internlm/internlm2_5-7b |
| 20B | `internlm/internlm2-20b` | https://huggingface.co/internlm/internlm2-20b |

- **Website:** https://internlm.intern-ai.org.cn/
- **GitHub:** https://github.com/InternLM/InternLM

---

### Yi 1.5 (01.AI)
- **Developer:** 01.AI (Kai-Fu Lee)
- **Release:** 2024
- **Architecture:** Dense Transformer
- **License:** Apache 2.0
- **Missing:** No 1-2B model

| Size | Model ID | HuggingFace |
|------|----------|-------------|
| 6B | `01-ai/Yi-1.5-6B` | https://huggingface.co/01-ai/Yi-1.5-6B |
| 9B | `01-ai/Yi-1.5-9B` | https://huggingface.co/01-ai/Yi-1.5-9B |
| 34B | `01-ai/Yi-1.5-34B` | https://huggingface.co/01-ai/Yi-1.5-34B |

- **Website:** https://www.01.ai/
- **GitHub:** https://github.com/01-ai/Yi-1.5

---

### StableLM 2 (Stability AI)
- **Developer:** Stability AI
- **Release:** 2024
- **Architecture:** Dense Transformer
- **License:** Stability AI Community License (custom)
- **Missing:** No 7-8B model (gap between 1.6B and 12B)

| Size | Model ID | HuggingFace |
|------|----------|-------------|
| 1.6B | `stabilityai/stablelm-2-1_6b` | https://huggingface.co/stabilityai/stablelm-2-1_6b |
| 12B | `stabilityai/stablelm-2-12b` | https://huggingface.co/stabilityai/stablelm-2-12b |

- **Website:** https://stability.ai/

---

### Baichuan 2 / Baichuan-M1
- **Developer:** Baichuan Intelligence
- **Release:** 2023 (Baichuan 2), 2025 (M1)
- **Architecture:** Dense Transformer
- **License:** Baichuan Community License (custom, commercial requires application)
- **Missing:** No 1-2B model

| Size | Model ID | HuggingFace |
|------|----------|-------------|
| 7B | `baichuan-inc/Baichuan-7B` | https://huggingface.co/baichuan-inc/Baichuan-7B |
| 13B | `baichuan-inc/Baichuan-13B-Base` | https://huggingface.co/baichuan-inc/Baichuan-13B-Base |
| 14B (Medical) | `baichuan-inc/Baichuan-M1-14B-Base` | https://huggingface.co/baichuan-inc/Baichuan-M1-14B-Base |

---

## Tier 3: MoE / Large-Scale Only

These families only offer very large models or use Mixture-of-Experts architecture.

### Meta Llama 4
- **Developer:** Meta
- **Release:** April 2025
- **Architecture:** MoE (all models)
- **License:** Llama 4 Community License
- **Base Models:** Not released (instruct only)

| Size | Total Params | Active Params | Experts |
|------|-------------|---------------|---------|
| Scout | 109B | 17B | 16 |
| Maverick | 400B | 17B | 128 |
| Behemoth | 2T | 288B | 16 (not released) |

- **Website:** https://www.llama.com/models/llama-4/

---

### DeepSeek V3
- **Developer:** DeepSeek
- **Release:** December 2024
- **Architecture:** MoE
- **License:** DeepSeek License (custom, permissive)
- **Base Model:** `deepseek-ai/DeepSeek-V3-Base` (671B total / 37B active)

- **Website:** https://www.deepseek.com/
- **GitHub:** https://github.com/deepseek-ai/DeepSeek-V3
- **Note:** Single massive model only. DeepSeek-R1 distills are available (1.5B-70B) but are NOT base models.

---

### DeepSeek R1 (Distilled Models)
- **Developer:** DeepSeek
- **Release:** January 2025
- **Architecture:** Dense Transformer (distilled from R1)
- **License:** MIT
- **IMPORTANT:** These are reasoning-tuned models, NOT base pretrained models.

| Size | Model ID | Base Architecture | HuggingFace |
|------|----------|-------------------|-------------|
| 1.5B | `deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B` | Qwen2.5 | https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B |
| 7B | `deepseek-ai/DeepSeek-R1-Distill-Qwen-7B` | Qwen2.5 | https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-7B |
| 8B | `deepseek-ai/DeepSeek-R1-Distill-Llama-8B` | Llama 3.1 | https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-8B |
| 14B | `deepseek-ai/DeepSeek-R1-Distill-Qwen-14B` | Qwen2.5 | https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-14B |
| 32B | `deepseek-ai/DeepSeek-R1-Distill-Qwen-32B` | Qwen2.5 | https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Qwen-32B |
| 70B | `deepseek-ai/DeepSeek-R1-Distill-Llama-70B` | Llama 3.1 | https://huggingface.co/deepseek-ai/DeepSeek-R1-Distill-Llama-70B |

- **GitHub:** https://github.com/deepseek-ai/DeepSeek-R1

---

### MiniMax M1 / M2
- **Developer:** MiniMax
- **Release:** 2025-2026
- **Architecture:** MoE with hybrid attention (Lightning Attention + Softmax Attention)
- **License:** Modified MIT
- **Base Models:** Not released (post-trained only)

| Model | Total Params | Active Params |
|-------|-------------|---------------|
| M1 | 456B | 45.9B |
| M2 | 230B | 10B |
| M2.5 | 230B+ | 10B+ |

- **Website:** https://www.minimaxi.com/
- **GitHub:** https://github.com/MiniMax-AI

---

### Kimi K2 / K2.5 (Moonshot AI)
- **Developer:** Moonshot AI
- **Release:** July 2025 (K2), January 2026 (K2.5)
- **Architecture:** MoE
- **License:** Modified MIT
- **Base Models:** Not released (instruct/agent-tuned only)

| Model | Total Params | Active Params |
|-------|-------------|---------------|
| K2 | 1T | 32B |
| K2.5 | 1T+ | unknown |

- **Website:** https://kimi.moonshot.cn/
- **GitHub:** https://github.com/MoonshotAI/Kimi-K2

---

### GLM-4 (Zhipu AI / Z.ai)
- **Developer:** Z.ai (formerly Zhipu AI / THUDM)
- **Release:** April 2025
- **Architecture:** Dense Transformer
- **License:** MIT
- **Missing:** No 1-2B model

| Size | Model ID | HuggingFace |
|------|----------|-------------|
| 9B | `THUDM/glm-4-9b` | https://huggingface.co/THUDM/glm-4-9b |
| 32B | `THUDM/GLM-4-32B-Base-0414` | https://huggingface.co/THUDM/GLM-4-32B-Base-0414 |

- **GitHub:** https://github.com/THUDM/GLM-4

---

### NVIDIA Nemotron 3
- **Developer:** NVIDIA
- **Release:** December 2025
- **Architecture:** MoE
- **License:** NVIDIA Open Model License

| Model | Total Params | Active Params | HuggingFace |
|-------|-------------|---------------|-------------|
| Nano | 31.6B | 3.2B | https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-Base-BF16 |

- **Website:** https://developer.nvidia.com/nemotron

---

### Microsoft Phi-3 / Phi-4
- **Developer:** Microsoft
- **Release:** 2024-2025
- **Architecture:** Dense Transformer
- **License:** MIT
- **IMPORTANT:** No base (pretrained) models released. All are instruction-tuned.

| Model | Size | Model ID | Type |
|-------|------|----------|------|
| Phi-3 Mini | 3.8B | `microsoft/Phi-3-mini-4k-instruct` | Instruct only |
| Phi-3 Medium | 14B | `microsoft/Phi-3-medium-4k-instruct` | Instruct only |
| Phi-4 | 14B | `microsoft/phi-4` | Instruct only |
| Phi-4 Mini | 3.8B | `microsoft/Phi-4-mini-instruct` | Instruct only |

- **Website:** https://azure.microsoft.com/en-us/products/phi
- **Note:** Cannot be used for RLHF-from-scratch research due to lack of base models.

---

## Tier 4: Specialized / Research

### RWKV-7 (Goose)
- **Developer:** RWKV Foundation / BlinkDL
- **Release:** March 2025
- **Architecture:** RNN (linear attention, NOT Transformer)
- **License:** Apache 2.0

| Size | Model ID | HuggingFace |
|------|----------|-------------|
| 0.1B | `RWKV/rwkv-7-world-0.1B` | https://huggingface.co/RWKV/rwkv-7-world-0.1B |
| 0.4B | `RWKV/rwkv-7-world-0.4B` | https://huggingface.co/RWKV/rwkv-7-world-0.4B |
| 1.5B | `RWKV/rwkv-7-world-1.5B` | https://huggingface.co/RWKV/rwkv-7-world-1.5B |
| 2.9B | `RWKV/rwkv-7-world-2.9B` | https://huggingface.co/RWKV/rwkv-7-world-2.9B |

- **Website:** https://www.rwkv.com/
- **GitHub:** https://github.com/BlinkDL/RWKV-LM

---

### Mamba / Mamba-2
- **Developer:** Albert Gu, Tri Dao (Princeton/CMU)
- **Release:** 2023-2024
- **Architecture:** State Space Model (SSM)
- **License:** Apache 2.0

| Size | Model ID | HuggingFace |
|------|----------|-------------|
| 130M | `state-spaces/mamba-130m` | https://huggingface.co/state-spaces/mamba-130m |
| 370M | `state-spaces/mamba-370m` | https://huggingface.co/state-spaces/mamba-370m |
| 790M | `state-spaces/mamba-790m` | https://huggingface.co/state-spaces/mamba-790m |
| 1.4B | `state-spaces/mamba-1.4b` | https://huggingface.co/state-spaces/mamba-1.4b |
| 2.8B | `state-spaces/mamba-2.8b` | https://huggingface.co/state-spaces/mamba-2.8b |

- **GitHub:** https://github.com/state-spaces/mamba

---

### SmolLM 2 / SmolLM 3 (Hugging Face)
- **Developer:** Hugging Face
- **Release:** 2024-2025
- **Architecture:** Dense Transformer
- **License:** Apache 2.0

| Size | Model ID | HuggingFace |
|------|----------|-------------|
| 135M | `HuggingFaceTB/SmolLM2-135M` | https://huggingface.co/HuggingFaceTB/SmolLM2-135M |
| 360M | `HuggingFaceTB/SmolLM2-360M` | https://huggingface.co/HuggingFaceTB/SmolLM2-360M |
| 1.7B | `HuggingFaceTB/SmolLM2-1.7B` | https://huggingface.co/HuggingFaceTB/SmolLM2-1.7B |
| 3B | `HuggingFaceTB/SmolLM3-3B-Base` | https://huggingface.co/HuggingFaceTB/SmolLM3-3B-Base |

- **Website:** https://huggingface.co/blog/smollm

---

### OpenELM (Apple)
- **Developer:** Apple
- **Release:** April 2024
- **Architecture:** Dense Transformer (layer-wise scaled attention)
- **License:** Apple Sample Code License

| Size | Model ID | HuggingFace |
|------|----------|-------------|
| 270M | `apple/OpenELM-270M` | https://huggingface.co/apple/OpenELM-270M |
| 450M | `apple/OpenELM-450M` | https://huggingface.co/apple/OpenELM-450M |
| 1.1B | `apple/OpenELM-1_1B` | https://huggingface.co/apple/OpenELM-1_1B |
| 3B | `apple/OpenELM-3B` | https://huggingface.co/apple/OpenELM-3B |

- **GitHub:** https://github.com/apple/corenet

---

### Skywork (Kunlun)
- **Developer:** Kunlun Wanwei / Skywork AI
- **Release:** 2023-2025
- **Architecture:** Dense Transformer
- **License:** Skywork Community License (custom)

| Size | Model ID | HuggingFace |
|------|----------|-------------|
| 13B | `SkyworkAI/Skywork-13B-Base` | https://huggingface.co/SkyworkAI/Skywork-13B-Base |

- **GitHub:** https://github.com/SkyworkAI/Skywork

---

### Zamba 2 (Zyphra)
- **Developer:** Zyphra
- **Release:** 2024-2025
- **Architecture:** Hybrid SSM-Transformer
- **License:** Apache 2.0

| Size | Model ID | HuggingFace |
|------|----------|-------------|
| 2.7B | `Zyphra/Zamba2-2.7B` | https://huggingface.co/Zyphra/Zamba2-2.7B |
| 7B | `Zyphra/Zamba2-7B` | https://huggingface.co/Zyphra/Zamba2-7B |

- **Website:** https://www.zyphra.com/
- **Note:** Hybrid architecture, interesting for architecture comparison.

---

### Jamba 1.5 / 2 (AI21 Labs)
- **Developer:** AI21 Labs
- **Release:** 2024-2025
- **Architecture:** Hybrid SSM-Transformer, MoE
- **License:** Jamba Open Model License (custom)

| Model | Total Params | Active Params | HuggingFace |
|-------|-------------|---------------|-------------|
| Jamba 1.5 Mini | 52B | 12B | https://huggingface.co/ai21labs/AI21-Jamba-1.5-Mini |
| Jamba 1.5 Large | 398B | 94B | https://huggingface.co/ai21labs/AI21-Jamba-1.5-Large |
| Jamba 2 | ~52B | ~12B | https://huggingface.co/ai21labs/ |

- **Website:** https://www.ai21.com/jamba

---

### BLOOM (BigScience)
- **Developer:** BigScience / Hugging Face
- **Release:** July 2022
- **Architecture:** Dense Transformer
- **License:** RAIL License (Responsible AI License)
- **Note:** Historically significant but very outdated.

| Size | Model ID | HuggingFace |
|------|----------|-------------|
| 560M | `bigscience/bloom-560m` | https://huggingface.co/bigscience/bloom-560m |
| 1.1B | `bigscience/bloom-1b1` | https://huggingface.co/bigscience/bloom-1b1 |
| 1.7B | `bigscience/bloom-1b7` | https://huggingface.co/bigscience/bloom-1b7 |
| 3B | `bigscience/bloom-3b` | https://huggingface.co/bigscience/bloom-3b |
| 7.1B | `bigscience/bloom-7b1` | https://huggingface.co/bigscience/bloom-7b1 |
| 176B | `bigscience/bloom` | https://huggingface.co/bigscience/bloom |

---

### Command R (Cohere)
- **Developer:** Cohere
- **Release:** 2024
- **Architecture:** Dense Transformer
- **License:** CC-BY-NC (non-commercial only)
- **Note:** No base models released. Instruct/chat only.

| Size | Model ID | HuggingFace |
|------|----------|-------------|
| 35B | `CohereForAI/c4ai-command-r-v01` | https://huggingface.co/CohereForAI/c4ai-command-r-v01 |
| 104B | `CohereForAI/c4ai-command-r-plus` | https://huggingface.co/CohereForAI/c4ai-command-r-plus |

---

### MAP-Neo
- **Developer:** MAP Team
- **Release:** 2024
- **Architecture:** Dense Transformer
- **License:** Apache 2.0

| Size | Model ID | HuggingFace |
|------|----------|-------------|
| 2B | `m-a-p/neo_2b` | https://huggingface.co/m-a-p/neo_2b |
| 7B | `m-a-p/neo_7b` | https://huggingface.co/m-a-p/neo_7b |

---

## Quick Comparison Table

### All Families At a Glance

| Family | Developer | Sizes Available | Base? | License | Released | Arch |
|--------|-----------|----------------|-------|---------|----------|------|
| Qwen3 | Alibaba | 0.6B-235B | Yes | Apache 2.0 | Apr 2025 | Dense+MoE |
| Qwen 2.5 | Alibaba | 0.5B-72B | Yes | Apache 2.0 | Sep 2024 | Dense |
| OLMo 2 | AI2 | 1B-32B | Yes | Apache 2.0 | Jan 2025 | Dense |
| Gemma 3 | Google | 270M-27B | Yes | Custom | Mar 2025 | Dense |
| Llama 3.1/3.2 | Meta | 1B-405B | Yes | Custom | 2024 | Dense |
| Llama 4 | Meta | 109B-2T | No | Custom | Apr 2025 | MoE |
| Ministral 3 | Mistral | 3B-14B | Yes | Apache 2.0 | Dec 2025 | Dense |
| Falcon 3 | TII | 1B-10B | Yes | Custom | Dec 2024 | Dense |
| Falcon-H1 | TII | 0.5B-34B | Yes | Custom | May 2025 | Hybrid |
| Granite 3/4 | IBM | 1B-8B | Yes | Apache 2.0 | 2024-25 | Dense+Hybrid |
| InternLM 2.5 | Shanghai AI | 1.8B-20B | Yes | Custom | 2024-25 | Dense |
| Yi 1.5 | 01.AI | 6B-34B | Yes | Apache 2.0 | 2024 | Dense |
| StableLM 2 | Stability | 1.6B-12B | Yes | Custom | 2024 | Dense |
| Pythia | EleutherAI | 14M-12B | Yes | Apache 2.0 | 2023 | Dense |
| DeepSeek V3 | DeepSeek | 671B | Yes | Custom | Dec 2024 | MoE |
| DeepSeek R1 | DeepSeek | 1.5B-70B | No* | MIT | Jan 2025 | Dense |
| GLM-4 | Z.ai | 9B-32B | Yes | MIT | Apr 2025 | Dense |
| MiniMax M1/M2 | MiniMax | 230B-456B | No | Mod MIT | 2025-26 | MoE |
| Kimi K2 | Moonshot | 1T | No | Mod MIT | Jul 2025 | MoE |
| Phi-3/4 | Microsoft | 3.8B-14B | No | MIT | 2024-25 | Dense |
| Nemotron 3 | NVIDIA | 31.6B | Yes | Custom | Dec 2025 | MoE |
| RWKV-7 | RWKV Found. | 0.1B-2.9B | Yes | Apache 2.0 | Mar 2025 | RNN |
| Mamba | Gu/Dao | 130M-2.8B | Yes | Apache 2.0 | 2023-24 | SSM |
| SmolLM 2/3 | HuggingFace | 135M-3B | Yes | Apache 2.0 | 2024-25 | Dense |
| OpenELM | Apple | 270M-3B | Yes | Custom | Apr 2024 | Dense |
| Baichuan 2 | Baichuan | 7B-14B | Yes | Custom | 2023-25 | Dense |
| Skywork | Kunlun | 13B | Yes | Custom | 2023-25 | Dense |
| Zamba 2 | Zyphra | 2.7B-7B | Yes | Apache 2.0 | 2024-25 | Hybrid |
| Jamba 1.5/2 | AI21 | 52B-398B | Partial | Custom | 2024-25 | Hybrid MoE |
| TeleChat | China Tel. | 1B-12B | Yes | Custom | 2024 | Dense |
| BLOOM | BigScience | 560M-176B | Yes | RAIL | 2022 | Dense |
| Command R | Cohere | 35B-104B | No | CC-BY-NC | 2024 | Dense |
| MAP-Neo | MAP Team | 2B-7B | Yes | Apache 2.0 | 2024 | Dense |

*DeepSeek R1 distills are reasoning-tuned, not base pretrained models.

---

## Key Frameworks for Fine-Tuning / RLHF

| Framework | URL | Supports |
|-----------|-----|----------|
| OpenRLHF | https://github.com/OpenRLHF/OpenRLHF | PPO, REINFORCE++, GRPO, DPO, RLOO |
| TRL | https://github.com/huggingface/trl | DPO, PPO, GRPO, SFT, ORPO |
| LlamaFactory | https://github.com/hiyouga/LlamaFactory | SFT, DPO, PPO, RLHF (100+ models) |
| Unsloth | https://github.com/unslothai/unsloth | SFT, DPO (2x faster, 60% less VRAM) |
| Axolotl | https://github.com/OpenAccess-AI-Collective/axolotl | SFT, DPO, RLHF |
| DeepSpeed-Chat | https://github.com/microsoft/DeepSpeedExamples | SFT, reward modeling, RLHF |

---

## Key Datasets for RLHF / Alignment Research

| Dataset | URL | Size | Format |
|---------|-----|------|--------|
| Anthropic HH-RLHF | https://huggingface.co/datasets/Anthropic/hh-rlhf | ~170K pairs | Chosen/rejected text |
| PKU-SafeRLHF | https://huggingface.co/datasets/PKU-Alignment/PKU-SafeRLHF | ~167K pairs | Safety preference pairs |
| BeaverTails | https://huggingface.co/datasets/PKU-Alignment/BeaverTails | 300K+ | 19 harm categories |
| UltraFeedback | https://huggingface.co/datasets/openbmb/UltraFeedback | ~64K prompts | Multi-aspect ratings |
| HelpSteer2 | https://huggingface.co/datasets/nvidia/HelpSteer2 | ~10K | Multi-attribute preference |
| Nectar | https://huggingface.co/datasets/berkeley-nest/Nectar | ~183K | 7-wise ranked comparisons |
