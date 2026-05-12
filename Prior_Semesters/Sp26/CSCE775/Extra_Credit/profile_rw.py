"""Profile batch random_walk to find remaining hotspots."""
import sys
sys.path.insert(0, "/Users/user/Downloads/graduate-coursework/Sp26/CSCE775/Extra_Credit/deepxube")

import cProfile
import pstats
import numpy as np
from deepxube.domains.warehouse_mapf import WarehouseMAPF

np.random.seed(42)
env = WarehouseMAPF(28, 28, 30)
states, goals = env.sample_goalstate_goal_pairs(10000)
env.set_active_goal(goals[0])
steps = list(np.random.randint(1, 50, size=10000))

cProfile.run('env.random_walk(states, steps)', '/tmp/rw_profile')
p = pstats.Stats('/tmp/rw_profile')
p.strip_dirs().sort_stats('cumulative').print_stats(20)
