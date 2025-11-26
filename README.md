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

  * `generator_script.py`: The Python script responsible for connecting to the Overture data source, performing statistical analysis, and compiling the final, comprehensive text file.
  * `README_generation_output.txt`: The resulting human- and LLM-readable text file containing the data schema, statistics, and prompts. This is the primary output file for user interaction.
  * `config.yaml`: Configuration file for database connection strings and parameters for statistical analysis.
  * `preliminary_prompts.txt`: A list of the predefined, context-setting prompts that get injected into the final output file.
  * `requirements.txt`: List of required Python packages to run the `generator_script.py`.

-----

## How to Run

1.  **Clone the repository:**

    ```bash
    git clone [repository-url]
    cd Project-D
    ```

2.  **Set up the environment:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure the database connection:**

      * Open `config.yaml`.
      * Update the database connection string with your credentials and Overture data source details.

4.  **Generate the LLM-readable file:**

    ```bash
    python generator_script.py
    ```

    This script will generate (or update) the `README_generation_output.txt` file.

5.  **Start your LLM investigation:**

      * Copy the entire contents of `README_generation_output.txt`.
      * Paste the content directly into the prompt/context window of your preferred LLM (e.g., ChatGPT, Claude, Gemini).
      * Begin asking your natural language questions about the Overture data\! The pre-injected prompts will help set the context for the LLM.