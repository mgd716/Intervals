## 2024-08-13 - [HIGH] XSS Vulnerability in index.html Template Literals
**Vulnerability:** Cross-Site Scripting (XSS) vulnerability found in `index.html`. Unsanitized user inputs from the Supabase database (`activity.name`, `activity.type`, `activity.id`) were being directly injected into HTML via template literals (e.g., `listItem.innerHTML` and map popups).
**Learning:** Even though the data is coming from a trusted internal database, using template literals to directly construct HTML strings is a critical anti-pattern that leads to XSS.
**Prevention:** Always sanitize untrusted input when injecting it into HTML context, especially when using template literals. Implement and enforce the usage of `escapeHTML` or similar sanitization helpers for all dynamically generated HTML.

## 2026-08-14 - [MEDIUM] Missing Timeout Configurations in External API Calls
**Vulnerability:** Missing timeout parameter in `requests.get()` calls to `intervals.icu` within `update_map.py`. This leaves the application vulnerable to indefinite hangs if the external service becomes unresponsive, which can lead to resource exhaustion and Denial of Service (DoS).
**Learning:** External network dependencies are fundamentally unreliable. Default behavior in some libraries (like `requests` in Python) is to wait indefinitely for a response unless a timeout is explicitly provided.
**Prevention:** Always configure explicit timeouts for all external HTTP requests. Enforce a standard timeout (e.g., `timeout=10`) across the application for any third-party API interactions.

## 2024-08-16 - [MEDIUM] Reverse Tabnabbing Vulnerability in index.html External Links
**Vulnerability:** Reverse Tabnabbing vulnerability found in `index.html`. External links (`target="_blank"`) to Intervals.icu lacked the `rel="noopener noreferrer"` attribute. This could allow the newly opened tab to access and potentially manipulate the original page's `window.opener` object, posing a phishing risk.
**Learning:** Browsers do not always automatically apply `noopener` to `target="_blank"` links. Without it, external, untrusted pages have a reference to the referring window.
**Prevention:** Always add `rel="noopener noreferrer"` when using `target="_blank"` for external links to ensure cross-origin isolation and protect users from malicious redirects.
