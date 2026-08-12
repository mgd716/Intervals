## 2023-10-28 - Bulk Upserts for Supabase

**Learning:** When dealing with multiple upserts to a Supabase table within a loop, batching them into a single array and using a bulk `upsert` call significantly reduces network overhead and improves performance, especially when avoiding rate limiters designed for external APIs.

**Action:** Whenever iterating through a dataset to insert or update records in a database, aggregate the records into a batch array first and perform a single bulk operation if the database client supports it.

## 2024-05-18 - Reduce DOM Elements & Network Overhead

**Learning:** When fetching large amounts of data to display in a UI, fetching everything before rendering causes a huge block. Incremental rendering with a `DocumentFragment` is significantly faster. Furthermore, minimizing the amount of HTML written to the DOM per item (e.g., using SVG `<use>` references instead of raw SVGs per item) massively decreases render time and memory footprint. Also, sorting at the database level eliminates the need for expensive client-side sort operations on initial load.

**Action:** For large list UIs, use `DocumentFragment` to batch appends incrementally. Refactor repetitive inline markup (like SVGs or heavy inline styles) into templates/definitions and CSS classes. Offload sorting to the database query when possible.

## 2026-08-12 - Tile Grid Performance Optimization

**Learning:** Calling intensive rendering functions like `drawTileGrid()` inside a loop or a batch processing function (`processAndRenderBatch`) that gets called multiple times per initial data load causes unnecessary re-renders. Moving it to execute only once at the end of the entire data load flow (`loadData`) significantly reduces load times (time roughly halved from 8.14s to 4.16s).

**Action:** Ensure that expensive map operations, like rendering grid systems based on map bounds, are only called when the final state of the map/data is reached, rather than iteratively during data population.
