# Part V Revision Guide

## Purpose

Part V extends labeled tables into spatial tables. Students first create and
project their own geometries, then load documented educational datasets and
combine layers in an applied mapping workflow.

## Learning sequence

1. **GeoPandas Foundations**: understand geometry columns and coordinate
   reference systems, create points, project coordinates, calculate distance
   in appropriate units, make buffers, and draw layered maps.
2. **GeoDatasets and Applied Mapping**: locate and cache educational datasets,
   inspect metadata, align coordinate systems, make a choropleth, perform a
   spatial join, summarize joined records, and export a multi-panel result.

## Boundaries

- The chapters focus on vector data. Raster processing, web tile servers,
  geocoding services, network routing, and production GIS databases remain
  outside this introductory part.
- Dataset downloads are explicit. Students are told when internet access and a
  local cache are involved.
- Maps are interpreted as analytical arguments, not decorative outputs.

## Validation targets

- examples run with current GeoPandas and `geodatasets` releases;
- every distance or area calculation uses a projected CRS with stated units;
- layers share a CRS before overlays or spatial joins;
- maps include titles, legends or direct labels, source notes, and restrained
  color choices; and
- long applications separate loading, inspection, transformation, analysis,
  visualization, and export.
