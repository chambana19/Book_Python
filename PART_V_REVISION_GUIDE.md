# Part V Revision Guide

## Purpose

Part V is the bridge between "the data is already a table" and the rest of the
book. Chapters 11 to 13 assume a DataFrame exists; Chapters 19 to 22 assume a
feature matrix exists. This part explains where that rectangle comes from when
the source is a nested record, a paragraph of prose, or a photograph.

## Chapter 14: Structured and Unstructured Data

- Teach the spectrum, not a binary. The organizing question is "who supplies
  the schema, and how much work is left for the analyst?"
- Correct the common misreading directly: "unstructured" describes the file,
  not the content. A work order is rich in meaning and poor in schema.
- Show that all three classes converge on one rectangular feature table, and
  name it as the same `X` matrix Chapters 19 to 22 require.
- Validate structured data against a stated schema, using `pd.api.types`
  predicates rather than literal dtype strings so checks survive version
  changes.
- Introduce grain explicitly when flattening. `record_path` decides what one
  row means; `meta` preserves parent identity, and omitting it is the common
  way flattening destroys information.
- Present feature extraction as a defensible judgment, not a conversion. The
  vocabulary is the model; the threshold is a modeling choice. Both must be
  published with any number derived from them.
- Show an image as a NumPy array before summarizing it, including the
  `(height, width, channels)` ordering and the `uint8` overflow hazard.
- State what a descriptor cannot express. Identical `hot_fraction` values can
  describe very different images.

## Boundaries

- Formats are surveyed and compared, but only CSV, JSON, and in-memory arrays
  are worked in depth. Parquet, XML parsing, and SQL queries are named with
  their trade-offs rather than taught.
- Text handling stops at keyword flags and counts. Stemming, embeddings, and
  language models are outside this part.
- Image handling stops at whole-image descriptors. Convolution, segmentation,
  and pretrained vision models are outside this part.
- All data is small, synthetic, and written in the listings, so the chapter
  needs no downloads and stays reproducible.

## Validation targets

- every listing runs top to bottom in one namespace, as a reader would;
- printed output in the chapter matches actual output exactly, including
  DataFrame formatting;
- schema validation passes on the clean frame and reports a specific, readable
  problem on a damaged one;
- the image example is seeded, so `hot_fraction` is reproducible; and
- the converged feature table is genuinely assembled from all three paths
  rather than restated.
