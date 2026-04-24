#!/usr/bin/env bash

set -euo pipefail

cd "$(dirname "$0")"

typst compile figures-src/estimator_flow.typ figures/estimator_flow.png
typst compile figures-src/estimator_flow.typ figures/estimator_flow.pdf
typst compile EMCH792_Final_Project_Report.typ EMCH792_Final_Project_Report.pdf
