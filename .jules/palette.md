## 2024-08-13 - [Focus visibility and ARIA roles for custom filters]
**Learning:** The custom specific sport filter setup and dropdowns didn't have adequate focus states for keyboard navigation, and the ARIA roles needed explicit updates alongside the javascript DOM toggling.
**Action:** Add explicit `:focus-visible` to interactive filter inputs, and use javascript to toggle `aria-expanded` on collapse/expand toggles.
## 2024-05-14 - Keyboard Accessibility for Custom Interactive Elements
**Learning:** When making `div` elements clickable (like `.activity-item`), they also need to be accessible to keyboard users. This requires adding `role="button"`, `tabindex="0"`, a `:focus-visible` outline for visual feedback, and a `keydown` event listener to trigger the click on 'Enter' or 'Space'.
**Action:** Always check interactive custom elements for keyboard navigation support and apply semantic HTML attributes and keyboard event handlers.
## 2026-08-17 - Adding Dynamic Loading and Empty States
**Learning:** Adding dynamic loading and empty states using `role="status"` and toggling `aria-busy` effectively communicates asynchronous status changes to screen readers and improves the UX for long-running operations or zero-state results.
**Action:** When creating interfaces that dynamically fetch or filter data, apply `role="status"` to visual message elements and correctly toggle `aria-busy="true"` and `aria-busy="false"` on the container processing the data to ensure robust accessibility support.
