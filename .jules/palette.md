## 2024-08-13 - [Focus visibility and ARIA roles for custom filters]
**Learning:** The custom specific sport filter setup and dropdowns didn't have adequate focus states for keyboard navigation, and the ARIA roles needed explicit updates alongside the javascript DOM toggling.
**Action:** Add explicit `:focus-visible` to interactive filter inputs, and use javascript to toggle `aria-expanded` on collapse/expand toggles.
## 2024-05-14 - Keyboard Accessibility for Custom Interactive Elements
**Learning:** When making `div` elements clickable (like `.activity-item`), they also need to be accessible to keyboard users. This requires adding `role="button"`, `tabindex="0"`, a `:focus-visible` outline for visual feedback, and a `keydown` event listener to trigger the click on 'Enter' or 'Space'.
**Action:** Always check interactive custom elements for keyboard navigation support and apply semantic HTML attributes and keyboard event handlers.
## 2025-02-16 - Dynamic State Feedback
**Learning:** When adding dynamic loading or empty state feedback in the vanilla JS frontend, ensure screen reader accessibility by applying `role="status"` to the visual message element and dynamically toggling `aria-busy="true"` / `aria-busy="false"` on the container element processing the data.
**Action:** Always include semantic ARIA attributes when implementing visual state feedback to ensure screen readers announce the changes correctly.
