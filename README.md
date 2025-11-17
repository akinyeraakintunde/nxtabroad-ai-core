# NxtAbroad AI Core

**NxtAbroad AI** is an intelligent decision-support engine for international student recruitment and visa advisory.

It powers:
- Lead scoring for prospective students
- Eligibility and risk triage (visa, finance, academic fit)
- Automated recommendations for programmes, countries and intakes

This repository contains the **core rules engine and scoring models** that sit behind the NxtAbroad platform.

---

## Project Goals

- Replace manual, spreadsheet-based assessments with **consistent, auditable rules**.
- Help advisors focus on **high-intent, high-potential leads**.
- Provide a foundation for future **ML-driven recommendations** (conversion prediction, churn, etc.).

---

## Core Features

- **Rules Engine**: Declarative rules for eligibility & risk (e.g. funds, grade, visa history).
- **Lead Scoring**: 0–100 score based on academic fit, financial strength, visa risk & engagement.
- **Data Pipeline**: Load leads from CSV/JSON and run them through the pipeline.
- **Extensible Design**: Add new rules and dimensions without breaking the core.

---

## High-Level Architecture

```text
                     +-------------------------+
                     |   Data Sources          |
                     |  (CRM, Forms, CSV)      |
                     +------------+------------+
                                  |
                                  v
                         [ Data Pipeline ]
                                  |
                                  v
                     +-------------------------+
                     |    Rules Engine         |
                     |  - eligibility rules    |
                     |  - risk categories      |
                     +------------+------------+
                                  |
                                  v
                     +-------------------------+
                     |    Lead Scoring         |
                     |  - 0–100 score          |
                     |  - reasons/explanations |
                     +------------+------------+
                                  |
                                  v
                         [ Downstream Systems ]
                         CRM • Dashboards • Advisors