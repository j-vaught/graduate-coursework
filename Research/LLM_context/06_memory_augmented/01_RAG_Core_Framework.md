# RAG: Retrieval-Augmented Generation - Core Framework

## Foundational Paper: Lewis et al. 2020

**Title:** Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks

**Authors:** Patrick Lewis, Ethan Perez, Aleksandara Pertodva, Fabio Petroni, Vladimir Karpukhin, Naman Goyal, Heinrich Küttler, Mike Lewis, Wen-tau Yih, Tim Rocktäschel, Sebastian Riedel, Douwe Kiela

**Year:** 2020

**Venue:** NeurIPS 2020

**arXiv ID:** 2005.11401

**URL:** https://arxiv.org/abs/2005.11401

**Conference Link:** https://proceedings.neurips.cc/paper/2020/file/6b493230205f780e1bc26945df7481e5-Paper.pdf

---

## Key Contributions

### Problem Statement
Language models suffer from knowledge limitations and generate outdated or factually incorrect information. Traditional approach relies purely on parametric memory encoded in model weights.

### Core Innovation
RAG combines:
- **Parametric memory**: Pre-trained seq2seq transformer (T5) that captures general linguistic knowledge
- **Non-parametric memory**: Dense vector index of Wikipedia documents retrieved via dense retriever

### Architecture Overview
1. **Retriever**: Pre-trained DPR (Dense Passage Retriever) to encode queries and retrieve relevant passages
2. **Generator**: Seq2seq model (T5) that generates outputs conditioned on retrieved documents
3. **Two formulations**:
   - RAG-Sequence: Same retrieved passages used for entire sequence generation
   - RAG-Token: Different passages can be used per token generation

### Training and Inference
- Fine-tuned end-to-end on knowledge-intensive tasks
- Uses maximum likelihood training with retrieved passage marginalization
- Can be applied to any generation task requiring external knowledge

---

## Performance Results

### Benchmark Performance
- **Open-domain QA**: State-of-the-art on Natural Questions, TriviaQA, WebQuestions
- **Fact verification**: Improved factuality and specificity compared to baseline
- **Text generation**: More diverse, specific, and factual language than parametric-only baselines

### Key Metrics
- Outperforms strong retrieval-only and generation-only baselines
- Reduces hallucination through grounding in retrieved documents
- Achieves better generalization to unseen domains

---

## Research Impact

### Why It Matters
- Pioneered combining retrieval with generation for all downstream tasks, not just QA
- Established RAG as foundational paradigm for knowledge-intensive NLP
- Influenced entire ecosystem of RAG variants and improvements

### Subsequent Work Built Upon
- Dense passage retrieval methods (DPR, ColBERT)
- Advanced RAG approaches (Self-RAG, CRAG, GraphRAG)
- Memory-augmented architectures (MemGPT, RETRO)

### Citation Count
One of most cited papers in modern NLP (10,000+ citations)

---

## Technical Details

### Retriever Component
- Uses BERT-based dual-encoder (Contriever or DPR)
- Retrieves top-k passages (typically k=2-10)
- Encoding space shared between query and passages

### Generator Component
- BART or T5-based seq2seq model
- Conditional generation: P(output | input, retrieved_passages)
- Marginalizes over retrieved documents during training

### Joint Training
- Differentiable: Gradient flows through retriever
- Corpus retrieval: Wikipedia with 100M passages
- Fine-tuning on task-specific labeled data

---

## Limitations and Open Questions

1. **Computational cost**: Joint optimization expensive; often retriever frozen in practice
2. **Passage selection**: Fixed retrieval strategy; no dynamic/adaptive retrieval
3. **Context window**: Limited to concatenating k documents; doesn't scale to large collections
4. **Multi-hop reasoning**: Single-shot retrieval insufficient for complex multi-step reasoning

---

## File Metadata
- **Research Area**: Retrieval-Augmented Generation, Knowledge-Intensive NLP, Dense Retrieval
- **Method Type**: Hybrid (Retrieval + Generation)
- **Code Available**: Official implementation at Facebook Research GitHub
- **Reproducibility**: Benchmarks (NQ, TriviaQA) publicly available; model checkpoints released
