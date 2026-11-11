## 2024-08-13 - [Focus visibility and ARIA roles for custom filters]
**Learning:** The custom specific sport filter setup and dropdowns didn't have adequate focus states for keyboard navigation, and the ARIA roles needed explicit updates alongside the javascript DOM toggling.
**Action:** Add explicit `:focus-visible` to interactive filter inputs, and use javascript to toggle `aria-expanded` on collapse/expand toggles.
## 2024-05-14 - Keyboard Accessibility for Custom Interactive Elements
**Learning:** When making `div` elements clickable (like `.activity-item`), they also need to be accessible to keyboard users. This requires adding `role="button"`, `tabindex="0"`, a `:focus-visible` outline for visual feedback, and a `keydown` event listener to trigger the click on 'Enter' or 'Space'.
**Action:** Always check interactive custom elements for keyboard navigation support and apply semantic HTML attributes and keyboard event handlers.
## 2024-08-18 - [Yielding to Event Loop for Visual Feedback]
**Learning:** When implementing visual loading states in vanilla JavaScript before heavy synchronous execution loops, the browser won't paint the loading state if the main thread is immediately blocked.
**Action:** Always explicitly yield to the event loop using `await new Promise(resolve => setTimeout(resolve, 0));` immediately after updating the DOM to show a loading state. This ensures it's painted and screen readers announce it.
## 2024-11-20 - [Accordion ARIA properties and sync]
**Learning:** When adding `.extended-stats` toggle logic on click in vanilla javascript, the trigger `div` wasn't properly communicating its state as an accordion to screen readers.
**Action:** Always add `aria-expanded` and `aria-controls` to the parent container when rendering components with expandable content, and ensure click events properly toggle the `aria-expanded` property.
## 2025-02-12 - [Keyboard Shortcuts for Search]
**Learning:** Frequently used inputs like search benefit greatly from keyboard shortcuts (like '/') to improve accessibility and user experience for power users. However, these shortcuts need to be carefully implemented to avoid interfering when the user is already typing in an input field.
**Action:** Add global keyboard event listeners for shortcuts, ensuring they check the currently active element (e.g., `document.activeElement.tagName`) before triggering. Inform users of the shortcut via placeholder text or ARIA attributes.
## 2025-02-13 - [Search Input UX]
**Learning:** Using `type="search"` instead of `type="text"` provides users with a native "clear" button inside the input field, which improves UX significantly for filter-heavy interfaces. However, native clear actions do not trigger `keyup` events, meaning filters won't update automatically.
**Action:** Always use `<input type="search">` for search inputs and bind filtering logic to the `oninput` event rather than `onkeyup` to ensure all state changes (including native clear and mouse pasting) are captured.
## 2025-02-14 - [Stateful ARIA Labels for Toggle Buttons]
**Learning:** When creating a button that toggles a state (like sort direction), a static `aria-label` like "Toggle sort direction" is insufficient for screen reader users as it doesn't indicate the current state or the result of the action.
**Action:** Dynamically update the `aria-label` (and `title` for visual tooltips) via JavaScript to reflect the action that will occur when the button is clicked (e.g., "Sort ascending" when currently descending, and vice versa) or the current state alongside the action.
## 2025-02-15 - [Screen Reader Live Region Updates & External Link Accessibility]
**Learning:** For dynamic interfaces that filter content, screen reader users might not know when search results change unless explicitly told. Also, external links with visual arrows like "↗" can be announced confusingly (e.g., "North East Arrow") by screen readers.
**Action:** Use an `aria-live="polite"` visually hidden region to announce search result counts on dynamic filtering. Ensure decorative icons/arrows inside links are wrapped in `<span aria-hidden="true">` and provide a clear `aria-label` for the link.
## 2025-02-16 - [Focus Management on Removing Elements & Initial State Synchronization]
**Learning:** When interactive elements (like a 'Clear filters' button in an empty state) hide themselves on click, focus drops to the body, breaking keyboard navigation. Also, toggle buttons using JavaScript `.style.display === ''` checks can become out-of-sync with CSS-defined initial visibility states (`display: none`), requiring two clicks to work.
**Action:** Always programmatically move focus to a logical stable element (like the primary search input) when hiding an active element. Ensure JS toggle logic checks `window.getComputedStyle(element).display` if inline styles are not initially present.
