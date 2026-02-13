#!/usr/bin/env python3
"""
Phase 3 Real Analysis: Course Offering Availability for USC Minors

Analyzes real grade spread data from multiple semesters to determine:
- Which required minor courses are offered
- How frequently they are offered (offering rate)
- Identifies "ghost" courses (never offered) and "zombie" courses (<30% offering)
- Determines if minors are actually completable

Usage:
    python3 phase3_real_analysis.py
"""

import os
import re
import csv
import pandas as pd
import openpyxl
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Set, Tuple
import sys
from datetime import datetime


class Phase3Analyzer:
    """Analyze course availability using real grade spread data."""

    def __init__(self, base_dir: str):
        """Initialize the analyzer with the base directory."""
        self.base_dir = Path(base_dir)
        self.grade_spreads_dir = self.base_dir / "usc_grade_spreads"
        self.master_analysis_file = self.base_dir / "00_MASTER_ANALYSIS" / "USC_Minors_Master_Analysis.csv"
        self.minors_dir = self.base_dir
        self.output_dir = self.base_dir / "00_MASTER_ANALYSIS"

        # Data structures
        self.semester_courses = {}  # {semester: {(SUBJECT, COURSE_NUMBER), ...}}
        self.all_minors = {}  # {minor_name: {year, category, required_courses}}
        self.required_courses_by_minor = {}  # {minor_name: {(SUBJECT, NUMBER), ...}}
        self.course_offerings = {}  # {(SUBJECT, NUMBER): {semesters_offered, times_offered}}

    def parse_semester_from_filename(self, filename: str) -> str:
        """Extract semester code from filename (e.g., 202505 from 202505_grade_spread_report.xlsx)."""
        match = re.match(r'(\d{6})', filename)
        return match.group(1) if match else None

    def semester_to_readable(self, semester_code: str) -> str:
        """Convert semester code (e.g., 202505) to readable format (Spring 2025)."""
        if not semester_code or len(semester_code) != 6:
            return semester_code

        year = semester_code[:4]
        month = semester_code[4:6]

        if month == "01":
            return f"Spring {year}"
        elif month == "05":
            return f"Summer {year}"
        elif month == "08":
            return f"Fall {year}"
        else:
            return semester_code

    def load_grade_spread_files(self) -> bool:
        """Load all Excel files from the grade spreads directory."""
        print("Loading grade spread files...")

        if not self.grade_spreads_dir.exists():
            print(f"Error: Directory {self.grade_spreads_dir} not found")
            return False

        xlsx_files = sorted(self.grade_spreads_dir.glob("*.xlsx"))
        if not xlsx_files:
            print("Error: No Excel files found")
            return False

        print(f"Found {len(xlsx_files)} grade spread files")

        for xlsx_file in xlsx_files:
            try:
                semester_code = self.parse_semester_from_filename(xlsx_file.name)
                if not semester_code:
                    print(f"Skipping {xlsx_file.name} - cannot parse semester")
                    continue

                print(f"  Processing {xlsx_file.name} ({self.semester_to_readable(semester_code)})...", end="")

                # Read Excel file
                df = pd.read_excel(xlsx_file)

                # Extract unique (SUBJECT, COURSE_NUMBER) combinations
                courses = set()
                for _, row in df.iterrows():
                    subject = str(row['SUBJECT']).strip()
                    course_num = str(row['COURSE_NUMBER']).strip()

                    # Skip invalid entries
                    if subject and course_num and subject != 'nan' and course_num != 'nan':
                        courses.add((subject, course_num))

                self.semester_courses[semester_code] = courses
                print(f" {len(courses)} courses")

            except Exception as e:
                print(f"\n  Error processing {xlsx_file.name}: {e}")
                continue

        print(f"Loaded {len(self.semester_courses)} semesters\n")
        return len(self.semester_courses) > 0

    def extract_required_courses_from_markdown(self, markdown_file: Path) -> Set[str]:
        """Extract required courses from a minor's markdown file."""
        required_courses = set()

        try:
            with open(markdown_file, 'r') as f:
                content = f.read()

            # Find the Required Courses section
            required_section = re.search(
                r'##\s*Required Courses.*?\n\n(.*?)(?=##|$)',
                content,
                re.DOTALL | re.IGNORECASE
            )

            if required_section:
                table_content = required_section.group(1)

                # Extract course codes from markdown table
                # Looking for patterns like "AFAM 201", "HIST 200", etc.
                course_pattern = r'\|\s*([A-Z]{2,})\s+(\d+)\s*\|'
                matches = re.findall(course_pattern, table_content)

                for subject, number in matches:
                    # Only include if it's in a "Required" row (simple heuristic)
                    required_courses.add((subject, number))

        except Exception as e:
            print(f"Warning: Error reading {markdown_file.name}: {e}")

        return required_courses

    def load_minors_from_markdown_files(self) -> bool:
        """Load all minor definitions from markdown files."""
        print("Loading minor definitions from markdown files...")

        markdown_files = sorted(self.minors_dir.glob("*_Minor.md"))
        if not markdown_files:
            print("Error: No minor markdown files found")
            return False

        print(f"Found {len(markdown_files)} minor definitions")

        for md_file in markdown_files:
            try:
                # Extract minor name from filename
                minor_name = md_file.stem.replace("_Minor", "").replace("_", " ")

                # Extract required courses
                required_courses = self.extract_required_courses_from_markdown(md_file)

                if required_courses:
                    self.required_courses_by_minor[minor_name] = required_courses
                    print(f"  {minor_name}: {len(required_courses)} required courses")

            except Exception as e:
                print(f"  Error processing {md_file.name}: {e}")
                continue

        print(f"Loaded {len(self.required_courses_by_minor)} minors with required courses\n")
        return len(self.required_courses_by_minor) > 0

    def analyze_course_offerings(self) -> None:
        """Analyze which courses were offered and how frequently."""
        print("Analyzing course offerings...")

        # For each required course in all minors
        all_required_courses = set()
        for minor_courses in self.required_courses_by_minor.values():
            all_required_courses.update(minor_courses)

        total_semesters = len(self.semester_courses)

        for course_key in sorted(all_required_courses):
            semesters_offered = []
            times_offered = 0

            for semester_code in sorted(self.semester_courses.keys()):
                if course_key in self.semester_courses[semester_code]:
                    semesters_offered.append(semester_code)
                    times_offered += 1

            offering_rate = (times_offered / total_semesters * 100) if total_semesters > 0 else 0

            self.course_offerings[course_key] = {
                'semesters': semesters_offered,
                'times': times_offered,
                'rate': offering_rate,
                'total_semesters': total_semesters
            }

        print(f"Analyzed {len(self.course_offerings)} unique required courses\n")

    def load_master_analysis_for_categories(self) -> Dict[str, str]:
        """Load minor categories from master analysis CSV."""
        minor_categories = {}

        try:
            df = pd.read_csv(self.master_analysis_file)
            for _, row in df.iterrows():
                minor_name = row['Minor Name']
                category = row.get('Category', 'Unknown')
                minor_categories[minor_name] = category
        except Exception as e:
            print(f"Warning: Could not load categories from master analysis: {e}")

        return minor_categories

    def classify_course_risk(self, offering_rate: float) -> str:
        """Classify course availability risk."""
        if offering_rate == 0:
            return "Critical"  # Ghost course
        elif offering_rate < 30:
            return "High"  # Zombie course
        elif offering_rate < 60:
            return "Medium"
        else:
            return "Low"

    def generate_phase3_course_offerings_report(self, minor_categories: Dict[str, str]) -> List[Dict]:
        """Generate the main Phase 3 course offerings report."""
        print("Generating Phase 3 Course Offerings Report...")

        results = []

        for minor_name in sorted(self.required_courses_by_minor.keys()):
            required_courses = self.required_courses_by_minor[minor_name]

            # Count offerings
            ever_offered = 0
            ghost_courses = []
            zombie_courses = []
            offering_rates = []

            for course_key in sorted(required_courses):
                if course_key in self.course_offerings:
                    offering_info = self.course_offerings[course_key]
                    rate = offering_info['rate']
                    offering_rates.append(rate)

                    if rate == 0:
                        ghost_courses.append(f"{course_key[0]} {course_key[1]}")
                    elif rate < 30:
                        zombie_courses.append(f"{course_key[0]} {course_key[1]}")
                    else:
                        ever_offered += 1
                else:
                    # Course not in offerings - treat as ghost
                    ghost_courses.append(f"{course_key[0]} {course_key[1]}")

            # Calculate stats
            min_rate = min(offering_rates) if offering_rates else 0
            max_rate = max(offering_rates) if offering_rates else 0
            avg_rate = sum(offering_rates) / len(offering_rates) if offering_rates else 0

            # Determine if minor is completable
            can_complete = "Yes" if len(ghost_courses) == 0 else "No"

            # Determine risk level
            if len(ghost_courses) > 0:
                risk_level = "Critical"
            elif len(zombie_courses) > 0:
                risk_level = "High"
            elif avg_rate < 60:
                risk_level = "Medium"
            else:
                risk_level = "Low"

            category = minor_categories.get(minor_name, "Unknown")

            results.append({
                'Minor Name': minor_name,
                'Category': category,
                'Total Required Courses': len(required_courses),
                'Required Courses Ever Offered': ever_offered + len(zombie_courses),
                'Ghost Courses': len(ghost_courses),
                'Ghost Course List': "; ".join(ghost_courses) if ghost_courses else "None",
                'Zombie Courses': len(zombie_courses),
                'Zombie Course List': "; ".join(zombie_courses) if zombie_courses else "None",
                'Min Offering Rate (%)': f"{min_rate:.1f}",
                'Max Offering Rate (%)': f"{max_rate:.1f}",
                'Avg Offering Rate (%)': f"{avg_rate:.1f}",
                'Can Complete Minor': can_complete,
                'Risk Level': risk_level
            })

        return results

    def generate_ghost_and_zombie_report(self) -> List[Dict]:
        """Generate detailed report of ghost and zombie courses."""
        print("Generating Ghost and Zombie Courses Report...")

        results = []

        # Build reverse mapping: which minors require each course
        course_to_minors = defaultdict(list)
        for minor_name, courses in self.required_courses_by_minor.items():
            for course_key in courses:
                course_to_minors[course_key].append(minor_name)

        # Process each course
        for course_key in sorted(self.course_offerings.keys()):
            offering_info = self.course_offerings[course_key]
            rate = offering_info['rate']
            times = offering_info['times']
            semesters = offering_info['semesters']

            # Only include ghost and zombie courses
            if rate == 0 or rate < 30:
                course_type = "Ghost" if rate == 0 else "Zombie"

                # Get semester display names
                readable_semesters = [self.semester_to_readable(s) for s in semesters]

                minors_requiring = course_to_minors.get(course_key, [])

                results.append({
                    'Course Code': f"{course_key[0]} {course_key[1]}",
                    'Subject Prefix': course_key[0],
                    'Type': course_type,
                    'Semesters Offered In': "; ".join(readable_semesters) if readable_semesters else "Never",
                    'Times Offered': times,
                    'Offering Rate (%)': f"{rate:.1f}",
                    'Required By Minors': len(minors_requiring),
                    'Minor Names': "; ".join(sorted(minors_requiring))
                })

        return sorted(results, key=lambda x: (x['Type'], -float(x['Offering Rate (%)'])))

    def generate_markdown_report(self,
                                 offerings_data: List[Dict],
                                 ghost_zombie_data: List[Dict]) -> str:
        """Generate comprehensive markdown report."""
        print("Generating Markdown Report...")

        # Separate ghost from zombie courses
        ghost_courses = [c for c in ghost_zombie_data if c['Type'] == 'Ghost']
        zombie_courses = [c for c in ghost_zombie_data if c['Type'] == 'Zombie']

        # Find worst minors
        critical_minors = [m for m in offerings_data if m['Risk Level'] == 'Critical']
        high_risk_minors = [m for m in offerings_data if m['Risk Level'] == 'High']

        # Count uncomplatable minors
        incomplete_minors = [m for m in offerings_data if m['Can Complete Minor'] == 'No']

        # Department analysis
        subject_to_courses = defaultdict(list)
        for course_key in self.course_offerings.keys():
            subject = course_key[0]
            offering_info = self.course_offerings[course_key]
            subject_to_courses[subject].append(offering_info['rate'])

        dept_stats = []
        for subject in sorted(subject_to_courses.keys()):
            rates = subject_to_courses[subject]
            avg_rate = sum(rates) / len(rates)
            dept_stats.append((subject, len(rates), avg_rate))

        dept_stats.sort(key=lambda x: x[2])  # Sort by avg rate
        worst_depts = dept_stats[:10]
        best_depts = dept_stats[-10:]

        report = f"""# Phase 3 Course Availability Analysis - Real Data Report

**Generated:** {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}
**Analysis Period:** {self.semester_to_readable(min(self.semester_courses.keys()))} - {self.semester_to_readable(max(self.semester_courses.keys()))}
**Total Semesters Analyzed:** {len(self.semester_courses)}

## Executive Summary

This analysis examines the actual availability of required courses across USC's minors using real grade spread data from {len(self.semester_courses)} semesters. The findings reveal significant challenges in course availability that directly impact students' ability to complete their chosen minors.

### Key Findings

- **Total Minors Analyzed:** {len(offerings_data)}
- **Minors That Cannot Be Completed:** {len(incomplete_minors)} ({len(incomplete_minors)/len(offerings_data)*100:.1f}%)
- **Total Unique Required Courses:** {len(self.course_offerings)}
- **Ghost Courses (Never Offered):** {len(ghost_courses)} ({len(ghost_courses)/len(self.course_offerings)*100:.1f}%)
- **Zombie Courses (<30% Offering):** {len(zombie_courses)} ({len(zombie_courses)/len(self.course_offerings)*100:.1f}%)
- **Uncomplatable Minors (Critical Risk):** {len(critical_minors)}

### Risk Distribution

- **Critical Risk Minors:** {len(critical_minors)} (cannot be completed)
- **High Risk Minors:** {len(high_risk_minors)} (missing or rarely-offered courses)
- **Medium/Low Risk Minors:** {len(offerings_data) - len(critical_minors) - len(high_risk_minors)}

## Minors That Cannot Be Completed

The following {len(incomplete_minors)} minors have required courses that have **never been offered** during the analysis period:

"""

        if incomplete_minors:
            for minor in sorted(incomplete_minors, key=lambda x: int(x['Ghost Courses'])):
                ghosts = minor['Ghost Course List']
                num_ghosts = int(minor['Ghost Courses'])
                report += f"\n### {minor['Minor Name']}\n"
                report += f"- **Category:** {minor['Category']}\n"
                report += f"- **Ghost Courses:** {num_ghosts}\n"
                report += f"- **Details:** {ghosts}\n"
        else:
            report += "\nGood news: All minors can be completed with required courses.\n"

        # Top 15 worst minors
        report += f"\n## Top 15 Minors with Worst Course Availability\n\n"
        report += "| Rank | Minor Name | Risk | Ghost | Zombie | Avg Rate | Category |\n"
        report += "|------|-----------|------|-------|--------|----------|----------|\n"

        sorted_by_risk = sorted(offerings_data,
                               key=lambda x: (-float(x['Ghost Courses']),
                                            -float(x['Zombie Courses']),
                                            float(x['Avg Offering Rate (%)'])))

        for i, minor in enumerate(sorted_by_risk[:15], 1):
            report += f"| {i} | {minor['Minor Name']} | {minor['Risk Level']} | "
            report += f"{minor['Ghost Courses']} | {minor['Zombie Courses']} | "
            report += f"{minor['Avg Offering Rate (%)']}% | {minor['Category']} |\n"

        # Department Analysis
        report += f"\n## Department Analysis\n\n"
        report += f"### Departments with Lowest Average Course Offering Rates\n\n"
        report += "| Department | Courses Analyzed | Avg Offering Rate |\n"
        report += "|-----------|------------------|-------------------|\n"

        for subject, count, rate in worst_depts:
            report += f"| {subject} | {count} | {rate:.1f}% |\n"

        report += f"\n### Departments with Highest Average Course Offering Rates\n\n"
        report += "| Department | Courses Analyzed | Avg Offering Rate |\n"
        report += "|-----------|------------------|-------------------|\n"

        for subject, count, rate in best_depts:
            report += f"| {subject} | {count} | {rate:.1f}% |\n"

        # Ghost courses details
        report += f"\n## Ghost Courses: Courses Never Offered\n\n"
        report += f"**Total Count:** {len(ghost_courses)}\n\n"
        report += "| Course | Subject | Required By | Semesters Analyzed |\n"
        report += "|--------|---------|-------------|-------------------|\n"

        for course in ghost_courses[:30]:  # Limit to 30
            course_code = course['Course Code']
            required_by = int(course['Required By Minors'])
            minors = course['Minor Names'].split("; ") if course['Minor Names'] else []
            report += f"| {course_code} | {course['Subject Prefix']} | {required_by} | {len(self.semester_courses)} |\n"

        if len(ghost_courses) > 30:
            report += f"\n*... and {len(ghost_courses) - 30} more ghost courses*\n"

        # Zombie courses details
        report += f"\n## Zombie Courses: Rarely Offered (< 30%)\n\n"
        report += f"**Total Count:** {len(zombie_courses)}\n\n"
        report += "| Course | Subject | Rate | Times Offered | Required By |\n"
        report += "|--------|---------|------|--------------|----------|\n"

        for course in zombie_courses[:30]:  # Limit to 30
            rate = float(course['Offering Rate (%)'])
            times = int(course['Times Offered'])
            required_by = int(course['Required By Minors'])
            report += f"| {course['Course Code']} | {course['Subject Prefix']} | {rate:.1f}% | {times}/{len(self.semester_courses)} | {required_by} |\n"

        if len(zombie_courses) > 30:
            report += f"\n*... and {len(zombie_courses) - 30} more zombie courses*\n"

        # Implications
        report += f"\n## Critical Findings & Implications\n\n"
        report += f"1. **Structural Issues:** {len(incomplete_minors)} minor programs cannot be completed due to missing required courses.\n\n"
        report += f"2. **Ghost Courses Problem:** {len(ghost_courses)} required courses have never been offered during the {len(self.semester_courses)}-semester analysis window.\n\n"
        report += f"3. **Zombie Course Problem:** {len(zombie_courses)} required courses are offered in less than 30% of semesters.\n\n"
        report += f"4. **Department Variation:** Course availability varies significantly by department, with {worst_depts[0][0]} showing only {worst_depts[0][2]:.1f}% average offering rate.\n\n"

        report += f"## Recommendations\n\n"
        report += f"1. **Immediate Action:** Review the {len(incomplete_minors)} minors with unmet requirements and either restore required courses or revise program requirements.\n\n"
        report += f"2. **Ghost Course Resolution:** Establish regular offering schedules for {len(ghost_courses)} currently-absent required courses.\n\n"
        report += f"3. **Zombie Course Stabilization:** Increase frequency of {len(zombie_courses)} rarely-offered courses to at least annual offerings.\n\n"
        report += f"4. **Department Support:** Provide resources to departments showing low offering rates to ensure course availability.\n\n"

        report += f"---\n\n*Analysis based on real grade spread data from {len(self.semester_courses)} semesters*\n"

        return report

    def save_results(self, offerings_data: List[Dict],
                    ghost_zombie_data: List[Dict],
                    report_text: str) -> None:
        """Save all results to output files."""
        print("\nSaving results...")

        # Ensure output directory exists
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Save offerings report
        offerings_file = self.output_dir / "11_Real_Phase_3_Course_Offerings.csv"
        with open(offerings_file, 'w', newline='') as f:
            if offerings_data:
                writer = csv.DictWriter(f, fieldnames=offerings_data[0].keys())
                writer.writeheader()
                writer.writerows(offerings_data)
        print(f"  Saved: {offerings_file}")

        # Save ghost/zombie report
        ghost_zombie_file = self.output_dir / "11_Real_Ghost_and_Zombie_Courses.csv"
        with open(ghost_zombie_file, 'w', newline='') as f:
            if ghost_zombie_data:
                writer = csv.DictWriter(f, fieldnames=ghost_zombie_data[0].keys())
                writer.writeheader()
                writer.writerows(ghost_zombie_data)
        print(f"  Saved: {ghost_zombie_file}")

        # Save markdown report
        report_file = self.output_dir / "11_Real_Phase_3_Report.md"
        with open(report_file, 'w') as f:
            f.write(report_text)
        print(f"  Saved: {report_file}")

        print("\nAll output files created successfully!")

    def run(self) -> bool:
        """Execute the complete analysis."""
        print("=" * 70)
        print("USC MINORS PHASE 3 ANALYSIS - REAL DATA")
        print("=" * 70)
        print()

        # Load data
        if not self.load_grade_spread_files():
            return False

        if not self.load_minors_from_markdown_files():
            return False

        # Analyze
        self.analyze_course_offerings()

        # Load categories
        minor_categories = self.load_master_analysis_for_categories()

        # Generate reports
        offerings_data = self.generate_phase3_course_offerings_report(minor_categories)
        ghost_zombie_data = self.generate_ghost_and_zombie_report()
        report_text = self.generate_markdown_report(offerings_data, ghost_zombie_data)

        # Save results
        self.save_results(offerings_data, ghost_zombie_data, report_text)

        print("\n" + "=" * 70)
        print("ANALYSIS COMPLETE")
        print("=" * 70)

        return True


def main():
    """Main entry point."""
    base_dir = "/Volumes/MacShare/graduate-coursework/Daily_Gamecock/Archive_writing/DailyGamecock_JVAUGHT_examples/Current_writing/Minors_courses"

    analyzer = Phase3Analyzer(base_dir)
    success = analyzer.run()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
