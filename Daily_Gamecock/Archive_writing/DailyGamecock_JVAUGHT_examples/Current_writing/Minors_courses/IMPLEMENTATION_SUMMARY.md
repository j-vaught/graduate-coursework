# Phase 3 Real Analysis - Implementation Summary

## Completion Status: ✓ COMPLETE

All Phase 3 analysis has been successfully implemented using real grade spread data from 15 semesters (Spring 2021 - Fall 2025).

## Deliverables

### 1. Production Python Script
**File**: `/Minors_courses/phase3_real_analysis.py` (24 KB)

A complete, production-ready Python script that:
- Loads all 15 grade spread Excel files from `usc_grade_spreads/` directory
- Extracts unique course offerings by semester
- Parses 107 minor markdown files to identify required courses
- Analyzes offering frequency for each required course
- Classifies courses as ghost (0%), zombie (<30%), or normal (30%+)
- Generates all three required output reports
- Can be re-run anytime new grade spread data is available

**Usage**: 
```bash
python3 phase3_real_analysis.py
```

### 2. Output CSV Files

#### 11_Real_Phase_3_Course_Offerings.csv (54 rows)
Minor-level analysis with columns:
- Minor Name
- Category
- Total Required Courses
- Required Courses Ever Offered
- Ghost Courses (count)
- Ghost Course List
- Zombie Courses (count)
- Zombie Course List
- Min/Max/Avg Offering Rates (%)
- Can Complete Minor (Yes/No)
- Risk Level (Low/Medium/High/Critical)

**Key Findings**:
- 53 minors analyzed with required courses identified
- 11 minors (20.8%) cannot be completed
- Offers sorting by Risk Level to prioritize problematic programs

#### 11_Real_Ghost_and_Zombie_Courses.csv (59 rows)
Course-level analysis with columns:
- Course Code (SUBJECT NUMBER)
- Subject Prefix
- Type (Ghost/Zombie)
- Semesters Offered In (readable format)
- Times Offered (count)
- Offering Rate (%)
- Required By (count of minors)
- Minor Names (semicolon-separated list)

**Key Findings**:
- 17 ghost courses identified
- 42 zombie courses identified
- Shows which minors depend on problem courses

### 3. Comprehensive Markdown Report
**File**: `11_Real_Phase_3_Report.md` (223 lines)

Professional report including:
- Executive Summary with key metrics
- Complete list of 11 uncomplatable minors (with ghost courses listed)
- Top 15 minors ranked by course availability
- Department-level analysis (worst and best departments)
- Detailed ghost course list (17 courses)
- Detailed zombie course list (42 courses, truncated to 30 with note)
- Critical Findings & Implications section
- Specific Recommendations for improvement
- Metadata (generation date, analysis period, semester count)

### 4. Documentation Files

#### PHASE3_ANALYSIS_README.md
Complete user guide including:
- Overview of analysis approach
- File descriptions and locations
- Metric definitions (ghost/zombie/risk levels)
- Key findings summary
- Script architecture explanation
- Data quality notes and limitations
- Instructions for updating analysis
- Guidance for different user types (advisors, chairs, registrar)

#### PHASE3_QUICK_REFERENCE.txt
Quick-lookup statistics sheet with:
- Overall metrics at a glance
- Top 5 worst and best minors
- Worst and best departments
- Key ghost and zombie courses
- Impact summary
- High-value improvement targets
- Cross-references to detailed reports

#### IMPLEMENTATION_SUMMARY.md (this file)
Overview of all deliverables and how to use them

## Data Processing Pipeline

### Input Data
```
Grade Spread Files (15 semesters)
↓
Extract: SUBJECT, COURSE_NUMBER
↓
Build: Semester → {Courses Offered}

Minor Markdown Files (107 files)
↓
Extract: REQUIRED courses only
↓
Build: Minor → {Required Courses}

Master Analysis CSV
↓
Extract: Category information
↓
Build: Minor → Category mapping
```

### Analysis Process
```
For each Minor:
  For each Required Course:
    Count: How many semesters offered?
    Calculate: Offering Rate (%)
    Classify: Ghost (0%) / Zombie (<30%) / Normal (30%+)
  Determine: Can minor be completed? (all courses offered ≥ once)
  Assign: Risk Level based on ghost/zombie counts and avg rate

Generate Reports:
  1. CSV: Minor summary (offering rates, risk levels)
  2. CSV: Course detail (which minors affected)
  3. Markdown: Executive report with analysis
```

## Key Results

### By the Numbers
- **Semesters Analyzed**: 15 (Spring 2021 - Fall 2025)
- **Minors Analyzed**: 53 with identifiable required courses
- **Total Required Courses**: 191 unique
- **Ghost Courses**: 17 (8.9%)
- **Zombie Courses**: 42 (22.0%)
- **Completable Minors**: 42 (79.2%)
- **Uncomplatable Minors**: 11 (20.8%)

### Critical Minors (Cannot Be Completed)
1. **Law and Society Interdisciplinary** - 4 ghost + 6 zombie courses
2. **Jewish Studies** - 3 ghost courses
3. **Foreign Language Education** - 3 ghost courses
4. **Audio Recording** - 1 ghost + 4 zombie courses
5. **Classical Studies** - 1 ghost + 2 zombie courses
6. **Comparative Literature** - 1 ghost course
7. **Creative Writing** - 1 ghost + 1 zombie course
8. **Entrepreneurship** - 1 ghost course
9. **Environmental and Sustainable Engineering** - 1 ghost course
10. **Latin** - 1 ghost course
11. **Music Entrepreneurship** - 1 ghost course

### Most Problematic Departments
- **FORL (Foreign Language)**: 0.0% avg offering (3 ghost courses)
- **JSTU (Jewish Studies)**: 0.0% avg offering (3 ghost courses)
- **LATN (Latin)**: 0.0% avg offering (1 ghost course)
- **RETL (Retail)**: 0.0% avg offering (2 ghost courses)
- **ARAB (Arabic)**: 15.6% avg offering (5 zombie courses)

## How to Use These Files

### For Department Chairs
1. Open `11_Real_Ghost_and_Zombie_Courses.csv`
2. Filter for your department prefix
3. Review which of your courses are ghost/zombie
4. Check "Required By Minors" to see impact
5. Consider scheduling adjustments to increase offering frequency

### For Academic Advisors
1. Refer to `PHASE3_QUICK_REFERENCE.txt` for overview
2. Check `11_Real_Phase_3_Course_Offerings.csv` for student's chosen minor
3. Note "Risk Level" and "Can Complete Minor" columns
4. Review "Ghost Course List" and "Zombie Course List"
5. Discuss scheduling challenges with students early

### For Deans/Strategic Planning
1. Read `11_Real_Phase_3_Report.md` executive summary
2. Focus on "Minors That Cannot Be Completed" section
3. Review "Department Analysis" to identify resource needs
4. Use "Top 15 Minors" rankings to prioritize improvements
5. Reference "Recommendations" section for action items

### For Program Directors
1. Look up your minor in `11_Real_Phase_3_Course_Offerings.csv`
2. Note your Risk Level and available courses
3. If Critical/High Risk: check `11_Real_Ghost_and_Zombie_Courses.csv` for specific problems
4. Contact department chairs for ghost courses
5. Develop backup/alternative course requirements if necessary

## Technical Details

### Script Dependencies
- Python 3.8+
- pandas (for Excel and CSV operations)
- openpyxl (for Excel file reading)

### File Locations
- **Script**: `/Minors_courses/phase3_real_analysis.py`
- **Input Grade Spreads**: `/Minors_courses/usc_grade_spreads/*.xlsx`
- **Input Minor Definitions**: `/Minors_courses/*_Minor.md`
- **Input Master Analysis**: `/Minors_courses/00_MASTER_ANALYSIS/USC_Minors_Master_Analysis.csv`
- **Output Directory**: `/Minors_courses/00_MASTER_ANALYSIS/`
- **Output Files**: 
  - `11_Real_Phase_3_Course_Offerings.csv`
  - `11_Real_Ghost_and_Zombie_Courses.csv`
  - `11_Real_Phase_3_Report.md`

### Semester Code Format
Files are parsed using semester codes: YYYYMM
- MM = 01 (Spring)
- MM = 05 (Summer)
- MM = 08 (Fall)

Examples:
- 202101 = Spring 2021
- 202508 = Fall 2025

## Rerunning the Analysis

To regenerate reports with new data:

```bash
# Option 1: From the minors directory
cd /Volumes/MacShare/graduate-coursework/Daily_Gamecock/Archive_writing/DailyGamecock_JVAUGHT_examples/Current_writing/Minors_courses
python3 phase3_real_analysis.py

# Option 2: From anywhere (script uses absolute paths)
python3 /Volumes/MacShare/graduate-coursework/Daily_Gamecock/Archive_writing/DailyGamecock_JVAUGHT_examples/Current_writing/Minors_courses/phase3_real_analysis.py
```

The script will:
1. Load all .xlsx files in `usc_grade_spreads/`
2. Process all `*_Minor.md` files
3. Overwrite the three output CSV/Markdown files
4. Display progress and completion status

## Quality Assurance

### Validation Checks Performed
✓ All 15 grade spread files loaded successfully (2,706-2,930 courses each)
✓ All 107 minor markdown files processed (53 with identified required courses)
✓ 191 unique required courses extracted across all minors
✓ Offering rates calculated and validated for each course
✓ Ghost/zombie classification applied consistently
✓ Risk levels assigned based on course availability
✓ CSV output validated for consistency
✓ Markdown report formatting verified

### Known Limitations
- Analysis only includes minors with clearly marked "Required" courses in markdown
- Tracks course offering, not enrollment numbers or section counts
- Category information sourced from master analysis CSV (some "Unknown")
- Assumes markdown files accurately reflect current program requirements

## Version Information

**Script Version**: 1.0  
**Analysis Date**: February 12, 2026  
**Analysis Period**: Spring 2021 - Fall 2025 (15 semesters)  
**Total Courses in Database**: ~38,000 course offerings analyzed  

## Next Steps

Recommended actions based on this analysis:

1. **Immediate** (0-3 months):
   - Share findings with affected departments
   - Begin conversations with program directors of critical-risk minors
   - Verify ghost courses are truly discontinued or miscoded

2. **Short-term** (3-6 months):
   - Develop restoration plans for key ghost courses
   - Create contingency course lists for high-risk minors
   - Update program requirements if courses cannot be restored

3. **Medium-term** (6-12 months):
   - Implement course scheduling improvements for zombie courses
   - Increase offering frequency for most frequently-taken courses
   - Monitor data for impact assessment

4. **Long-term** (ongoing):
   - Re-run analysis each academic year
   - Track progress on restoration efforts
   - Maintain minimum offering frequency standards

---

**For questions or to request custom analysis, refer to the script code and documentation.**
