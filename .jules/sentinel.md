## 2024-08-13 - [HIGH] XSS Vulnerability in index.html Template Literals
**Vulnerability:** Cross-Site Scripting (XSS) vulnerability found in `index.html`. Unsanitized user inputs from the Supabase database (`activity.name`, `activity.type`, `activity.id`) were being directly injected into HTML via template literals (e.g., `listItem.innerHTML` and map popups).
**Learning:** Even though the data is coming from a trusted internal database, using template literals to directly construct HTML strings is a critical anti-pattern that leads to XSS.
**Prevention:** Always sanitize untrusted input when injecting it into HTML context, especially when using template literals. Implement and enforce the usage of `escapeHTML` or similar sanitization helpers for all dynamically generated HTML.

## 2026-08-14 - [MEDIUM] Missing Timeout Configurations in External API Calls
**Vulnerability:** Missing timeout parameter in `requests.get()` calls to `intervals.icu` within `update_map.py`. This leaves the application vulnerable to indefinite hangs if the external service becomes unresponsive, which can lead to resource exhaustion and Denial of Service (DoS).
**Learning:** External network dependencies are fundamentally unreliable. Default behavior in some libraries (like `requests` in Python) is to wait indefinitely for a response unless a timeout is explicitly provided.
**Prevention:** Always configure explicit timeouts for all external HTTP requests. Enforce a standard timeout (e.g., `timeout=10`) across the application for any third-party API interactions.

## 2025-02-13 - [MEDIUM] Reverse Tabnabbing Vulnerability via target="_blank"
**Vulnerability:** External links created with `target="_blank"` in the frontend (e.g., `index.html`) did not include the `rel="noopener noreferrer"` attribute. This exposes users to Reverse Tabnabbing, where the newly opened page can access the original page's `window` object via `window.opener` and potentially redirect it to a malicious site.
**Learning:** Adding `target="_blank"` without `rel="noopener noreferrer"` is a common security oversight that can compromise the user's origin session.
**Prevention:** Always add `rel="noopener noreferrer"` when using `target="_blank"` on links navigating to external domains.
