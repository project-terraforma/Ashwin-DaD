# Ashwin Prabou - Project D

-----

## Context

While **interactive dashboards** are useful, they often fail to address the specific, nuanced questions individual users have about Overture's data. We need a more **flexible and user-driven method** for data exploration. The goal is to empower users to query data through **natural language** using their preferred **Large Language Models (LLMs)**, moving beyond the limitations of static dashboards.

-----

## Solution

We will generate a **single, comprehensive text file** that is both **human- and LLM-readable**. This file will contain:

  * **Relevant data statistics** (e.g., column distributions, null counts).
  * A full **natural language description** of Overture's themes and schema.
  * A set of **pre-injected prompts** designed to guide LLM-based investigation.

This approach will allow any user to load the file into an LLM and immediately begin investigating the data according to their specific interests, essentially turning the text file into an **LLM-friendly data dictionary and query guide**.

-----

## What the Repo Includes

  * `generate_llm_context.py`: The main Python script that analyzes Overture metrics CSV files and generates the comprehensive LLM-readable context document.
  * `analyze_metrics.py`: Helper script for detailed statistical analysis of metrics data (optional for debugging).
  * `README_generation_output.txt`: The resulting human- and LLM-readable text file containing the data schema, statistics, and prompts. This is the primary output file for user interaction. **This file is auto-generated - do not edit manually.**
  * `Metrics/metrics/`: Directory containing Overture metrics data organized by release date.
  * `requirements.txt`: List of required Python packages (pandas, glob, pathlib).

-----

## How to Run

1.  **Clone the repository:**

    ```bash
    git clone [repository-url]
    cd Ashwin-DaD
    ```

2.  **Set up the environment:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Ensure Metrics data is present:**

      * The `Metrics/metrics/` directory should contain Overture metrics CSV files organized by release date.
      * The script automatically detects the latest release.

4.  **Generate the LLM-readable file:**

    ```bash
    python3 generate_llm_context.py
    ```

    This script will:
    - Analyze all metrics CSV files from the latest release
    - Extract schema information and statistics
    - Generate (or update) the `README_generation_output.txt` file
    - Report file size and completion status

5.  **Start your LLM investigation:**

      * Copy the entire contents of `README_generation_output.txt`.
      * Paste the content directly into the prompt/context window of your preferred LLM (e.g., ChatGPT, Claude, Gemini).
      * Begin asking your natural language questions about the Overture data! The pre-injected prompts will help set the context for the LLM.

## Example Usage

After generating the context file, you can ask questions like:

- "Which countries have the highest concentration of Places data?"
- "What percentage of buildings are residential vs commercial?"
- "How has the data changed in this release compared to the previous one?"
- "What are the most common road types in the Transportation theme?"

The LLM will use the statistics and schema information in the context document to provide accurate, data-driven answers.