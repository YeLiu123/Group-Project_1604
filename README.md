# Group-Project_1604

Python Quiz Answers Pattern Analysis — group project on a 100-question multiple-choice quiz (25 respondents). This repository contains a complete modular pipeline to parse, prepare, analyze, visualize, and report potential answer patterns.

## Roles & Contributions
- Owner of this repo (me): responsible for Task 3 and Task 4
- Personal responsibilities and contributions:
  - Task 3 – Analysis Module (`data_analysis_M3.py`)
    - Implemented `generate_means_sequence(collated_answers_path)`: compute per-question means (excluding 0)
    - Implemented `visualize_data(path, n)`: n=1 (means scatter), n=2 (all respondents line plot, unanswered at y=0 with baseline)
    - Implemented `analyze_answer_patterns(collated_answers_path)`: basic pattern checks and statistical summary
  - Task 4 – Integration & Execution (`run_full_analysis_M4.py`)
    - Integrated M1/M2/M3 into a full pipeline: Data Preparation → Answer Extraction → Statistical Analysis → Pattern Detection → Visualization/Reporting
    - Produced outputs: `analysis_results/comprehensive_analysis_report.txt` and `analysis_results/analysis_results.json`
    - Unified visualization: all figures are saved to `pics/` first, then displayed

## Other Team Tasks – Status (by teammates)
- Task 1 – Parsing Module (`data_extraction_M1.py`): Completed by teammate
  - `extract_answers_sequence(file_path)`: parse each raw quiz file into a list of 100 integers (1–4; 0 = unanswered)
  - `write_answers_sequence(answers, n)`: save parsed sequences as `answers_list_respondent_n.txt`
  - Robust validation and error handling for the given file format
- Task 2 – Download & Collation Module (`data_preparation_M2.py`): Completed by teammate
  - `download_answer_files(cloud_url, data_dir, n)`: download `a1.txt..an.txt` and rename to `answers_respondent_i.txt`
  - `collate_answer_files(data_dir)`: merge into `output/collated_answers.txt`, with respondents separated by a single line containing `*`
  - `simulate_download_from_local()`: convenient local testing by copying from `quiz_answers_named_a1_to_a25/`

## How to Run
1) Prepare data
- Local simulation (default): the script copies 25 `a*.txt` files from `quiz_answers_named_a1_to_a25/` to `data/`
- Or call `download_answer_files(cloud_url, 'data', n)` to download from cloud

2) Run the full pipeline
```
python run_full_analysis_M4.py
```
- Intermediate artifacts: `data/answers_respondent_*.txt`, `output/collated_answers.txt`, `answers_list_respondent_*.txt`
- Outputs:
  - Report: `analysis_results/comprehensive_analysis_report.txt`
  - JSON: `analysis_results/analysis_results.json`
  - Figures: `pics/means_scatter_*.png`, `pics/individual_lines_*.png`

3) Visualizations only (optional)
```python
from data_analysis_M3 import visualize_data
visualize_data('data', 1)  # per-question means (scatter)
visualize_data('data', 2)  # all respondents (lines)
```

## Repository Structure (key files)
- `data_extraction_M1.py`: parsing and saving answer sequences (Task 1)
- `data_preparation_M2.py`: download and collation (Task 2)
- `data_analysis_M3.py`: statistics and visualizations (Task 3)
- `run_full_analysis_M4.py`: integration and execution (Task 4)
- `quiz_answers_named_a1_to_a25/`: raw example files `a*.txt`
- `data/`, `output/`, `analysis_results/`, `pics/`: generated directories and results

## Notes
- To keep the repo clean, consider adding generated directories to `.gitignore` (e.g., `data/`, `output/`, `analysis_results/`, `pics/`).
