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
## 2024-08-18 - [MEDIUM] Missing Content Security Policy\n**Vulnerability:** The `index.html` file lacked a Content-Security-Policy (CSP) meta tag, making the application more susceptible to Cross-Site Scripting (XSS) attacks and unauthorized data exfiltration.\n**Learning:** Even static or vanilla JS applications without complex build steps need security headers. While typically set by a web server, they can also be enforced via HTML meta tags when serving static files.\n**Prevention:** Always include a baseline CSP in the `<head>` of HTML entry points, restricting resources to trusted origins.

## 2026-08-21 - [HIGH] Missing Subresource Integrity (SRI) on CDN Assets
**Vulnerability:** External JavaScript and CSS libraries (Leaflet, Supabase) were loaded from public CDNs (unpkg, jsdelivr) without integrity checks. This creates a risk where a compromised CDN could serve malicious code that executes in the context of the application.
**Learning:** Loading from CDNs without SRI trusts the CDN completely. If the CDN is breached or the DNS is hijacked, attackers can inject arbitrary scripts (XSS).
**Prevention:** Always include `integrity` and `crossorigin="anonymous"` attributes when loading third-party assets from CDNs. When using CDNs like jsdelivr that allow version aliasing (e.g., `@2`), pin the dependency to an exact version (e.g., `@2.112.3`) to ensure the integrity hash remains valid over time.

## 2024-08-22 - [MEDIUM] Missing Input Length Limits (DoS risk)
**Vulnerability:** The search input field (`#search-box`) in `index.html` lacked a `maxlength` attribute, allowing users or bots to paste excessively long strings, which could cause client-side performance issues or crashes during filter processing.
**Learning:** Client-side inputs should have bounded lengths to prevent resource exhaustion, even if the processing is entirely local.
**Prevention:** Always add a reasonable `maxlength` attribute (e.g., `maxlength="100"`) to text input fields, especially those that trigger expensive JavaScript operations on input.

## 2024-08-25 - [MEDIUM] Incomplete Input Sanitization in Template Literals
**Vulnerability:** While primary attributes like `activity.id` and `activity.name` were being sanitized in `index.html` via `escapeHTML`, dynamically generated values derived from unvalidated database fields (such as `dateStr` constructed from `activity.start_date` or `activity.year`) were missed and injected directly into template literals. This leaves a partial XSS vulnerability.
**Learning:** Sanitization must be applied universally to *all* dynamically generated content injected into HTML, not just obvious strings. Even values that appear to be structured data (like dates) can carry XSS payloads if the underlying data source is untrusted or improperly validated.
**Prevention:** Apply `escapeHTML` to every variable before injecting it into DOM template literals, regardless of its expected type, unless the data has been strictly validated as a safe type (e.g., explicitly coerced to an integer) prior to injection.

## 2024-10-27 - [HIGH] Unencrypted Sensitive Data Transmission
**Vulnerability:** The backend configuration allowed `SUPABASE_URL` to use the unencrypted `http://` protocol instead of strictly enforcing `https://`.
**Learning:** Permitting `http://` for endpoints requiring authentication (like `SUPABASE_KEY`) risks exposing sensitive credentials to Man-in-the-Middle (MitM) attacks. Secure transport must be enforced even in backend CLI scripts.
**Prevention:** Always explicitly validate and enforce the `https://` protocol for any URL configuration responsible for transmitting sensitive API keys or credentials.
