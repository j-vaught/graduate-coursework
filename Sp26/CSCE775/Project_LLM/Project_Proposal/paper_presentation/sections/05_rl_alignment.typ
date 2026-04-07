// Section 05: Reinforcement Learning for Large Language Model Alignment

#set page(margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)
#set par(leading: 0.65em, justify: true)

= 5. Reinforcement Learning for Large Language Model Alignment

The application of reinforcement learning to the alignment of large language models represents one of the most consequential transfers of RL methodology from its traditional game-playing and robotics domains into natural language processing. The central problem is straightforward in motivation but formidable in execution. A pretrained language model possesses broad knowledge and fluent generation capabilities, yet it has no intrinsic mechanism for distinguishing helpful, truthful, and safe outputs from harmful or misleading ones. Reinforcement learning provides the optimization machinery to steer model behavior toward human-preferred outputs, and the story of how this machinery has evolved over the past decade is one of progressive simplification, from heavyweight actor-critic pipelines to elegant closed-form solutions.

== 5.1 Origins of RLHF

The intellectual foundation for reinforcement learning from human feedback was laid by Christiano et al. [Christiano2017], who demonstrated that complex RL tasks in Atari and simulated robotics could be solved using human preference comparisons rather than hand-specified reward functions. Their method maintained two learned components: a policy trained via standard RL and a reward model trained on human comparisons between trajectory segment pairs. Critically, the approach required feedback on less than one percent of the agent's environment interactions, establishing the practical feasibility of human-in-the-loop reward learning. Stiennon et al. [Stiennon2020] extended this paradigm to natural language, showing that a reward model trained on human comparisons between summaries could guide policy optimization to produce outputs that human evaluators preferred over both supervised baselines and human-written reference summaries.

== 5.2 InstructGPT and the Three-Stage Pipeline

The landmark contribution of Ouyang et al. [Ouyang2022] was to scale RLHF to large language models, producing InstructGPT. Their three-stage pipeline became the template for an entire generation of aligned models. In the first stage, a pretrained GPT-3 model is fine-tuned via supervised learning on high-quality human demonstrations of instruction-following, yielding a supervised fine-tuned (SFT) model. In the second stage, human labelers rank multiple model outputs for a given prompt, and these ranked comparisons train a reward model that learns to predict human preferences. In the third stage, Proximal Policy Optimization (PPO) optimizes the SFT model against the learned reward signal, with a KL-divergence penalty to prevent the policy from deviating too far from the SFT baseline. The results were striking. A 1.3 billion parameter InstructGPT model was preferred by human evaluators over the 175 billion parameter GPT-3, demonstrating that alignment training could be far more efficient than simply scaling model size.

== 5.3 Direct Preference Optimization and Its Variants

Despite the success of the PPO-based pipeline, its complexity motivated the search for simpler alternatives. Rafailov et al. [Rafailov2023] introduced Direct Preference Optimization (DPO), which eliminated the reward model entirely through an elegant reparameterization. The key insight was that the optimal policy under the RLHF objective can be expressed in closed form as a function of the reward, and conversely, the reward can be expressed in terms of the optimal policy and a reference policy. By substituting this reparameterized reward into the Bradley-Terry preference model, the intractable partition function cancels, yielding a simple binary cross-entropy loss defined directly over preference pairs. DPO thus collapses the three-stage RLHF pipeline into a single-stage classification problem, matching or exceeding PPO-based RLHF on tasks ranging from sentiment control to summarization and dialogue.

The simplicity of the DPO framework catalyzed a rapid proliferation of variants. Azar et al. [Azar2024] proposed Identity Preference Optimization (IPO), which replaces the logistic loss with a squared loss and incorporates a margin term, addressing the observation that DPO's implicit reward gap between chosen and rejected responses can grow unboundedly during training, driving the policy toward extreme probability assignments. Ethayarajh et al. [Ethayarajh2024] introduced Kahneman-Tversky Optimization (KTO), inspired by prospect theory, which maximizes the utility of generations directly and requires only binary accept/reject labels rather than paired comparisons, dramatically simplifying data collection. Meng et al. [Meng2024] proposed SimPO, a reference-model-free approach that adopts length-normalized likelihoods and a constant margin to separate preferred from dispreferred responses, further reducing computational overhead. Each variant addresses a specific limitation of the original DPO formulation, whether in training stability, data requirements, or computational cost, while preserving the core advantage of avoiding explicit reward model training.

== 5.4 Constitutional AI and AI Feedback

An alternative approach to reducing reliance on human labelers was proposed by Bai et al. [Bai2022] through Constitutional AI. Rather than collecting human preference labels for harmlessness training, the method uses a set of written principles, a "constitution," to guide an AI system in critiquing and revising its own outputs. In the supervised phase, the model generates responses, self-critiques them against constitutional principles, and produces revised outputs on which the model is then fine-tuned. In the RL phase, the model evaluates pairs of its own outputs to generate preference labels, and a reward model is trained on these AI-generated comparisons. This approach, termed Reinforcement Learning from AI Feedback (RLAIF), demonstrated that harmless behavior could be induced with minimal human oversight while avoiding the evasiveness that often accompanies safety-focused training.

== 5.5 GRPO and the Elimination of the Critic

Group Relative Policy Optimization (GRPO), introduced by Shao et al. [Shao2024] in the DeepSeek-Math work, represents a different axis of simplification targeting the RL training itself rather than the preference modeling. Standard PPO requires a critic (value) network to estimate the advantage function, which roughly doubles the memory and compute requirements of training. GRPO eliminates the critic entirely by sampling a group of multiple outputs for each prompt and using the group-level statistics, specifically the mean and standard deviation of reward scores within each group, to compute relative advantages. This group-relative normalization provides a stable baseline without learning a separate value function, achieving substantial improvements on mathematical reasoning benchmarks while dramatically reducing resource requirements.

== 5.6 DeepSeek-R1 and Emergent Reasoning from Pure RL

The most dramatic demonstration of RL-driven alignment came with DeepSeek-R1 [DeepSeekAI2025], released in January 2025. The DeepSeek-R1-Zero experiment applied GRPO directly to a base language model without any supervised fine-tuning, using only rule-based rewards for answer correctness and output formatting. The results were remarkable. On the AIME 2024 mathematics benchmark, pass@1 accuracy rose from 15.6% to 71.0% over the course of training, with majority voting pushing performance to 86.7%. More striking than the quantitative gains were the emergent behaviors: the model spontaneously developed self-verification, reflection, and extended chains of thought. The researchers documented what they termed an "aha moment," in which the model learned to pause, reconsider its reasoning, and correct errors using an almost anthropomorphic tone of self-discovery. While the pure RL approach suffered from readability issues and language mixing, these findings demonstrated that sophisticated reasoning strategies could emerge from RL optimization alone, without being explicitly taught through supervised demonstrations. The full DeepSeek-R1 pipeline incorporated cold-start SFT data to mitigate these issues while preserving the emergent capabilities.

== 5.7 RLVR and Reward Model Overoptimization

The success of DeepSeek-R1 has intensified interest in Reinforcement Learning with Verifiable Rewards (RLVR), a term coined by Lambert et al. [Lambert2024] in the Tulu 3 work. RLVR sidesteps the learned reward model entirely for domains where correctness can be checked programmatically, such as mathematics and code generation, using deterministic verifiers as the reward signal. The Tulu 3 pipeline combined SFT, DPO, and RLVR to produce models that surpassed the instruction-tuned versions of Llama 3.1, Qwen 2.5, and even closed models such as GPT-4o-mini on certain benchmarks.

The motivation for verifiable rewards is sharpened by the problem of reward model overoptimization, characterized formally by Gao et al. [Gao2023]. Their work established scaling laws for the phenomenon in which optimizing too aggressively against a learned proxy reward model leads to degraded performance on the true objective, a manifestation of Goodhart's law. They showed that the relationship between proxy reward optimization and ground truth performance follows predictable functional forms whose coefficients scale smoothly with reward model size, providing practitioners with quantitative guidance on when to stop optimization. This fundamental tension between reward model fidelity and optimization pressure remains one of the central challenges in RLHF-based alignment, and the shift toward verifiable rewards for suitable domains represents a partial but principled resolution.

#pagebreak()

== References

+ #text(size: 10pt)[[Christiano2017] P. Christiano, J. Leike, T. Brown, M. Martic, S. Legg, and D. Amodei. "Deep Reinforcement Learning from Human Preferences." _NeurIPS_, 2017.]

+ #text(size: 10pt)[[Stiennon2020] N. Stiennon, L. Ouyang, J. Wu, D. Ziegler, R. Lowe, C. Voss, A. Radford, D. Amodei, and P. Christiano. "Learning to Summarize from Human Feedback." _NeurIPS_, 2020.]

+ #text(size: 10pt)[[Ouyang2022] L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. Wainwright, P. Mishkin, C. Zhang, S. Agarwal, K. Slama, A. Ray, et al. "Training Language Models to Follow Instructions with Human Feedback." _NeurIPS_, 2022.]

+ #text(size: 10pt)[[Bai2022] Y. Bai, S. Kadavath, S. Kundu, A. Askell, J. Kernion, A. Jones, A. Chen, A. Goldie, A. Mirhoseini, C. McKinnon, et al. "Constitutional AI: Harmlessness from AI Feedback." _arXiv preprint arXiv:2212.08073_, 2022.]

+ #text(size: 10pt)[[Rafailov2023] R. Rafailov, A. Sharma, E. Mitchell, S. Ermon, C. Manning, and C. Finn. "Direct Preference Optimization: Your Language Model is Secretly a Reward Model." _NeurIPS_, 2023.]

+ #text(size: 10pt)[[Gao2023] L. Gao, J. Schulman, and J. Hilton. "Scaling Laws for Reward Model Overoptimization." _ICML_, 2023.]

+ #text(size: 10pt)[[Azar2024] M. Azar, M. Rowland, B. Piot, D. Guo, D. Calandriello, M. Valko, and R. Munos. "A General Theoretical Paradigm to Understand Learning from Human Feedback." _AISTATS_, 2024.]

+ #text(size: 10pt)[[Ethayarajh2024] K. Ethayarajh, W. Xu, N. Muennighoff, D. Jurafsky, and D. Kiela. "KTO: Model Alignment as Prospect Theoretic Optimization." _ICML_, 2024.]

+ #text(size: 10pt)[[Meng2024] Y. Meng, M. Xia, and D. Chen. "SimPO: Simple Preference Optimization with a Reference-Free Reward." _NeurIPS_, 2024.]

+ #text(size: 10pt)[[Shao2024] Z. Shao, P. Wang, Q. Zhu, R. Xu, J. Song, M. Zhang, Y. Li, Y. Wu, and D. Guo. "DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models." _arXiv preprint arXiv:2402.03300_, 2024.]

+ #text(size: 10pt)[[Lambert2024] N. Lambert, J. Morrison, M. Pyatkin, S. Huang, H. Ivison, F. Brahman, L. Miranda, A. Liu, N. Dziri, S. Lyu, et al. "Tulu 3: Pushing Frontiers in Open Language Model Post-Training." _arXiv preprint arXiv:2411.15124_, 2024.]

+ #text(size: 10pt)[[DeepSeekAI2025] DeepSeek-AI. "DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning." _arXiv preprint arXiv:2501.12948_, 2025.]
