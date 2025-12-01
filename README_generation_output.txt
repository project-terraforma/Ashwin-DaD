================================================================================
OVERTURE MAPS DATA - LLM EXPLORATION GUIDE
================================================================================
Release Version: 2025-09-24.0
Document Purpose: Enable natural language querying of Overture Maps data
Generated: 2025-11-27 17:19:37

<<<INSTRUCTIONS_START>>>

## YOUR ROLE
You are a data analyst assistant helping users understand and explore Overture Maps
data. This document contains comprehensive statistics, schema definitions, and
context about the Overture Maps Foundation's open geospatial datasets.

## HOW TO USE THIS DOCUMENT
- Answer user questions about data distributions, coverage, and characteristics
- Provide specific numbers, percentages, and comparisons when available
- Reference the schema definitions to explain data structure
- Use the statistics sections to support your analysis
- Be precise and cite specific metrics from this document

## KEY CONSTRAINTS
- Data is from release 2025-09-24.0 only
- All statistics represent aggregated counts across multiple data sources
- Some themes may have data quality variations by geographic region
- Confidence scores in Places theme range from 0.0 (closed/doesn't exist) to 1.0 (verified)

<<<INSTRUCTIONS_END>>>


================================================================================
## OVERTURE MAPS FOUNDATION OVERVIEW
================================================================================

Overture Maps Foundation is an open data initiative that provides free,
interoperable geospatial datasets for mapping applications worldwide. The data
is released as GeoParquet files with a JSON schema definition, using GeoJSON
as the canonical geospatial format.

### THE SIX DATA THEMES

**ADDRESSES**
   - 445.93M addresses
   - Address points with hierarchical administrative levels
   - Simplified, worldwide address schema based primarily on OpenAddresses
   - Includes hierarchical administrative levels (address_level_1, 2, 3)
   - Coverage varies significantly by country

**BUILDINGS**
   - 5.08B buildings
   - Building footprints categorized by use and construction details
   - Categorized by use (residential, commercial, industrial, etc.)
   - Sources: Google Open Buildings, Microsoft ML Buildings, OpenStreetMap
   - Includes detailed attributes: height, floors, construction details

**PLACES**
   - 143.25M places
   - Points of interest including businesses, landmarks, and amenities
   - Businesses, landmarks, amenities, and services worldwide
   - Confidence scores indicate data quality (0.0 to 1.0)
   - Primary sources: Meta, Microsoft
   - Over 2,000 unique place categories

**DIVISIONS**
   - 11.18M divisions
   - Administrative boundaries and divisions
   - Nine administrative levels: country → dependency → region → county → localadmin → locality → macrohood → neighborhood → microhood
   - Translated into 40+ languages
   - Includes population data and administrative hierarchies

**TRANSPORTATION**
   - 1.43B features
   - Transportation network including roads, rails, and waterways
   - Includes segments (pathways) and connectors (intersections)
   - Detailed routing attributes: speed limits, access restrictions, surface types
   - Primarily road data with some rail and water routes

**BASE**
   - 763.87M features
   - Contextual features including land, water, and infrastructure
   - Six feature types: land, water, land_cover, land_use, infrastructure, bathymetry
   - Includes natural features (forests, streams) and infrastructure (bridges, power lines)
   - Land cover data from ESA WorldCover 2020 (10m resolution)


================================================================================
<<<SCHEMA_START>>>
## SCHEMA REFERENCE - GROUPING COLUMNS
================================================================================

This section defines the key columns used to categorize and group data across
all themes. Understanding these columns is essential for querying the data.

---
### UNIVERSAL COLUMNS (All Themes)
---

**datasets**
Definition: The original source(s) of the feature data
Type: String (comma-separated for multiple sources)
Notes: Common values include OpenStreetMap, Microsoft ML Buildings, Google Open Buildings, Meta, ESA WorldCover, and others

**change_type**
Definition: Feature's status compared to the previous Overture release
Type: Enumerated string
Possible Values:
  - unchanged: Feature exists in both releases with identical data
  - data_changed: Feature exists in both but has modified attributes
  - added: New feature in this release
  - removed: Feature existed in previous release but not current

---
### ADDRESSES THEME COLUMNS
---

**country**
Definition: ISO 3166-1 Alpha-2 country code
Type: 2-character string
Examples: US, BR, IN, CN, GB
Usage: Identifies the country where the feature is located

**address_level_1**
Definition: First-level administrative division (state/province)
Type: String
Examples: California, Oaxaca, Ontario, Queensland
Notes: Meaning varies by country (US: state, Canada: province, etc.)

**address_level_2**
Definition: Second-level administrative division (county/municipality)
Type: String
Examples: Los Angeles County, Santa Cruz Amilpas
Notes: May represent city, county, or district depending on country

**address_level_3**
Definition: Third-level administrative division (neighborhood/district)
Type: String
Notes: Optional; not all countries use three address levels

---
### BUILDINGS THEME COLUMNS
---

**subtype**
Definition: Broad category of the feature (meaning varies by theme)
Type: Enumerated string
Notes: Buildings: use type (residential, commercial, etc.); Transportation: pathway type (road, rail, water); Base: feature category; Divisions: administrative level

**class**
Definition: More specific classification within the subtype
Type: Enumerated string
Notes: Provides finer granularity than subtype

---
### PLACES THEME COLUMNS
---

**place_countries**
Definition: ISO 3166-1 Alpha-2 code for the country where place is located
Type: 2-character string
Usage: Identifies place location in Places theme

**primary_category**
Definition: Main category describing the place's purpose or service
Type: String
Notes: Over 2,000 unique categories exist in Places theme

**confidence**
Definition: Numerical score indicating certainty of place existence
Type: Float (0.0 to 1.0)
Interpretation: 1.0 = verified/confirmed; 0.5-0.8 = moderate confidence; 0.0 = permanently closed or does not exist
Notes: This is NOT operating hours; it is existence certainty

---
### DIVISIONS THEME COLUMNS
---

**subtype**
Definition: Broad category of the feature (meaning varies by theme)
Type: Enumerated string
Notes: Buildings: use type (residential, commercial, etc.); Transportation: pathway type (road, rail, water); Base: feature category; Divisions: administrative level

**class**
Definition: More specific classification within the subtype
Type: Enumerated string
Notes: Provides finer granularity than subtype

**country**
Definition: ISO 3166-1 Alpha-2 country code
Type: 2-character string
Examples: US, BR, IN, CN, GB
Usage: Identifies the country where the feature is located

---
### TRANSPORTATION THEME COLUMNS
---

**subtype**
Definition: Broad category of the feature (meaning varies by theme)
Type: Enumerated string
Notes: Buildings: use type (residential, commercial, etc.); Transportation: pathway type (road, rail, water); Base: feature category; Divisions: administrative level

**class**
Definition: More specific classification within the subtype
Type: Enumerated string
Notes: Provides finer granularity than subtype

**subclass**
Definition: Optional refinement of class (primarily in Transportation)
Type: Enumerated string
Examples: driveway, parking_aisle, sidewalk, link, crosswalk, alley

---
### BASE THEME COLUMNS
---

**subtype**
Definition: Broad category of the feature (meaning varies by theme)
Type: Enumerated string
Notes: Buildings: use type (residential, commercial, etc.); Transportation: pathway type (road, rail, water); Base: feature category; Divisions: administrative level

**class**
Definition: More specific classification within the subtype
Type: Enumerated string
Notes: Provides finer granularity than subtype

<<<SCHEMA_END>>>


================================================================================
## THEME STATISTICS: ADDRESSES
================================================================================

**Total Features**: 445,932,761 addresses

**Release Comparison** (vs. baseline):
  Type: address
  - Total Change: 0.00%
  - Added: 0 (0.00%)
  - Removed: 0 (0.00%)
  - Data Changed: 0 (0.00%)
  - Unchanged: 446,544,475 (100.00%)

**Country**:
  Unique Values: 37
  Top Values:
    US: 112,368,106 (25.20%)
    BR: 89,819,678 (20.14%)
    MX: 28,380,668 (6.36%)
    FR: 26,041,619 (5.84%)
    IT: 25,924,802 (5.81%)
    JP: 19,553,779 (4.38%)
    CA: 17,062,677 (3.83%)
    DE: 15,827,023 (3.55%)
    AU: 15,673,903 (3.51%)
    ES: 13,185,788 (2.96%)

**Datasets**:
  Unique Values: 177
  Top Values:
    br_ibge: 89,819,678 (20.14%)
    NAD: 74,814,222 (16.78%)
    OpenAddresses/AddressForAll/INEGI: 28,380,668 (6.36%)
    OpenAddresses/adresse.data.gouv.fr: 26,041,619 (5.84%)
    OpenAddresses/Istat e dall'Agenzia delle Entrate: 25,924,802 (5.81%)
    OpenAddresses/Japanese Ministry of Land, Infrastructure and Transport: 19,553,779 (4.38%)
    OpenAddresses/Statistics Canada: 17,038,770 (3.82%)
    OpenAddresses/Geoscape Australia: 15,673,903 (3.51%)
    OpenAddresses/scne.es: 13,185,788 (2.96%)
    OpenAddresses/NGR: 9,845,860 (2.21%)

**Address Level 1**:
  Unique Values: 151030
  Top Values:
    SP: 17,434,203 (3.92%)
    CA: 14,541,127 (3.27%)
    FL: 10,489,171 (2.36%)
    MG: 9,962,739 (2.24%)
    TX: 9,799,798 (2.20%)
    BA: 7,693,202 (1.73%)
    MA: 6,594,386 (1.48%)
    RJ: 6,496,070 (1.46%)
    NY: 6,482,888 (1.46%)
    ON: 6,206,742 (1.40%)

**Address Level 2**:
  Unique Values: 51152
  Top Values:
    São Paulo: 3,503,297 (1.10%)
    UNINCORPORATED: 2,004,358 (0.63%)
    Rio de Janeiro: 1,798,005 (0.57%)
    Roma: 1,075,327 (0.34%)
    Bogotá Distrito Capital: 1,075,087 (0.34%)
    New York: 967,732 (0.30%)
    Salvador: 943,583 (0.30%)
    Brasília: 941,191 (0.30%)
    Fortaleza: 867,970 (0.27%)
    Belo Horizonte: 748,157 (0.24%)

**Change Type**:
  Unique Values: 1
  Top Values:
    unchanged: 445,932,761 (100.00%)


================================================================================
## THEME STATISTICS: BUILDINGS
================================================================================

**Total Features**: 5,076,549,472 buildings

**Release Comparison** (vs. baseline):
  Type: building
  - Total Change: -0.17%
  - Added: 4,479,724 (0.18%)
  - Removed: 8,798,318 (0.35%)
  - Data Changed: 3,076,432 (0.12%)
  - Unchanged: 2,527,295,734 (99.53%)
  Type: building_part
  - Total Change: 1.17%
  - Added: 43,177 (1.28%)
  - Removed: 3,507 (0.10%)
  - Data Changed: 23,246 (0.69%)
  - Unchanged: 3,356,423 (99.21%)

**Subtype**:
  Unique Values: 13
  Top Values:
    residential: 220,944,752 (80.79%)
    outbuilding: 16,035,270 (5.86%)
    commercial: 9,116,418 (3.33%)
    agricultural: 8,744,346 (3.20%)
    industrial: 7,142,798 (2.61%)
    education: 3,433,476 (1.26%)
    religious: 2,192,822 (0.80%)
    civic: 2,108,358 (0.77%)
    service: 1,712,644 (0.63%)
    transportation: 958,550 (0.35%)

**Class**:
  Unique Values: 87
  Top Values:
    house: 124,644,148 (46.20%)
    residential: 31,278,878 (11.59%)
    detached: 18,320,328 (6.79%)
    garage: 15,372,170 (5.70%)
    apartments: 14,639,606 (5.43%)
    shed: 8,356,984 (3.10%)
    industrial: 6,934,120 (2.57%)
    hut: 4,832,962 (1.79%)
    farm_auxiliary: 4,497,588 (1.67%)
    roof: 4,443,844 (1.65%)

**Datasets**:
  Unique Values: 16
  Top Values:
    Google Open Buildings: 1,829,688,206 (36.04%)
    Microsoft ML Buildings: 1,438,493,676 (28.34%)
    OpenStreetMap: 1,141,631,158 (22.49%)
    doi:10.5281/zenodo.8174931: 426,445,362 (8.40%)
    Microsoft ML Buildings,OpenStreetMap: 163,293,846 (3.22%)
    Esri Community Maps: 27,823,584 (0.55%)
    Instituto Geográfico Nacional (España): 24,127,718 (0.48%)
    OpenStreetMap,USGS Lidar: 10,727,636 (0.21%)
    Esri Community Maps,Microsoft ML Buildings: 6,960,322 (0.14%)
    Esri Community Maps,OpenStreetMap: 4,498,822 (0.09%)

**Change Type**:
  Unique Values: 3
  Top Values:
    unchanged: 2,530,652,157 (99.70%)
    added: 4,522,901 (0.18%)
    data_changed: 3,099,678 (0.12%)


================================================================================
## THEME STATISTICS: PLACES
================================================================================

**Total Features**: 143,249,058 places

**Release Comparison** (vs. baseline):
  Type: place
  - Total Change: 9.61%
  - Added: 9,876,570 (15.12%)
  - Removed: 3,594,864 (5.50%)
  - Data Changed: 61,747,959 (94.50%)
  - Unchanged: 0 (0.00%)

**Datasets**:
  Unique Values: 19
  Top Values:
    meta: 112,459,274 (78.51%)
    Foursquare: 12,178,594 (8.50%)
    Microsoft: 10,645,408 (7.43%)
    Microsoft,meta: 5,642,282 (3.94%)
    SparkGeo-confidence-conflation,meta: 1,082,336 (0.76%)
    Microsoft,SparkGeo-confidence-conflation,meta: 823,894 (0.58%)
    Microsoft,PinMeTo: 155,594 (0.11%)
    Microsoft,SparkGeo-confidence-conflation: 125,502 (0.09%)
    Microsoft,PinMeTo,meta: 69,568 (0.05%)
    PinMeTo: 32,368 (0.02%)

**Place Countries**:
  Unique Values: 251
  Top Values:
    US: 30,135,038 (21.05%)
    BR: 10,538,468 (7.36%)
    IN: 8,140,810 (5.69%)
    GB: 6,401,248 (4.47%)
    DE: 6,251,772 (4.37%)
    MX: 5,863,536 (4.09%)
    JP: 5,388,906 (3.76%)
    IT: 4,817,040 (3.36%)
    FR: 4,327,712 (3.02%)
    ID: 3,892,416 (2.72%)

**Primary Category**:
  Unique Values: 2079
  Top Values:
    restaurant: 3,570,674 (2.49%)
    professional_services: 3,121,786 (2.18%)
    hotel: 3,114,792 (2.17%)
    beauty_salon: 2,887,876 (2.02%)
    shopping: 2,194,772 (1.53%)
    landmark_and_historical_building: 2,036,668 (1.42%)
    automotive_repair: 1,919,264 (1.34%)
    clothing_store: 1,894,614 (1.32%)
    church_cathedral: 1,790,266 (1.25%)
    hospital: 1,757,262 (1.23%)

**Change Type**:
  Unique Values: 2
  Top Values:
    data_changed: 61,747,959 (86.21%)
    added: 9,876,570 (13.79%)


================================================================================
## THEME STATISTICS: DIVISIONS
================================================================================

**Total Features**: 11,178,066 divisions

**Release Comparison** (vs. baseline):
  Type: division
  - Total Change: 0.62%
  - Added: 39,338 (0.89%)
  - Removed: 11,726 (0.26%)
  - Data Changed: 119,975 (2.71%)
  - Unchanged: 4,294,343 (97.02%)
  Type: division_area
  - Total Change: 1.16%
  - Added: 17,043 (1.65%)
  - Removed: 5,061 (0.49%)
  - Data Changed: 49,376 (4.77%)
  - Unchanged: 981,312 (94.74%)
  Type: division_boundary
  - Total Change: 0.31%
  - Added: 309 (0.35%)
  - Removed: 38 (0.04%)
  - Data Changed: 2,804 (3.21%)
  - Unchanged: 84,533 (96.75%)

**Subtype**:
  Unique Values: 9
  Top Values:
    locality: 7,811,468 (69.88%)
    neighborhood: 1,952,396 (17.47%)
    microhood: 588,570 (5.27%)
    macrohood: 390,008 (3.49%)
    county: 314,972 (2.82%)
    localadmin: 84,456 (0.76%)
    region: 33,572 (0.30%)
    country: 2,308 (0.02%)
    dependency: 316 (0.00%)

**Class**:
  Unique Values: 6
  Top Values:
    hamlet: 3,263,764 (37.38%)
    village: 2,962,262 (33.93%)
    land: 2,258,626 (25.87%)
    town: 205,684 (2.36%)
    city: 27,754 (0.32%)
    maritime: 12,128 (0.14%)

**Country**:
  Unique Values: 271
  Top Values:
    CN: 1,034,078 (9.25%)
    IN: 804,650 (7.20%)
    FR: 734,412 (6.57%)
    RU: 668,444 (5.98%)
    US: 536,036 (4.80%)
    JP: 496,126 (4.44%)
    BR: 367,014 (3.28%)
    PL: 309,274 (2.77%)
    DE: 303,332 (2.71%)
    ID: 292,396 (2.62%)

**Datasets**:
  Unique Values: 8
  Top Values:
    OpenStreetMap: 11,084,396 (99.16%)
    geoBoundaries: 57,286 (0.51%)
    Linz: 13,024 (0.12%)
    Esri Community Maps,OpenStreetMap: 12,968 (0.12%)
    DadosAbertos: 8,172 (0.07%)
    Maps Entity Variant Names,OpenStreetMap: 1,708 (0.02%)
    Esri Community Maps,Maps Entity Variant Names,OpenStreetMap: 504 (0.00%)
    Esri Community Maps,Linz: 8 (0.00%)

**Change Type**:
  Unique Values: 3
  Top Values:
    unchanged: 5,360,188 (95.91%)
    data_changed: 172,155 (3.08%)
    added: 56,690 (1.01%)


================================================================================
## THEME STATISTICS: TRANSPORTATION
================================================================================

**Total Features**: 1,428,054,092 features

**Release Comparison** (vs. baseline):
  Type: connector
  - Total Change: 0.63%
  - Added: 2,797,905 (0.73%)
  - Removed: 385,586 (0.10%)
  - Data Changed: 954,440 (0.25%)
  - Unchanged: 381,735,412 (99.65%)
  Type: segment
  - Total Change: 0.46%
  - Added: 2,259,885 (0.69%)
  - Removed: 746,326 (0.23%)
  - Data Changed: 5,192,746 (1.59%)
  - Unchanged: 321,086,658 (98.18%)

**Subtype**:
  Unique Values: 3
  Top Values:
    road: 653,071,822 (99.39%)
    rail: 3,950,102 (0.60%)
    water: 56,654 (0.01%)

**Class**:
  Unique Values: 24
  Top Values:
    residential: 251,771,750 (38.32%)
    service: 115,886,728 (17.64%)
    unclassified: 59,297,958 (9.03%)
    track: 50,579,278 (7.70%)
    footway: 43,681,092 (6.65%)
    tertiary: 40,357,296 (6.14%)
    path: 27,046,782 (4.12%)
    secondary: 22,252,886 (3.39%)
    primary: 14,378,334 (2.19%)
    trunk: 8,023,178 (1.22%)

**Subclass**:
  Unique Values: 7
  Top Values:
    driveway: 33,523,554 (50.67%)
    parking_aisle: 12,710,248 (19.21%)
    sidewalk: 7,190,700 (10.87%)
    link: 4,746,824 (7.17%)
    crosswalk: 4,439,362 (6.71%)
    alley: 3,433,546 (5.19%)
    cycle_crossing: 115,914 (0.18%)

**Datasets**:
  Unique Values: 2
  Top Values:
    OpenStreetMap: 1,425,296,208 (99.81%)
    TomTom: 2,757,884 (0.19%)

**Change Type**:
  Unique Values: 3
  Top Values:
    unchanged: 702,822,070 (98.43%)
    data_changed: 6,147,186 (0.86%)
    added: 5,057,790 (0.71%)


================================================================================
## THEME STATISTICS: BASE
================================================================================

**Total Features**: 763,872,793 features

**Release Comparison** (vs. baseline):
  Type: bathymetry
  - Total Change: 0.00%
  - Added: 0 (0.00%)
  - Removed: 0 (0.00%)
  - Data Changed: 0 (0.00%)
  - Unchanged: 59,963 (100.00%)
  Type: infrastructure
  - Total Change: 1.00%
  - Added: 1,501,897 (1.09%)
  - Removed: 134,082 (0.10%)
  - Data Changed: 1,421,409 (1.04%)
  - Unchanged: 135,751,760 (98.87%)
  Type: land
  - Total Change: 0.84%
  - Added: 663,913 (0.98%)
  - Removed: 91,004 (0.13%)
  - Data Changed: 211,968 (0.31%)
  - Unchanged: 67,696,380 (99.55%)
  Type: land_cover
  - Total Change: 0.00%
  - Added: 0 (0.00%)
  - Removed: 0 (0.00%)
  - Data Changed: 0 (0.00%)
  - Unchanged: 123,302,114 (100.00%)
  Type: land_use
  - Total Change: 0.62%
  - Added: 385,095 (0.75%)
  - Removed: 67,827 (0.13%)
  - Data Changed: 321,020 (0.63%)
  - Unchanged: 50,848,377 (99.24%)
  Type: water
  - Total Change: 0.98%
  - Added: 639,265 (1.05%)
  - Removed: 42,568 (0.07%)
  - Data Changed: 227,724 (0.37%)
  - Unchanged: 60,586,550 (99.56%)

**Subtype**:
  Unique Values: 67
  Top Values:
    power: 89,370,300 (11.70%)
    tree: 64,067,742 (8.39%)
    barrier: 61,362,798 (8.03%)
    stream: 54,986,014 (7.20%)
    forest: 54,840,087 (7.18%)
    shrub: 46,763,809 (6.12%)
    transportation: 45,797,714 (6.00%)
    water: 34,925,630 (4.57%)
    agriculture: 34,671,526 (4.54%)
    transit: 34,411,314 (4.51%)

**Datasets**:
  Unique Values: 3
  Top Values:
    OpenStreetMap: 640,510,716 (83.85%)
    ESA WorldCover: 123,302,114 (16.14%)
    ETOPO/GLOBathy: 59,963 (0.01%)

**Change Type**:
  Unique Values: 3
  Top Values:
    unchanged: 438,245,144 (98.79%)
    added: 3,190,170 (0.72%)
    data_changed: 2,182,121 (0.49%)

**Class**:
  Unique Values: 339
  Top Values:
    tree: 60,381,956 (9.43%)
    stream: 54,986,014 (8.58%)
    power_tower: 35,062,936 (5.47%)
    power_pole: 34,710,164 (5.42%)
    water: 32,677,324 (5.10%)
    wood: 23,211,168 (3.62%)
    crossing: 22,930,152 (3.58%)
    farmland: 21,686,056 (3.39%)
    residential: 19,933,634 (3.11%)
    fence: 17,171,792 (2.68%)


================================================================================
<<<PROMPTS_START>>>
## SUGGESTED EXPLORATION PROMPTS
================================================================================

Use these prompts to begin exploring the Overture Maps data. Each prompt is
designed to leverage the statistics and schema information in this document.

### Geographic Distribution

1. "Which countries have the highest concentration of Places data? Show me the top 10 countries and their percentages."

2. "Compare the distribution of Divisions data across China, India, and the United States."

3. "What percentage of global building data comes from each data source?"

### Data Quality & Confidence

1. "What proportion of Places have high confidence scores (0.8 or above)?"

2. "In the Buildings theme, how much data changed between releases?"

3. "Which themes had no changes in this release?"

### Category Analysis

1. "What are the top 10 most common building types globally?"

2. "For the Places theme, list the top 15 primary categories."

3. "In Transportation, what's the breakdown between road, rail, and water segments?"

### Comparative Insights

1. "Compare the data source distribution across all six themes."

2. "Which theme has the most diverse categorical values?"

3. "What are the most common road classes in the Transportation theme?"

<<<PROMPTS_END>>>


================================================================================
## ADDITIONAL RESOURCES
================================================================================

**Official Documentation**:
  - Overture Maps Documentation: https://docs.overturemaps.org/
  - Schema Reference: https://docs.overturemaps.org/schema/reference/
  - Data Guides: https://docs.overturemaps.org/guides/

**Data Sources**:
  - OpenStreetMap: https://www.openstreetmap.org/
  - ESA WorldCover: https://worldcover.esa.int/
  - Overture GitHub: https://github.com/OvertureMaps/data

================================================================================
END OF DOCUMENT
================================================================================
