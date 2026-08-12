## 2024-05-24 - [Vanilla JS Search Filtering]
**Learning:** Attaching heavy O(N) DOM and Leaflet map filtering directly to `keyup` events without debouncing causes severe typing latency as the number of activities grows.
**Action:** Always wrap frequent event handlers (like search inputs or scroll events) that trigger heavy computations or DOM updates in a debounce or throttle function.
