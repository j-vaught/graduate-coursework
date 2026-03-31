# Theia HPC Cluster Reference

## Access

- **SSH via Tailscale:** `ssh theia`
- **SSH direct:** `ssh -p222 jvaught@login-theia.rc.sc.edu`
- **Authentication:** USC network credentials (AD-synced password)
- **Web portal (Open OnDemand):** https://login-theia.rc.sc.edu/pun/sys/dashboard

## Directories

| Path | Notes |
|------|-------|
| `/home/jvaught/` | Home directory |
| `/work/jvaught/` | Preferred workspace, faster filesystem |

## Critical Rules

1. **Do NOT run applications on the login node.** This includes VS Code, Claude Code, tmux long-running sessions, or any AI/LLM tools. Violations crash the login node and affect all users.
2. **No VS Code remote sessions on the login node.** Resource exhaustion from VS Code has caused crashes. Use Open OnDemand desktop sessions instead.
3. **No AI coding tools on login nodes.** All dev environments and LLM tools must run on compute nodes only.
4. **All dev work must happen on compute nodes** via batch jobs or interactive/OOD sessions.

## Interactive Sessions

- **Terminal (4 hours):** From the login node, run `idev` (CPU) or `idev_gpu` (GPU)
- **Virtual desktop:** Open OnDemand > Interactive Apps > Hyperion Desktop

## Job Submission (Slurm)

```bash
# Submit a job
sbatch script.sh

# Check job status
squeue -u jvaught

# Cancel a job
scancel <jobid>
```

All job scripts must include:
```bash
#SBATCH --account rc_general
```

## Modules

```bash
# List available software
module avail

# Load software (example)
module load python3/anaconda/3.12
```

Request additional software: https://scprod.service-now.com/sp?id=sc_cat_item&sys_id=a100fb030f396300c1c0563be1050eba

## File Transfer

Use `sftp` or `scp` with the same address and port:
```bash
scp -P222 file.txt jvaught@login-theia.rc.sc.edu:/work/jvaught/
```

Or via Tailscale (no port needed):
```bash
scp file.txt theia:/work/jvaught/
```

## Support

- **Office Hours:** https://sc.edu/about/offices_and_divisions/division_of_information_technology/rc/index.php
- **Contacts:** Myk Milligan (setup), Nathan Elger (HPC systems)
