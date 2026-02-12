# Phase 3 Real Analysis - Course Availability Report

## Overview

The Phase 3 analysis uses real grade spread data from 15 semesters (Spring 2021 - Fall 2025) to determine the actual availability of required courses for USC minors. This analysis identifies courses that are never offered (ghost courses) or rarely offered (zombie courses), and determines which minors cannot realistically be completed.

## Files

### Input Data
- **Grade Spread Excel Files**: `/Minors_courses/usc_grade_spreads/`
  - 15 semesters of USC course offerings (202101 through 202508)
  - Each file contains SUBJECT, COURSE_NUMBER, and other enrollment data

- **Minor Definitions**: `/Minors_courses/*_Minor.md`
  - 107 markdown files with course requirements for each minor
  - Each file identifies which courses are REQUIRED vs ELECTIVE

- **Master Analysis CSV**: `/Minors_courses/00_MASTER_ANALYSIS/USC_Minors_Master_Analysis.csv`
  - Summary information about each minor

### Output Files
Generated in `/Minors_courses/00_MASTER_ANALYSIS/`:

1. **11_Real_Phase_3_Course_Offerings.csv**
   - Main analysis report with one row per minor
   - Columns: Minor Name, Category, Total Required Courses, Ghost Courses, Zombie Courses, offering rates, completion status, risk level
   - Use for: Identifying problematic minors and comparing offering frequency

2. **11_Real_Ghost_and_Zombie_Courses.csv**
   - Detailed course-level analysis
   - Columns: Course Code, Subject Prefix, Type (Ghost/Zombie), Semesters Offered, Times Offered, Offering Rate, Required By (count), Minor Names
   - Use for: Understanding specific problem courses and which minors are affected

3. **11_Real_Phase_3_Report.md**
   - Comprehensive human-readable markdown report
   - Includes: Executive summary, uncomplatable minors, top 15 worst minors, department analysis, ghost/zombie course lists, recommendations
   - Use for: Presentations and strategic planning

## Key Metrics

### Course Types

**Ghost Courses (0% offering rate)**
- Required courses that have **never been offered** during the entire analysis period
- Examples: MUSC 571, JSTU 373, FORL 510
- 17 ghost courses total across all minors

**Zombie Courses (<30% offering rate)**
- Required courses offered in fewer than 30% of semesters
- Examples: ARAB 121 (26.7%), CLAS 321 (20.0%)
- 42 zombie courses total across all minors

### Minor Risk Levels

- **Low Risk**: All required courses offered regularly (60%+ offering rate), no ghost/zombie courses
- **Medium Risk**: No ghost courses, but some zombie courses or averaging 60% offering rate
- **High Risk**: No ghost courses but multiple zombie courses or low average offering rate
- **Critical Risk**: Has ghost courses, meaning the minor **cannot be completed**

## Key Findings

From analysis of 15 semesters (Spring 2021 - Fall 2025):

- **53 minors analyzed** (from 107 total minors with identifiable required courses)
- **191 unique required courses** across all minors
- **11 minors cannot be completed** (20.8%) due to ghost courses
- **17 ghost courses** never offered (8.9% of required courses)
- **42 zombie courses** rarely offered (22.0% of required courses)
- **27 minors at high or critical risk**

### Critical Issues

1. **Foreign Language Education**: 3 ghost courses, cannot be completed
2. **Jewish Studies**: 3 ghost courses, 0% average offering rate
3. **Law and Society**: 4 ghost courses, only 34.2% average offering rate
4. **Audio Recording**: 1 ghost course + 4 zombie courses, only 18.9% average offering rate
5. **Classical Studies**: 1 ghost course + 2 zombie courses, only 16.7% average offering rate

### Department-Level Problems

**Worst Performing Departments** (by avg offering rate):
- FORL (Foreign Language): 0.0% (3 courses, all ghost)
- JSTU (Jewish Studies): 0.0% (3 courses, all ghost)
- LATN (Latin): 0.0% (1 course, ghost)
- RETL (Retail): 0.0% (2 courses, ghost)
- ARAB (Arabic): 15.6% (6 courses, heavy zombie problem)

**Best Performing Departments**:
- ACCT, CHEM, MATH, MGMT, MGSC, MKTG: 100% (all required courses every semester)
- ARTH (Art History): 96.7%
- EDPY (Educational Psychology): 93.3%

## Script: phase3_real_analysis.py

### Dependencies
- Python 3.8+
- pandas
- openpyxl

### Usage
```bash
python3 phase3_real_analysis.py
```

The script will:
1. Load all Excel grade spread files
2. Extract unique course offerings by semester
3. Load all minor markdown files
4. Extract required courses from each minor
5. Analyze offering frequency for each required course
6. Classify courses as ghost, zombie, or normal
7. Generate all three output files
8. Display progress and results to console

### Script Architecture

**Phase3Analyzer Class**
- `load_grade_spread_files()`: Reads Excel files and builds semester course inventory
- `load_minors_from_markdown_files()`: Extracts required courses from markdown files
- `analyze_course_offerings()`: Calculates offering frequencies
- `generate_phase3_course_offerings_report()`: Creates main CSV output
- `generate_ghost_and_zombie_report()`: Creates detailed course analysis CSV
- `generate_markdown_report()`: Creates human-readable report
- `save_results()`: Writes all output files

## Data Quality Notes

### Considerations
1. **Semester Codes**: Parsed as YYYYMM format (202101 = Spring 2021, 202105 = Summer 2021, 202108 = Fall 2021)
2. **Course Matching**: Based on (SUBJECT, COURSE_NUMBER) pairs from grade spreads matched to markdown files
3. **Category Data**: Extracted from master analysis CSV (some entries marked as "Unknown" if not found)
4. **Offering Rate Calculation**: (# semesters offered) / (total semesters in period) × 100%

### Limitations
- Analysis limited to minors with clearly marked "Required" courses in markdown files
- Only tracks whether course was offered, not enrollment or section count
- Assumes markdown files accurately reflect current requirements
- Some minors may not have required course lists clearly delineated

## Interpreting Results

### For Advising
- **Red Flag**: Any minor with Risk Level = "Critical" cannot be completed
- **Yellow Flag**: High-risk minors should be discussed with students - multiple zombie courses mean unpredictable offerings
- **OK**: Low/Medium risk minors are generally completable but may require planning

### For Department Chairs
- Review ghost and zombie courses in your department
- Consider scheduling conflicts or staffing limitations
- Evaluate whether courses should remain required or become elective
- Plan course schedule to ensure more regular offerings

### For Registrar
- Use as input for course scheduling planning
- Identify bottleneck courses that many minors depend on
- Consider rotating zombie courses to annual (or more frequent) schedule
- Flag permanently discontinued courses that remain in requirements

## Updating the Analysis

To re-run with new grade spread data:

1. Add new Excel files to `usc_grade_spreads/` directory
2. Ensure filenames follow format: `YYYYMM_grade_spread_report.xlsx` or `YYYYMM_grade_spread_report_2.xlsx`
3. Run: `python3 phase3_real_analysis.py`
4. Output files will be overwritten with updated results

## Contact & Questions

For questions about this analysis:
- Check the embedded comments in `phase3_real_analysis.py`
- Review the markdown report for interpretation help
- Cross-reference with individual minor markdown files for specific course requirements

---

**Last Generated**: February 12, 2026
**Analysis Period**: Spring 2021 - Fall 2025 (15 semesters)
**Script Version**: 1.0
