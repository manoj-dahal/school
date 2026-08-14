/*
 * Siddeshwor School frontend configuration.
 *
 * window.SSN_API points a static deployment (e.g. GitHub Pages) at a running
 * backend. Leave it as "" when the site is served by the FastAPI backend
 * itself — every API call then uses same-origin paths like /api/news.
 *
 * For a static deployment, set it to the backend's origin, for example:
 *
 *   window.SSN_API = "https://school-backend.example.com";
 *
 * With SSN_API empty on a static host (*.github.io or file://), the pages
 * still work as a read-only copy: the gallery falls back to the bundled
 * JSON, and forms/search show a friendly "needs the live site" notice.
 */
window.SSN_API = "";
