#!/usr/bin/env python3
"""
Phase 3: Structural Vulnerability Analysis for TIER 1 CRITICAL Minors
Analyzes 81 TIER 1 CRITICAL minors for structural weaknesses and impossible-to-complete scenarios.
"""

import csv
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple
from dataclasses import dataclass, field

@dataclass
class MinorAnalysis:
    """Data class for minor analysis results."""
    minor_name: str
    category: str
    total_courses: int
    required_courses: int
    elective_courses: int
    unique_prefixes: int
    prefix_list: str
    required_prefixes: List[str] = field(default_factory=list)
    required_prefix_str: str = ""
    severity_score: float = 0.0
    risk_tier: str = ""

    # Calculated metrics
    impossible_if_one_required: float = 0.0
    required_course_percentage: float = 0.0
    single_department: bool = False
    required_prefix_count: int = 0
    flexibility_score: float = 0.0
    critical_risk_factors: List[str] = field(default_factory=list)
    recommendation: str = ""


def read_master_analysis(filepath: str) -> pd.DataFrame:
    """Read the master analysis CSV."""
    df = pd.read_csv(filepath)
    return df


def read_severity_ranking(filepath: str) -> pd.DataFrame:
    """Read the severity ranking CSV."""
    df = pd.read_csv(filepath)
    return df


def extract_required_prefixes(minor_row: pd.Series) -> Tuple[List[str], str]:
    """
    Extract required course prefixes from the minor data.
    This is a simplified approach - we'll infer from the data available.
    """
    # For now, we'll use the overall prefix list and try to infer
    # In reality, we'd need more granular data on which courses are required
    prefix_list = str(minor_row.get('Prefix List', ''))

    if not prefix_list or prefix_list == 'nan':
        return [], ""

    prefixes = [p.strip() for p in prefix_list.split(',')]
    return prefixes, prefix_list


def calculate_impossible_if_one_required(num_required: int) -> float:
    """
    Calculate the % of minor that becomes impossible if any one required course is unavailable.
    Score = 100 / num_required_courses
    High scores (>33%) indicate extreme vulnerability.
    """
    if num_required == 0:
        return 0.0
    return (100.0 / num_required) if num_required > 0 else 0.0


def calculate_required_percentage(required: int, total: int) -> float:
    """Calculate what percentage of total courses are required."""
    if total == 0:
        return 0.0
    return (required / total) * 100.0


def check_single_department(prefixes: List[str]) -> bool:
    """Check if all required courses are from a single department."""
    return len(set(prefixes)) == 1 if prefixes else False


def calculate_flexibility_score(required: int, elective: int, total: int) -> float:
    """
    Calculate flexibility score (0-100).
    Based on available electives and their ratio to required courses.
    0 = no flexibility, 100 = high flexibility.
    """
    if elective == 0:
        return 0.0
    if required == 0:
        return 100.0

    # Flexibility = (electives / total) * 100, capped at 100
    flexibility = min(100.0, (elective / total) * 100.0)
    return flexibility


def identify_critical_risk_factors(analysis: MinorAnalysis) -> List[str]:
    """Identify critical risk factors for the minor."""
    factors = []

    # IMPOSSIBLE_IF_SINGLE_COURSE_DOWN: 1-3 required courses
    if 1 <= analysis.required_courses <= 3:
        factors.append("IMPOSSIBLE_IF_SINGLE_COURSE_DOWN")

    # High required course concentration (>50%)
    if analysis.required_course_percentage > 50:
        factors.append("HIGH_REQUIRED_CONCENTRATION")

    # Single department bottleneck
    if analysis.single_department and analysis.required_courses > 0:
        factors.append("SINGLE_DEPARTMENT_BOTTLENECK")

    # No electives for flexibility
    if analysis.elective_courses == 0:
        factors.append("NO_FLEXIBILITY_SAFETY_NET")

    # Low prefix diversity in required courses (all from 1-2 prefixes)
    if analysis.required_prefix_count <= 2 and analysis.required_courses > 0:
        factors.append("LOW_PREFIX_DIVERSITY")

    # Very high impossible-if-one score (>25%)
    if analysis.impossible_if_one_required > 25:
        factors.append("EXTREME_SINGLE_COURSE_VULNERABILITY")

    return factors


def generate_recommendation(analysis: MinorAnalysis) -> str:
    """Generate a recommendation based on risk analysis."""
    if not analysis.critical_risk_factors:
        return "Review and monitor"

    factor_count = len(analysis.critical_risk_factors)

    if factor_count >= 4:
        return "Requires immediate restructuring - multiple critical vulnerabilities"
    elif "IMPOSSIBLE_IF_SINGLE_COURSE_DOWN" in analysis.critical_risk_factors:
        return "Critical: Add required courses or restructure as electives"
    elif "SINGLE_DEPARTMENT_BOTTLENECK" in analysis.critical_risk_factors:
        return "Urgent: Diversify departments or add alternative courses"
    elif "NO_FLEXIBILITY_SAFETY_NET" in analysis.critical_risk_factors:
        return "Add elective courses to provide flexibility"
    elif "EXTREME_SINGLE_COURSE_VULNERABILITY" in analysis.critical_risk_factors:
        return "Reduce number of required courses or add alternatives"
    else:
        return "Monitor and address identified risk factors"


def analyze_tier1_minors(master_df: pd.DataFrame, severity_df: pd.DataFrame) -> List[MinorAnalysis]:
    """Analyze all TIER 1 CRITICAL minors."""
    analyses = []

    # Get tier 1 critical minors from severity ranking
    tier1_df = severity_df[severity_df['Risk Tier'].str.contains('TIER 1', na=False)]

    for _, severity_row in tier1_df.iterrows():
        minor_name = severity_row['Minor Name']

        # Find matching row in master analysis
        master_rows = master_df[master_df['Minor Name'] == minor_name]

        if master_rows.empty:
            print(f"Warning: {minor_name} not found in master analysis")
            continue

        master_row = master_rows.iloc[0]

        # Create analysis object
        analysis = MinorAnalysis(
            minor_name=minor_name,
            category=master_row.get('Category', ''),
            total_courses=int(master_row.get('Total Courses', 0)),
            required_courses=int(master_row.get('Required', 0)),
            elective_courses=int(master_row.get('Elective', 0)),
            unique_prefixes=int(master_row.get('Unique Prefixes', 0)),
            prefix_list=str(master_row.get('Prefix List', '')),
            severity_score=float(severity_row.get('Severity Score', 0)),
            risk_tier=severity_row.get('Risk Tier', ''),
        )

        # Extract required prefixes (using all prefixes as approximation)
        required_prefixes, prefix_str = extract_required_prefixes(master_row)
        analysis.required_prefixes = required_prefixes
        analysis.required_prefix_str = prefix_str
        analysis.required_prefix_count = len(set(required_prefixes))

        # Calculate metrics
        analysis.impossible_if_one_required = calculate_impossible_if_one_required(
            analysis.required_courses
        )
        analysis.required_course_percentage = calculate_required_percentage(
            analysis.required_courses,
            analysis.total_courses
        )
        analysis.single_department = check_single_department(required_prefixes)
        analysis.flexibility_score = calculate_flexibility_score(
            analysis.required_courses,
            analysis.elective_courses,
            analysis.total_courses
        )

        # Identify risk factors and recommendation
        analysis.critical_risk_factors = identify_critical_risk_factors(analysis)
        analysis.recommendation = generate_recommendation(analysis)

        analyses.append(analysis)

    # Sort by impossible_if_one_required score (descending)
    analyses.sort(key=lambda x: x.impossible_if_one_required, reverse=True)

    return analyses


def write_output_csv(analyses: List[MinorAnalysis], output_path: str) -> None:
    """Write analysis results to CSV."""
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Write header
        writer.writerow([
            'Minor Name',
            'Total Required Courses',
            'Required Course Prefixes',
            'Prefixes in Required Courses',
            'Single Department?',
            'Impossible-if-One-Required Score',
            'Required Course % of Total',
            'Department Bottleneck Risk',
            'Flexibility Score (0-100)',
            'Critical Risk Factors',
            'Recommendation'
        ])

        # Write data rows
        for analysis in analyses:
            # Determine bottleneck risk label
            if analysis.single_department and analysis.required_courses > 0:
                bottleneck_risk = "EXTREME"
            elif analysis.required_prefix_count == 1 and analysis.required_courses > 0:
                bottleneck_risk = "HIGH"
            elif analysis.required_prefix_count <= 2:
                bottleneck_risk = "MODERATE"
            else:
                bottleneck_risk = "LOW"

            writer.writerow([
                analysis.minor_name,
                analysis.required_courses,
                analysis.required_prefix_str,
                analysis.required_prefix_count,
                'Yes' if analysis.single_department else 'No',
                f"{analysis.impossible_if_one_required:.2f}%",
                f"{analysis.required_course_percentage:.2f}%",
                bottleneck_risk,
                f"{analysis.flexibility_score:.2f}",
                '; '.join(analysis.critical_risk_factors) if analysis.critical_risk_factors else 'None',
                analysis.recommendation
            ])


def generate_markdown_report(analyses: List[MinorAnalysis], output_path: str) -> None:
    """Generate a comprehensive markdown report."""

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# Phase 3: Structural Vulnerability Analysis Report\n\n")
        f.write("## Executive Summary\n\n")
        f.write(f"Analysis Date: February 12, 2026\n")
        f.write(f"Total TIER 1 CRITICAL Minors Analyzed: {len(analyses)}\n\n")

        # Critical statistics
        impossible_count = sum(1 for a in analyses if any(
            factor in a.critical_risk_factors
            for factor in ['IMPOSSIBLE_IF_SINGLE_COURSE_DOWN', 'EXTREME_SINGLE_COURSE_VULNERABILITY']
        ))
        no_flexibility = sum(1 for a in analyses if 'NO_FLEXIBILITY_SAFETY_NET' in a.critical_risk_factors)
        single_dept = sum(1 for a in analyses if a.single_department)

        f.write(f"- **Minors at Extreme Risk of Becoming Impossible**: {impossible_count} ({100*impossible_count/len(analyses):.1f}%)\n")
        f.write(f"- **Minors with No Flexibility Safety Net**: {no_flexibility} ({100*no_flexibility/len(analyses):.1f}%)\n")
        f.write(f"- **Single-Department Minors**: {single_dept} ({100*single_dept/len(analyses):.1f}%)\n\n")

        # Top 15 at highest risk
        f.write("## Top 15 Minors at Highest Structural Risk\n\n")
        f.write("Ranked by Impossible-if-One-Required Score (% of minor lost if single course unavailable):\n\n")

        for i, analysis in enumerate(analyses[:15], 1):
            f.write(f"### {i}. {analysis.minor_name}\n\n")
            f.write(f"- **Impossible-if-One-Required Score**: {analysis.impossible_if_one_required:.2f}%\n")
            f.write(f"- **Required Courses**: {analysis.required_courses}/{analysis.total_courses} ({analysis.required_course_percentage:.1f}%)\n")
            f.write(f"- **Department Coverage**: {analysis.required_prefix_count} prefix(es): {analysis.required_prefix_str}\n")
            f.write(f"- **Single Department**: {'Yes' if analysis.single_department else 'No'}\n")
            f.write(f"- **Flexibility Score**: {analysis.flexibility_score:.1f}/100\n")
            f.write(f"- **Critical Risk Factors**: {'; '.join(analysis.critical_risk_factors) if analysis.critical_risk_factors else 'None'}\n")
            f.write(f"- **Recommendation**: {analysis.recommendation}\n\n")

        # Pattern analysis
        f.write("## Pattern Analysis: Why These Minors Are Impossible to Complete\n\n")

        f.write("### Pattern 1: Minimal Required Courses (1-3 courses)\n")
        minimal_required = [a for a in analyses if 1 <= a.required_courses <= 3]
        f.write(f"Count: {len(minimal_required)}\n")
        if minimal_required:
            f.write("Impact: A single course becoming unavailable makes the entire minor impossible.\n")
            f.write("Examples:\n")
            for analysis in minimal_required[:5]:
                f.write(f"  - {analysis.minor_name}: {analysis.required_courses} required, {analysis.impossible_if_one_required:.1f}% loss per course\n")
        f.write("\n")

        f.write("### Pattern 2: Single-Department Minors\n")
        single_dept_analyses = [a for a in analyses if a.single_department]
        f.write(f"Count: {len(single_dept_analyses)}\n")
        if single_dept_analyses:
            f.write("Impact: Department scheduling or staffing changes directly threaten minor viability.\n")
            f.write("Examples:\n")
            for analysis in single_dept_analyses[:5]:
                f.write(f"  - {analysis.minor_name}: {analysis.required_prefix_str} (Dept={analysis.required_prefix_str})\n")
        f.write("\n")

        f.write("### Pattern 3: No Flexibility or Safety Net\n")
        no_flex = [a for a in analyses if a.flexibility_score == 0 or a.elective_courses == 0]
        f.write(f"Count: {len(no_flex)}\n")
        if no_flex:
            f.write("Impact: Students have no alternative courses if required courses are unavailable.\n")
            f.write("Examples:\n")
            for analysis in no_flex[:5]:
                f.write(f"  - {analysis.minor_name}: {analysis.elective_courses} electives, {analysis.required_courses} required\n")
        f.write("\n")

        f.write("### Pattern 4: High Required Course Concentration (>50% required)\n")
        high_req = [a for a in analyses if a.required_course_percentage > 50]
        f.write(f"Count: {len(high_req)}\n")
        if high_req:
            f.write("Impact: Limited flexibility in course selection; curriculum is rigidly structured.\n")
            f.write("Examples:\n")
            for analysis in high_req[:5]:
                f.write(f"  - {analysis.minor_name}: {analysis.required_course_percentage:.1f}% required ({analysis.required_courses}/{analysis.total_courses})\n")
        f.write("\n")

        # Recommendations for departments
        f.write("## Recommendations for Immediate Department Review\n\n")

        f.write("### Tier A: Critical - Requires Restructuring\n")
        tier_a = [a for a in analyses if len(a.critical_risk_factors) >= 3]
        f.write(f"Count: {len(tier_a)} minors\n\n")
        f.write("Actions:\n")
        f.write("1. **Restructure Required Courses**: Convert non-foundational required courses to electives\n")
        f.write("2. **Add Course Alternatives**: Create equivalent courses from different departments\n")
        f.write("3. **Cross-Listing Opportunities**: Collaborate with other departments for co-listed courses\n\n")

        f.write("### Tier B: High Risk - Requires Attention\n")
        tier_b = [a for a in analyses if len(a.critical_risk_factors) == 2]
        f.write(f"Count: {len(tier_b)} minors\n\n")
        f.write("Actions:\n")
        f.write("1. **Expand Elective Options**: Increase number of elective courses\n")
        f.write("2. **Diversify Required Course Prefixes**: Add courses from other departments\n")
        f.write("3. **Create Substitution Paths**: Allow alternative courses to satisfy requirements\n\n")

        f.write("### Tier C: Moderate Risk - Monitor\n")
        tier_c = [a for a in analyses if len(a.critical_risk_factors) == 1]
        f.write(f"Count: {len(tier_c)} minors\n\n")
        f.write("Actions:\n")
        f.write("1. **Ensure Course Stability**: Verify required courses are offered regularly\n")
        f.write("2. **Build Backup Resources**: Develop alternative learning materials\n")
        f.write("3. **Plan Department Communication**: Establish regular updates between departments\n\n")

        # Framework for Phase 4
        f.write("## Framework for Phase 4: Integrating Grade Spread & Enrollment Data\n\n")

        f.write("### Data Points to Collect in Phase 4\n\n")
        f.write("1. **Course Availability & Scheduling**\n")
        f.write("   - Historical course offering frequency (per academic year, per semester)\n")
        f.write("   - Instructor availability and course load distributions\n")
        f.write("   - Planned course cancellations or retirements\n\n")

        f.write("2. **Student Enrollment Patterns**\n")
        f.write("   - Grade distributions for each required course (A-F breakdown)\n")
        f.write("   - Historical course enrollment caps and actual enrollment\n")
        f.write("   - Pass rates and prerequisite satisfaction rates\n\n")

        f.write("3. **Grade Spread Analysis**\n")
        f.write("   - Percentage of students unable to satisfy prerequisites (Grade <C)\n")
        f.write("   - Correlation between required course difficulty and minor completion rates\n")
        f.write("   - Impact of grade requirements on forward progression\n\n")

        f.write("4. **Temporal Dynamics**\n")
        f.write("   - When required courses are offered (Spring vs. Fall bias)\n")
        f.write("   - Multi-year scheduling conflicts with other minors or majors\n")
        f.write("   - Semester-to-semester course availability variance\n\n")

        f.write("### Phase 4 Analysis Questions\n\n")
        f.write("1. Of the 81 TIER 1 minors, how many become **actually impossible** when combined with:\n")
        f.write("   - Grade prerequisites (e.g., Grade <C = no credit)\n")
        f.write("   - Actual course availability in recent years\n")
        f.write("   - Enrollment caps that exclude students\n\n")

        f.write("2. What is the **true student completion rate** for each minor?\n")
        f.write("   - How many students start vs. finish each minor\n")
        f.write("   - Where do students drop out (after which course)\n")
        f.write("   - How do completion rates correlate with our Phase 3 vulnerability scores\n\n")

        f.write("3. Which minors are at **greatest risk of de facto elimination**?\n")
        f.write("   - Even if technically possible, completion rates <20% indicate real problems\n")
        f.write("   - Recommend these for immediate curricular redesign\n\n")

        f.write("### Integration Methodology\n\n")
        f.write("1. **Overlay Phase 3 Vulnerability with Phase 4 Data**\n")
        f.write("   - High structural risk (Phase 3) + Low actual availability (Phase 4) = CRISIS\n")
        f.write("   - Create risk matrix: Structural Risk vs. Actual Risk\n\n")

        f.write("2. **Recalculate Impossible-if-One-Required with Real Data**\n")
        f.write("   - Use actual course offering frequency from 5-year historical data\n")
        f.write("   - Weight by probability of course not being available\n")
        f.write("   - Adjust scores for actual pass rates and grade requirements\n\n")

        f.write("3. **Identify Recovery Paths**\n")
        f.write("   - For impossible minors, identify which courses could be made available online\n")
        f.write("   - Which electives could substitute for required courses\n")
        f.write("   - Which courses could be co-listed with other departments\n\n")

        f.write("### Deliverables for Phase 4\n\n")
        f.write("1. **09_Phase_4_Actual_Risk_Assessment.csv** - Structural risk integrated with real data\n")
        f.write("2. **09_Phase_4_Recovery_Pathways.csv** - Specific recommendations to make minors viable\n")
        f.write("3. **09_Phase_4_Report.md** - Detailed analysis with priorities for implementation\n\n")


def main():
    """Main execution function."""
    base_path = Path("/Volumes/MacShare/graduate-coursework/Daily_Gamecock/Archive_writing/DailyGamecock_JVAUGHT_examples/Current_writing/Minors_courses/00_MASTER_ANALYSIS")

    # File paths
    master_analysis_file = base_path / "01_USC_Minors_Master_Analysis.csv"
    severity_ranking_file = base_path / "06_Severity_Ranking.csv"
    output_csv = base_path / "09_Phase_3_Structural_Vulnerability.csv"
    output_md = base_path / "09_Phase_3_Report.md"

    print("Phase 3: Structural Vulnerability Analysis")
    print("=" * 60)

    # Read data
    print(f"\nReading master analysis from: {master_analysis_file}")
    master_df = read_master_analysis(str(master_analysis_file))
    print(f"  Loaded {len(master_df)} minors")

    print(f"\nReading severity ranking from: {severity_ranking_file}")
    severity_df = read_severity_ranking(str(severity_ranking_file))
    print(f"  Loaded {len(severity_df)} severity records")

    # Perform analysis
    print("\nAnalyzing TIER 1 CRITICAL minors...")
    analyses = analyze_tier1_minors(master_df, severity_df)
    print(f"  Analyzed {len(analyses)} TIER 1 CRITICAL minors")

    # Write outputs
    print(f"\nWriting CSV output to: {output_csv}")
    write_output_csv(analyses, str(output_csv))
    print(f"  CSV written successfully")

    print(f"\nGenerating markdown report: {output_md}")
    generate_markdown_report(analyses, str(output_md))
    print(f"  Report generated successfully")

    # Summary statistics
    print("\n" + "=" * 60)
    print("ANALYSIS SUMMARY")
    print("=" * 60)

    impossible_count = sum(1 for a in analyses if any(
        factor in a.critical_risk_factors
        for factor in ['IMPOSSIBLE_IF_SINGLE_COURSE_DOWN', 'EXTREME_SINGLE_COURSE_VULNERABILITY']
    ))

    avg_impossible_score = sum(a.impossible_if_one_required for a in analyses) / len(analyses)
    max_impossible_score = max(a.impossible_if_one_required for a in analyses)
    min_impossible_score = min(a.impossible_if_one_required for a in analyses)

    print(f"\nMinors with Extreme Impossible-if-One Vulnerability: {impossible_count}")
    print(f"Average Impossible-if-One Score: {avg_impossible_score:.2f}%")
    print(f"Range: {min_impossible_score:.2f}% to {max_impossible_score:.2f}%")

    print(f"\nTop 5 Most Vulnerable:")
    for i, analysis in enumerate(analyses[:5], 1):
        print(f"  {i}. {analysis.minor_name}: {analysis.impossible_if_one_required:.2f}%")

    print("\nPhase 3 analysis complete!")


if __name__ == "__main__":
    main()
