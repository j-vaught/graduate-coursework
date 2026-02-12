# User Preferences

## Plotting & Visualization
Use brand colors for all plots and visualizations:

**Primary:**
| Color | Hex | RGB |
|-------|-----|-----|
| Garnet | #73000A | 115, 0, 10 |
| Black | #000000 | 0, 0, 0 |
| White | #FFFFFF | 255, 255, 255 |

**Neutral:**
| Color | Hex | RGB |
|-------|-----|-----|
| 90% Black | #363636 | 54, 54, 54 |
| 70% Black | #5C5C5C | 92, 92, 92 |
| 50% Black | #A2A2A2 | 162, 162, 162 |
| 30% Black | #C7C7C7 | 199, 199, 199 |
| 10% Black | #ECECEC | 235, 235, 235 |
| Warm Grey | #676156 | 103, 97, 86 |
| Sandstorm | #FFF2E3 | 255, 242, 227 |

**Accent:**
| Color | Hex | RGB |
|-------|-----|-----|
| Rose | #CC2E40 | 204, 46, 64 |
| Atlantic | #466A9F | 70, 106, 159 |
| Congaree | #1F414D | 31, 65, 77 |
| Horseshoe | #65780B | 101, 120, 11 |
| Grass | #CED318 | 206, 211, 24 |
| Honeycomb | #A49137 | 164, 145, 55 |

- Avoid rounded edges on all plots, figures, and graphical elements
- Always use high contrast color schemes

## Authorship & Attribution
- Author name for all GitHub commits, pull requests, and code contributions: `j-vaught`
- Email for all GitHub code work: `jvaught@sc.edu`
- Written authorship (readmes, documentation, articles): `J.C. Vaught`

## Restrictions
- Never mention Claude Code, Anthropic, opus, haiku, or sonnet in:
  - Code comments
  - GitHub commit messages
  - Pull request descriptions
  - READMEs or documentation
  - Code authorship/co-author fields

## GitHub Management
- If a github repository exists, push and commit after each change. 
  - If a repo does not exist, ask the user after each prompt if they want to create a github repo
  - Recommend branches and PRs when they make sense.
  - Always add a .gitignore file to the repo to ignore Virtual environments, build files, and compilation artifacts. 
  - Do not add output files like png, mp4, tex, pdf, and similar to the .gitignore

## Compiling LaTeX Documents
- If asked to write a .tex file, always compile it twice after writing. 
- Always delete compilation files, except the pdf, after the second compilation.