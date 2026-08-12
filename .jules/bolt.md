## 2024-05-24 - [Vanilla JS Search Filtering]
**Learning:** Attaching heavy O(N) DOM and Leaflet map filtering directly to `keyup` events without debouncing causes severe typing latency as the number of activities grows.
**Action:** Always wrap frequent event handlers (like search inputs or scroll events) that trigger heavy computations or DOM updates in a debounce or throttle function.
## 2024-11-20 - [Supabase Bulk Upserts]
**Learning:** Performing Supabase API calls (e.g., upserts) inside a loop (N+1 query) significantly degrades performance due to network overhead.
**Action:** Always accumulate records in a list and perform a single bulk API operation (e.g., `table().upsert(data)`) to minimize network latency and improve execution time.
