import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime
from collections import Counter

# Brand colors
GARNET = '#73000A'
BLACK = '#000000'
ROSE = '#CC2E40'
ATLANTIC = '#466A9F'
CONGAREE = '#1F414D'
HORSESHOE = '#65780B'
GRASS = '#CED318'
HONEYCOMB = '#A49137'
BLACK_90 = '#363636'
BLACK_70 = '#5C5C5C'
BLACK_50 = '#A2A2A2'
BLACK_30 = '#C7C7C7'
WARM_GREY = '#676156'
SANDSTORM = '#FFF2E3'

# Format: (date_str, org, country, model_name, [sizes_in_billions], 'open'|'closed')
# For closed models with unknown sizes, use None in the list
releases = [
    # ===================================================================
    # OPEN-WEIGHT MODELS
    # ===================================================================

    # ===== 2019 =====
    ('2019-02-14', 'OpenAI', 'United States', 'GPT-2', [0.124, 0.355, 0.774, 1.558], 'open'),
    ('2019-10-23', 'Google', 'United States', 'T5', [0.060, 0.220, 0.770, 3.0, 11.0], 'open'),

    # ===== 2020 =====
    # (open-weight: none notable)

    # ===== 2021 =====
    ('2021-03-21', 'EleutherAI', 'United States', 'GPT-Neo', [0.125, 1.3, 2.7], 'open'),
    ('2021-06-04', 'EleutherAI', 'United States', 'GPT-J', [6.053], 'open'),

    # ===== 2022 =====
    ('2022-02-09', 'EleutherAI', 'United States', 'GPT-NeoX', [20.0], 'open'),
    ('2022-05-03', 'Meta', 'United States', 'OPT', [0.125, 0.350, 1.3, 2.7, 6.7, 13.0, 30.0, 66.0, 175.0], 'open'),
    ('2022-07-12', 'BigScience (Hugging Face)', 'France', 'BLOOM', [0.560, 1.1, 1.7, 3.0, 7.1, 176.247], 'open'),
    ('2022-10-20', 'Google', 'United States', 'Flan-T5', [0.080, 0.250, 0.780, 3.0, 11.0], 'open'),

    # ===== 2023 =====
    ('2023-02-27', 'Meta', 'United States', 'LLaMA 1', [6.7, 13.0, 32.5, 65.2], 'open'),
    ('2023-03-28', 'Cerebras Systems', 'United States', 'Cerebras-GPT', [0.111, 0.256, 0.590, 1.3, 2.7, 6.7, 13.0], 'open'),
    ('2023-04-19', 'Stability AI', 'United Kingdom', 'StableLM-Alpha', [3.0, 7.0], 'open'),
    ('2023-05-04', 'BigCode (Hugging Face / ServiceNow)', 'International', 'StarCoder', [1.0, 3.0, 7.0, 15.5], 'open'),
    ('2023-05-05', 'MosaicML', 'United States', 'MPT', [6.7, 30.0], 'open'),
    ('2023-05-25', 'Technology Innovation Institute', 'United Arab Emirates', 'Falcon', [7.0, 40.0], 'open'),
    ('2023-06-15', 'Baichuan Intelligent Technology', 'China', 'Baichuan', [7.0, 13.0], 'open'),
    ('2023-06-20', 'Microsoft', 'United States', 'Phi-1', [1.3], 'open'),
    ('2023-07-18', 'Meta', 'United States', 'Llama 2', [7.0, 13.0, 70.0], 'open'),
    ('2023-08-03', 'Alibaba Cloud (Qwen Team)', 'China', 'Qwen v1', [7.0, 14.0, 72.0], 'open'),
    ('2023-08-24', 'Meta', 'United States', 'Code Llama', [7.0, 13.0, 34.0], 'open'),
    ('2023-09-06', 'Technology Innovation Institute', 'United Arab Emirates', 'Falcon-180B', [180.0], 'open'),
    ('2023-09-12', 'Microsoft', 'United States', 'Phi-1.5', [1.3], 'open'),
    ('2023-09-27', 'Mistral AI', 'France', 'Mistral 7B', [7.24], 'open'),
    ('2023-11-02', '01.AI', 'China', 'Yi', [6.0, 34.0], 'open'),
    ('2023-11-02', 'DeepSeek AI', 'China', 'DeepSeek-Coder', [1.3, 5.7, 6.7, 33.0], 'open'),
    ('2023-11-29', 'DeepSeek AI', 'China', 'DeepSeek-LLM', [7.0, 67.0], 'open'),
    ('2023-12-11', 'Mistral AI', 'France', 'Mixtral 8x7B', [46.7], 'open'),
    ('2023-12-12', 'Microsoft', 'United States', 'Phi-2', [2.7], 'open'),

    # ===== 2024 =====
    ('2024-01-11', 'DeepSeek AI', 'China', 'DeepSeek-MoE', [16.4], 'open'),
    ('2024-02-04', 'Alibaba Cloud (Qwen Team)', 'China', 'Qwen1.5', [0.5, 1.8, 4.0, 7.0, 14.0, 32.0, 72.0, 110.0], 'open'),
    ('2024-02-05', 'DeepSeek AI', 'China', 'DeepSeek-Math', [7.0], 'open'),
    ('2024-02-21', 'Google DeepMind', 'United States', 'Gemma 1', [2.51, 8.54], 'open'),
    ('2024-02-29', 'BigCode (Hugging Face / ServiceNow)', 'International', 'StarCoder 2', [3.0, 7.0, 15.0], 'open'),
    ('2024-03-12', 'Cohere', 'Canada', 'Command R', [35.0], 'open'),
    ('2024-03-17', 'xAI', 'United States', 'Grok-1', [314.0], 'open'),
    ('2024-03-27', 'Databricks', 'United States', 'DBRX', [132.0], 'open'),
    ('2024-04-10', 'Mistral AI', 'France', 'Mixtral 8x22B', [141.0], 'open'),
    ('2024-04-18', 'Meta', 'United States', 'Llama 3', [8.0, 70.0], 'open'),
    ('2024-04-23', 'Microsoft', 'United States', 'Phi-3', [3.8, 7.0, 14.0], 'open'),
    ('2024-04-24', 'Apple', 'United States', 'OpenELM', [0.27, 0.45, 1.1, 3.0], 'open'),
    ('2024-04-24', 'Snowflake', 'United States', 'Arctic', [480.0], 'open'),
    ('2024-05-07', 'DeepSeek AI', 'China', 'DeepSeek-V2', [236.0], 'open'),
    ('2024-05-14', 'Technology Innovation Institute', 'United Arab Emirates', 'Falcon 2', [11.0], 'open'),
    ('2024-05-29', 'Mistral AI', 'France', 'Codestral', [22.0], 'open'),
    ('2024-06-07', 'Alibaba Cloud (Qwen Team)', 'China', 'Qwen2', [0.49, 1.54, 7.6, 57.0, 72.7], 'open'),
    ('2024-06-14', 'NVIDIA', 'United States', 'Nemotron-4 340B', [340.0], 'open'),
    ('2024-06-17', 'DeepSeek AI', 'China', 'DeepSeek-Coder-V2', [16.0, 236.0], 'open'),
    ('2024-06-27', 'Google DeepMind', 'United States', 'Gemma 2', [2.61, 9.24, 27.23], 'open'),
    ('2024-07-18', 'Mistral AI', 'France', 'Mistral Nemo', [12.0], 'open'),
    ('2024-07-23', 'Meta', 'United States', 'Llama 3.1', [8.0, 70.0, 405.0], 'open'),
    ('2024-07-24', 'Mistral AI', 'France', 'Mistral Large 2', [123.0], 'open'),
    ('2024-08-21', 'Microsoft', 'United States', 'Phi-3.5', [3.8, 4.2, 41.9], 'open'),
    ('2024-09-05', 'DeepSeek AI', 'China', 'DeepSeek-V2.5', [236.0], 'open'),
    ('2024-09-19', 'Alibaba Cloud (Qwen Team)', 'China', 'Qwen2.5', [0.49, 1.54, 3.09, 7.61, 14.7, 32.5, 72.7], 'open'),
    ('2024-09-25', 'Meta', 'United States', 'Llama 3.2', [1.0, 3.0, 11.0, 90.0], 'open'),
    ('2024-10-16', 'Mistral AI', 'France', 'Ministral', [3.0, 8.0], 'open'),
    ('2024-10-21', 'IBM', 'United States', 'Granite 3.0', [1.0, 2.5, 3.0, 8.1], 'open'),
    ('2024-11-18', 'Mistral AI', 'France', 'Pixtral Large', [124.0], 'open'),
    ('2024-11-26', 'Allen Institute for AI (Ai2)', 'United States', 'OLMo 2', [7.0, 14.0], 'open'),
    ('2024-11-27', 'Alibaba Cloud (Qwen Team)', 'China', 'QwQ-32B', [32.5], 'open'),
    ('2024-12-06', 'Meta', 'United States', 'Llama 3.3', [70.0], 'open'),
    ('2024-12-12', 'Microsoft', 'United States', 'Phi-4', [14.0], 'open'),
    ('2024-12-17', 'Technology Innovation Institute', 'United Arab Emirates', 'Falcon 3', [1.0, 3.0, 7.0, 10.0], 'open'),
    ('2024-12-26', 'DeepSeek AI', 'China', 'DeepSeek-V3', [671.0], 'open'),

    # ===== 2025 =====
    ('2025-01-15', 'MiniMax', 'China', 'MiniMax-Text-01', [456.0], 'open'),
    ('2025-01-15', 'Shanghai AI Laboratory', 'China', 'InternLM3', [8.0], 'open'),
    ('2025-01-20', 'DeepSeek AI', 'China', 'DeepSeek-R1', [671.0], 'open'),
    ('2025-01-20', 'DeepSeek AI', 'China', 'DeepSeek-R1-Distill', [1.5, 7.0, 8.0, 14.0, 32.0, 70.0], 'open'),
    ('2025-01-26', 'Alibaba Cloud (Qwen Team)', 'China', 'Qwen2.5-VL', [3.0, 7.0, 72.0], 'open'),
    ('2025-01-30', 'Mistral AI', 'France', 'Mistral Small 3', [24.0], 'open'),
    ('2025-02-01', 'Microsoft', 'United States', 'Phi-4-mini', [3.8], 'open'),
    ('2025-02-18', 'Baichuan Intelligent Technology', 'China', 'Baichuan-M1', [14.0], 'open'),
    ('2025-02-19', 'Alibaba Cloud (Qwen Team)', 'China', 'Qwen2.5-VL-32B', [32.0], 'open'),
    ('2025-02-26', 'Microsoft', 'United States', 'Phi-4-multimodal', [5.6], 'open'),
    ('2025-03-10', 'Reka AI', 'United States', 'Reka Flash 3', [21.0], 'open'),
    ('2025-03-12', 'Google DeepMind', 'United States', 'Gemma 3', [1.0, 4.0, 12.0, 27.0], 'open'),
    ('2025-03-13', 'Allen Institute for AI (Ai2)', 'United States', 'OLMo 2 32B', [32.0], 'open'),
    ('2025-03-16', 'Cohere', 'Canada', 'Command A', [111.0], 'open'),
    ('2025-03-17', 'Mistral AI', 'France', 'Mistral Small 3.1', [24.0], 'open'),
    ('2025-03-18', 'NVIDIA', 'United States', 'Nemotron-Nano-8B', [8.0], 'open'),
    ('2025-03-24', 'DeepSeek AI', 'China', 'DeepSeek-V3-0324', [671.0], 'open'),
    ('2025-03-26', 'Alibaba Cloud (Qwen Team)', 'China', 'Qwen2.5-Omni', [7.0], 'open'),
    ('2025-04-05', 'Meta', 'United States', 'Llama 4 Scout', [109.0], 'open'),
    ('2025-04-05', 'Meta', 'United States', 'Llama 4 Maverick', [400.0], 'open'),
    ('2025-04-07', 'NVIDIA', 'United States', 'Nemotron-Ultra-253B', [253.0], 'open'),
    ('2025-04-16', 'IBM', 'United States', 'Granite 3.3', [2.5, 8.0], 'open'),
    ('2025-04-29', 'Alibaba Cloud (Qwen Team)', 'China', 'Qwen3', [0.6, 1.7, 4.0, 8.0, 14.0, 30.0, 32.0, 235.0], 'open'),
    ('2025-04-30', 'Microsoft', 'United States', 'Phi-4-reasoning', [14.0], 'open'),
    ('2025-04-30', 'Microsoft', 'United States', 'Phi-4-reasoning-plus', [14.0], 'open'),
    ('2025-04-30', 'DeepSeek AI', 'China', 'DeepSeek-Prover-V2', [7.0, 671.0], 'open'),
    ('2025-05-01', 'Allen Institute for AI (Ai2)', 'United States', 'OLMo 2 1B', [1.0], 'open'),
    ('2025-05-07', 'Mistral AI', 'France', 'Mistral Medium 3', [70.0], 'open'),
    ('2025-05-11', 'ByteDance', 'China', 'Seed1.5-VL', [20.0], 'open'),
    ('2025-05-20', 'NVIDIA', 'United States', 'Nemotron-Nano-4B', [4.0], 'open'),
    ('2025-05-21', 'Mistral AI', 'France', 'Devstral', [24.0], 'open'),
    ('2025-05-28', 'DeepSeek AI', 'China', 'DeepSeek-R1-0528', [671.0], 'open'),
    ('2025-06-10', 'Mistral AI', 'France', 'Magistral Small', [24.0], 'open'),
    ('2025-06-17', 'MiniMax', 'China', 'MiniMax-M1', [456.0], 'open'),
    ('2025-06-20', 'Mistral AI', 'France', 'Mistral Small 3.2', [24.0], 'open'),
    ('2025-07-08', 'Hugging Face', 'United States', 'SmolLM3', [3.0], 'open'),
    ('2025-07-11', 'Moonshot AI', 'China', 'Kimi K2', [1000.0], 'open'),
    ('2025-07-22', 'Alibaba Cloud (Qwen Team)', 'China', 'Qwen3-Coder', [480.0], 'open'),
    ('2025-07-25', 'NVIDIA', 'United States', 'Nemotron-Super-49B', [49.9], 'open'),
    ('2025-07-28', 'Zhipu AI (Z.ai)', 'China', 'GLM-4.5', [355.0, 106.0], 'open'),
    ('2025-07-30', 'Tencent', 'China', 'Hunyuan Small', [0.5, 1.8, 4.0, 7.0], 'open'),
    ('2025-07-31', 'StepFun', 'China', 'Step3', [321.0], 'open'),
    ('2025-08-01', 'Mistral AI', 'France', 'Codestral 25.08', [22.0], 'open'),
    ('2025-08-05', 'OpenAI', 'United States', 'GPT-OSS', [20.9, 117.0], 'open'),
    ('2025-08-11', 'Baichuan Intelligent Technology', 'China', 'Baichuan-M2', [32.0], 'open'),
    ('2025-08-14', 'Google DeepMind', 'United States', 'Gemma 3 270M', [0.27], 'open'),
    ('2025-08-20', 'ByteDance', 'China', 'Seed-OSS-36B', [36.0], 'open'),
    ('2025-08-21', 'DeepSeek AI', 'China', 'DeepSeek-V3.1', [685.0], 'open'),
    ('2025-08-25', 'xAI', 'United States', 'Grok 2.5', [270.0], 'open'),
    ('2025-09-09', 'Alibaba Cloud (Qwen Team)', 'China', 'Qwen3-Next', [80.0], 'open'),
    ('2025-09-18', 'Moondream', 'United States', 'Moondream 3', [9.0], 'open'),
    ('2025-09-22', 'Alibaba Cloud (Qwen Team)', 'China', 'Qwen3-Omni', [30.0], 'open'),
    ('2025-09-24', 'Meta (FAIR)', 'United States', 'Code World Model', [32.0], 'open'),
    ('2025-09-29', 'DeepSeek AI', 'China', 'DeepSeek-V3.2-Exp', [685.0], 'open'),
    ('2025-09-30', 'Zhipu AI (Z.ai)', 'China', 'GLM-4.6', [357.0], 'open'),
    ('2025-10-02', 'IBM', 'United States', 'Granite 4.0', [3.0, 7.0, 32.0], 'open'),
    ('2025-10-04', 'Alibaba Cloud (Qwen Team)', 'China', 'Qwen3-VL', [2.0, 4.0, 8.0, 32.0], 'open'),
    ('2025-10-27', 'MiniMax', 'China', 'MiniMax-M2', [230.0], 'open'),
    ('2025-11-06', 'Moonshot AI', 'China', 'Kimi K2 Thinking', [1000.0], 'open'),
    ('2025-11-20', 'Allen Institute for AI (Ai2)', 'United States', 'OLMo 3', [7.0, 32.0], 'open'),
    ('2025-11-27', 'DeepSeek AI', 'China', 'DeepSeekMath-V2', [685.0], 'open'),
    ('2025-12-01', 'DeepSeek AI', 'China', 'DeepSeek-V3.2', [685.0], 'open'),
    ('2025-12-02', 'Mistral AI', 'France', 'Mistral Large 3', [675.0], 'open'),
    ('2025-12-02', 'Mistral AI', 'France', 'Ministral 3', [3.0, 8.0, 14.0], 'open'),
    ('2025-12-05', 'Tencent', 'China', 'Hunyuan 2.0', [406.0], 'open'),
    ('2025-12-09', 'Mistral AI', 'France', 'Devstral 2', [123.0], 'open'),
    ('2025-12-09', 'Mistral AI', 'France', 'Devstral Small 2', [24.0], 'open'),
    ('2025-12-15', 'NVIDIA', 'United States', 'Nemotron 3 Nano', [31.6], 'open'),
    ('2025-12-16', 'Xiaomi', 'China', 'MiMo-V2-Flash', [309.0], 'open'),
    ('2025-12-22', 'Zhipu AI (Z.ai)', 'China', 'GLM-4.7', [355.0], 'open'),
    ('2025-12-23', 'MiniMax', 'China', 'MiniMax-M2.1', [230.0], 'open'),

    # ===== 2026 =====
    ('2026-01-13', 'Google', 'United States', 'MedGemma 1.5', [4.0], 'open'),
    ('2026-01-15', 'Google', 'United States', 'TranslateGemma', [4.0, 12.0, 27.0], 'open'),
    ('2026-01-27', 'Moonshot AI', 'China', 'Kimi K2.5', [1000.0], 'open'),
    ('2026-01-28', 'Arcee AI', 'United States', 'Trinity Large', [398.0], 'open'),
    ('2026-02-03', 'StepFun', 'China', 'Step 3.5 Flash', [196.81], 'open'),
    ('2026-02-03', 'Alibaba Cloud (Qwen Team)', 'China', 'Qwen3-Coder-Next', [80.0], 'open'),
    ('2026-02-11', 'Zhipu AI (Z.ai)', 'China', 'GLM-5', [744.0], 'open'),
    ('2026-02-12', 'MiniMax', 'China', 'MiniMax-M2.5', [230.0], 'open'),
    ('2026-02-16', 'Alibaba Cloud (Qwen Team)', 'China', 'Qwen3.5', [0.8, 2.0, 4.0, 9.0, 27.0, 122.0, 397.0], 'open'),
    ('2026-02-16', 'Ant Group', 'China', 'Ling-2.5-1T', [1000.0], 'open'),
    ('2026-02-17', 'Cohere', 'Canada', 'Tiny Aya', [3.35], 'open'),
    ('2026-03-04', 'Microsoft', 'United States', 'Phi-4-Reasoning-Vision', [15.0], 'open'),

    # ===================================================================
    # CLOSED-SOURCE MODELS
    # ===================================================================

    # ===== 2020 =====
    ('2020-06-11', 'OpenAI', 'United States', 'GPT-3', [175.0, 6.7, 1.3, 0.35], 'closed'),

    # ===== 2021 =====
    ('2021-05-18', 'Google', 'United States', 'LaMDA 1', [137.0], 'closed'),
    ('2021-08-01', 'AI21 Labs', 'Israel', 'Jurassic-1', [178.0, 7.5], 'closed'),
    ('2021-08-10', 'OpenAI', 'United States', 'Codex', [12.0], 'closed'),
    ('2021-05-25', 'Naver', 'South Korea', 'HyperCLOVA', [204.0], 'closed'),

    # ===== 2022 =====
    ('2022-05-11', 'Google', 'United States', 'LaMDA 2', [137.0], 'closed'),
    ('2022-03-15', 'OpenAI', 'United States', 'InstructGPT', [175.0], 'closed'),
    ('2022-11-30', 'OpenAI', 'United States', 'ChatGPT (GPT-3.5)', [175.0], 'closed'),
    ('2022-11-08', 'Cohere', 'Canada', 'Command (xlarge)', [52.0], 'closed'),

    # ===== 2023 =====
    ('2023-03-09', 'AI21 Labs', 'Israel', 'Jurassic-2', [178.0], 'closed'),
    ('2023-03-14', 'OpenAI', 'United States', 'GPT-4', [1760.0], 'closed'),
    ('2023-03-14', 'Anthropic', 'United States', 'Claude 1.0', [None], 'closed'),
    ('2023-03-14', 'Google', 'United States', 'PaLM API', [540.0], 'closed'),
    ('2023-03-16', 'Baidu', 'China', 'ERNIE Bot 3.0', [10.0], 'closed'),
    ('2023-04-11', 'Alibaba Cloud', 'China', 'Tongyi Qianwen 1.0', [None], 'closed'),
    ('2023-05-03', 'Inflection AI', 'United States', 'Inflection-1 (Pi)', [None], 'closed'),
    ('2023-05-10', 'Google', 'United States', 'PaLM 2', [340.0], 'closed'),
    ('2023-07-11', 'Anthropic', 'United States', 'Claude 2', [None], 'closed'),
    ('2023-08-24', 'Naver', 'South Korea', 'HyperCLOVA X', [204.0], 'closed'),
    ('2023-10-17', 'Baidu', 'China', 'ERNIE Bot 4.0', [None], 'closed'),
    ('2023-11-06', 'OpenAI', 'United States', 'GPT-4 Turbo', [1760.0], 'closed'),
    ('2023-11-08', 'Samsung Electronics', 'South Korea', 'Samsung Gauss', [20.0], 'closed'),
    ('2023-11-16', 'Moonshot AI', 'China', 'Kimi v1', [None], 'closed'),
    ('2023-11-21', 'Anthropic', 'United States', 'Claude 2.1', [None], 'closed'),
    ('2023-11-22', 'Inflection AI', 'United States', 'Inflection-2', [None], 'closed'),
    ('2023-12-06', 'Google', 'United States', 'Gemini 1.0', [1.8, 3.25], 'closed'),
    ('2023-12-11', 'Mistral AI', 'France', 'Mistral Medium', [None], 'closed'),

    # ===== 2024 =====
    ('2024-01-16', 'Zhipu AI', 'China', 'GLM-4 (API)', [None], 'closed'),
    ('2024-01-30', 'iFlytek', 'China', 'Spark 3.5', [None], 'closed'),
    ('2024-02-08', 'Google DeepMind', 'United States', 'Gemini 1.0 Ultra', [None], 'closed'),
    ('2024-02-15', 'Google DeepMind', 'United States', 'Gemini 1.5 Pro', [None], 'closed'),
    ('2024-02-26', 'Mistral AI', 'France', 'Mistral Large (API)', [123.0], 'closed'),
    ('2024-03-04', 'Anthropic', 'United States', 'Claude 3 Opus', [None], 'closed'),
    ('2024-03-04', 'Anthropic', 'United States', 'Claude 3 Sonnet', [None], 'closed'),
    ('2024-03-13', 'Anthropic', 'United States', 'Claude 3 Haiku', [None], 'closed'),
    ('2024-03-07', 'Inflection AI', 'United States', 'Inflection 2.5', [None], 'closed'),
    ('2024-04-17', 'MiniMax', 'China', 'ABAB 6.5', [None], 'closed'),
    ('2024-04-24', 'SenseTime', 'China', 'SenseNova 5.0', [None], 'closed'),
    ('2024-05-13', 'OpenAI', 'United States', 'GPT-4o', [None], 'closed'),
    ('2024-05-14', 'Google DeepMind', 'United States', 'Gemini 1.5 Flash', [None], 'closed'),
    ('2024-06-20', 'Anthropic', 'United States', 'Claude 3.5 Sonnet', [None], 'closed'),
    ('2024-06-27', 'iFlytek', 'China', 'Spark 4.0', [None], 'closed'),
    ('2024-06-28', 'Baidu', 'China', 'ERNIE 4.0 Turbo', [None], 'closed'),
    ('2024-07-04', 'SenseTime', 'China', 'SenseNova 5.5', [600.0], 'closed'),
    ('2024-07-18', 'OpenAI', 'United States', 'GPT-4o mini', [None], 'closed'),
    ('2024-08-13', 'xAI', 'United States', 'Grok 2', [None], 'closed'),
    ('2024-09-12', 'OpenAI', 'United States', 'o1-preview', [None], 'closed'),
    ('2024-09-12', 'OpenAI', 'United States', 'o1-mini', [None], 'closed'),
    ('2024-10-22', 'Anthropic', 'United States', 'Claude 3.5 Sonnet v2', [None], 'closed'),
    ('2024-11-04', 'Anthropic', 'United States', 'Claude 3.5 Haiku', [None], 'closed'),
    ('2024-12-03', 'Amazon Web Services', 'United States', 'Nova Pro', [None], 'closed'),
    ('2024-12-03', 'Amazon Web Services', 'United States', 'Nova Lite', [None], 'closed'),
    ('2024-12-05', 'OpenAI', 'United States', 'o1', [None], 'closed'),
    ('2024-12-11', 'Google DeepMind', 'United States', 'Gemini 2.0 Flash', [None], 'closed'),
    ('2024-03-25', 'NTT Corporation', 'Japan', 'tsuzumi', [7.0, 70.0], 'closed'),

    # ===== 2025 =====
    ('2025-01-20', 'Moonshot AI', 'China', 'Kimi k1.5', [None], 'closed'),
    ('2025-01-31', 'OpenAI', 'United States', 'o3-mini', [None], 'closed'),
    ('2025-02-05', 'Google DeepMind', 'United States', 'Gemini 2.0 Pro', [None], 'closed'),
    ('2025-02-17', 'xAI', 'United States', 'Grok 3', [None], 'closed'),
    ('2025-02-24', 'Anthropic', 'United States', 'Claude 3.7 Sonnet', [None], 'closed'),
    ('2025-02-27', 'OpenAI', 'United States', 'GPT-4.5', [None], 'closed'),
    ('2025-03-16', 'Baidu', 'China', 'ERNIE 4.5', [None], 'closed'),
    ('2025-03-25', 'Google DeepMind', 'United States', 'Gemini 2.5 Pro', [None], 'closed'),
    ('2025-04-14', 'OpenAI', 'United States', 'GPT-4.1', [None], 'closed'),
    ('2025-04-14', 'OpenAI', 'United States', 'GPT-4.1 mini', [None], 'closed'),
    ('2025-04-14', 'OpenAI', 'United States', 'GPT-4.1 nano', [None], 'closed'),
    ('2025-04-16', 'OpenAI', 'United States', 'o3', [None], 'closed'),
    ('2025-04-16', 'OpenAI', 'United States', 'o4-mini', [None], 'closed'),
    ('2025-04-30', 'Amazon Web Services', 'United States', 'Nova Premier', [None], 'closed'),
    ('2025-05-05', 'xAI', 'United States', 'Grok 3.5', [None], 'closed'),
    ('2025-05-20', 'Google DeepMind', 'United States', 'Gemini 2.5 Flash', [None], 'closed'),
    ('2025-05-22', 'Anthropic', 'United States', 'Claude Sonnet 4', [None], 'closed'),
    ('2025-05-22', 'Anthropic', 'United States', 'Claude Opus 4', [None], 'closed'),
    ('2025-09-29', 'Anthropic', 'United States', 'Claude Sonnet 4.5', [None], 'closed'),

    # ===== 2026 =====
    ('2026-02-17', 'Anthropic', 'United States', 'Claude Sonnet 4.6', [None], 'closed'),
]


# ---- Flatten data ----
dates_all, sizes_all, orgs_all, countries_all, names_all, types_all = [], [], [], [], [], []

for entry in releases:
    date_str, org, country, model, sizes, mtype = entry
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    for s in sizes:
        if s is not None:  # skip unknown sizes for scatter plot
            dates_all.append(dt)
            sizes_all.append(s)
            orgs_all.append(org)
            countries_all.append(country)
            names_all.append(model)
            types_all.append(mtype)

# Also build a list counting ALL releases (including None sizes) for bar charts
dates_count, orgs_count, countries_count, types_count = [], [], [], []
for entry in releases:
    date_str, org, country, model, sizes, mtype = entry
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    # Count each release as 1 entry (not per-size)
    dates_count.append(dt)
    orgs_count.append(org)
    countries_count.append(country)
    types_count.append(mtype)

years = sorted(set(d.year for d in dates_all + dates_count))


# ---- FIGURE 1: Scatter plot with open vs closed markers ----
fig, ax = plt.subplots(figsize=(18, 10))
fig.patch.set_facecolor('white')
ax.set_facecolor('white')

# Open = filled square, Closed = hollow circle
open_mask = [t == 'open' for t in types_all]
closed_mask = [t == 'closed' for t in types_all]

open_d = [dates_all[i] for i in range(len(types_all)) if open_mask[i]]
open_s = [sizes_all[i] for i in range(len(types_all)) if open_mask[i]]
closed_d = [dates_all[i] for i in range(len(types_all)) if closed_mask[i]]
closed_s = [sizes_all[i] for i in range(len(types_all)) if closed_mask[i]]

ax.scatter(open_d, open_s, c=ATLANTIC, s=40, alpha=0.8, label='Open-Weight',
           edgecolors=BLACK, linewidths=0.3, zorder=3, marker='s')
ax.scatter(closed_d, closed_s, c=GARNET, s=40, alpha=0.8, label='Closed-Source',
           edgecolors=BLACK, linewidths=0.3, zorder=3, marker='D')

# GPU memory tier lines
gpu_tiers = [
    (7, '~7B — Consumer GPU', BLACK_50),
    (13, '~13B — Prosumer GPU (24GB)', BLACK_50),
    (70, '~70B — A100/H100 (80GB)', BLACK_50),
    (405, '~400B — Multi-GPU node', BLACK_50),
]
for size, label, color in gpu_tiers:
    ax.axhline(y=size, color=color, linestyle='--', linewidth=0.8, alpha=0.5, zorder=1)
    ax.text(datetime(2019, 1, 1), size * 1.15, label, fontsize=7.5,
            color=BLACK_70, va='bottom', ha='left')

ax.set_yscale('log')
ax.set_ylabel('Parameters (Billions)', fontsize=12, color=BLACK)
ax.set_xlabel('Release Date', fontsize=12, color=BLACK)
ax.set_title('LLM Releases: Open-Weight vs Closed-Source (2019–2026)', fontsize=14,
             fontweight='bold', color=BLACK, pad=15)

ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
ax.xaxis.set_minor_locator(mdates.MonthLocator(bymonth=[4, 7, 10]))

yticks = [0.1, 0.5, 1, 3, 7, 13, 30, 70, 120, 235, 405, 671, 1000, 1760]
ax.set_yticks(yticks)
ax.set_yticklabels([f'{y/1000:.1f}T' if y >= 1000 else (f'{y}B' if y >= 1 else f'{int(y*1000)}M') for y in yticks])
ax.set_ylim(0.05, 2500)

ax.tick_params(colors=BLACK_90)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_color(BLACK_90)
ax.spines['bottom'].set_color(BLACK_90)

ax.legend(loc='upper left', fontsize=10, framealpha=0.9, edgecolor=BLACK_50)
ax.grid(True, which='major', axis='y', alpha=0.15, color=BLACK_50)

plt.tight_layout()
plt.savefig('/Users/user/Downloads/graduate-coursework/Sp26/CSCE775/Project/Proposal_llm_5/model_sizes_timeline.png',
            dpi=200, bbox_inches='tight', facecolor='white')
plt.close()


# ---- FIGURE 2: Releases per year, open vs closed ----
fig2, ax2 = plt.subplots(figsize=(14, 7))
fig2.patch.set_facecolor('white')
ax2.set_facecolor('white')

year_open = {y: 0 for y in years}
year_closed = {y: 0 for y in years}
for i in range(len(dates_count)):
    y = dates_count[i].year
    if types_count[i] == 'open':
        year_open[y] += 1
    else:
        year_closed[y] += 1

x = np.arange(len(years))
width = 0.65
open_counts = [year_open[y] for y in years]
closed_counts = [year_closed[y] for y in years]

ax2.bar(x, open_counts, width, label='Open-Weight', color=ATLANTIC, edgecolor='white', linewidth=0.5)
ax2.bar(x, closed_counts, width, bottom=open_counts, label='Closed-Source', color=GARNET, edgecolor='white', linewidth=0.5)

# Total labels
for i, y in enumerate(years):
    total = open_counts[i] + closed_counts[i]
    ax2.text(i, total + 0.5, str(total), ha='center', va='bottom',
             fontsize=10, fontweight='bold', color=BLACK_90)

ax2.set_xticks(x)
ax2.set_xticklabels(years, fontsize=10)
ax2.set_ylabel('Number of Model Releases', fontsize=12, color=BLACK)
ax2.set_xlabel('Year', fontsize=12, color=BLACK)
ax2.set_title('LLM Releases Per Year: Open-Weight vs Closed-Source', fontsize=14,
              fontweight='bold', color=BLACK, pad=15)

ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.spines['left'].set_color(BLACK_90)
ax2.spines['bottom'].set_color(BLACK_90)
ax2.tick_params(colors=BLACK_90)
ax2.legend(loc='upper left', fontsize=10, framealpha=0.9, edgecolor=BLACK_50)

plt.tight_layout()
plt.savefig('/Users/user/Downloads/graduate-coursework/Sp26/CSCE775/Project/Proposal_llm_5/model_sizes_by_tier.png',
            dpi=200, bbox_inches='tight', facecolor='white')
plt.close()


# ---- FIGURE 3: By country, open vs closed side by side ----
fig3, (ax3a, ax3b) = plt.subplots(1, 2, figsize=(18, 7), sharey=True)
fig3.patch.set_facecolor('white')

country_groups = {
    'United States': ATLANTIC,
    'China': GARNET,
    'France': ROSE,
    'Canada': HONEYCOMB,
    'United Arab Emirates': CONGAREE,
    'Israel': '#8B4513',
    'South Korea': '#4B0082',
    'Japan': '#2E8B57',
    'Other': WARM_GREY,
}

def get_country_group(c):
    return c if c in country_groups else 'Other'

for ax_sub, mtype, title_suffix in [(ax3a, 'open', 'Open-Weight'), (ax3b, 'closed', 'Closed-Source')]:
    ax_sub.set_facecolor('white')
    year_cc = {y: {c: 0 for c in country_groups} for y in years}
    for i in range(len(dates_count)):
        if types_count[i] == mtype:
            yr = dates_count[i].year
            cg = get_country_group(countries_count[i])
            year_cc[yr][cg] += 1

    bottoms = np.zeros(len(years))
    for country, color in country_groups.items():
        counts = [year_cc[y][country] for y in years]
        ax_sub.bar(x, counts, width, bottom=bottoms, label=country, color=color,
                   edgecolor='white', linewidth=0.5)
        bottoms += np.array(counts)

    ax_sub.set_xticks(x)
    ax_sub.set_xticklabels(years, fontsize=9)
    ax_sub.set_title(title_suffix, fontsize=13, fontweight='bold', color=BLACK)
    ax_sub.spines['top'].set_visible(False)
    ax_sub.spines['right'].set_visible(False)
    ax_sub.spines['left'].set_color(BLACK_90)
    ax_sub.spines['bottom'].set_color(BLACK_90)
    ax_sub.tick_params(colors=BLACK_90)

ax3a.set_ylabel('Number of Model Releases', fontsize=12, color=BLACK)
ax3b.legend(loc='upper left', fontsize=8, framealpha=0.9, edgecolor=BLACK_50)
fig3.suptitle('LLM Releases by Country: Open-Weight vs Closed-Source', fontsize=14,
              fontweight='bold', color=BLACK, y=1.02)

plt.tight_layout()
plt.savefig('/Users/user/Downloads/graduate-coursework/Sp26/CSCE775/Project/Proposal_llm_5/model_sizes_by_country.png',
            dpi=200, bbox_inches='tight', facecolor='white')
plt.close()


# ---- FIGURE 4: Unique companies per year, open vs closed ----
fig4, ax4 = plt.subplots(figsize=(14, 7))
fig4.patch.set_facecolor('white')
ax4.set_facecolor('white')

def normalize_org(org):
    if 'DeepSeek' in org: return 'DeepSeek'
    if 'Qwen' in org or 'Alibaba' in org: return 'Alibaba / Qwen'
    if 'Meta' in org: return 'Meta'
    if 'Google' in org: return 'Google'
    if 'Hugging Face' in org or 'BigCode' in org or 'BigScience' in org: return 'Hugging Face'
    if 'Technology Innovation Institute' in org: return 'TII (UAE)'
    if 'Allen Institute' in org or 'Ai2' in org: return 'Allen AI'
    if 'Zhipu' in org or 'Z.ai' in org: return 'Zhipu AI'
    if 'Baichuan' in org: return 'Baichuan'
    if 'Shanghai AI' in org: return 'Shanghai AI Lab'
    if 'Amazon' in org: return 'Amazon'
    return org

year_open_orgs = {y: set() for y in years}
year_closed_orgs = {y: set() for y in years}
for entry in releases:
    date_str, org, country, model, sizes, mtype = entry
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    normed = normalize_org(org)
    if mtype == 'open':
        year_open_orgs[dt.year].add(normed)
    else:
        year_closed_orgs[dt.year].add(normed)

open_org_counts = [len(year_open_orgs[y]) for y in years]
closed_only_counts = [len(year_closed_orgs[y] - year_open_orgs[y]) for y in years]
both_counts = [len(year_closed_orgs[y] & year_open_orgs[y]) for y in years]

ax4.bar(x, open_org_counts, width, label='Open-Weight Only', color=ATLANTIC,
        edgecolor='white', linewidth=0.5)
ax4.bar(x, both_counts, width, bottom=open_org_counts, label='Both Open + Closed',
        color=HONEYCOMB, edgecolor='white', linewidth=0.5)
ax4.bar(x, closed_only_counts, width,
        bottom=[o + b for o, b in zip(open_org_counts, both_counts)],
        label='Closed-Source Only', color=GARNET, edgecolor='white', linewidth=0.5)

for i, y in enumerate(years):
    total = open_org_counts[i] + closed_only_counts[i] + both_counts[i]
    ax4.text(i, total + 0.3, str(total), ha='center', va='bottom',
             fontsize=10, fontweight='bold', color=BLACK_90)

ax4.set_xticks(x)
ax4.set_xticklabels(years, fontsize=10)
ax4.set_ylabel('Number of Unique Organizations', fontsize=12, color=BLACK)
ax4.set_xlabel('Year', fontsize=12, color=BLACK)
ax4.set_title('Unique Organizations Releasing LLMs Per Year', fontsize=14,
              fontweight='bold', color=BLACK, pad=15)

ax4.spines['top'].set_visible(False)
ax4.spines['right'].set_visible(False)
ax4.spines['left'].set_color(BLACK_90)
ax4.spines['bottom'].set_color(BLACK_90)
ax4.tick_params(colors=BLACK_90)
ax4.legend(loc='upper left', fontsize=9, framealpha=0.9, edgecolor=BLACK_50)

plt.tight_layout()
plt.savefig('/Users/user/Downloads/graduate-coursework/Sp26/CSCE775/Project/Proposal_llm_5/model_sizes_companies.png',
            dpi=200, bbox_inches='tight', facecolor='white')
plt.close()


# Print stats
open_r = sum(1 for e in releases if e[5] == 'open')
closed_r = sum(1 for e in releases if e[5] == 'closed')
print(f"Total releases: {len(releases)} ({open_r} open, {closed_r} closed)")
print(f"Total plottable model variants (known size): {len(dates_all)}")
print(f"Saved: model_sizes_timeline.png")
print(f"Saved: model_sizes_by_tier.png (open vs closed per year)")
print(f"Saved: model_sizes_by_country.png (side-by-side)")
print(f"Saved: model_sizes_companies.png (orgs per year)")
