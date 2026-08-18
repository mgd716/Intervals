## 2024-08-13 - [Focus visibility and ARIA roles for custom filters]
**Learning:** The custom specific sport filter setup and dropdowns didn't have adequate focus states for keyboard navigation, and the ARIA roles needed explicit updates alongside the javascript DOM toggling.
**Action:** Add explicit `:focus-visible` to interactive filter inputs, and use javascript to toggle `aria-expanded` on collapse/expand toggles.
## 2024-05-14 - Keyboard Accessibility for Custom Interactive Elements
**Learning:** When making `div` elements clickable (like `.activity-item`), they also need to be accessible to keyboard users. This requires adding `role="button"`, `tabindex="0"`, a `:focus-visible` outline for visual feedback, and a `keydown` event listener to trigger the click on 'Enter' or 'Space'.
**Action:** Always check interactive custom elements for keyboard navigation support and apply semantic HTML attributes and keyboard event handlers.
## 2024-08-18 - [Yielding to Event Loop for Visual Feedback]
**Learning:** When implementing visual loading states in vanilla JavaScript before heavy synchronous execution loops, the browser won't paint the loading state if the main thread is immediately blocked.
**Action:** Always explicitly yield to the event loop using `await new Promise(resolve => setTimeout(resolve, 0));` immediately after updating the DOM to show a loading state. This ensures it's painted and screen readers announce it.
