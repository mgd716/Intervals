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
## 2025-05-19 - [Search Input UX and Events]
**Learning:** For search inputs, using `<input type="search">` instead of `type="text"` provides native browser functionality like a clear button. Furthermore, binding filter logic to `onkeyup` fails to capture mouse-based pastes or clicks on the native clear button.
**Action:** Always use `<input type="search">` for search fields and bind filter logic to the `oninput` event rather than `onkeyup` to ensure all forms of input (typing, pasting, clear button clicks) trigger the filtering correctly.
