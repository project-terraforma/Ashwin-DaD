import os
import pandas as pd
from datetime import datetime

# ----------------------------
# CONFIGURATION
# ----------------------------
METRICS_BASE_DIR = "Metrics"  # Base Metrics folder
COLUMN_STATS_DIR = os.path.join(METRICS_BASE_DIR, "theme_column_summary_stats")  # Use this as primary source
CLASS_STATS_DIR = os.path.join(METRICS_BASE_DIR, "theme_class_summary_stats")
OUTPUT_FILE = "overture_metrics_context_v0.1.txt"
MAX_RELEASES = 10  # limit for compact summary


# ----------------------------
# HELPER FUNCTIONS
# ----------------------------
def get_releases_from_column_stats():
    """Extract release dates from theme_column_summary_stats filenames."""
    if not os.path.exists(COLUMN_STATS_DIR):
        print(f"⚠️ Column stats directory not found: {COLUMN_STATS_DIR}")
        return []
    
    releases = set()
    for filename in os.listdir(COLUMN_STATS_DIR):
        if filename.endswith('.csv'):
            # Extract release from filename like "2025-01-22.0.theme=addresses.type=address.csv"
            release = filename.split('.')[0] + '.' + filename.split('.')[1]
            releases.add(release)
    
    return sorted(list(releases))


def process_column_stats(releases):
    """Process theme column summary stats files and sum actual data values."""
    summaries = []
    
    for release in releases:
        pattern = f"{release}.theme="
        matching_files = [f for f in os.listdir(COLUMN_STATS_DIR) if f.startswith(pattern)]
        print(f"🔍 Processing release {release}: found {len(matching_files)} files")
        
        for filename in matching_files:
            # Parse filename: "2025-01-22.0.theme=addresses.type=address.csv"
            parts = filename.replace('.csv', '').split('.')
            theme = parts[2].replace('theme=', '')
            data_type = parts[3].replace('type=', '') if len(parts) > 3 else 'unknown'
            
            filepath = os.path.join(COLUMN_STATS_DIR, filename)
            try:
                df = pd.read_csv(filepath)
                print(f"📊 {theme} ({data_type}) - CSV shape: {df.shape}, columns: {df.columns.tolist()}")
                
                # Look for common count columns that might contain the actual data totals
                count_columns = [col for col in df.columns if 'count' in col.lower() or 'total' in col.lower()]
                
                if count_columns:
                    # Sum the first count column found
                    total_count = df[count_columns[0]].sum()
                    print(f"✅ Found count column '{count_columns[0]}', total: {total_count:,}")
                else:
                    # If no count column, check if there's a numeric column we can sum
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    if len(numeric_cols) > 0:
                        # Use the last numeric column (often the count/total)
                        count_col = numeric_cols[-1]
                        total_count = df[count_col].sum()
                        print(f"✅ Using numeric column '{count_col}', total: {total_count:,}")
                    else:
                        # Fallback to row count
                        total_count = len(df)
                        print(f"⚠️ No numeric columns found, using row count: {total_count}")
                
                summaries.append({
                    "release": release,
                    "theme": theme,
                    "type": data_type,
                    "total_rows": total_count,
                    "csv_rows": len(df)  # Keep track of CSV row count too
                })
                
            except Exception as e:
                print(f"⚠️ Error processing {filepath}: {e}")
    
    return pd.DataFrame(summaries)


def analyze_csv_structure(releases):
    """Analyze the structure of CSV files to understand the data better."""
    print("\n🔬 ANALYZING CSV STRUCTURE...")
    
    sample_files = []
    for release in releases[:2]:  # Just check first 2 releases
        pattern = f"{release}.theme="
        matching_files = [f for f in os.listdir(COLUMN_STATS_DIR) if f.startswith(pattern)]
        sample_files.extend(matching_files[:3])  # Take first 3 files from each release
    
    for filename in sample_files:
        filepath = os.path.join(COLUMN_STATS_DIR, filename)
        try:
            df = pd.read_csv(filepath)
            print(f"\n📄 File: {filename}")
            print(f"   Shape: {df.shape}")
            print(f"   Columns: {df.columns.tolist()}")
            if len(df) > 0:
                print(f"   Sample data:")
                print(f"   {df.head(2).to_string(index=False)}")
                
                # Show numeric column summaries
                numeric_cols = df.select_dtypes(include=['number']).columns
                if len(numeric_cols) > 0:
                    print(f"   Numeric totals:")
                    for col in numeric_cols:
                        print(f"     {col}: {df[col].sum():,}")
        except Exception as e:
            print(f"   ⚠️ Error reading {filename}: {e}")


def calculate_percent_changes(df_summary):
    """Add percentage change between releases per theme."""
    if df_summary.empty:
        print("⚠️ DataFrame is empty, skipping percentage calculations")
        return df_summary
        
    df_summary = df_summary.sort_values(by=["theme", "type", "release"])
    df_summary["pct_change"] = 0.0
    
    # Group by theme and type for percentage calculations
    for theme in df_summary["theme"].unique():
        for data_type in df_summary[df_summary["theme"] == theme]["type"].unique():
            mask = (df_summary["theme"] == theme) & (df_summary["type"] == data_type)
            df_summary.loc[mask, "pct_change"] = (
                df_summary[mask]["total_rows"].pct_change() * 100
            )
    
    return df_summary


def aggregate_by_theme(df_summary):
    """Aggregate data by theme across all types for simpler reporting."""
    if df_summary.empty:
        return df_summary
    
    # Group by release and theme, sum total_rows
    theme_summary = df_summary.groupby(["release", "theme"])["total_rows"].sum().reset_index()
    
    # Calculate percentage changes
    theme_summary = theme_summary.sort_values(by=["theme", "release"])
    theme_summary["pct_change"] = 0.0
    
    for theme in theme_summary["theme"].unique():
        mask = theme_summary["theme"] == theme
        theme_summary.loc[mask, "pct_change"] = (
            theme_summary[mask]["total_rows"].pct_change() * 100
        )
    
    return theme_summary


# ----------------------------
# MAIN GENERATION LOGIC
# ----------------------------
def generate_context_file():
    # Verify base directory exists
    if not os.path.exists(METRICS_BASE_DIR):
        print(f"❌ Metrics base directory not found: {METRICS_BASE_DIR}")
        print("Make sure you're running this script from the correct directory.")
        return
    
    print(f"✅ Found metrics base directory: {METRICS_BASE_DIR}")
    
    # Get releases from column stats files
    releases = get_releases_from_column_stats()
    if not releases:
        print("❌ No releases found in column stats directory.")
        return

    print(f"📅 Found {len(releases)} releases: {releases}")
    releases = releases[-MAX_RELEASES:]  # Limit recent releases
    print(f"📅 Processing last {len(releases)} releases: {releases}")
    
    # Analyze CSV structure first
    analyze_csv_structure(releases)
    
    # Process column stats data
    df_summary = process_column_stats(releases)
    
    if df_summary.empty:
        print("❌ No data found to process. Check your theme_column_summary_stats folder.")
        return
    
    print(f"📊 Processed {len(df_summary)} records")
    print(f"📊 Data summary:\n{df_summary.head(10)}")
    
    # Calculate percentage changes
    df_summary = calculate_percent_changes(df_summary)
    
    # Create aggregated theme summary for cleaner reporting
    theme_summary = aggregate_by_theme(df_summary)

    # Generate the context file
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        now = datetime.now().strftime("%B %d, %Y")
        f.write(f"# Overture Metrics LLM Context File v0.1\n")
        f.write(f"Generated: {now}\n")
        f.write(f"Releases: {releases[0]} → {releases[-1]}\n\n")

        f.write("="*60 + "\nSECTION 1 — OVERVIEW\n" + "="*60 + "\n")
        f.write("This file summarizes Overture's theme_column_summary_stats for LLM-based exploration.\n\n")
        f.write("Data Source: Pre-aggregated column statistics that compare total counts per release.\n")
        f.write("Themes include: addresses, base, buildings, divisions, places, and others.\n\n")

        f.write("="*60 + "\nSECTION 2 — THEME SUMMARY (AGGREGATED)\n" + "="*60 + "\n")
        
        if not theme_summary.empty:
            for theme in sorted(theme_summary["theme"].unique()):
                f.write(f"\n### THEME: {theme}\n")
                sub = theme_summary[theme_summary["theme"] == theme]
                f.write("| Release | Total Count | % Change |\n")
                f.write("|----------|-------------|----------|\n")
                for _, row in sub.iterrows():
                    pct = f"{row['pct_change']:.2f}%" if pd.notnull(row["pct_change"]) and row["pct_change"] != 0 else "-"
                    f.write(f"| {row['release']} | {int(row['total_rows']):,} | {pct} |\n")
                f.write("\n")

        f.write("="*60 + "\nSECTION 3 — DETAILED BREAKDOWN BY TYPE\n" + "="*60 + "\n")
        
        if not df_summary.empty:
            for theme in sorted(df_summary["theme"].unique()):
                f.write(f"\n### THEME: {theme}\n")
                theme_data = df_summary[df_summary["theme"] == theme]
                
                for data_type in sorted(theme_data["type"].unique()):
                    f.write(f"\n#### Type: {data_type}\n")
                    type_data = theme_data[theme_data["type"] == data_type]
                    f.write("| Release | Total Count | CSV Rows | % Change |\n")
                    f.write("|----------|-------------|----------|----------|\n")
                    for _, row in type_data.iterrows():
                        pct = f"{row['pct_change']:.2f}%" if pd.notnull(row["pct_change"]) and row["pct_change"] != 0 else "-"
                        f.write(f"| {row['release']} | {int(row['total_rows']):,} | {int(row['csv_rows'])} | {pct} |\n")
                    f.write("\n")

        f.write("="*60 + "\nSECTION 4 — SAMPLE PROMPTS\n" + "="*60 + "\n")
        prompts = [
            "Summarize major changes between the first and last releases.",
            "Which theme had the largest data growth?",
            "Find anomalies in row counts across releases.",
            "Compare buildings vs addresses growth rate.",
            "Which data types within themes show the most volatility?",
            "Identify themes with consistent growth patterns.",
            "What are the top 3 fastest growing themes?"
        ]
        for i, p in enumerate(prompts, 1):
            f.write(f"{i}. {p}\n")

        f.write("\n" + "="*60 + "\nSECTION 5 — METADATA\n" + "="*60 + "\n")
        f.write(f"Data Source: Overture theme_column_summary_stats\n")
        f.write(f"Generated on: {now}\n")
        f.write(f"Source Directory: {COLUMN_STATS_DIR}\n")
        f.write(f"Total Releases Processed: {len(releases)}\n")
        f.write(f"Total Records Analyzed: {len(df_summary)}\n")
        f.write(f"License: ODbL 1.0\n")
        f.write(f"Contact: metrics@overture.org\n")

    print(f"✅ Context file generated: {OUTPUT_FILE}")
    print(f"📊 Processed {len(releases)} releases with {len(df_summary)} total records")

    generate_prototype_file(df_summary, theme_summary, releases)

def generate_prototype_file(df_summary, theme_summary, releases):
    """Generate a compact prototype summary file based on processed data."""
    if df_summary.empty or theme_summary.empty:
        print("⚠️ Skipping prototype generation — no data available.")
        return
    
    output_path = "overture_metrics_prototype.md"
    now = datetime.now().strftime("%B %d, %Y")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(f"# Overture Metrics Prototype (auto-generated)\n")
        f.write(f"Generated: {now}\n\n")
        f.write(f"## Overview\n")
        f.write(f"Releases covered: {releases[0]} → {releases[-1]}\n")
        themes = ", ".join(sorted(theme_summary['theme'].unique()))
        f.write(f"Themes analyzed: {themes}\n\n")

        f.write(f"## Key Changes Summary\n")
        recent = theme_summary.groupby("theme").tail(1).sort_values("pct_change", ascending=False)
        for _, row in recent.iterrows():
            pct = row['pct_change']
            theme = row['theme']
            count = int(row['total_rows'])
            if pd.isna(pct) or pct == 0:
                f.write(f"- {theme}: {count:,} records (stable)\n")
            elif pct > 0:
                f.write(f"- {theme}: {count:,} records (grew +{pct:.1f}%)\n")
            else:
                f.write(f"- {theme}: {count:,} records (decreased {pct:.1f}%)\n")
        f.write("\n")

        f.write(f"## Theme Snapshots\n")
        for theme in sorted(theme_summary["theme"].unique()):
            f.write(f"### {theme}\n")
            sub = theme_summary[theme_summary["theme"] == theme].tail(2)
            f.write("| Release | Records | Δ% |\n|----------|---------|----|\n")
            for _, row in sub.iterrows():
                pct = f"{row['pct_change']:.1f}%" if pd.notnull(row['pct_change']) and row['pct_change'] != 0 else "-"
                f.write(f"| {row['release']} | {int(row['total_rows']):,} | {pct} |\n")
            f.write("\n")

        f.write(f"## Notes\n")
        f.write("This file provides a quick summary of recent Overture metrics.\n")
        f.write("Data represents actual record counts from theme column summary statistics.\n")

    print(f"✅ Prototype file generated: {output_path}")


if __name__ == "__main__":
    generate_context_file()
