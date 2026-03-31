# DeepXube Pathfinding Domain Ideas

Candidate domains for extending the DeepXube framework beyond its current implementations (Grid, N-Puzzle, Rubik's Cube, Lights Out, Sokoban, Continuous Grid).

---

## Easy — Clean Fit to Existing Framework

### 8/15/24-Puzzle (Larger Variants)

- **State:** Tile arrangement on an N×N board
- **Actions:** Slide a tile into the blank space
- **Why Interesting:** N-puzzle already exists in DeepXube, but scaling to 24-puzzle (5×5) tests whether the learned heuristic remains effective as the state space grows exponentially. Known optimal solutions exist for benchmarking.

### Tower of Hanoi

- **State:** Position of each disk across K pegs
- **Actions:** Move the top disk from one peg to another
- **Why Interesting:** Exponential state space (3^N for 3 pegs, N disks) with known optimal solutions. Tests whether DeepXube can learn recursive structure. Simple to implement, clean evaluation.

### Pancake Sorting

- **State:** A permutation of N pancakes (stack order)
- **Actions:** Flip the top K pancakes (prefix reversal)
- **Why Interesting:** Open combinatorics problem. The diameter of the pancake graph (maximum number of flips needed) is not fully solved for large N. Provides a clean benchmark where heuristic quality directly impacts solution length.

### Maze Navigation

- **State:** (x, y) position in a grid with walls
- **Actions:** Move up, down, left, or right
- **Why Interesting:** Grid domain already exists, but adding walls fundamentally changes heuristic learning. The network must learn to reason about obstacles and dead ends, not just Euclidean distance. Easily scalable by increasing maze size or complexity.

---

## Medium — Requires Some Design Work

### Multi-Agent Pathfinding

- **State:** N agent positions on a shared grid
- **Actions:** Move each agent simultaneously (joint action space)
- **Why Interesting:** Exponential branching factor (4^N for N agents with 4 directions). Requires learning collision avoidance and coordination. Active research area in robotics and warehouse automation.

### Warehouse / Multi-Box Sokoban

- **State:** Agent position + N box positions on a grid
- **Actions:** Move agent (pushing boxes on contact)
- **Why Interesting:** Sokoban exists in DeepXube but is limited in scale. Multiple boxes create complex interactions where moving one box can block another. PSPACE-complete, so optimal solvers fail on larger instances.

### Graph Coloring

- **State:** Partial color assignment to graph vertices
- **Actions:** Assign a color to the next uncolored vertex
- **Why Interesting:** Frames constraint satisfaction as pathfinding. The heuristic must learn which assignments lead to dead ends. NP-complete in general, with applications in scheduling and register allocation.

### Word Ladder

- **State:** A current word (e.g., "COLD")
- **Actions:** Change one letter to form a valid word
- **Why Interesting:** NLP-flavored pathfinding in a discrete, finite space. The state graph is implicitly defined by a dictionary. Branching factor varies wildly depending on the word. Simple to implement, fun to demonstrate.

### Traveling Salesman Problem (Small Instances)

- **State:** Set of visited cities + current city
- **Actions:** Travel to any unvisited city
- **Why Interesting:** Classic NP-hard optimization problem. Tests whether DeepXube's heuristic can learn tour-cost estimation. Small instances (10-20 cities) are tractable for search, and solution quality is easy to evaluate against known optima.

### Protein Folding (2D HP Lattice Model)

- **State:** Partial fold of a protein sequence on a 2D grid
- **Actions:** Place the next amino acid residue at an adjacent grid position
- **Why Interesting:** Simplified model of a real bioinformatics problem. The objective is to maximize hydrophobic contacts. NP-complete on the 2D lattice. Connects DeepXube to computational biology applications.

---

## Hard — Ambitious but Publishable

### Robot Arm Inverse Kinematics

- **State:** Joint angles of an N-joint robotic arm
- **Actions:** Adjust a joint angle by a continuous increment
- **Why Interesting:** Continuous, high-dimensional state space. The heuristic must learn the nonlinear relationship between joint angles and end-effector position. Direct application to robotics. Similar in structure to continuous grid but with coupled, non-Euclidean geometry.

### Circuit Layout / Wire Routing

- **State:** Partial wire placement on a 2D grid
- **Actions:** Extend a wire segment in a cardinal direction
- **Why Interesting:** Real engineering application in VLSI design. Multiple wires must be routed without crossing. Combines pathfinding with constraint satisfaction. Industry relevance makes this compelling for publication.

### Molecular Generation

- **State:** Partial molecular graph (atoms and bonds placed so far)
- **Actions:** Add an atom or bond to the molecule
- **Why Interesting:** Drug discovery framing. The heuristic learns chemical validity and property optimization simultaneously. Active research area at the intersection of ML and chemistry. Novel application of heuristic search to generative molecular design.

### Reference-Guided SAM Segmentation

- **State:** Current partial mask coverage of target image
- **Actions:** Place a positive SAM prompt point at (x, y) in the target image
- **Why Interesting:** Reformulates image segmentation as sequential pathfinding through mask-coverage space. A reference image + mask pair defines the "goal object." The agent learns to build up a union of small, confident sub-masks, avoiding the instability of negative-point prompting. A leakage penalty during training enforces boundary-aware placement. This extends DeepXube from discrete combinatorial puzzles to a continuous, vision-grounded domain with a real-world application in computer vision.
