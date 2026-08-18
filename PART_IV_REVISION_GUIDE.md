# Part IV Revision Guide

## Purpose

Part IV moves from numerical arrays to labeled tables and then to visual
communication. Each chapter introduces a small set of durable operations before
students combine them in the next chapter.

## Learning sequence

1. **NumPy Arrays and Vectorized Calculations**: create and inspect arrays,
   select and filter values, calculate without explicit element-by-element
   loops, summarize by axis, reshape compatible data, and copy slices safely.
2. **pandas DataFrames and Table Analysis**: add row and column labels, inspect
   tables, select and filter rows, calculate columns, handle missing values,
   group observations, and move data through CSV.
3. **Visualizing Data with Matplotlib**: match plots to questions, use the
   Figure/Axes pattern, label units, apply a restrained color system, interpret
   rendered results, compare showcase cases, build a multi-panel dashboard,
   and save figures.

The order keeps library-specific syntax attached to concepts students already
know. NumPy extends list calculations, pandas extends dictionaries and CSV
tables, and Matplotlib consumes prepared arrays or DataFrame columns.

## Content boundaries

- Advanced linear algebra, random-number modeling, and complex broadcasting
  remain outside the introductory NumPy chapter.
- Excel engines, multi-level indexes, joins, pivot tables, and time-series
  specialization remain outside the introductory pandas chapter.
- Heat maps, uncertainty bands, distributions, stacked areas, contours, and a
  single 3D surface appear as curated extensions. Dense parameter catalogs and
  advanced rendering internals remain outside the introductory chapter.
- Examples use small embedded data or create their own local files, so no
  external dataset is required.

## Visual and structural consistency

- One chapter heading per file; shared macros control every heading level.
- Learning and summary boxes use orange frames, white backgrounds, and 2 mm
  corners.
- The practice ladder remains Read, Modify, Complete, Apply, Challenge.
- Chart examples use `tab:blue` as the primary color and `tab:orange` as the
  comparison color. Labels, markers, or line styles duplicate color meaning.
- Titles use sentence case; axes include units when values are measurements;
  grids remain light and subordinate to the data.

## Assembly file

Use `main_part_iv_self_study.tex` to assemble Part IV by itself. The integrated
book file places Part IV after files and paths, which supplies the CSV and path
skills used by pandas and Matplotlib examples.

## Validation targets

- one chapter heading and the shared chapter rhythm in every file;
- exact learning and summary box colors and geometry;
- unique code labels and syntactically valid Python examples;
- independent execution of every complete Python example;
- no external input files or interactive input requirements; and
- no references to semester-specific deliverables.
