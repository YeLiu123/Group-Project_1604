# Group-Project_1604

Python Quiz Answers Pattern Analysis - group project (100 MCQs, 25 respondents).

## Roles & Contributions
- 负责人：本仓库维护者（我）
- 个人职责与贡献：
  - Task 1 – Parsing Module (`data_extraction_M1.py`)
    - 实现 `extract_answers_sequence(file_path)`：解析原始答题文本为长度 100 的整数序列（1-4，未答为 0）
    - 实现 `write_answers_sequence(answers, n)`：将序列写出为 `answers_list_respondent_n.txt`
    - 完成健壮的输入校验与异常处理，适配题目给定的题目/选项格式
  - Task 4 – Integration & Execution (`run_full_analysis_M4.py`)
    - 集成 M1/M2/M3，构建完整流水线：数据准备 → 答案提取 → 统计分析 → 模式检测 → 可视化/报告
    - 产出报告与结构化结果：`analysis_results/comprehensive_analysis_report.txt`、`analysis_results/analysis_results.json`
    - 可视化统一保存到 `pics/` 后再展示

## Other Team Tasks – Status
- Task 2 – Download & Collation Module (`data_preparation_M2.py`)：已完成
  - `download_answer_files(cloud_url, data_dir, n)`：从云端下载 `a1.txt..an.txt`，重命名为 `answers_respondent_i.txt`
  - `collate_answer_files(data_dir)`：合并为 `output/collated_answers.txt`，不同受试者以单独一行 `*` 分隔
  - 提供 `simulate_download_from_local()` 便于本地测试（从 `quiz_answers_named_a1_to_a25/` 拷贝）
- Task 3 – Analysis Module (`data_analysis_M3.py`)：已完成
  - `generate_means_sequence(collated_answers_path)`：计算每题均值（排除 0）
  - `visualize_data(path, n)`：
    - n=1：均值散点图（支持传入数据文件夹或整理文件）
    - n=2：全体受试者折线图（横轴 1-100；未作答绘制在 y=0，基准线可视）
  - 额外：`analyze_answer_patterns()` 进行简单模式检测与统计摘要

## How to Run
1) 准备数据
- 本地模拟（默认）：脚本会从 `quiz_answers_named_a1_to_a25/` 拷贝 25 份 `a*.txt` 到 `data/`
- 或者自行调用 `download_answer_files(cloud_url, 'data', n)` 从云端下载

2) 运行完整流水线
```
python run_full_analysis_M4.py
```
- 中间产物：`data/answers_respondent_*.txt`、`output/collated_answers.txt`、`answers_list_respondent_*.txt`
- 结果产出：
  - 报告：`analysis_results/comprehensive_analysis_report.txt`
  - JSON：`analysis_results/analysis_results.json`
  - 图片：`pics/means_scatter_*.png`、`pics/individual_lines_*.png`

3) 单独可视化（可选）
```python
from data_analysis_M3 import visualize_data
visualize_data('data', 1)  # 均值散点图
visualize_data('data', 2)  # 全员折线图
```

## Repo Structure (key files)
- `data_extraction_M1.py`：解析与写出答案序列（Task 1）
- `data_preparation_M2.py`：下载与合并（Task 2）
- `data_analysis_M3.py`：统计与可视化（Task 3）
- `run_full_analysis_M4.py`：集成与执行（Task 4）
- `quiz_answers_named_a1_to_a25/`：原始 `a*.txt` 示例
- `data/`、`output/`、`analysis_results/`、`pics/`：运行时生成/结果目录

## Notes
- 可根据需要将生成目录加入 `.gitignore`（如 `data/`、`output/`、`analysis_results/`、`pics/`），保持仓库整洁。
