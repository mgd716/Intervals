## 2024-08-13 - [HIGH] XSS Vulnerability in index.html Template Literals
**Vulnerability:** Cross-Site Scripting (XSS) vulnerability found in `index.html`. Unsanitized user inputs from the Supabase database (`activity.name`, `activity.type`, `activity.id`) were being directly injected into HTML via template literals (e.g., `listItem.innerHTML` and map popups).
**Learning:** Even though the data is coming from a trusted internal database, using template literals to directly construct HTML strings is a critical anti-pattern that leads to XSS.
**Prevention:** Always sanitize untrusted input when injecting it into HTML context, especially when using template literals. Implement and enforce the usage of `escapeHTML` or similar sanitization helpers for all dynamically generated HTML.

## 2026-08-14 - [MEDIUM] Missing Timeout Configurations in External API Calls
**Vulnerability:** Missing timeout parameter in `requests.get()` calls to `intervals.icu` within `update_map.py`. This leaves the application vulnerable to indefinite hangs if the external service becomes unresponsive, which can lead to resource exhaustion and Denial of Service (DoS).
**Learning:** External network dependencies are fundamentally unreliable. Default behavior in some libraries (like `requests` in Python) is to wait indefinitely for a response unless a timeout is explicitly provided.
**Prevention:** Always configure explicit timeouts for all external HTTP requests. Enforce a standard timeout (e.g., `timeout=10`) across the application for any third-party API interactions.

## 2024-08-15 - [LOW] Reverse Tabnabbing in target="_blank" Links
**Vulnerability:** Anchor tags (`<a>`) using `target="_blank"` without `rel="noopener noreferrer"` were present in `index.html`. This creates a risk of reverse tabnabbing, where the newly opened page can access the `window.opener` object and potentially redirect the original page to a malicious site.
**Learning:** Even internal or trusted external links should use `rel="noopener noreferrer"` when opening in a new tab as a defense-in-depth measure.
**Prevention:** Always include `rel="noopener noreferrer"` on any anchor tag that specifies `target="_blank"`.
