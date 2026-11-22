"""Air Europa Metabuscadores UX preview - authenticated delivery only.

This repository contains only the generic server code. The internal presentation
and screenshots are loaded from Render's private environment variables.
"""
import base64
import hmac
import os
import re
import json
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
    patch_css = os.environ.get("METAS_PRESENTATION_PATCH_CSS", "")
    patch_js = os.environ.get("METAS_PRESENTATION_PATCH_JS", "")
    if patch_css:
        html = html.replace("</style>", patch_css + "\n</style>", 1)
    if patch_js:
        html = html.replace("</body>", "<script>\n" + patch_js + "\n</script></body>", 1)
    replacements_json = os.environ.get("METAS_PRESENTATION_TEXT_FIXES", "")
    if replacements_json:
        try:
            fixes = json.loads(replacements_json)
            for old, new in fixes.items():
                if isinstance(old, str) and isinstance(new, str) and old:
                    html = html.replace(old, new)
        except (TypeError, ValueError):
            pass
    return html.encode("utf-8")


def _debug_layout_structure():
    """Temporary, structural-only diagnostic. Never prints private text or metrics."""
    try:
        source = get_html().decode("utf-8")
        import re as _r
        target = _r.search(r'<[^>]{0,350}\bid=["\\\']rendimiento["\\\'][^>]*>', source, _r.I)
        if not target:
            print("METAS_LAYOUT: no exact rendimiento id", flush=True)
            return
        window = source[max(0, target.start()-1200):target.start()+16000]
        out = []
        for t in _r.finditer(r'<([a-z][\w-]*)([^<>]{0,600})>', window, _r.I):
            attrs = t.group(2)
            ids = _r.search(r'\bid=["\\\']([^"\\\']+)["\\\']', attrs)
            classes = _r.search(r'\bclass=["\\\']([^"\\\']+)["\\\']', attrs)
            if ids or classes:
                out.append(t.group(1).lower()+" #"+(ids.group(1) if ids else "")+" ."+(classes.group(1) if classes else ""))
            if len(out)>=105: break
        print("METAS_LAYOUT_START"+"\n" + "\n".join(out)+"\nMETAS_LAYOUT_END", flush=True)
    except Exception:
        print("METAS_LAYOUT: introspection unavailable", flush=True)

_debug_layout_structure()

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

    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
