import os
import pandas as pd
from datetime import datetime

# ----------------------------
# CONFIGURATION
# ----------------------------
METRICS_DIR = "metrics"
COLUMN_STATS_DIR = "theme_column_summary_stats"
CLASS_STATS_DIR = "theme_class_summary_stats"
OUTPUT_FILE = "overture_metrics_context_v0.1.txt"
MAX_RELEASES = 10  # limit for compact summary


# ----------------------------
# HELPER FUNCTIONS
# ----------------------------
def get_releases(metrics_dir):
    """List release folders in chronological order (e.g., 2025-01-22.0)."""
    releases = [
        r for r in os.listdir(metrics_dir)
        if os.path.isdir(os.path.join(metrics_dir, r))
    ]
    releases.sort()
    return releases


def summarize_row_counts(metrics_dir, releases):
    """Aggregate total rows per theme per release."""
    summaries = []

    for rel in releases:
        row_counts_dir = os.path.join(metrics_dir, rel, "row_counts")
        if not os.path.exists(row_counts_dir):
            continue

        for file in os.listdir(row_counts_dir):
            if file.endswith(".csv"):
                theme = file.replace(".csv", "")
                path = os.path.join(row_counts_dir, file)
                try:
                    df = pd.read_csv(path)
                    total_rows = len(df)
                    summaries.append({
                        "release": rel,
                        "theme": theme,
                        "total_rows": total_rows
                    })
                except Exception as e:
                    print(f"⚠️ Skipping {path}: {e}")

    df_summary = pd.DataFrame(summaries)
    return df_summary


def summarize_changelog(metrics_dir, releases):
    """Extract changelog summaries (if available)."""
    changelogs = {}
    for rel in releases:
        path = os.path.join(metrics_dir, rel, "changelog_stats.md")
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                changelogs[rel] = f.read().strip()
    return changelogs


def calculate_percent_changes(df_summary):
    """Add percentage change between releases per theme."""
    df_summary = df_summary.sort_values(by=["theme", "release"])
    df_summary["pct_change"] = 0.0
    for theme in df_summary["theme"].unique():
        mask = df_summary["theme"] == theme
        df_summary.loc[mask, "pct_change"] = (
            df_summary[mask]["total_rows"].pct_change() * 100
        )
    return df_summary


# ----------------------------
# MAIN GENERATION LOGIC
# ----------------------------
def generate_context_file():
    releases = get_releases(METRICS_DIR)
    if not releases:
        print("No releases found in metrics folder.")
        return

    releases = releases[-MAX_RELEASES:]  # Limit recent releases
    df_summary = summarize_row_counts(METRICS_DIR, releases)
    df_summary = calculate_percent_changes(df_summary)
    changelogs = summarize_changelog(METRICS_DIR, releases)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        now = datetime.now().strftime("%B %d, %Y")
        f.write(f"# Overture Metrics LLM Context File v0.1\n")
        f.write(f"Generated: {now}\n")
        f.write(f"Releases: {releases[0]} → {releases[-1]}\n\n")

        f.write("="*60 + "\nSECTION 1 — OVERVIEW\n" + "="*60 + "\n")
        f.write("This file summarizes Overture’s Metrics releases for LLM-based exploration.\n\n")
        f.write("Themes include: addresses, base, buildings, divisions, places, and others.\n\n")

        f.write("="*60 + "\nSECTION 2 — METRICS SUMMARY\n" + "="*60 + "\n")

        if not df_summary.empty:
            for theme in sorted(df_summary["theme"].unique()):
                f.write(f"\n### THEME: {theme}\n")
                sub = df_summary[df_summary["theme"] == theme]
                f.write("| Release | Total Rows | % Change |\n")
                f.write("|----------|-------------|----------|\n")
                for _, row in sub.iterrows():
                    pct = f"{row['pct_change']:.2f}%" if pd.notnull(row["pct_change"]) else "-"
                    f.write(f"| {row['release']} | {int(row['total_rows']):,} | {pct} |\n")
                f.write("\n")

        f.write("="*60 + "\nSECTION 3 — CHANGELOG SUMMARIES\n" + "="*60 + "\n")
        for rel, log in changelogs.items():
            f.write(f"\n### {rel}\n")
            f.write(log + "\n")

        f.write("="*60 + "\nSECTION 4 — SAMPLE PROMPTS\n" + "="*60 + "\n")
        prompts = [
            "Summarize major changes between the first and last releases.",
            "Which theme had the largest data growth?",
            "Find anomalies in row counts across releases.",
            "List schema or column changes mentioned in changelogs.",
            "Compare buildings vs addresses growth rate."
        ]
        for i, p in enumerate(prompts, 1):
            f.write(f"{i}. {p}\n")

        f.write("\n" + "="*60 + "\nSECTION 5 — METADATA\n" + "="*60 + "\n")
        f.write(f"Data Source: Overture Metrics\n")
        f.write(f"Generated on: {now}\n")
        f.write(f"Folder Structure: metrics/, theme_column_summary_stats/, theme_class_summary_stats/\n")
        f.write(f"License: ODbL 1.0\n")
        f.write(f"Contact: metrics@overture.org\n")

    print(f"✅ Prototype context file generated: {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_context_file()
