## 2023-10-28 - Bulk Upserts for Supabase

**Learning:** When dealing with multiple upserts to a Supabase table within a loop, batching them into a single array and using a bulk `upsert` call significantly reduces network overhead and improves performance, especially when avoiding rate limiters designed for external APIs.

**Action:** Whenever iterating through a dataset to insert or update records in a database, aggregate the records into a batch array first and perform a single bulk operation if the database client supports it.

## 2024-05-18 - Reduce DOM Elements & Network Overhead

**Learning:** When fetching large amounts of data to display in a UI, fetching everything before rendering causes a huge block. Incremental rendering with a `DocumentFragment` is significantly faster. Furthermore, minimizing the amount of HTML written to the DOM per item (e.g., using SVG `<use>` references instead of raw SVGs per item) massively decreases render time and memory footprint. Also, sorting at the database level eliminates the need for expensive client-side sort operations on initial load.

**Action:** For large list UIs, use `DocumentFragment` to batch appends incrementally. Refactor repetitive inline markup (like SVGs or heavy inline styles) into templates/definitions and CSS classes. Offload sorting to the database query when possible.

## 2026-08-12 - Tile Grid Performance Optimization

**Learning:** Calling intensive rendering functions like `drawTileGrid()` inside a loop or a batch processing function (`processAndRenderBatch`) that gets called multiple times per initial data load causes unnecessary re-renders. Moving it to execute only once at the end of the entire data load flow (`loadData`) significantly reduces load times (time roughly halved from 8.14s to 4.16s).

**Action:** Ensure that expensive map operations, like rendering grid systems based on map bounds, are only called when the final state of the map/data is reached, rather than iteratively during data population.
## 2026-08-12 - [Supabase Query Optimization]
 **Learning:** [Using `select('*')` on large tables with JSONB columns significantly slows down frontend load times due to massive data payloads.]
 **Action:** [Always query only the specific columns needed, and extract specific nested fields from JSONB columns using `->` syntax in Supabase (e.g., `raw_data->distance`) to minimize payload size.]
## 2025-02-12 - Inline Redundant Math Operations

**Learning:** When generating multiple map tiles per coordinate, repeatedly calling a function that performs expensive trigonometric calculations (like `math.asinh(math.tan())`) introduces significant overhead. Precomputing constants and computing the latitude-dependent base formula once per coordinate, then formatting the final strings, provides a measurable speedup (e.g. ~30% faster in our benchmark).

**Action:** When a calculation is required multiple times within a tight loop and shares common expensive sub-calculations, inline the common parts and precompute constants outside the loop to optimize performance.

## 2026-08-13 - [Supabase Query Optimization Correction]
 **Learning:** [Querying native, top-level columns in PostgreSQL (Supabase) is significantly faster and results in a smaller/similar payload compared to using JSONB extraction operators (e.g., `raw_data->distance`) at query time. The previous optimization that extracted from JSONB missed that these fields were already top-level columns.]
 **Action:** [Always query native columns when they are available instead of extracting values from a JSONB column on the fly. Check the schema/ingestion script first to confirm if a field is already mapped to a native column.]

## 2024-05-18 - Single-Pass Filter Optimization

**Learning:** When dealing with dual-state synchronization (e.g., updating a map's lines and a sidebar's corresponding list items), maintaining a single object relationship reference (`line.sidebarItem = listItem`) and iterating over a shared array (`runningMapLines.forEach`) eliminates expensive repeated DOM tree walks using `document.querySelectorAll()`.

**Action:** Whenever a large list UI reflects parallel states on map items, consolidate synchronization operations into a single-pass loop utilizing pre-cached direct object references.

## 2023-11-20 - Avoid Layout Thrashing in Map/DOM Sync

**Learning:** When synchronizing map state with DOM elements in a loop (e.g. filtering thousands of items), unconditionally calling `line.setStyle()` and `item.style.display` triggers expensive Leaflet SVG redraws and browser reflows even if the style hasn't changed.
**Action:** Always check the current property value before applying a new style (`if (item.style.display !== newDisplay) ...`) to skip redundant DOM updates.

## 2023-11-20 - Sort Optimization (Schwartzian Transform)

**Learning:** Sorting thousands of DOM elements by reading `data-*` attributes (`getAttribute`) and parsing dates/floats inside the `sort` comparison function is extremely slow due to repeated operations.
**Action:** Use a Schwartzian transform (map to objects with pre-extracted values, sort, then map back/re-append) and `DocumentFragment` to batch DOM modifications. Also, prefer `Array.from(container.children)` over `container.querySelectorAll('.class')` for simple collections.
## 2024-05-19 - Use Connection Pooling for API Calls

**Learning:** When making multiple consecutive HTTP requests to the same domain (e.g., in a loop to fetch paginated data or details for many items), creating a new TCP connection and negotiating TLS for every request (which `requests.get` does) adds significant overhead. A benchmark showed a 3x speedup by reusing connections.

**Action:** Whenever a script makes multiple HTTP requests to the same host, create a `requests.Session()` object and reuse it across all requests instead of using top-level `requests.get()` functions. Make sure to update any tests mocking the network calls to patch the session object appropriately.
## 2024-05-19 - Spatial Search Optimization

**Learning:** When checking spatial intersections in a loop (like finding map lines near a cursor click), calling functions that allocate new objects on each iteration (e.g., `bounds.pad(0.01)`) creates massive garbage collection overhead and slows down the loop.

**Action:** Pre-calculate bounding boxes or test ranges outside of the loop (e.g., `clickBounds`) and use simple intersection methods (`intersects()`) to fast-fail candidates before performing expensive geometric calculations.
## 2026-08-14 - Pre-calculate and Map DOM Attributes

**Learning:** Evaluating strings (`.includes`) or querying DOM state within highly iterative loops (like `filterSidebar` scanning thousands of map lines) causes massive performance overhead.

**Action:** To optimize filtering performance, attach pre-calculated properties (e.g. `sportCategory`) to objects during their initial creation. Inside filter loops, pre-fetch DOM state into O(1) structures like Sets or pre-computed Object Maps (`categoryVisibility`, `configs`) to bypass evaluating complex logic repeatedly.
## 2026-08-25 - Avoid Redundant Database Queries on Load

**Learning:** Making separate, paginated API calls to a database just to populate a filter dropdown (e.g., getting unique years), and then immediately making another set of paginated calls to fetch the full records, effectively doubles the initial load time and network requests.
**Action:** Consolidate data processing. When fetching large datasets in chunks, extract unique filter values (like years or categories) directly from the primary data fetch loop and update the UI once the loop completes.

## 2026-08-26 - Spatial Search Re-projection Optimization

**Learning:** When checking spatial intersections on polylines segment-by-segment (like finding map lines near a cursor click), repeatedly calling `map.project(coords[i])` and `map.project(coords[i+1])` inside the loop redundantly projects the same coordinate twice.

**Action:** Cache the projected end point of the previous segment to use as the starting point of the next segment. This effectively halves the number of expensive `map.project` calls and provides a measurable speedup during spatial search operations.
## 2023-11-20 - Lazy Evaluation for Map Filtering Operations

**Learning:** When generating large volumes of data for display and storage, generating intermediary data structures or running functions on parts of the array that are inevitably discarded via slicing uses massive amounts of RAM and time. In python, when list comprehensions are combined with downsampling slices (e.g. `[::4]`), it triggers greedy evaluation.
**Action:** Use a generator expression combined with `itertools.islice` to evaluate only the retained elements lazily.
