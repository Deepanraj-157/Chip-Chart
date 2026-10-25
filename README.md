# ChipChart 🔌

**An AI-powered ESP32 datasheet assistant for accurate hardware specifications and battery-life calculations.**

## Problem Statement

Hardware engineers must navigate hundreds or thousands of pages of datasheets and Technical Reference Manuals (TRMs) to compare ESP32 chips, understand electrical characteristics, estimate current consumption, calculate battery life, and identify GPIO limitations.

General-purpose LLMs can misread technical tables, confuse operating conditions, or perform arithmetic incorrectly. These errors can lead to inaccurate power budgets and hardware design decisions.

ChipChart aims to solve this problem by combining document retrieval with structured technical data and deterministic Python calculations.

## Target Users

Hardware design engineers working at IoT product development companies, particularly engineers who need to:

- Compare ESP32-family chips for a product.
- Estimate average current consumption and battery life.
- Check GPIO and electrical limitations.
- Locate technical specifications directly in official documentation.

## Signature Feature: Battery-Life Calculator

Enter a battery capacity, operating modes, and duty cycle to estimate average current consumption and battery life.

The system is designed to provide:

- Average current consumption based on selected operating modes.
- Estimated battery life in hours or days.
- Source document and page references for technical values.
- Transparent calculations that can be independently verified.

**Example question:**  
"What would the estimated battery life be for an ESP32-C6 using a 2,000 mAh battery if the radio is active for 2% of the time?"

Actual results depend on the selected current values, operating conditions, and other system loads.

## Dataset

ChipChart uses official Espressif documentation as its technical knowledge base.

### Current collection status

| Metric | Current status |
|---|---:|
| PDF documents collected | 41 |
| Total readable PDF pages | 10,499 |
| Initial collection target | 50+ pages |
| Overall project target | 5,000+ pages |
| Collection target status | Achieved |

### Document categories

The current collection includes documents covering:

- ESP32
- ESP32-C3
- ESP32-C5
- ESP32-C6
- ESP32-H2
- ESP32-S2
- ESP32-S3
- ESP32 modules, including WROOM, WROVER, MINI, and other variants
- Technical Reference Manuals
- Hardware design guidelines
- Chip errata and test documentation

### Dataset organization

```text
data/
├── raw/
│   ├── esp32/
│   ├── esp32-c3/
│   ├── esp32-c5/
│   ├── esp32-c6/
│   ├── esp32-h2/
│   ├── esp32-s2/
│   └── esp32-s3/
├── sample/
└── manifest.csv
```

The `raw/` directory contains the collected source PDFs. The `sample/` directory is intended for permitted example documents, and `manifest.csv` records metadata such as file paths, page counts, file sizes, SHA-256 hashes, duplicate indicators, and processing status.

Raw PDFs should not be committed to Git unless redistribution is permitted by the applicable document terms.

## Technical Approach

The key engineering challenge is converting technical document tables into reliable, structured data.

The intended workflow is:

1. **Document collection:** Collect relevant datasheets, TRMs, and hardware documentation.
2. **PDF processing:** Extract text and tables, using OCR when necessary.
3. **Structured extraction:** Represent electrical characteristics as typed records containing parameters, operating conditions, minimum, typical and maximum values, and units.
4. **Retrieval:** Find the relevant technical records for a user's question.
5. **Deterministic calculation:** Use Python to calculate average current, battery life, and other supported quantities.
6. **Source attribution:** Link results to their source documents, pages, and tables.
7. **Validation:** Compare calculated results against hand-checked reference calculations.

The LLM assists with selecting relevant information and explaining results. Python performs the numerical calculations rather than relying on the LLM to do arithmetic.

## Hardest Technical Problem

**Turning unstructured datasheet tables into trustworthy numbers.**

Electrical specifications depend on operating conditions, units, and whether a value is minimum, typical, or maximum. Incorrectly selecting a row or mixing conditions can produce misleading calculations.

The project aims to evaluate numeric accuracy using 60 hand-checked calculations. Results should be reported only after the evaluation has been completed, including the test methodology and observed errors.

## Example Questions

See [docs/QUESTIONS.md](https://github.com/Deepanraj-157/Chip-Chart/blob/main/docs/QUESTIONS.md).

Example questions include:

1. What is the deep-sleep current of ESP32-C3 compared with ESP32-S3?
2. What is the estimated battery life of an ESP32-C6 with a 2,000 mAh battery and a 2% radio duty cycle?
3. Which GPIO pins on ESP32-S3 have strapping functions?
4. What are the relevant operating conditions for a specified current-consumption value?
5. Which source table and page support a particular electrical specification?

## Technology Stack

The project is intended to use:

- **Language:** Python
- **Backend:** FastAPI
- **Document processing:** PDF text and table extraction, with OCR where required
- **Calculation engine:** Python
- **Data storage:** Structured technical records and source metadata
- **AI component:** LLM-assisted retrieval and explanation

Update this list to match the technologies actually implemented in the repository.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Deepanraj-157/Chip-Chart.git
cd Chip-Chart
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements-dev.txt
```

Use the dependency file that exists in your repository. If you only have `requirements.txt`, use that instead.

### 4. Configure environment variables

**Windows PowerShell:**

```powershell
Copy-Item .env.example .env
```

**Linux/macOS:**

```bash
cp .env.example .env
```

Add the required API keys and configuration values to `.env` if the application requires them. Never commit secrets to Git.

### 5. Run the application

```bash
uvicorn app.main:app --reload
```

Open the API health endpoint:

```text
http://localhost:8000/health
```

Or test it from another terminal:

```bash
curl http://localhost:8000/health
```

These commands assume the corresponding application files, dependencies, and health endpoint have been implemented.

## Dataset Tools

Recount the collected PDF pages and regenerate the dataset manifest:

```bash
python tools/count_pages.py
```

The tool scans PDFs under `data/raw/`, counts readable pages, calculates file hashes, and writes metadata to `data/manifest.csv`.

## Evaluation Goals

The project aims to measure:

- Numeric accuracy on 60 hand-checked calculations.
- Correct selection of technical specifications and operating conditions.
- Correct source document and page attribution.
- Reliability of battery-life and average-current calculations.

A target such as 98% numeric accuracy should be presented as achieved only after testing supports it.

## Repository

[GitHub: Deepanraj-157/Chip-Chart](https://github.com/Deepanraj-157/Chip-Chart)

## Live Demo

Not available yet. Add the deployed application URL here when a live version is available.
