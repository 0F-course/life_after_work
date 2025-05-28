# Life After Work Data Visualization

A quick script to explore retirement age and life expectancy trends across countries using Plotly. Generates both static PNGs and interactive HTML charts.

## Data

All CSVs are preloaded in `data/`:

* `average-effective-retirement-women.csv`
* `average-effective-retirement-men.csv`
* `life-expectancy.csv`
* `healthy-life-expectancy-at-birth.csv`

## Requirements

* Python 3.7+
* pandas
* plotly

## Usage

```bash
python life_after_work.py
```

Results appear in:

* `images/` (PNG files)
* `plots/` (HTML files)

## What It Does

1. **Loads & Cleans** retirement and life expectancy data
2. **Merges** male/female retirement ages, HALE, and total life expectancy
3. **Calculates** years lived in retirement and in less-than-full health
4. **Plots** multiple figures:

   * Retirement age (overall & Portugal-specific)
   * Life expectancy trends
   * Box plots for years in retirement and years unhealthy
   * Scatter of retired years vs life expectancy
