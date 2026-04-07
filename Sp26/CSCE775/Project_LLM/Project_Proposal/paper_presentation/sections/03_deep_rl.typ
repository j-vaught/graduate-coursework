// Section 03: Deep Reinforcement Learning: The Revolution

#set page(margin: 1in)
#set text(font: "New Computer Modern", size: 11pt)
#set par(leading: 0.65em, justify: true)

= Deep Reinforcement Learning: The Revolution

The synthesis of deep neural networks with reinforcement learning transformed the field from a collection of elegant but limited tabular algorithms into a general-purpose framework capable of mastering complex, high-dimensional tasks. This section traces that transformation, beginning with the classical foundations of temporal-difference learning and Q-learning, proceeding through the deep Q-network breakthrough, and arriving at the modern actor-critic algorithms that now serve as standard baselines for continuous control.

== Classical Foundations

The intellectual roots of deep reinforcement learning lie in the temporal-difference (TD) methods formalized by Sutton [Sutton1988]. TD learning introduced the idea of updating value estimates based on the difference between temporally successive predictions rather than waiting for a final outcome, enabling incremental, online learning in environments where outcomes are delayed. This principle proved foundational to nearly every algorithm that followed. Building on TD methods, Watkins [Watkins1989] proposed Q-learning, an off-policy algorithm that learns the optimal action-value function $Q^*(s, a)$ directly, without requiring a model of the environment's dynamics. Watkins and Dayan [WatkinsDayan1992] subsequently proved that Q-learning converges to $Q^*$ with probability one, provided all state-action pairs are visited infinitely often and the learning rates satisfy the Robbins-Monro conditions. These convergence guarantees, however, applied only to the tabular setting. The comprehensive treatment by Sutton and Barto [SuttonBarto2018] remains the standard reference for these foundations, presenting TD learning, Monte Carlo methods, and dynamic programming as a unified framework for sequential decision-making under uncertainty.

The policy gradient theorem, established by Sutton, McAllester, Singh, and Mansour [Sutton2000], opened a parallel line of research by demonstrating that the gradient of expected cumulative reward with respect to policy parameters can be expressed in a form amenable to estimation from sampled trajectories. Specifically, the theorem shows that $nabla_theta J(theta) = bb(E)_(pi_theta) [nabla_theta log pi_theta (a | s) Q^(pi_theta)(s, a)]$, where $pi_theta$ is a parameterized stochastic policy and $Q^(pi_theta)$ is the corresponding action-value function. This result provided the theoretical foundation for REINFORCE, actor-critic methods, and the entire family of policy optimization algorithms that would later prove essential for continuous action spaces.

== The DQN Breakthrough

The deep Q-network (DQN), introduced by Mnih et al. [Mnih2013] and refined in their landmark Nature paper [Mnih2015], demonstrated for the first time that a single reinforcement learning agent could learn to play a diverse collection of Atari 2600 games directly from raw pixel inputs. The key architectural insight was to represent the action-value function $Q(s, a; theta)$ with a convolutional neural network, taking stacked frames as input and outputting Q-values for each discrete action. Two algorithmic innovations proved essential for stable training. First, experience replay, originally proposed by Lin [Lin1992], stores transitions $(s_t, a_t, r_t, s_(t+1))$ in a fixed-size buffer and samples mini-batches uniformly at random, breaking the temporal correlations that destabilize stochastic gradient descent on sequentially collected data. Second, a separate target network with parameters $theta^-$, updated periodically from the online network, provides stable regression targets $r + gamma max_(a') Q(s', a'; theta^-)$ and prevents the feedback loop in which the network chases its own shifting predictions. Evaluated on the Arcade Learning Environment [Bellemare2013], DQN achieved human-level performance on the majority of 49 tested games using identical hyperparameters and architecture across all domains, establishing the first convincing demonstration that deep reinforcement learning could scale to high-dimensional sensory inputs.

== Asynchronous and Actor-Critic Methods

While DQN demonstrated the viability of deep RL in discrete action spaces, scaling to continuous control and improving training efficiency required new paradigms. Mnih et al. [Mnih2016] proposed the Asynchronous Advantage Actor-Critic (A3C), which replaced the replay buffer with multiple parallel actor-learner threads, each interacting with its own copy of the environment. By aggregating gradients asynchronously, A3C achieved a decorrelation effect analogous to experience replay while enabling on-policy learning. The advantage function $A(s, a) = Q(s, a) - V(s)$ reduced variance in the policy gradient estimates. A3C surpassed DQN's Atari performance while training in half the time on a single multi-core CPU, demonstrating that parallelism could substitute for the memory overhead of replay buffers.

For continuous action spaces, Lillicrap et al. [Lillicrap2016] introduced the Deep Deterministic Policy Gradient (DDPG), which combined the deterministic policy gradient with DQN-style innovations. DDPG maintains an actor network $mu(s, theta^mu)$ that outputs a continuous action and a critic network $Q(s, a, theta^Q)$ that evaluates it, using experience replay and target networks for stability. The algorithm solved over 20 simulated physics tasks from simple balance problems to complex locomotion, establishing the actor-critic template that subsequent continuous-control algorithms would refine. However, DDPG exhibited well-documented brittleness to hyperparameter choices, often requiring careful tuning to avoid divergence caused by overestimation in the learned Q-function.

== Addressing Overestimation: TD3

Fujimoto, van Hoof, and Meger [Fujimoto2018] diagnosed overestimation bias as the primary failure mode of DDPG and proposed Twin Delayed Deep Deterministic Policy Gradient (TD3) to address it through three mechanisms. First, clipped double Q-learning maintains two independent critic networks and uses the minimum of their predictions to form the Bellman target, $y = r + gamma min_(i=1,2) Q(s', tilde(a); theta_i^-)$, systematically suppressing the positive bias that accumulates when a single critic's errors are exploited by the policy. Second, delayed policy updates reduce the frequency of actor updates relative to critic updates, allowing the value estimates to stabilize before the policy adapts to them. Third, target policy smoothing adds clipped noise to the target action, regularizing the critic by preventing it from developing sharp peaks that the actor could exploit. Together, these modifications produced consistent improvements across the MuJoCo benchmark suite [Todorov2012], outperforming DDPG in every environment tested.

== Maximum Entropy RL: Soft Actor-Critic

Haarnoja et al. [Haarnoja2018a] reframed the reinforcement learning objective itself by augmenting the standard expected return with an entropy bonus, yielding the maximum entropy objective $J(pi) = sum_t bb(E)_(pi) [r(s_t, a_t) + alpha cal(H)(pi(dot | s_t))]$, where $alpha$ is a temperature parameter controlling the trade-off between reward maximization and stochastic exploration. The resulting Soft Actor-Critic (SAC) algorithm inherits the off-policy efficiency of DDPG while gaining several advantages from the entropy regularization. The stochastic policy explores more broadly, the optimization landscape is smoother, and the algorithm is substantially more robust to hyperparameter choices. In a follow-up paper, Haarnoja et al. [Haarnoja2018b] introduced automatic temperature tuning by casting the temperature selection as a constrained optimization problem, eliminating the most sensitive hyperparameter and making SAC nearly turnkey for new domains. SAC rapidly became the de facto standard for continuous control benchmarks, achieving state-of-the-art performance on MuJoCo tasks [Todorov2012] and the DeepMind Control Suite [Tassa2018] while demonstrating successful transfer to real-world robotic manipulation and locomotion.

== Benchmarks and the Standardization of Evaluation

The rapid progress described above was enabled in no small part by the development of standardized evaluation platforms. The Arcade Learning Environment [Bellemare2013] provided a uniform interface to over a hundred Atari 2600 games, each presenting distinct challenges in exploration, credit assignment, and partial observability. For continuous control, the MuJoCo physics engine [Todorov2012] enabled the creation of a canonical suite of locomotion and manipulation tasks that became the primary testbed for algorithms like DDPG, TD3, and SAC. The DeepMind Control Suite [Tassa2018] later offered a curated, standardized set of continuous-control tasks with interpretable reward functions built on MuJoCo, further facilitating reproducible comparison. These benchmarks collectively established the empirical methodology of the field, providing the common ground on which algorithmic claims could be evaluated and contested.

#pagebreak()

== References

+ #label("Sutton1988") R. S. Sutton, "Learning to predict by the methods of temporal differences," _Machine Learning_, vol. 3, pp. 9--44, 1988. https://doi.org/10.1007/BF00115009

+ #label("Watkins1989") C. J. C. H. Watkins, "Learning from delayed rewards," Ph.D. thesis, King's College, University of Cambridge, 1989.

+ #label("WatkinsDayan1992") C. J. C. H. Watkins and P. Dayan, "Q-learning," _Machine Learning_, vol. 8, pp. 279--292, 1992. https://doi.org/10.1007/BF00992698

+ #label("Lin1992") L.-J. Lin, "Self-improving reactive agents based on reinforcement learning, planning and teaching," _Machine Learning_, vol. 8, pp. 293--321, 1992. https://doi.org/10.1007/BF00992699

+ #label("Sutton2000") R. S. Sutton, D. McAllester, S. Singh, and Y. Mansour, "Policy gradient methods for reinforcement learning with function approximation," in _Advances in Neural Information Processing Systems 12 (NeurIPS)_, 1999, pp. 1057--1063.

+ #label("Mnih2013") V. Mnih, K. Kavukcuoglu, D. Silver, A. Graves, I. Antonoglou, D. Wierstra, and M. Riedmiller, "Playing Atari with deep reinforcement learning," _NIPS Deep Learning Workshop_, 2013. arXiv:1312.5602.

+ #label("Mnih2015") V. Mnih, K. Kavukcuoglu, D. Silver, A. A. Rusu, J. Veness, M. G. Bellemare, A. Graves, M. Riedmiller, A. K. Fidjeland, G. Ostrovski, S. Petersen, C. Beattie, A. Sadik, I. Antonoglou, H. King, D. Kumaran, D. Wierstra, S. Legg, and D. Hassabis, "Human-level control through deep reinforcement learning," _Nature_, vol. 518, pp. 529--533, 2015. https://doi.org/10.1038/nature14236

+ #label("Mnih2016") V. Mnih, A. P. Badia, M. Mirza, A. Graves, T. Lillicrap, T. Harley, D. Silver, and K. Kavukcuoglu, "Asynchronous methods for deep reinforcement learning," in _Proceedings of the 33rd International Conference on Machine Learning (ICML)_, 2016, pp. 1928--1937.

+ #label("Lillicrap2016") T. P. Lillicrap, J. J. Hunt, A. Pritzel, N. Heess, T. Erez, Y. Tassa, D. Silver, and D. Wierstra, "Continuous control with deep reinforcement learning," in _Proceedings of the 4th International Conference on Learning Representations (ICLR)_, 2016. arXiv:1509.02971.

+ #label("Fujimoto2018") S. Fujimoto, H. van Hoof, and D. Meger, "Addressing function approximation error in actor-critic methods," in _Proceedings of the 35th International Conference on Machine Learning (ICML)_, 2018, pp. 1587--1596. arXiv:1802.09477.

+ #label("Haarnoja2018a") T. Haarnoja, A. Zhou, P. Abbeel, and S. Levine, "Soft actor-critic: Off-policy maximum entropy deep reinforcement learning with a stochastic actor," in _Proceedings of the 35th International Conference on Machine Learning (ICML)_, 2018, pp. 1861--1870. arXiv:1801.01290.

+ #label("Haarnoja2018b") T. Haarnoja, A. Zhou, K. Hartikainen, G. Tucker, S. Ha, J. Tan, V. Kumar, H. Zhu, A. Gupta, P. Abbeel, and S. Levine, "Soft actor-critic algorithms and applications," _arXiv preprint arXiv:1812.05905_, 2018.

+ #label("SuttonBarto2018") R. S. Sutton and A. G. Barto, _Reinforcement Learning: An Introduction_, 2nd ed. Cambridge, MA: MIT Press, 2018.

+ #label("Bellemare2013") M. G. Bellemare, Y. Naddaf, J. Veness, and M. Bowling, "The Arcade Learning Environment: An evaluation platform for general agents," _Journal of Artificial Intelligence Research_, vol. 47, pp. 253--279, 2013. https://doi.org/10.1613/jair.3912

+ #label("Todorov2012") E. Todorov, T. Erez, and Y. Tassa, "MuJoCo: A physics engine for model-based control," in _IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)_, 2012, pp. 5026--5033. https://doi.org/10.1109/IROS.2012.6386109

+ #label("Tassa2018") Y. Tassa, Y. Doron, A. Muldal, T. Erez, Y. Li, D. de Las Casas, D. Budden, A. Abdolmaleki, J. Merel, A. Lefrancq, T. Lillicrap, and M. Riedmiller, "DeepMind Control Suite," _arXiv preprint arXiv:1801.00690_, 2018.
