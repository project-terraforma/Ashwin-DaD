"""
Generate LLM-readable context document from Overture Metrics data.

This script:
1. Analyzes all metrics CSV files
2. Extracts schema information and statistics
3. Generates a comprehensive, LLM-ready text file
"""

import pandas as pd
import glob
import os
from datetime import datetime
from pathlib import Path

# Configuration
METRICS_BASE = "Metrics/metrics"
OUTPUT_FILE = "README_generation_output.txt"

# Schema definitions (could be externalized to a config file)
COLUMN_DEFINITIONS = {
    'datasets': {
        'definition': 'The original source(s) of the feature data',
        'type': 'String (comma-separated for multiple sources)',
        'notes': 'Common values include OpenStreetMap, Microsoft ML Buildings, Google Open Buildings, Meta, ESA WorldCover, and others'
    },
    'change_type': {
        'definition': "Feature's status compared to the previous Overture release",
        'type': 'Enumerated string',
        'values': {
            'unchanged': 'Feature exists in both releases with identical data',
            'data_changed': 'Feature exists in both but has modified attributes',
            'added': 'New feature in this release',
            'removed': 'Feature existed in previous release but not current'
        }
    },
    'country': {
        'definition': 'ISO 3166-1 Alpha-2 country code',
        'type': '2-character string',
        'examples': 'US, BR, IN, CN, GB',
        'usage': 'Identifies the country where the feature is located'
    },
    'address_level_1': {
        'definition': 'First-level administrative division (state/province)',
        'type': 'String',
        'examples': 'California, Oaxaca, Ontario, Queensland',
        'notes': 'Meaning varies by country (US: state, Canada: province, etc.)'
    },
    'address_level_2': {
        'definition': 'Second-level administrative division (county/municipality)',
        'type': 'String',
        'examples': 'Los Angeles County, Santa Cruz Amilpas',
        'notes': 'May represent city, county, or district depending on country'
    },
    'address_level_3': {
        'definition': 'Third-level administrative division (neighborhood/district)',
        'type': 'String',
        'notes': 'Optional; not all countries use three address levels'
    },
    'subtype': {
        'definition': 'Broad category of the feature (meaning varies by theme)',
        'type': 'Enumerated string',
        'notes': 'Buildings: use type (residential, commercial, etc.); Transportation: pathway type (road, rail, water); Base: feature category; Divisions: administrative level'
    },
    'class': {
        'definition': 'More specific classification within the subtype',
        'type': 'Enumerated string',
        'notes': 'Provides finer granularity than subtype'
    },
    'subclass': {
        'definition': 'Optional refinement of class (primarily in Transportation)',
        'type': 'Enumerated string',
        'examples': 'driveway, parking_aisle, sidewalk, link, crosswalk, alley'
    },
    'place_countries': {
        'definition': 'ISO 3166-1 Alpha-2 code for the country where place is located',
        'type': '2-character string',
        'usage': 'Identifies place location in Places theme'
    },
    'primary_category': {
        'definition': "Main category describing the place's purpose or service",
        'type': 'String',
        'notes': 'Over 2,000 unique categories exist in Places theme'
    },
    'confidence': {
        'definition': 'Numerical score indicating certainty of place existence',
        'type': 'Float (0.0 to 1.0)',
        'interpretation': '1.0 = verified/confirmed; 0.5-0.8 = moderate confidence; 0.0 = permanently closed or does not exist',
        'notes': 'This is NOT operating hours; it is existence certainty'
    }
}

THEME_DESCRIPTIONS = {
    'addresses': {
        'title': 'ADDRESSES',
        'description': 'Address points with hierarchical administrative levels',
        'feature_count_label': 'addresses',
        'key_points': [
            'Simplified, worldwide address schema based primarily on OpenAddresses',
            'Includes hierarchical administrative levels (address_level_1, 2, 3)',
            'Coverage varies significantly by country'
        ]
    },
    'buildings': {
        'title': 'BUILDINGS',
        'description': 'Building footprints categorized by use and construction details',
        'feature_count_label': 'buildings',
        'key_points': [
            'Categorized by use (residential, commercial, industrial, etc.)',
            'Sources: Google Open Buildings, Microsoft ML Buildings, OpenStreetMap',
            'Includes detailed attributes: height, floors, construction details'
        ]
    },
    'places': {
        'title': 'PLACES',
        'description': 'Points of interest including businesses, landmarks, and amenities',
        'feature_count_label': 'places',
        'key_points': [
            'Businesses, landmarks, amenities, and services worldwide',
            'Confidence scores indicate data quality (0.0 to 1.0)',
            'Primary sources: Meta, Microsoft',
            'Over 2,000 unique place categories'
        ]
    },
    'divisions': {
        'title': 'DIVISIONS',
        'description': 'Administrative boundaries and divisions',
        'feature_count_label': 'divisions',
        'key_points': [
            'Nine administrative levels: country → dependency → region → county → localadmin → locality → macrohood → neighborhood → microhood',
            'Translated into 40+ languages',
            'Includes population data and administrative hierarchies'
        ]
    },
    'transportation': {
        'title': 'TRANSPORTATION',
        'description': 'Transportation network including roads, rails, and waterways',
        'feature_count_label': 'features',
        'key_points': [
            'Includes segments (pathways) and connectors (intersections)',
            'Detailed routing attributes: speed limits, access restrictions, surface types',
            'Primarily road data with some rail and water routes'
        ]
    },
    'base': {
        'title': 'BASE',
        'description': 'Contextual features including land, water, and infrastructure',
        'feature_count_label': 'features',
        'key_points': [
            'Six feature types: land, water, land_cover, land_use, infrastructure, bathymetry',
            'Includes natural features (forests, streams) and infrastructure (bridges, power lines)',
            'Land cover data from ESA WorldCover 2020 (10m resolution)'
        ]
    }
}


def get_latest_release():
    """Find the most recent release directory"""
    releases = glob.glob(f"{METRICS_BASE}/*/")
    if not releases:
        raise FileNotFoundError(f"No releases found in {METRICS_BASE}")

    # Extract release dates and sort
    release_dates = []
    for r in releases:
        release_name = os.path.basename(r.rstrip('/'))
        release_dates.append(release_name)

    release_dates.sort(reverse=True)
    return release_dates[0]


def analyze_theme_data(theme, release):
    """Analyze all CSV files for a given theme"""
    pattern = f"{METRICS_BASE}/{release}/row_counts/theme={theme}/**/*.csv"
    files = glob.glob(pattern, recursive=True)

    if not files:
        return None

    # Concatenate all CSV files
    dfs = []
    for file in files:
        try:
            df = pd.read_csv(file, on_bad_lines='skip')
            dfs.append(df)
        except Exception as e:
            print(f"Warning: Error reading {file}: {e}")
            continue

    if not dfs:
        return None

    combined_df = pd.concat(dfs, ignore_index=True)

    # Determine count column
    count_col = 'total_count' if 'total_count' in combined_df.columns else 'id_count'
    if count_col not in combined_df.columns:
        count_col = None

    result = {
        'total_records': len(combined_df),
        'total_features': combined_df[count_col].sum() if count_col else 0,
        'columns': {}
    }

    # Analyze each column
    for col in combined_df.columns:
        if col in ['total_count', 'id_count', 'geometry_count', 'bbox_count', 'version_count',
                   'sources_count', 'average_geometry_length_km', 'total_geometry_length_km',
                   'average_geometry_area_km2', 'total_geometry_area_km2']:
            continue  # Skip metric columns

        if combined_df[col].dtype == 'object' or combined_df[col].dtype.name == 'category':
            # Aggregate by column value
            if count_col:
                value_counts = combined_df.groupby(col)[count_col].sum().sort_values(ascending=False)
            else:
                value_counts = combined_df[col].value_counts()

            total = value_counts.sum()

            result['columns'][col] = {
                'unique_count': len(value_counts),
                'top_values': []
            }

            for value, count in value_counts.head(15).items():
                percentage = (count / total * 100) if total > 0 else 0
                result['columns'][col]['top_values'].append({
                    'value': str(value),
                    'count': int(count),
                    'percentage': percentage
                })

    return result


def load_changelog_stats(release):
    """Load changelog statistics"""
    pattern = f"{METRICS_BASE}/{release}/changelog_stats/*.csv"
    files = glob.glob(pattern)

    if not files:
        return None

    try:
        df = pd.read_csv(files[0], sep='\t')
        return df
    except:
        return None


def format_large_number(num):
    """Format large numbers with proper suffixes"""
    if num >= 1_000_000_000:
        return f"{num/1_000_000_000:.2f}B"
    elif num >= 1_000_000:
        return f"{num/1_000_000:.2f}M"
    elif num >= 1_000:
        return f"{num/1_000:.2f}K"
    else:
        return str(num)


def generate_document():
    """Main function to generate the LLM context document"""

    print("=" * 80)
    print("GENERATING LLM CONTEXT DOCUMENT")
    print("=" * 80)

    # Find latest release
    latest_release = get_latest_release()
    print(f"\nUsing release: {latest_release}")

    # Analyze all themes
    print("\nAnalyzing themes...")
    themes_data = {}
    for theme in ['addresses', 'buildings', 'places', 'divisions', 'transportation', 'base']:
        print(f"  - {theme}...")
        data = analyze_theme_data(theme, latest_release)
        if data:
            themes_data[theme] = data

    # Load changelog
    print("\nLoading changelog statistics...")
    changelog = load_changelog_stats(latest_release)

    # Generate document
    print(f"\nGenerating {OUTPUT_FILE}...")

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        # Header
        f.write("=" * 80 + "\n")
        f.write("OVERTURE MAPS DATA - LLM EXPLORATION GUIDE\n")
        f.write("=" * 80 + "\n")
        f.write(f"Release Version: {latest_release}\n")
        f.write("Document Purpose: Enable natural language querying of Overture Maps data\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

        # Instructions
        f.write("<<<INSTRUCTIONS_START>>>\n\n")
        f.write("## YOUR ROLE\n")
        f.write("You are a data analyst assistant helping users understand and explore Overture Maps\n")
        f.write("data. This document contains comprehensive statistics, schema definitions, and\n")
        f.write("context about the Overture Maps Foundation's open geospatial datasets.\n\n")

        f.write("## HOW TO USE THIS DOCUMENT\n")
        f.write("- Answer user questions about data distributions, coverage, and characteristics\n")
        f.write("- Provide specific numbers, percentages, and comparisons when available\n")
        f.write("- Reference the schema definitions to explain data structure\n")
        f.write("- Use the statistics sections to support your analysis\n")
        f.write("- Be precise and cite specific metrics from this document\n\n")

        f.write("## KEY CONSTRAINTS\n")
        f.write(f"- Data is from release {latest_release} only\n")
        f.write("- All statistics represent aggregated counts across multiple data sources\n")
        f.write("- Some themes may have data quality variations by geographic region\n")
        f.write("- Confidence scores in Places theme range from 0.0 (closed/doesn't exist) to 1.0 (verified)\n\n")

        f.write("<<<INSTRUCTIONS_END>>>\n\n\n")

        # Overview
        f.write("=" * 80 + "\n")
        f.write("## OVERTURE MAPS FOUNDATION OVERVIEW\n")
        f.write("=" * 80 + "\n\n")

        f.write("Overture Maps Foundation is an open data initiative that provides free,\n")
        f.write("interoperable geospatial datasets for mapping applications worldwide. The data\n")
        f.write("is released as GeoParquet files with a JSON schema definition, using GeoJSON\n")
        f.write("as the canonical geospatial format.\n\n")

        f.write("### THE SIX DATA THEMES\n\n")

        for theme, info in THEME_DESCRIPTIONS.items():
            if theme in themes_data:
                data = themes_data[theme]
                f.write(f"**{info['title']}**\n")
                f.write(f"   - {format_large_number(data['total_features'])} {info['feature_count_label']}\n")
                f.write(f"   - {info['description']}\n")
                for point in info['key_points']:
                    f.write(f"   - {point}\n")
                f.write("\n")

        # Schema Reference
        f.write("\n" + "=" * 80 + "\n")
        f.write("<<<SCHEMA_START>>>\n")
        f.write("## SCHEMA REFERENCE - GROUPING COLUMNS\n")
        f.write("=" * 80 + "\n\n")

        f.write("This section defines the key columns used to categorize and group data across\n")
        f.write("all themes. Understanding these columns is essential for querying the data.\n\n")

        # Universal columns
        f.write("---\n### UNIVERSAL COLUMNS (All Themes)\n---\n\n")
        for col in ['datasets', 'change_type']:
            if col in COLUMN_DEFINITIONS:
                defn = COLUMN_DEFINITIONS[col]
                f.write(f"**{col}**\n")
                f.write(f"Definition: {defn['definition']}\n")
                f.write(f"Type: {defn['type']}\n")
                if 'values' in defn:
                    f.write("Possible Values:\n")
                    for val, desc in defn['values'].items():
                        f.write(f"  - {val}: {desc}\n")
                if 'notes' in defn:
                    f.write(f"Notes: {defn['notes']}\n")
                f.write("\n")

        # Theme-specific columns
        theme_columns = {
            'ADDRESSES THEME': ['country', 'address_level_1', 'address_level_2', 'address_level_3'],
            'BUILDINGS THEME': ['subtype', 'class'],
            'PLACES THEME': ['place_countries', 'primary_category', 'confidence'],
            'DIVISIONS THEME': ['subtype', 'class', 'country'],
            'TRANSPORTATION THEME': ['subtype', 'class', 'subclass'],
            'BASE THEME': ['subtype', 'class']
        }

        for section, columns in theme_columns.items():
            f.write(f"---\n### {section} COLUMNS\n---\n\n")
            for col in columns:
                if col in COLUMN_DEFINITIONS:
                    defn = COLUMN_DEFINITIONS[col]
                    f.write(f"**{col}**\n")
                    f.write(f"Definition: {defn['definition']}\n")
                    f.write(f"Type: {defn['type']}\n")
                    if 'examples' in defn:
                        f.write(f"Examples: {defn['examples']}\n")
                    if 'usage' in defn:
                        f.write(f"Usage: {defn['usage']}\n")
                    if 'interpretation' in defn:
                        f.write(f"Interpretation: {defn['interpretation']}\n")
                    if 'notes' in defn:
                        f.write(f"Notes: {defn['notes']}\n")
                    f.write("\n")

        f.write("<<<SCHEMA_END>>>\n\n\n")

        # Theme Statistics
        for theme, data in themes_data.items():
            info = THEME_DESCRIPTIONS[theme]

            f.write("=" * 80 + "\n")
            f.write(f"## THEME STATISTICS: {info['title']}\n")
            f.write("=" * 80 + "\n\n")

            f.write(f"**Total Features**: {data['total_features']:,} {info['feature_count_label']}\n\n")

            # Changelog info if available
            if changelog is not None:
                theme_changelog = changelog[changelog['theme'] == theme]
                if not theme_changelog.empty:
                    f.write("**Release Comparison** (vs. baseline):\n")
                    for _, row in theme_changelog.iterrows():
                        f.write(f"  Type: {row['type']}\n")
                        f.write(f"  - Total Change: {row['total_diff_perc']:.2f}%\n")
                        f.write(f"  - Added: {int(row['added']):,} ({row['added_perc']:.2f}%)\n")
                        f.write(f"  - Removed: {int(row['removed']):,} ({row['removed_perc']:.2f}%)\n")
                        f.write(f"  - Data Changed: {int(row['data_changed']):,} ({row['data_changed_perc']:.2f}%)\n")
                        f.write(f"  - Unchanged: {int(row['unchanged']):,} ({row['unchanged_perc']:.2f}%)\n")
                    f.write("\n")

            # Column statistics
            for col, col_data in data['columns'].items():
                if col in ['change_type', 'datasets', 'subtype', 'class', 'subclass',
                           'country', 'place_countries', 'primary_category', 'confidence',
                           'address_level_1', 'address_level_2']:

                    f.write(f"**{col.replace('_', ' ').title()}**:\n")
                    f.write(f"  Unique Values: {col_data['unique_count']}\n")

                    if col_data['top_values']:
                        f.write(f"  Top Values:\n")
                        for item in col_data['top_values'][:10]:
                            f.write(f"    {item['value']}: {item['count']:,} ({item['percentage']:.2f}%)\n")
                    f.write("\n")

            f.write("\n")

        # Suggested Prompts
        f.write("=" * 80 + "\n")
        f.write("<<<PROMPTS_START>>>\n")
        f.write("## SUGGESTED EXPLORATION PROMPTS\n")
        f.write("=" * 80 + "\n\n")

        f.write("Use these prompts to begin exploring the Overture Maps data. Each prompt is\n")
        f.write("designed to leverage the statistics and schema information in this document.\n\n")

        prompts = [
            ("Geographic Distribution", [
                "Which countries have the highest concentration of Places data? Show me the top 10 countries and their percentages.",
                "Compare the distribution of Divisions data across China, India, and the United States.",
                "What percentage of global building data comes from each data source?"
            ]),
            ("Data Quality & Confidence", [
                "What proportion of Places have high confidence scores (0.8 or above)?",
                "In the Buildings theme, how much data changed between releases?",
                "Which themes had no changes in this release?"
            ]),
            ("Category Analysis", [
                "What are the top 10 most common building types globally?",
                "For the Places theme, list the top 15 primary categories.",
                "In Transportation, what's the breakdown between road, rail, and water segments?"
            ]),
            ("Comparative Insights", [
                "Compare the data source distribution across all six themes.",
                "Which theme has the most diverse categorical values?",
                "What are the most common road classes in the Transportation theme?"
            ])
        ]

        for category, prompt_list in prompts:
            f.write(f"### {category}\n\n")
            for i, prompt in enumerate(prompt_list, 1):
                f.write(f"{i}. \"{prompt}\"\n\n")

        f.write("<<<PROMPTS_END>>>\n\n\n")

        # Additional Resources
        f.write("=" * 80 + "\n")
        f.write("## ADDITIONAL RESOURCES\n")
        f.write("=" * 80 + "\n\n")

        f.write("**Official Documentation**:\n")
        f.write("  - Overture Maps Documentation: https://docs.overturemaps.org/\n")
        f.write("  - Schema Reference: https://docs.overturemaps.org/schema/reference/\n")
        f.write("  - Data Guides: https://docs.overturemaps.org/guides/\n\n")

        f.write("**Data Sources**:\n")
        f.write("  - OpenStreetMap: https://www.openstreetmap.org/\n")
        f.write("  - ESA WorldCover: https://worldcover.esa.int/\n")
        f.write("  - Overture GitHub: https://github.com/OvertureMaps/data\n\n")

        f.write("=" * 80 + "\n")
        f.write("END OF DOCUMENT\n")
        f.write("=" * 80 + "\n")

    print(f"\n✓ Document generated successfully: {OUTPUT_FILE}")
    print(f"  File size: {os.path.getsize(OUTPUT_FILE) / 1024:.1f} KB")
    print("\nYou can now load this file into an LLM for natural language querying!")


if __name__ == "__main__":
    generate_document()
