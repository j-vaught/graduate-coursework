#!/usr/bin/env python3
"""
Phase 3: Minors Analysis - Course Offerings Cross-Reference
Analyzes required vs. actual course offerings from grade spread data.

Author: J.C. Vaught
"""

import os
import sys
import pandas as pd
import numpy as np
from pathlib import Path
from collections import defaultdict
import logging
from typing import Dict, List, Tuple, Set

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CourseOfferingAnalyzer:
    """Analyzes course requirements vs. actual offerings."""

    def __init__(self, master_analysis_path: str, grade_spreads_dir: str):
        """Initialize analyzer with master analysis and grade spreads data."""
        self.master_analysis_path = master_analysis_path
        self.grade_spreads_dir = grade_spreads_dir

        # Data structures
        self.master_df = None
        self.severity_df = None
        self.course_offerings = {}  # course_code -> list of semesters
        self.total_semesters = 0

    def load_master_analysis(self) -> bool:
        """Load master minors analysis CSV."""
        try:
            self.master_df = pd.read_csv(self.master_analysis_path)
            logger.info(f"Loaded master analysis: {len(self.master_df)} minors")
            return True
        except Exception as e:
            logger.error(f"Failed to load master analysis: {e}")
            return False

    def load_severity_ranking(self, severity_path: str) -> bool:
        """Load severity ranking CSV."""
        try:
            self.severity_df = pd.read_csv(severity_path)
            logger.info(f"Loaded severity ranking: {len(self.severity_df)} entries")
            return True
        except Exception as e:
            logger.error(f"Failed to load severity ranking: {e}")
            return False

    def parse_course_codes_from_prefix_list(self, row: pd.Series) -> List[str]:
        """
        Extract course codes from a minor row.
        Handles 'Prefix List' column which contains course prefixes.
        Real course codes should come from additional data or requirement details.
        """
        course_codes = []

        # This is a placeholder - in real implementation, would need to either:
        # 1. Have a detailed requirements file with actual course codes
        # 2. Parse the prefix list and common courses
        # 3. Cross-reference with institutional course catalog

        return course_codes

    def read_excel_file(self, file_path: str) -> Tuple[str, List[str]]:
        """
        Read Excel file and extract course codes and semester.

        Returns:
            Tuple of (semester, list of course codes)
        """
        semester = None
        course_codes = []

        try:
            # Extract semester from filename (e.g., 202008 -> 2020-08)
            filename = Path(file_path).stem
            if len(filename) >= 6 and filename[:6].isdigit():
                semester = filename[:6]
            else:
                logger.warning(f"Could not extract semester from {filename}")
                return None, []

            # Try multiple approaches to read the file
            dfs = None

            try:
                # Try with openpyxl
                dfs = pd.read_excel(file_path, sheet_name=None, engine='openpyxl')
            except Exception:
                try:
                    # Try with xlrd
                    dfs = pd.read_excel(file_path, sheet_name=None, engine='xlrd')
                except Exception:
                    try:
                        # Try with pandas default
                        dfs = pd.read_excel(file_path, sheet_name=None)
                    except Exception as e:
                        logger.warning(f"Could not read {file_path}: {e}")
                        return semester, []

            if not dfs:
                return semester, []

            # Process each sheet
            for sheet_name, df in dfs.items():
                if df is None or df.empty:
                    continue

                # Look for course code columns
                course_codes.extend(self._extract_courses_from_dataframe(df))

            return semester, list(set(course_codes))  # Remove duplicates

        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            return semester, []

    def _extract_courses_from_dataframe(self, df: pd.DataFrame) -> List[str]:
        """Extract course codes from a dataframe."""
        courses = []

        # Look for patterns like "SUBJECT CODE" or common column names
        potential_columns = []

        for col in df.columns:
            col_lower = str(col).lower()
            if any(x in col_lower for x in ['course', 'code', 'subj', 'subject', 'crs']):
                potential_columns.append(col)

        # If no specific columns found, try first few columns
        if not potential_columns:
            potential_columns = df.columns[:3].tolist()

        for col in potential_columns:
            for value in df[col]:
                if pd.isna(value):
                    continue

                value_str = str(value).strip().upper()

                # Match pattern: XXXX NNNN (e.g., BIOL 1010)
                if ' ' in value_str:
                    parts = value_str.split()
                    if len(parts) >= 2 and parts[0].isalpha() and parts[1].isdigit():
                        course_code = f"{parts[0]} {parts[1]}"
                        if course_code not in courses:
                            courses.append(course_code)

                # Match pattern: XXXXNNNN (e.g., BIOL1010)
                elif len(value_str) >= 5:
                    # Find where letters end and numbers begin
                    split_idx = 0
                    for i, c in enumerate(value_str):
                        if not c.isalpha():
                            split_idx = i
                            break

                    if split_idx > 0 and value_str[split_idx:].isdigit():
                        prefix = value_str[:split_idx]
                        code = value_str[split_idx:]
                        if len(prefix) <= 4 and len(code) >= 3:
                            course_code = f"{prefix} {code}"
                            if course_code not in courses:
                                courses.append(course_code)

        return courses

    def process_grade_spreads(self) -> bool:
        """Process all Excel files in grade spreads directory."""
        try:
            excel_files = list(Path(self.grade_spreads_dir).glob("*.xlsx"))

            if not excel_files:
                logger.warning(f"No Excel files found in {self.grade_spreads_dir}")
                return False

            logger.info(f"Processing {len(excel_files)} Excel files")

            semesters_seen = set()

            for file_path in sorted(excel_files):
                semester, courses = self.read_excel_file(str(file_path))

                if not semester:
                    continue

                semesters_seen.add(semester)

                for course in courses:
                    if course not in self.course_offerings:
                        self.course_offerings[course] = []
                    if semester not in self.course_offerings[course]:
                        self.course_offerings[course].append(semester)

                logger.info(f"  {semester}: {len(courses)} courses")

            self.total_semesters = len(semesters_seen)
            logger.info(f"Total semesters found: {self.total_semesters}")

            return True

        except Exception as e:
            logger.error(f"Error processing grade spreads: {e}")
            return False

    def classify_courses(self, required_courses: List[str]) -> Dict:
        """
        Classify required courses as Ghost, Zombie, or Normal.

        Ghost: Never offered (0% offering rate)
        Zombie: Offered in < 30% of semesters
        """
        result = {
            'ghost_courses': [],
            'zombie_courses': [],
            'offering_rates': {},
            'offering_stats': {}
        }

        if self.total_semesters == 0:
            logger.warning("No semesters data available")
            return result

        for course in required_courses:
            if course not in self.course_offerings:
                # Ghost course - never offered
                result['ghost_courses'].append(course)
                result['offering_rates'][course] = 0.0
            else:
                semesters_offered = len(self.course_offerings[course])
                offering_rate = (semesters_offered / self.total_semesters) * 100
                result['offering_rates'][course] = offering_rate

                if offering_rate < 30:
                    result['zombie_courses'].append((course, offering_rate))

        # Calculate stats
        if result['offering_rates']:
            rates = list(result['offering_rates'].values())
            result['offering_stats'] = {
                'min': min(rates),
                'max': max(rates),
                'avg': np.mean(rates)
            }

        return result

    def analyze_minors(self) -> pd.DataFrame:
        """Analyze all minors and generate results."""
        results = []

        for idx, row in self.master_df.iterrows():
            minor_name = row['Minor Name']
            category = row['Category']
            total_required = int(row['Required'])

            # Extract required course codes
            # Note: This requires actual course code data
            required_courses = self._extract_required_courses_for_minor(row)

            if not required_courses:
                logger.warning(f"No required courses found for {minor_name}")
                continue

            # Classify courses
            classification = self.classify_courses(required_courses)

            ghost_count = len(classification['ghost_courses'])
            zombie_count = len(classification['zombie_courses'])

            offering_stats = classification['offering_stats']
            min_rate = offering_stats.get('min', 0)
            max_rate = offering_stats.get('max', 0)
            avg_rate = offering_stats.get('avg', 0)

            # Determine if completable
            is_completable = "Yes" if (ghost_count == 0 and zombie_count == 0) else "No"

            # Impossible if all required courses are ghost/zombie
            impossible = "Yes" if (ghost_count + zombie_count >= len(required_courses)) else "No"

            # Determine risk level
            if impossible == "Yes":
                risk_level = "CRITICAL"
            elif ghost_count + zombie_count > len(required_courses) * 0.5:
                risk_level = "CRITICAL"
            elif ghost_count + zombie_count > 0:
                risk_level = "HIGH"
            elif avg_rate < 50:
                risk_level = "MODERATE"
            else:
                risk_level = "LOW"

            results.append({
                'Minor Name': minor_name,
                'Category': category,
                'Total Required Courses': len(required_courses),
                'Ghost Courses (count)': ghost_count,
                'Ghost Course List': '; '.join(classification['ghost_courses']),
                'Zombie Courses (count)': zombie_count,
                'Zombie Course List': '; '.join([c[0] for c in classification['zombie_courses']]),
                'Min Offering Rate Among Required (%)': round(min_rate, 1),
                'Max Offering Rate Among Required (%)': round(max_rate, 1),
                'Avg Offering Rate Among Required (%)': round(avg_rate, 1),
                'Impossible to Complete': impossible,
                'Risk Level': risk_level
            })

        return pd.DataFrame(results)

    def _extract_required_courses_for_minor(self, row: pd.Series) -> List[str]:
        """
        Extract required course codes for a minor.
        This is a placeholder - requires detailed course data.
        """
        # In production, this would:
        # 1. Look up minor in a detailed requirements database
        # 2. Parse the 'Prefix List' and match with actual courses
        # 3. Handle special cases where all courses are from one prefix

        return []

    def generate_ghost_zombie_report(self, analysis_df: pd.DataFrame) -> pd.DataFrame:
        """Generate detailed ghost and zombie course report."""
        records = []

        # Collect all ghost/zombie courses with their minors
        course_minors = defaultdict(lambda: {'type': set(), 'minors': []})

        for idx, row in analysis_df.iterrows():
            minor_name = row['Minor Name']

            # Process ghost courses
            if pd.notna(row['Ghost Course List']) and row['Ghost Course List']:
                for course in str(row['Ghost Course List']).split('; '):
                    if course.strip():
                        course_minors[course.strip()]['type'].add('Ghost')
                        if minor_name not in course_minors[course.strip()]['minors']:
                            course_minors[course.strip()]['minors'].append(minor_name)

            # Process zombie courses
            if pd.notna(row['Zombie Course List']) and row['Zombie Course List']:
                for course in str(row['Zombie Course List']).split('; '):
                    if course.strip():
                        course_minors[course.strip()]['type'].add('Zombie')
                        if minor_name not in course_minors[course.strip()]['minors']:
                            course_minors[course.strip()]['minors'].append(minor_name)

        # Build report
        for course, data in sorted(course_minors.items()):
            course_type = '/'.join(sorted(data['type']))

            # Extract prefix
            prefix = course.split()[0] if ' ' in course else course[:4]

            # Get offering rate
            times_offered = len(self.course_offerings.get(course, []))
            offering_rate = (times_offered / self.total_semesters * 100) if self.total_semesters > 0 else 0

            records.append({
                'Course Code': course,
                'Prefix': prefix,
                'Type': course_type,
                'Times Offered in Data': times_offered,
                'Offering Rate (%)': round(offering_rate, 1),
                'Which Minors Require It': '; '.join(data['minors'])
            })

        return pd.DataFrame(records)

    def generate_report_markdown(self, analysis_df: pd.DataFrame,
                                 ghost_zombie_df: pd.DataFrame) -> str:
        """Generate markdown report."""
        report = []

        # Title
        report.append("# Phase 3: Minors Analysis - Course Offerings Report\n")

        # Executive Summary
        report.append("## Executive Summary\n")

        impossible_count = len(analysis_df[analysis_df['Impossible to Complete'] == 'Yes'])
        critical_count = len(analysis_df[analysis_df['Risk Level'] == 'CRITICAL'])
        high_count = len(analysis_df[analysis_df['Risk Level'] == 'HIGH'])

        report.append(f"- **Total Minors Analyzed**: {len(analysis_df)}\n")
        report.append(f"- **Impossible to Complete**: {impossible_count}\n")
        report.append(f"- **Critical Risk**: {critical_count}\n")
        report.append(f"- **High Risk**: {high_count}\n")
        report.append(f"- **Total Semesters in Grade Data**: {self.total_semesters}\n\n")

        # Impossible Minors
        if impossible_count > 0:
            report.append("## Minors Impossible to Complete\n")
            report.append("These minors cannot be completed - all required courses are ghost or zombie courses:\n\n")

            impossible_minors = analysis_df[analysis_df['Impossible to Complete'] == 'Yes'].sort_values('Minor Name')
            for idx, row in impossible_minors.iterrows():
                report.append(f"### {row['Minor Name']}\n")
                report.append(f"- Category: {row['Category']}\n")
                report.append(f"- Total Required: {row['Total Required Courses']}\n")
                report.append(f"- Ghost Courses: {row['Ghost Courses (count)']}\n")
                report.append(f"- Zombie Courses: {row['Zombie Courses (count)']}\n\n")

            report.append("\n")

        # Top 15 Worst Offering Rates
        report.append("## Top 15 Minors with Worst Offering Rates\n\n")

        worst_15 = analysis_df.nsmallest(15, 'Avg Offering Rate Among Required (%)')
        for idx, row in worst_15.iterrows():
            report.append(f"### {row['Minor Name']}\n")
            report.append(f"- Avg Offering Rate: {row['Avg Offering Rate Among Required (%)']}%\n")
            report.append(f"- Min/Max: {row['Min Offering Rate Among Required (%)']}% / {row['Max Offering Rate Among Required (%)']}%\n")
            report.append(f"- Ghost: {row['Ghost Courses (count)']}, Zombie: {row['Zombie Courses (count)']}\n")
            report.append(f"- Risk: {row['Risk Level']}\n\n")

        # Department Analysis
        report.append("## Department Analysis\n\n")

        if not ghost_zombie_df.empty:
            prefix_stats = ghost_zombie_df.groupby('Prefix').agg({
                'Course Code': 'count',
                'Times Offered in Data': 'mean',
                'Offering Rate (%)': 'mean'
            }).rename(columns={'Course Code': 'Ghost/Zombie Count'})

            prefix_stats = prefix_stats.sort_values('Ghost/Zombie Count', ascending=False)

            report.append("### Departments with Most Ghost/Zombie Courses\n\n")
            report.append("| Prefix | Ghost/Zombie Count | Avg Offering Rate (%) |\n")
            report.append("|--------|-------------------|----------------------|\n")

            for prefix, row in prefix_stats.head(15).iterrows():
                count = int(row['Ghost/Zombie Count'])
                avg_rate = row['Offering Rate (%)']
                report.append(f"| {prefix} | {count} | {avg_rate:.1f}% |\n")

            report.append("\n")

        # Ghost and Zombie Course Summary
        report.append("## Ghost and Zombie Courses Summary\n\n")

        if not ghost_zombie_df.empty:
            ghost_count = len(ghost_zombie_df[ghost_zombie_df['Type'] == 'Ghost'])
            zombie_count = len(ghost_zombie_df[ghost_zombie_df['Type'] == 'Zombie'])

            report.append(f"- **Total Ghost Courses**: {ghost_count}\n")
            report.append(f"- **Total Zombie Courses**: {zombie_count}\n")
            report.append(f"- **Total Unique Ghost/Zombie Courses**: {len(ghost_zombie_df)}\n\n")

        # Recommendations
        report.append("## Recommendations\n\n")
        report.append("### Immediate Actions\n\n")
        report.append("1. **Address Impossible Minors**\n")
        report.append("   - Develop alternative course options or requirements\n")
        report.append("   - Consider consolidating with similar minors\n\n")
        report.append("2. **Improve Zombie Courses (< 30% offering)**\n")
        report.append("   - Increase course frequency in regular rotation\n")
        report.append("   - Ensure predictable scheduling\n\n")
        report.append("3. **Department-Level Issues**\n")
        report.append("   - Review staffing for single-department minors\n")
        report.append("   - Consider cross-listing opportunities\n\n")

        return '\n'.join(report)

    def run(self, output_dir: str) -> bool:
        """Run complete analysis and generate output files."""
        logger.info("Starting Phase 3 minors analysis...")

        # Load data
        if not self.load_master_analysis():
            return False

        severity_path = os.path.join(
            os.path.dirname(self.master_analysis_path),
            "06_Severity_Ranking.csv"
        )
        if not self.load_severity_ranking(severity_path):
            logger.warning("Could not load severity ranking (non-critical)")

        # Process grade spreads
        if not self.process_grade_spreads():
            logger.warning("Could not process grade spread files")

        # Analyze minors
        logger.info("Analyzing minors...")
        analysis_df = self.analyze_minors()

        if analysis_df.empty:
            logger.error("No analysis results generated")
            return False

        # Generate ghost/zombie report
        ghost_zombie_df = self.generate_ghost_zombie_report(analysis_df)

        # Generate markdown report
        markdown_report = self.generate_report_markdown(analysis_df, ghost_zombie_df)

        # Save outputs
        logger.info(f"Saving results to {output_dir}")

        try:
            # Save analysis CSV
            analysis_output = os.path.join(output_dir, "09_Phase_3_Course_Offerings.csv")
            analysis_df.to_csv(analysis_output, index=False)
            logger.info(f"Saved: {analysis_output}")

            # Save ghost/zombie CSV
            ghost_zombie_output = os.path.join(output_dir, "10_Ghost_and_Zombie_Courses.csv")
            ghost_zombie_df.to_csv(ghost_zombie_output, index=False)
            logger.info(f"Saved: {ghost_zombie_output}")

            # Save markdown report
            report_output = os.path.join(output_dir, "10_Phase_3_Report.md")
            with open(report_output, 'w') as f:
                f.write(markdown_report)
            logger.info(f"Saved: {report_output}")

            logger.info("Phase 3 analysis complete!")
            return True

        except Exception as e:
            logger.error(f"Error saving results: {e}")
            return False


def main():
    """Main entry point."""
    master_analysis_path = (
        "/Volumes/MacShare/graduate-coursework/Daily_Gamecock/Archive_writing/"
        "DailyGamecock_JVAUGHT_examples/Current_writing/Minors_courses/"
        "00_MASTER_ANALYSIS/USC_Minors_Master_Analysis.csv"
    )

    grade_spreads_dir = (
        "/Volumes/MacShare/graduate-coursework/Daily_Gamecock/Archive_writing/"
        "DailyGamecock_JVAUGHT_examples/Current_writing/Minors_courses/"
        "usc_grade_spreads"
    )

    output_dir = (
        "/Volumes/MacShare/graduate-coursework/Daily_Gamecock/Archive_writing/"
        "DailyGamecock_JVAUGHT_examples/Current_writing/Minors_courses/"
        "00_MASTER_ANALYSIS"
    )

    analyzer = CourseOfferingAnalyzer(master_analysis_path, grade_spreads_dir)
    success = analyzer.run(output_dir)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
