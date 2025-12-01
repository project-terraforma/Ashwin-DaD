"""
Analyze Overture Metrics CSV files to extract:
1. Top categorical values for key grouping columns
2. Summary statistics per theme
3. Distribution of change_types
"""

import pandas as pd
import glob
import os
from collections import defaultdict
from pathlib import Path

# Configuration
METRICS_BASE = "Metrics/metrics"
LATEST_RELEASE = "2025-08-20.1"  # Use the latest release
METRICS_PATH = f"{METRICS_BASE}/{LATEST_RELEASE}"

# Grouping columns to analyze by theme
GROUPING_COLUMNS = {
    'addresses': ['country', 'address_level_1', 'address_level_2', 'datasets', 'change_type'],
    'buildings': ['subtype', 'class', 'datasets', 'change_type'],
    'base': ['subtype', 'class', 'datasets', 'change_type'],
    'places': ['place_countries', 'primary_category', 'confidence', 'datasets', 'change_type'],
    'divisions': ['subtype', 'class', 'country', 'datasets', 'change_type'],
    'transportation': ['subtype', 'class', 'subclass', 'datasets', 'change_type']
}


def analyze_csv_files(theme, csv_pattern):
    """Analyze all CSV files for a given theme"""
    files = glob.glob(csv_pattern)

    if not files:
        print(f"No files found for pattern: {csv_pattern}")
        return None

    print(f"\n{'='*80}")
    print(f"Analyzing {theme.upper()} theme - Found {len(files)} files")
    print(f"{'='*80}")

    # Concatenate all CSV files for this theme
    dfs = []
    for file in files:
        try:
            df = pd.read_csv(file)
            dfs.append(df)
        except Exception as e:
            print(f"Error reading {file}: {e}")

    if not dfs:
        return None

    combined_df = pd.concat(dfs, ignore_index=True)

    # Get total count
    total_records = len(combined_df)
    total_features = combined_df['total_count'].sum() if 'total_count' in combined_df.columns else combined_df['id_count'].sum()

    print(f"\nTotal Records: {total_records:,}")
    print(f"Total Feature Count: {total_features:,}")

    # Analyze each grouping column
    results = {
        'theme': theme,
        'total_records': total_records,
        'total_features': total_features,
        'column_analysis': {}
    }

    columns_to_analyze = GROUPING_COLUMNS.get(theme, [])

    for col in columns_to_analyze:
        if col not in combined_df.columns:
            continue

        print(f"\n{'-'*60}")
        print(f"Column: {col}")
        print(f"{'-'*60}")

        # Get value counts
        if 'total_count' in combined_df.columns:
            # Aggregate by grouping column
            value_counts = combined_df.groupby(col)['total_count'].sum().sort_values(ascending=False)
        elif 'id_count' in combined_df.columns:
            value_counts = combined_df.groupby(col)['id_count'].sum().sort_values(ascending=False)
        else:
            value_counts = combined_df[col].value_counts()

        # Top 15 values
        top_values = value_counts.head(15)
        total = value_counts.sum()

        results['column_analysis'][col] = {
            'unique_values': len(value_counts),
            'top_values': []
        }

        for value, count in top_values.items():
            percentage = (count / total * 100) if total > 0 else 0
            print(f"  {value}: {count:,} ({percentage:.2f}%)")
            results['column_analysis'][col]['top_values'].append({
                'value': value,
                'count': count,
                'percentage': percentage
            })

    return results


def main():
    """Main analysis function"""
    all_results = {}

    # Analyze each theme
    theme_patterns = {
        'addresses': f"{METRICS_PATH}/row_counts/theme=addresses/**/*.csv",
        'buildings': f"{METRICS_PATH}/row_counts/theme=buildings/**/*.csv",
        'base': f"{METRICS_PATH}/row_counts/theme=base/**/*.csv",
        'places': f"{METRICS_PATH}/row_counts/theme=places/**/*.csv",
        'divisions': f"{METRICS_PATH}/row_counts/theme=divisions/**/*.csv",
        'transportation': f"{METRICS_PATH}/row_counts/theme=transportation/**/*.csv"
    }

    for theme, pattern in theme_patterns.items():
        result = analyze_csv_files(theme, pattern)
        if result:
            all_results[theme] = result

    # Analyze changelog stats
    changelog_file = f"{METRICS_PATH}/changelog_stats/*.csv"
    changelog_files = glob.glob(changelog_file)
    if changelog_files:
        print(f"\n{'='*80}")
        print(f"Analyzing CHANGELOG STATS")
        print(f"{'='*80}")
        df = pd.read_csv(changelog_files[0])
        print("\nRelease Summary:")
        print(df.to_string(index=False))

    # Save results summary
    output_file = "metrics_analysis_summary.txt"
    with open(output_file, 'w') as f:
        for theme, result in all_results.items():
            f.write(f"\n{'='*80}\n")
            f.write(f"{theme.upper()} THEME\n")
            f.write(f"{'='*80}\n")
            f.write(f"Total Records: {result['total_records']:,}\n")
            f.write(f"Total Features: {result['total_features']:,}\n")

            for col, analysis in result['column_analysis'].items():
                f.write(f"\n{col}:\n")
                f.write(f"  Unique Values: {analysis['unique_values']}\n")
                f.write(f"  Top Values:\n")
                for item in analysis['top_values'][:10]:
                    f.write(f"    {item['value']}: {item['count']:,} ({item['percentage']:.2f}%)\n")

    print(f"\n\nAnalysis complete! Results saved to {output_file}")


if __name__ == "__main__":
    main()
