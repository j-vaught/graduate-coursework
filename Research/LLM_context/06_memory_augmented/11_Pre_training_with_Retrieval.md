# Pre-training with Retrieval: REALM and FiD

## Paper 1: REALM (Guu et al. 2020)

**Title:** REALM: Retrieval-Augmented Language Model Pre-Training

**Authors:** Kelvin Guu, Kenton Lee, Zora Tung, Panupong Pasupat, Ming-Wei Chang

**Year:** 2020

**Venue:** ICML 2020

**arXiv ID:** 2002.08909

**arXiv URL:** https://arxiv.org/abs/2002.08909

**Conference Link:** http://proceedings.mlr.press/v119/guu20a/guu20a.pdf

**Official Blog:** https://research.google/blog/realm-integrating-retrieval-into-language-representation-models/

---

## Paper 2: Fusion-in-Decoder (FiD) (Izacard & Grave 2020)

**Title:** Leveraging Passage Retrieval with Generative Models for Open Domain Question Answering

**Authors:** Gautier Izacard, Édouard Grave

**Year:** 2020

**Venue:** EMNLP 2020

**GitHub:** https://github.com/facebookresearch/FiD

**ParlAI Documentation:** https://parl.ai/docs/agent_refs/fid.html

---

## REALM: Retrieval-Augmented Pre-training

### Problem Statement
Language model pre-training stores knowledge implicitly in model parameters. As knowledge evolves:
- Models become outdated without retraining
- Parameter count must grow to store more facts
- Knowledge not interpretable or verifiable
- No efficient way to update specific facts

### Core Innovation: Latent Knowledge Retriever

#### Key Components
1. **Knowledge Retriever**: Learns to retrieve relevant documents
2. **Knowledge Encoder**: Encodes retrieved documents
3. **Language Representation Model**: ELECTRA or RoBERTa-based
4. **Joint Pre-training**: Train retriever and representation jointly

#### Architecture Overview
```
Input Text + Masked Tokens
  ↓
Encode Query (masked position) → Query embedding
  ↓
Retrieve: Find top-k documents using Dense retriever
  ↓
Encode Documents: Get document embeddings
  ↓
Feed Supporting Document + Original Text
  ↓
Language Model: Predict masked tokens
  ↓
Loss: MLM loss + Retriever training (unsupervised signal)
```

### Key Innovation: Unsupervised Retriever Training

#### Pre-training Signal
- **Input**: Masked language modeling objective
- **Supervision**: Only masked token predictions
- **Retriever Training**: Backprop through retriever to improve selection

#### Mechanism
```
For each masked token position:
1. Encode query (surrounding context) → query_vec
2. Retrieve top-k documents from corpus
3. Best document = document containing answer token
4. Use MLM loss to improve retriever selection
5. Retriever learns to select documents containing answers
```

### Technical Details

#### Retriever Architecture
- **Query Encoder**: BERT-based, encodes surrounding context
- **Document Encoder**: Same BERT, encodes document passages
- **Similarity**: Inner product in embedding space
- **Index**: FAISS index for efficient retrieval

#### Pre-training Procedure
1. **Corpus**: Wikipedia (13.3M documents)
2. **Training**: Masked language modeling
3. **Retrieval Database**: Static during training (updated periodically)
4. **Negative Sampling**: Use random documents as negatives

#### Model Sizes
- **Query Encoder**: 110M parameters
- **Document Encoder**: 110M parameters (shared)
- **Full Model**: ~300M parameters (efficient for 2020)

### Performance Results

### REALM Results

#### Pre-training Benchmarks
- **Perplexity**: Competitive with baseline on unlabeled data
- **Downstream Tasks**: Better transfer to downstream tasks

#### Open-Domain QA
- **Natural Questions**: 4-16% absolute improvement over previous SOTA
- **WebQuestions**: Strong performance improvement
- **TriviaQA**: Significant gains

#### Efficiency
- **Parameter Count**: 300M (competitive with 11B T5)
- **Performance vs. Size**: Outperforms much larger models
- **Knowledge Efficiency**: Demonstrates modularity of knowledge

### Key Findings

1. **Unsupervised Retriever Learning**: Can train retriever on MLM signal alone
2. **Modular Knowledge**: Separating parametric and non-parametric memory effective
3. **Interpretability**: Retrieved documents explain predictions
4. **Factual Accuracy**: Better factual accuracy than parametric baselines
5. **Updatable Knowledge**: Can update facts without retraining

---

## FiD: Fusion-in-Decoder

### Problem Statement
Standard approaches to open-domain QA:
- **Retriever-only**: Poor accuracy (limited context)
- **Reader + Retriever**: Reader must score each passage separately
- **Dense Fusion**: Early interaction limits scalability

Need efficient passage aggregation that scales to 100+ passages.

### Core Innovation: Encode Independently, Fuse in Decoder

#### Architecture Overview
```
For each retrieved passage:
  Document[i] + Query → T5 Encoder → Encoded[i]

All Encoded passages → Decoder (attends to all)
  ↓
Generates Answer

Key: Each passage encoded independently, fused in decoder
```

#### Why Fusion-in-Decoder?
- **Independence**: Each passage encoded separately (embarrassingly parallel)
- **Fusion**: Decoder attends to all passage representations
- **Scalability**: Can efficiently use 100+ passages
- **Quality**: Decoder can synthesize across passages

### Technical Details

#### Encoder
```
Input: [Query] [passage text]
Output: Contextualized representation per passage
Note: Query repeated per passage for each encoding
```

#### Decoder
```
Input: Concatenate encoded passages + decoder embeddings
Attention: Decoder attends over all passages simultaneously
Output: Generates answer token-by-token

Cross-attention: Decoder queries can attend to:
- All passages simultaneously
- Learn to attend to relevant evidence
- Can aggregate multiple passages
```

### Performance Results

#### Open-Domain QA Benchmarks
- **Natural Questions**: New state-of-the-art
- **TriviaQA**: Strong performance, scales well
- **WebQuestions**: Competitive results

#### Scaling Properties
- **Number of Passages**: Scales effectively from 1 to 100 passages
- **Passage Relevance**: Handles both relevant and irrelevant passages
- **Efficiency**: Outperforms slower cross-encoder approaches

#### Efficiency vs Accuracy
| Config | Speed | Accuracy |
|--------|-------|----------|
| Top-1 passage | Very Fast | Low |
| Top-10 passages | Fast | Good |
| Top-100 passages | Moderate | Excellent |
| Cross-encoder (top-10) | Slow | Excellent |

### Why FiD Succeeds

1. **Efficient Attention**: Parallel encoding, sequential fusion
2. **Multi-Passage Reasoning**: Decoder naturally combines evidence
3. **Flexible**: Works with any retriever
4. **Simple**: Clean, implementable architecture

---

## Comparative Analysis: REALM vs FiD

| Aspect | REALM | FiD |
|--------|-------|-----|
| **Scope** | Pre-training + Fine-tuning | Fine-tuning only |
| **Knowledge Storage** | Learned + Indexed | Indexed only |
| **Task** | General NLP | Open-domain QA |
| **Retriever Training** | Joint unsupervised | Fixed |
| **Efficiency** | Parameter-efficient | Passage-efficient |
| **Explainability** | High (retrieved docs) | Medium |

---

## Key Innovations Compared to Earlier Work

### vs. Traditional QA Systems
- **Retrievers**: Hand-crafted vs. learned embeddings
- **Readers**: Discrete span prediction vs. generative
- **Knowledge**: Static vs. retrievable

### vs. Parametric Models
- **Size**: Smaller (modular) vs. larger (all-in-weights)
- **Updateability**: Updatable (documents) vs. fixed (weights)
- **Interpretability**: Explainable (retrieved docs) vs. black-box

---

## Follow-up Work and Impact

### REALM Extensions
- **REALM+**: Improved context, better retriever
- **Domain-Specific REALM**: Specialized pre-training
- **Multilingual REALM**: Cross-lingual retrieval

### FiD Extensions
- **FiD-ICL**: In-context learning variant
- **FiDO**: Optimized FiD architecture
- **KG-FiD**: Knowledge graph enhanced FiD

### Influenced Subsequent Work
- **RAG**: Generalization of both ideas
- **RETRO**: Similar retrieval-in-pretraining idea
- **Self-RAG**: Combines ideas with self-critique

---

## Practical Implementation Considerations

### REALM Implementation
```
1. Pre-compute document embeddings
2. Build FAISS index
3. During pre-training:
   - Sample masked positions
   - Retrieve top documents for prediction
   - Compute MLM loss + ranking loss
   - Backprop through retriever
4. Fine-tune on downstream tasks
```

### FiD Implementation
```
1. Retrieve top-k passages
2. Tokenize: [CLS] query [SEP] passage [SEP] ... [CLS] query [SEP] passage
3. Encode each passage (can parallelize)
4. Concatenate encoded passages
5. Decoder generates answer attending over all
```

---

## Lessons from These Papers

### From REALM
1. **Unsupervised Signals**: Can train retriever without explicit supervision
2. **Modularity**: Separating knowledge storage from computation effective
3. **Efficiency**: Smaller models can match larger parametric models
4. **Updatability**: External knowledge more maintainable

### From FiD
1. **Fusion Strategy**: Late fusion in decoder very effective
2. **Passage Scaling**: Can effectively use 100+ passages
3. **Architecture Matters**: How you combine info important as much as what info
4. **Simplicity**: Simple, clean architectures often best

---

## File Metadata
- **Research Area**: Retrieval-Augmented Pre-training, Open-Domain QA
- **Method Types**: Unsupervised Retriever Learning, Multi-Passage Fusion
- **Publication Tier**: Top-tier (ICML, EMNLP)
- **Citation Count**: Highly cited (REALM: 1000+, FiD: 500+)
- **Code Availability**: Official implementations released
- **Reproducibility**: Good experimental details provided

## Cross-References
- Foundation for: RAG (Lewis et al. 2020), RETRO (Borgeaud et al. 2022)
- Related to: DPR (Karpukhin et al. 2020)
- Extended by: Self-RAG, CRAG, and subsequent RAG variants
