# Phase 3: Structural Vulnerability Analysis - Completion Summary

**Project**: Comprehensive Structural Vulnerability Analysis of USC TIER 1 CRITICAL Minors
**Scope**: 81 TIER 1 CRITICAL minors from University of South Carolina
**Analysis Date**: February 12, 2026
**Status**: COMPLETE

---

## Deliverables Overview

### 1. Python Analysis Script
**File**: `/Volumes/MacShare/graduate-coursework/Daily_Gamecock/Archive_writing/DailyGamecock_JVAUGHT_examples/Current_writing/phase_3_analysis.py`

**Capabilities**:
- Reads master analysis and severity ranking CSVs from source directory
- Analyzes all 81 TIER 1 CRITICAL minors
- Calculates 6 distinct vulnerability metrics per minor
- Generates structured CSV output with 11 analytical columns
- Produces comprehensive markdown report with patterns and recommendations
- Sorts output by Impossible-if-One-Required Score (descending order)

**Key Functions**:
- `analyze_tier1_minors()`: Core analysis function for all minors
- `calculate_impossible_if_one_required()`: Vulnerability calculation
- `identify_critical_risk_factors()`: Risk factor classification
- `write_output_csv()`: Structured CSV generation
- `generate_markdown_report()`: Comprehensive reporting

### 2. Structural Vulnerability CSV
**File**: `/Volumes/MacShare/graduate-coursework/Daily_Gamecock/Archive_writing/DailyGamecock_JVAUGHT_examples/Current_writing/Minors_courses/00_MASTER_ANALYSIS/09_Phase_3_Structural_Vulnerability.csv`

**Format**: 81 records × 11 columns

**Column Definitions**:
1. **Minor Name**: Official minor title from USC catalog
2. **Total Required Courses**: Number of courses designated as required
3. **Required Course Prefixes**: Comma-separated list of department prefixes
4. **Prefixes in Required Courses**: Count of unique departments in required courses
5. **Single Department?**: Yes/No indicator for single-department minors
6. **Impossible-if-One-Required Score**: % vulnerability if one required course unavailable
7. **Required Course % of Total**: Required courses as percentage of total minor courses
8. **Department Bottleneck Risk**: Classification (LOW/MODERATE/HIGH/EXTREME)
9. **Flexibility Score (0-100)**: Measure of student flexibility (based on electives)
10. **Critical Risk Factors**: Comma-separated list of identified vulnerabilities
11. **Recommendation**: Specific action recommendations for departments

### 3. Comprehensive Analysis Report
**File**: `/Volumes/MacShare/graduate-coursework/Daily_Gamecock/Archive_writing/DailyGamecock_JVAUGHT_examples/Current_writing/Minors_courses/00_MASTER_ANALYSIS/09_Phase_3_Report.md`

**Sections**:
1. Executive Summary (key statistics and findings)
2. Top 15 minors at highest structural risk (detailed analysis)
3. Pattern analysis (4 major vulnerability patterns identified)
4. Department review recommendations (tiered by urgency)
5. Phase 4 integration framework (methodology for next phase)

---

## Key Findings

### Executive Statistics
- **Total minors analyzed**: 81 TIER 1 CRITICAL
- **Minors with extreme vulnerability**: 31 (38.3%)
- **Minors with no flexibility**: 14 (17.3%)
- **Single-department minors**: 47 (58.0%)

### Impossible-if-One-Required Score Distribution
| Score | Count | % | Interpretation |
|-------|-------|---|---|
| 100.00% | 7 | 8.6% | 1 required course only |
| 50.00% | 14 | 17.3% | 2 required courses |
| 33.33% | 10 | 12.3% | 3 required courses |
| 25.00% | 11 | 13.6% | 4 required courses |
| 20.00% | 7 | 8.6% | 5 required courses |
| <20.00% | 32 | 39.5% | 6+ required courses |
| 0.00% | 6 | 7.4% | All electives |

**Average Score**: 30.50%
**Median Score**: 25.00%
**Range**: 0.00% to 100.00%

### Top 5 Most Vulnerable Minors

1. **Russian and Eurasian Studies Minor** - 100.00%
   - 1 required course out of 11 total
   - 4-department spread (FORL, HIST, POLI, RUSS)
   - Recommendation: Critical - Add required courses or restructure

2. **International Studies Minor** - 100.00%
   - 1 required course out of 32 total (3.1%)
   - Single-department (POLI)
   - 4 critical risk factors identified
   - Recommendation: Requires immediate restructuring

3. **Psychology Minor** - 100.00%
   - 1 required course out of 17 total (5.9%)
   - 2-department spread (NSCI, PSYC)
   - Recommendation: Critical - Add required courses

4. **Professional Writing and Communication Minor** - 100.00%
   - 1 required course out of 15 total (6.7%)
   - 2-department spread (ENGL, SPCH)
   - Recommendation: Critical - Add required courses

5. **Astronomy Minor** - 100.00%
   - 1 required course out of 11 total (9.1%)
   - 8-department spread (high diversity but single requirement)
   - Recommendation: Critical - Add required courses

### Identified Vulnerability Patterns

#### Pattern 1: Minimal Required Courses (1-3 courses)
- **Count**: 31 minors (38.3%)
- **Impact**: Single course unavailability makes entire minor impossible
- **Examples**: Russian Studies (1), Psychology (1), Forensics (2)
- **Core Issue**: Insufficient redundancy in requirement structure

#### Pattern 2: Single-Department Minors
- **Count**: 47 minors (58.0%)
- **Impact**: Department scheduling/staffing changes threaten viability
- **Examples**: Mathematics (MATH only), Spanish (SPAN only), Latin (LATN only)
- **Core Issue**: Departmental concentration creates bottleneck

#### Pattern 3: No Flexibility or Safety Net
- **Count**: 14 minors (17.3%)
- **Impact**: Students have no alternative courses if required unavailable
- **Examples**: Linguistics (2 required, 0 electives), Jewish Studies (3 req, 0 elec)
- **Core Issue**: Inflexible curriculum structure

#### Pattern 4: High Required Course Concentration (>50%)
- **Count**: 25 minors (30.9%)
- **Impact**: Limited flexibility in course selection
- **Examples**: Linguistics (100% required), Informatics (75% required)
- **Core Issue**: Rigid curriculum design

### Critical Risk Factors Breakdown

| Risk Factor | Count | % of minors |
|-------------|-------|-------------|
| LOW_PREFIX_DIVERSITY | 52 | 64.2% |
| SINGLE_DEPARTMENT_BOTTLENECK | 41 | 50.6% |
| IMPOSSIBLE_IF_SINGLE_COURSE_DOWN | 31 | 38.3% |
| EXTREME_SINGLE_COURSE_VULNERABILITY | 31 | 38.3% |
| HIGH_REQUIRED_CONCENTRATION | 25 | 30.9% |
| NO_FLEXIBILITY_SAFETY_NET | 14 | 17.3% |

### Department Bottleneck Risk Distribution

| Risk Level | Count | % | Definition |
|-----------|-------|---|---|
| EXTREME | 41 | 50.6% | Single department OR single required course |
| MODERATE | 17 | 21.0% | 2-3 department prefixes in requirements |
| LOW | 23 | 28.4% | 4+ department prefixes in requirements |

### Flexibility Score Analysis

| Flexibility Level | Count | Interpretation |
|------------------|-------|---|
| 0 (No flexibility) | 14 | No electives available; rigid structure |
| <25% (Low) | 3 | Very few alternatives |
| 25-75% (Moderate) | 29 | Some alternatives available |
| >75% (High) | 34 | Good flexibility for substitution |
| 100% (Complete) | 6 | All courses are electives |

---

## Analytical Metrics Explained

### 1. Impossible-if-One-Required Score
**Definition**: Percentage of minor that becomes impossible if ANY ONE required course becomes unavailable

**Formula**:
```
Score = (100 / number_of_required_courses)
```

**Interpretation**:
- 100% = Single required course (loss = entire minor)
- 50% = Two required courses (loss of one = half the minor gone)
- 25% = Four required courses (loss of one = 25% gone)
- 0% = All electives (loss of one course has no impact on completion)

**Risk Thresholds**:
- >25%: EXTREME vulnerability
- 20-25%: HIGH vulnerability
- 10-20%: MODERATE vulnerability
- <10%: LOW vulnerability

### 2. Required Course Concentration
**Definition**: Percentage of total minor courses that are designated as required

**Interpretation**:
- >75%: Nearly all courses mandatory (rigid structure)
- 50-75%: More than half mandatory (limited flexibility)
- 25-50%: Balanced requirement (moderate flexibility)
- <25%: Mostly elective (high flexibility)
- 0%: All electives (maximum flexibility)

**Risk Indicator**: >50% indicates inflexible curriculum

### 3. Department Bottleneck Score
**Definition**: Concentration of required courses within single or few departments

**Risk Categories**:
- **EXTREME**: All required courses from one department
- **HIGH**: Required courses from only 1-2 departments
- **MODERATE**: Required courses from 2-3 departments
- **LOW**: Required courses spread across 4+ departments

**Logic**: Single-department minors vulnerable to departmental changes (scheduling, staffing, budget)

### 4. Required Course Diversity
**Definition**: Number of different department prefixes represented in required courses

**Interpretation**:
- 1 prefix: Complete bottleneck risk
- 2 prefixes: High bottleneck risk
- 3 prefixes: Moderate bottleneck risk
- 4+ prefixes: Low bottleneck risk

**Benefit**: Multiple departments = resilience to single-department changes

### 5. Elective Safety Net
**Definition**: Availability of alternative courses for substitution

**Calculation**:
```
If electives = 0: NO_FLEXIBILITY_SAFETY_NET flag
If electives > 0: Students can substitute courses
```

**Impact**: Even if required course unavailable, students may complete minor via elective substitution

### 6. Flexibility Score (0-100)
**Definition**: Overall measure of student flexibility based on elective availability

**Formula**:
```
Flexibility_Score = MIN(100, (electives / total_courses) * 100)
```

**Interpretation**:
- 0: No flexibility; no alternative course options
- 25-50: Limited flexibility; some alternatives available
- 51-75: Moderate flexibility; reasonable alternatives
- 76-100: High flexibility; many alternatives available

---

## Recommendations by Tier

### Tier A: Critical - Requires Restructuring (36 minors, 44.4%)
**Characteristics**: 3+ critical risk factors, multiple structural vulnerabilities

**Required Actions**:
1. **Restructure Required Courses**
   - Convert non-foundational required courses to electives
   - Identify which requirements are truly essential vs. customary
   - Reduce number of required courses to 4+ minimum

2. **Add Course Alternatives**
   - Create equivalent courses from different departments
   - Enable course substitution for same competencies
   - Partner with other departments for cross-listed courses

3. **Cross-Listing Opportunities**
   - Work with related departments to co-list courses
   - Share courses across related minors
   - Build interdepartmental support

**Timeline**: Implement within 1-2 academic years

### Tier B: High Risk - Requires Attention (22 minors, 27.2%)
**Characteristics**: 2 critical risk factors; some structural concerns

**Required Actions**:
1. **Expand Elective Options**
   - Add 3-5 additional elective courses
   - Enable student choice and substitution
   - Create multiple pathways to completion

2. **Diversify Required Course Prefixes**
   - Ensure required courses span at least 2-3 departments
   - Reduce single-department concentration
   - Build interdisciplinary connections

3. **Create Substitution Paths**
   - Allow alternative courses to satisfy requirements
   - Build flexibility into requirement definitions
   - Document acceptable alternatives

**Timeline**: Implement within 1-2 academic years

### Tier C: Moderate Risk - Monitor (7 minors, 8.6%)
**Characteristics**: 1 critical risk factor; mostly structural

**Required Actions**:
1. **Ensure Course Stability**
   - Verify required courses offered every academic year
   - Confirm instructor availability
   - Plan for enrollment increases

2. **Build Backup Resources**
   - Develop alternative learning materials
   - Create online course options where possible
   - Establish substitute instructor pool

3. **Plan Department Communication**
   - Establish regular updates between departments
   - Coordinate scheduling across departments
   - Create contingency plans for course cancellation

**Timeline**: Monitor annually; implement as needed

---

## Phase 4 Integration Framework

### Objectives
Phase 4 will overlay Phase 3 structural analysis with actual operational data to identify which minors are ACTUALLY impossible to complete (not just theoretically vulnerable).

### Data Points to Collect

#### 1. Course Availability & Scheduling
- Historical course offering frequency (per academic year, per semester)
- Planned course cancellations or retirements
- Instructor availability and course load distributions
- Enrollment cap constraints
- Prerequisites and co-requisites

#### 2. Student Enrollment Patterns
- Grade distributions for each required course (A-F breakdown)
- Historical course enrollment by semester
- Pass rates by course (especially required courses)
- Prerequisite satisfaction rates

#### 3. Grade Spread Analysis
- Percentage of students unable to satisfy prerequisites
- Correlation between required course difficulty and minor completion
- Impact of grade requirements on forward progression
- Repeat rates for challenging courses

#### 4. Temporal Dynamics
- When required courses are offered (Spring vs. Fall patterns)
- Multi-year scheduling conflicts with other minors/majors
- Semester-to-semester course availability variance
- Coordination of required courses within minor

### Phase 4 Analysis Questions

1. **How many minors become ACTUALLY IMPOSSIBLE when combined with:**
   - Grade prerequisites (e.g., Grade <C = no credit)
   - Actual course availability in recent years
   - Enrollment caps that exclude students

2. **What is the TRUE STUDENT COMPLETION RATE for each minor?**
   - How many students start vs. finish each minor
   - Where do students drop out (after which course)
   - How completion rates correlate with Phase 3 vulnerability scores

3. **Which minors are at GREATEST RISK OF DE FACTO ELIMINATION?**
   - Minors with completion rates <20% despite being technically possible
   - Minors with only 1-2 completions per year
   - Minors trending toward zero enrollments

### Integration Methodology

#### Step 1: Overlay Phase 3 with Phase 4 Data
- **High structural risk + Low actual availability** = CRISIS
- **Low structural risk + High actual availability** = VIABLE
- Create risk matrix: Structural Risk vs. Actual Risk
- Identify minors where theory doesn't match reality

#### Step 2: Recalculate Impossible-if-One-Required with Real Data
- Use actual course offering frequency from 5-year historical data
- Weight vulnerability score by probability of course unavailability
- Adjust scores for actual pass rates and grade requirements
- Factor in enrollment caps and prerequisites

#### Step 3: Identify Recovery Paths
- For impossible minors, identify recovery options:
  - Which courses could be made available online
  - Which electives could substitute for required courses
  - Which courses could be co-listed with other departments
  - Which courses need instructor training/development

#### Step 4: Prioritize for Implementation
- Rank minors by actual vs. structural risk gap
- Identify quick wins (easy fixes with high impact)
- Plan phased implementation across 2-3 years
- Build departmental change management plan

### Phase 4 Deliverables

1. **09_Phase_4_Actual_Risk_Assessment.csv**
   - All 81 minors with Phase 3 + Phase 4 metrics combined
   - Recalculated vulnerability scores based on real data
   - Actual completion rate data
   - True vs. theoretical risk comparison

2. **09_Phase_4_Recovery_Pathways.csv**
   - Specific recovery recommendations per minor
   - Course alternatives and cross-listing options
   - Online/hybrid course opportunities
   - Interdepartmental collaboration options

3. **09_Phase_4_Report.md**
   - Detailed analysis integrating structure + operations
   - Prioritized action list (by department)
   - Implementation roadmap (12-36 month timeline)
   - Success metrics and monitoring framework

---

## Methodological Notes

### Data Sources
- **01_USC_Minors_Master_Analysis.csv**: Course structure (required/elective breakdown)
- **06_Severity_Ranking.csv**: Severity scores and TIER classifications

### Analysis Approach
1. Parse master analysis data for each TIER 1 CRITICAL minor
2. Calculate 6 distinct vulnerability metrics
3. Identify critical risk factors based on thresholds
4. Generate tiered recommendations based on risk profile
5. Sort by Impossible-if-One-Required Score for prioritization

### Limitations in Phase 3
- **Structural analysis only**: Based on curriculum design, not actual operations
- **Inferred required courses**: Required courses inferred from overall prefix lists (not granular course-level data)
- **No availability data**: Doesn't consider actual course offering frequency
- **No student data**: No integration of grade distributions or pass rates
- **No temporal analysis**: Doesn't account for semester-to-semester variations

### Strengths in Phase 3
- **Objective framework**: Systematic, reproducible methodology
- **Actionable metrics**: Each metric targets specific vulnerability
- **Tiered recommendations**: Prioritized by urgency and impact
- **Clear identification**: Specific risk factors clearly identified
- **Comprehensive coverage**: All 81 TIER 1 minors analyzed uniformly

---

## Success Metrics for Implementation

### Short-term (1 year)
- 100% of Tier A minors have implementation plan drafted
- 50% of Tier A minors have begun restructuring
- All departments aware of vulnerability findings

### Medium-term (2 years)
- 75% of Tier A minors restructured
- 100% of Tier B minors have implementation plan
- 25% of Tier B minors implemented
- Phase 4 analysis complete with recovery pathways

### Long-term (3 years)
- 100% of Tier A minors restructured and stabilized
- 75% of Tier B minors implemented and monitored
- Minimum 4 required courses in all TIER 1 minors
- Minimum 50% elective flexibility in all TIER 1 minors
- No minors with 0 electives

---

## Conclusion

Phase 3 structural analysis identifies critical vulnerabilities in 81 TIER 1 CRITICAL minors:

- **38.3% at extreme risk** of becoming impossible if single required course unavailable
- **58.0% concentrated** in single departments, vulnerable to institutional changes
- **17.3% with no flexibility** to substitute courses if required course unavailable
- **30.9% with rigid structure** (>50% required courses)

**Immediate Actions Required**:
1. Share findings with all department heads
2. Convene curriculum committees for Tier A minors
3. Begin Phase 4 data collection
4. Draft implementation timeline for Tier A restructuring
5. Establish interdepartmental coordination mechanisms

The analysis provides actionable insights for making USC minors more viable, flexible, and resilient to operational constraints.

---

**Report Generated**: February 12, 2026
**Analysis Tool**: phase_3_analysis.py
**Output Files**:
- 09_Phase_3_Structural_Vulnerability.csv
- 09_Phase_3_Report.md
