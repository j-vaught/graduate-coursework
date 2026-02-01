# Gemini Review — Wang_Active-Acquisition.tex
**Date:** 2026-02-01
**Reviewer:** Gemini 2.5 Pro (via Gemini CLI)

---

## 1. Structure & Flow

### 1.1 Weak Ending (Major)
- **Location:** Section VII.F (Airplanes Test Case)
- **Issue:** Feels tacked on. Too short (two paragraphs), disconnects from the strong quantitative drone tracking results.
- **Recommendation:** Merge into a broader Discussion section or integrate with VII.E (In-Lab Airplane Detection). If it represents ongoing work, frame it as "Future Applications" in the Conclusion rather than a standalone experimental subsection.

### 1.2 Section Header — "Hardware and Software Roles"
- **Location:** Section III.A
- **Issue:** Title is slightly informal for a conference paper.
- **Recommendation:** Rename to "System Architecture" or "Hardware-Software Integration."

### 1.3 Methodology Placement
- **Location:** Section VII.C (Tracking Controller)
- **Issue:** Contains core methodology (PID gains, state machine logic) but is buried in the Experimental Validation section.
- **Recommendation:** Move control logic (state machine, PID formulation) to Section V (PTZ Triggering...) or a new "Control Framework" section. Keep only the tuning results and performance characterization in the Experiments section.

---

## 2. Formatting & LaTeX Usage

### 2.1 Author Block (Critical)
- **Issue:** Paper uses `\author{Name\footnote{...}}` manually, but `new-aiaa.cls` loads the `authblk` package. Mixing manual footnotes with `authblk` can lead to symbol/numbering mismatches.
- **Recommendation:** Use standard `authblk` syntax:
  ```latex
  \author[1]{Jackie Wang}
  \author[2]{J.C. Vaught}
  \affil[1]{Graduate Student, Dept. of Mechanical Engineering...}
  ```
  Note: If the class file strictly enforces the current style, ensure the symbols match AIAA guidelines (usually *, †, etc.).

### 2.2 Bibliography Format
- **Issue:** Paper uses a manual `\begin{thebibliography}` environment. Manual bibliographies are error-prone (formatting, ordering).
- **Recommendation:** Since `new-aiaa.bst` is present in the directory, switch to BibTeX:
  ```latex
  \bibliographystyle{new-aiaa}
  \bibliography{your_bib_file}
  ```

### 2.3 Abstract Length
- **Issue:** Abstract is detailed but slightly long.
- **Recommendation:** Ensure it fits within strict word count limits (often 200–250 words) for the specific AIAA conference.

---

## 3. Professional Tone & Content

### 3.1 Hedging Language
- **Issue:** Phrasing like "The current implementation uses..." sounds tentative.
- **Recommendation:** Replace with "The system uses..." or "We employ..." throughout to sound more definitive.

### 3.2 Terminology
- **Positive:** "Slew-to-classification" is a strong, novel term — keep emphasizing it.

### 3.3 Units — Imperial to Metric
- **Location:** Section III.A — "three-foot stand"
- **Issue:** Imperial units; AIAA papers target an international audience.
- **Recommendation:** Convert to metric: "0.9 m stand" or provide both ("three-foot (0.9 m) stand").

### 3.4 Figure Quality
- **Figure 1 (Hardware photo):** Ensure high contrast for print reproduction.
- **Figure 3 (GUI screenshot):** Screenshots of GUIs are often hard to read in print. Ensure text labels are legible or re-create the diagram as a vector graphic if possible.

---

## Summary of Recommended Changes

| Priority | Change | Location |
|----------|--------|----------|
| High | Merge or reframe Airplanes Test Case as future work | VII.F |
| High | Remove hedging language ("current implementation" → "the system") | Throughout |
| Medium | Rename III.A to "System Architecture" | Section header |
| Medium | Move control logic from VII.C to Section V | VII.C → V |
| Medium | Convert imperial to metric ("three-foot" → "0.9 m") | III.A |
| Medium | Standardize author block with `authblk` syntax | Preamble |
| Low | Switch to BibTeX with `new-aiaa.bst` | Bibliography |
| Low | Check abstract word count (target 200–250 words) | Abstract |
| Low | Ensure GUI screenshot legibility in print | Figure 3 |
