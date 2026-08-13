## 2024-08-13 - [HIGH] XSS Vulnerability in index.html Template Literals
**Vulnerability:** Cross-Site Scripting (XSS) vulnerability found in `index.html`. Unsanitized user inputs from the Supabase database (`activity.name`, `activity.type`, `activity.id`) were being directly injected into HTML via template literals (e.g., `listItem.innerHTML` and map popups).
**Learning:** Even though the data is coming from a trusted internal database, using template literals to directly construct HTML strings is a critical anti-pattern that leads to XSS.
**Prevention:** Always sanitize untrusted input when injecting it into HTML context, especially when using template literals. Implement and enforce the usage of `escapeHTML` or similar sanitization helpers for all dynamically generated HTML.
