"""Air Europa Metabuscadores UX preview - authenticated delivery only.

This repository contains only the generic server code. The internal presentation
and screenshots are loaded from Render's private environment variables.
"""
import base64
import hmac
import os
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

USER = os.environ.get("METAS_AUTH_USER", "")
PASSWORD = os.environ.get("METAS_AUTH_PASS", "")
PORT = int(os.environ.get("PORT", "10000"))

def get_html():
    parts = []
    for i in range(100):
        val = os.environ.get("METAS_HTML_%02d" % i)
        if val is None:
            break
        parts.append(val)
    html = "".join(parts)
    # Use a separate override layer for the audited Untitled UI-based design system.
    theme = os.environ.get("METAS_THEME_CSS", "")
    if theme:
        html = html.replace("</style>", theme + "</style>", 1)
    html = re.sub(r'(<img class="brand-logo" src=")data:image/png;base64,[^"]+', lambda m: m.group(1) + '/brand/air-europa.svg', html, count=1)
    return html.encode("utf-8")

class Handler(BaseHTTPRequestHandler):
    server_version = "AirEuropaPreview"

    def log_message(self, fmt, *args):
        # Do not log Authorization, token-bearing URLs, or internal data.
        return

    def _headers(self, code, mime="text/html; charset=utf-8", size=None):
        self.send_response(code)
        self.send_header("Content-Type", mime)
        self.send_header("Cache-Control", "private, no-store, max-age=0")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Cross-Origin-Resource-Policy", "same-origin")
        self.send_header("Content-Security-Policy", "default-src 'none'; img-src 'self' data:; style-src 'unsafe-inline'; script-src 'unsafe-inline'; connect-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'")
        if size is not None:
            self.send_header("Content-Length", str(size))

    def _authorized(self):
        if not USER or not PASSWORD:
            return False
        header = self.headers.get("Authorization", "")
        if not header.startswith("Basic "):
            return False
        try:
            raw = base64.b64decode(header[6:].strip(), validate=True)
            candidate = raw.decode("utf-8")
        except (ValueError, UnicodeError):
            return False
        return hmac.compare_digest(candidate, USER + ":" + PASSWORD)

    def _send_body(self, code, data, mime="text/html; charset=utf-8"):
        self._headers(code, mime, len(data))
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(data)

    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        if not self._authorized():
            self.send_response(401)
            self.send_header("WWW-Authenticate", 'Basic realm="Air Europa - Metabuscadores", charset="UTF-8"')
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", "0")
            self.end_headers()
            return

        path = urlsplit(self.path).path
        if path == "/brand/air-europa.svg":
            svg = os.environ.get("METAS_BRAND_SVG", "")
            if not svg.startswith("<svg"):
                self._send_body(503, b"Logo not configured", "text/plain")
                return
            self._send_body(200, svg.encode("utf-8"), "image/svg+xml")
            return
        if path in ("/", "/index.html"):
            data = get_html()
            if not data:
                self._send_body(503, b"Presentation not configured", "text/plain; charset=utf-8")
            else:
                self._send_body(200, data)
            return
        if path.startswith("/media/") and path.endswith(".png"):
            name = path.removeprefix("/media/").removesuffix(".png")
            if name not in ("transicion", "continuidad", "tarifa", "precio", "pasajeros", "actual-transicion", "actual-continuidad", "actual-tarifa", "actual-precio", "actual-pasajeros", "banner-desktop", "banner-mobile"):
                self._send_body(404, b"Not found", "text/plain")
                return
            raw = "".join(os.environ.get("METAS_IMG_" + name.upper().replace("-", "_") + "_%02d" % i, "") for i in range(100))
            if not raw:
                self._send_body(404, b"Not found", "text/plain")
                return
            try:
                data = base64.b64decode(raw, validate=True)
            except ValueError:
                self._send_body(503, b"Image data error", "text/plain")
                return
            self._send_body(200, data, "image/png")
            return
        self._send_body(404, b"Not found", "text/plain; charset=utf-8")

if __name__ == "__main__":
    if not USER or not PASSWORD:
        raise RuntimeError("Authentication credentials are required")

    # TEMPORARY EDITORIAL QA: headings and analytical paragraphs only (not figures).
    try:
        import re
        from html import unescape
        markup = get_html().decode("utf-8")
        sections = re.findall(r'<section class="scene [^"]*" data-slug="([^"]+)"[^>]*>(.*?)</section>', markup, re.S)
        def clean(x):
            x = re.sub(r"<[^>]*>", " ", x)
            x = unescape(re.sub(r"\\s+", " ", x)).strip()
            return re.sub(r"(?<![A-Za-z])\\d+[.,]?\\d*\\s*[%€M]*", "[n]", x)
        print("METAS_COPY_AUDIT scene_count=" + str(len(sections)), flush=True)
        for slug, body in sections:
            ts = re.findall(r'<h[1-4][^>]*>(.*?)</h[1-4]>', body, re.S)
            ps = re.findall(r'<p[^>]*>(.*?)</p>', body, re.S)
            blocks = re.findall(r'<div class="(?:reading|ranking-reading|big-note|takeaway|point|insight|editorial)[^"]*"[^>]*>(.*?)</div>',body,re.S)
            print("METAS_COPY_AUDIT " + slug + " | H: " + " | ".join(clean(x)[:110] for x in ts[:2]) + " | P: " + " | ".join(clean(x)[:175] for x in ps[:3]) + " | BLOCK: " + " | ".join(clean(x)[:110] for x in blocks[:2]), flush=True)
    except Exception as e:
        print("METAS_COPY_AUDIT ERROR " + type(e).__name__, flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
