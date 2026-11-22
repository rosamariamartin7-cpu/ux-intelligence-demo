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

RANKING_LAYOUT_CSS = r"""
/* Rendimiento: stable two-column dashboard and Untitled UI-style metric card. */
.interactive-grid:has(#rank-chart) {
  --rank-card-height: 392px;
  display: grid !important;
  grid-template-columns: minmax(0, 1fr) minmax(0, 306px) !important;
  align-items: stretch !important;
  gap: 20px !important;
  grid-auto-flow: row !important;
  width: 100%;
  max-width: 100%;
}
.interactive-grid:has(#rank-chart) > .chart-panel {
  box-sizing: border-box;
  min-width: 0 !important;
  width: 100% !important;
  max-width: 100%;
  height: var(--rank-card-height) !important;
  min-height: var(--rank-card-height) !important;
  margin: 0 !important;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.interactive-grid:has(#rank-chart) > .chart-panel .panel-top {
  min-width: 0;
  width: 100%;
  max-width: 100%;
  flex-wrap: nowrap !important;
}
.interactive-grid:has(#rank-chart) > .chart-panel .panel-top :is(h2, h3, h4, .panel-title) {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.interactive-grid:has(#rank-chart) > .chart-panel .segmented {
  flex-wrap: nowrap !important;
  flex-shrink: 0;
  min-width: 0;
}
.interactive-grid:has(#rank-chart) > .chart-panel .seg-btn {
  white-space: nowrap !important;
  flex-shrink: 0;
}
.interactive-grid:has(#rank-chart) #rank-chart {
  box-sizing: border-box;
  width: 100%;
  max-width: 100%;
  min-width: 0;
  min-height: 0;
  flex: 1 1 0;
  overflow: hidden;
}
.interactive-grid:has(#rank-chart) #rank-chart svg {
  max-width: 100%;
}
.interactive-grid:has(#rank-chart) > .ranking-reading {
  box-sizing: border-box !important;
  width: 306px !important;
  max-width: 306px !important;
  min-width: 306px !important;
  height: var(--rank-card-height) !important;
  min-height: var(--rank-card-height) !important;
  max-height: var(--rank-card-height) !important;
  margin: 0 !important;
  padding: 24px !important;
  background: #fff !important;
  border: 1px solid #eaecf0 !important;
  border-radius: 14px !important;
  box-shadow: 0 1px 2px rgba(16, 24, 40, .05), 0 1px 3px rgba(16, 24, 40, .03);
  display: flex !important;
  flex-direction: column !important;
  align-items: stretch !important;
  gap: 10px;
  overflow: hidden;
  color: #101828;
}
.interactive-grid:has(#rank-chart) > .ranking-reading > * {
  box-sizing: border-box;
  min-width: 0;
  max-width: 100%;
}
.interactive-grid:has(#rank-chart) .ranking-main-value {
  font-variant-numeric: tabular-nums;
  font-size: clamp(25px, 2.5vw, 35px) !important;
  line-height: 1.13 !important;
  letter-spacing: -.035em;
  white-space: nowrap !important;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 100%;
}
.interactive-grid:has(#rank-chart) .ranking-winner {
  max-width: 100%;
  white-space: nowrap !important;
  overflow: hidden;
  text-overflow: ellipsis;
}
.interactive-grid:has(#rank-chart) .ranking-winner *,
.interactive-grid:has(#rank-chart) .ranking-reading .source-note {
  max-width: 100%;
}
.interactive-grid:has(#rank-chart) .ranking-reading .source-note {
  margin-top: auto;
  font-size: 12px;
  line-height: 1.4;
  color: #667085;
  overflow: hidden;
}
.interactive-grid:has(#rank-chart) .ranking-reading .reading-divider {
  width: 100%;
  flex: 0 0 auto;
}
@media (max-width: 920px) {
  .interactive-grid:has(#rank-chart) {
    --rank-card-height: 372px;
    grid-template-columns: minmax(0, 1fr) !important;
    gap: 16px !important;
  }
  .interactive-grid:has(#rank-chart) > .ranking-reading {
    width: 100% !important;
    min-width: 0 !important;
    max-width: 100% !important;
    height: 288px !important;
    min-height: 288px !important;
    max-height: 288px !important;
    padding: 20px !important;
  }
  .interactive-grid:has(#rank-chart) .ranking-main-value {
    font-size: clamp(25px, 5vw, 34px) !important;
  }
}
@media (max-width: 520px) {
  .interactive-grid:has(#rank-chart) {
    --rank-card-height: 330px;
  }
  .interactive-grid:has(#rank-chart) > .chart-panel .panel-top {
    gap: 8px;
  }
  .interactive-grid:has(#rank-chart) > .ranking-reading {
    height: 278px !important;
    min-height: 278px !important;
    max-height: 278px !important;
    padding: 18px !important;
  }
}
"""



PROCEDENCIA_DASHBOARD_CSS = r"""
/* Procedencia: two aligned cards in the existing Air Europa / Untitled UI visual language. */
.scene[data-slug="procedencia"] .two-col.source-layout {
  --source-card-height: 350px;
  box-sizing: border-box;
  display: grid !important;
  grid-template-columns: minmax(0, .98fr) minmax(0, 1.54fr) !important;
  gap: 20px !important;
  align-items: stretch !important;
  width: 100%;
  max-width: 100%;
}
.scene[data-slug="procedencia"] .two-col.source-layout > :first-child,
.scene[data-slug="procedencia"] .two-col.source-layout > .chart-card {
  box-sizing: border-box !important;
  min-width: 0 !important;
  width: 100% !important;
  max-width: 100% !important;
  min-height: var(--source-card-height) !important;
  height: var(--source-card-height) !important;
  margin: 0 !important;
  background: #ffffff !important;
  border: 1px solid #eaecf0 !important;
  border-radius: 14px !important;
  box-shadow: 0 1px 2px rgba(16,24,40,.05), 0 1px 3px rgba(16,24,40,.03) !important;
}
.scene[data-slug="procedencia"] .two-col.source-layout > :first-child {
  display: flex !important;
  flex-direction: column !important;
  justify-content: center !important;
  align-items: flex-start !important;
  padding: 26px 28px !important;
  overflow: hidden;
}
.scene[data-slug="procedencia"] .hero-count {
  max-width: 100%;
  margin: 0 0 6px !important;
  font-variant-numeric: tabular-nums;
  white-space: nowrap;
  color: #101f46 !important;
}
.scene[data-slug="procedencia"] .hero-label {
  max-width: 100%;
  margin: 0 0 12px !important;
  color: #344054;
}
.scene[data-slug="procedencia"] .body-lead {
  max-width: 100%;
  margin: 0 !important;
  color: #475467;
  line-height: 1.52 !important;
  text-wrap: pretty;
}
.scene[data-slug="procedencia"] .two-col.source-layout > .chart-card {
  display: flex !important;
  flex-direction: column !important;
  padding: 20px 26px 22px !important;
  gap: 0 !important;
  overflow: hidden;
}
.scene[data-slug="procedencia"] .source-chart-heading {
  padding: 0 0 13px;
  border-bottom: 1px solid #eaecf0;
  flex: 0 0 auto;
}
.scene[data-slug="procedencia"] .source-chart-heading h3 {
  font-size: 18px !important;
  font-weight: 700 !important;
  line-height: 1.3 !important;
  letter-spacing: -.02em;
  color: #101828;
  margin: 0 0 5px !important;
}
.scene[data-slug="procedencia"] .source-chart-heading p {
  font-size: 13px;
  line-height: 1.4;
  color: #667085;
  margin: 0 !important;
}
.scene[data-slug="procedencia"] .source-chart-column-headings {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-top: 13px;
  padding-bottom: 1px;
  font-size: 12px;
  font-weight: 650;
  line-height: 1.3;
  color: #667085;
  letter-spacing: .005em;
}
.scene[data-slug="procedencia"] .source-chart-column-headings span:last-child {
  text-align: right;
}
.scene[data-slug="procedencia"] .chart-card > .chart {
  display: flex !important;
  flex-direction: column !important;
  justify-content: space-evenly !important;
  flex: 1 1 auto;
  min-height: 0;
  width: 100%;
  gap: 8px;
}
.scene[data-slug="procedencia"] .chart-row {
  display: grid !important;
  grid-template-columns: minmax(120px, .9fr) minmax(100px, 1.55fr) minmax(66px, .55fr) !important;
  align-items: center !important;
  gap: 14px !important;
  width: 100%;
  margin: 0 !important;
  min-width: 0;
}
.scene[data-slug="procedencia"] .chart-name {
  display: flex;
  gap: 9px;
  align-items: center;
  min-width: 0;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-weight: 600 !important;
}
.scene[data-slug="procedencia"] .chart-name:before {
  content: "";
  display: inline-block;
  flex: 0 0 8px;
  width: 8px;
  height: 8px;
  background: var(--meta-chart-color, #1b58b9);
  border-radius: 50%;
}
.scene[data-slug="procedencia"] .chart-track {
  background: #edf2fa !important;
  min-width: 0;
  overflow: hidden;
  border-radius: 5px;
}
.scene[data-slug="procedencia"] .chart-fill {
  background: var(--meta-chart-color, #1b58b9) !important;
  border-radius: 5px;
}
.scene[data-slug="procedencia"] .chart-row:nth-child(1) { --meta-chart-color: #1453ae; }
.scene[data-slug="procedencia"] .chart-row:nth-child(2) { --meta-chart-color: #5499d8; }
.scene[data-slug="procedencia"] .chart-row:nth-child(3) { --meta-chart-color: #293e72; }
.scene[data-slug="procedencia"] .chart-row:nth-child(4) { --meta-chart-color: #94b9df; }
.scene[data-slug="procedencia"] .chart-value {
  min-width: 0;
  text-align: right !important;
  white-space: nowrap !important;
  font-variant-numeric: tabular-nums;
  color: #101f46 !important;
  font-weight: 700 !important;
}
.scene[data-slug="procedencia"] .section-head h2 .source-title-line {
  white-space: nowrap;
}
@media (max-width: 950px) {
  .scene[data-slug="procedencia"] .two-col.source-layout {
    grid-template-columns: minmax(0, 1fr) !important;
    --source-card-height: auto;
    gap: 16px !important;
  }
  .scene[data-slug="procedencia"] .two-col.source-layout > :first-child,
  .scene[data-slug="procedencia"] .two-col.source-layout > .chart-card {
    height: auto !important;
    min-height: 0 !important;
  }
  .scene[data-slug="procedencia"] .two-col.source-layout > :first-child {
    padding: 24px !important;
  }
  .scene[data-slug="procedencia"] .two-col.source-layout > .chart-card {
    min-height: 310px !important;
    padding: 20px 22px 22px !important;
  }
}
@media (max-width: 540px) {
  .scene[data-slug="procedencia"] .chart-row {
    grid-template-columns: minmax(82px, .85fr) minmax(64px, 1.1fr) minmax(54px, .52fr) !important;
    gap: 9px !important;
  }
  .scene[data-slug="procedencia"] .chart-name {
    gap: 5px;
    font-size: 12px;
  }
  .scene[data-slug="procedencia"] .chart-name:before {
    flex-basis: 6px;
    width: 6px;
    height: 6px;
  }
  .scene[data-slug="procedencia"] .chart-value {
    font-size: 12px !important;
  }
  .scene[data-slug="procedencia"] .source-chart-heading h3 {
    font-size: 16px !important;
  }
  .scene[data-slug="procedencia"] .section-head h2 .source-title-line {
    white-space: normal;
  }
}
"""

CORPORATE_SELECTED_TABS_CSS = r"""
/* Clear corporate-blue selected state, shared by interactive dashboard tabs. */
.segmented .seg-btn.selected,
.segmented .seg-btn[aria-selected="true"],
.segmented .seg-btn[aria-pressed="true"],
.tabs button.active,
.tabs button[aria-selected="true"],
.tab-list [role="tab"][aria-selected="true"],
.tab-bar button.active,
.tab-buttons button.active {
  background: #1659bd !important;
  color: #ffffff !important;
  border-color: #1659bd !important;
  box-shadow: 0 1px 3px rgba(13,55,128,.19) !important;
  font-weight: 700 !important;
}
.segmented .seg-btn.selected:hover,
.tabs button.active:hover,
.tab-bar button.active:hover {
  background: #0e459e !important;
  border-color: #0e459e !important;
}
.segmented .seg-btn:focus-visible,
.tabs button:focus-visible,
.tab-list [role="tab"]:focus-visible,
.tab-bar button:focus-visible,
.tab-buttons button:focus-visible {
  outline: 3px solid #94bdf4 !important;
  outline-offset: 2px;
}
"""


def patch_procedencia_html(html):
    """Apply structural enrichment to the Procedencia slide only."""
    marker = re.search(r'<section\b[^>]*\bdata-slug\s*=\s*["\']procedencia["\'][^>]*>', html, flags=re.I)
    if not marker:
        return html
    after = re.search(r'<section\b[^>]*\bclass\s*=\s*["\'][^"\']*\bscene\b', html[marker.end():], flags=re.I)
    end = marker.end() + after.start() if after else len(html)
    slide = html[marker.start():end]
    title_pattern = re.compile(r'(Google Flights y Skyscanner reúnen el 82,9\s*%)(\s+)de las sesiones', flags=re.I)
    slide = title_pattern.sub(
        r'\1<br><span class="source-title-line">de las sesiones</span>', slide, count=1
    )
    if 'source-chart-heading' not in slide:
        chart_intro = (
            '<div class="source-chart-heading">'
            '<h3>Sesiones por metabuscador</h3>'
            '<p>Participación de cada plataforma en el total de sesiones del canal</p>'
            '</div>'
            '<div class="source-chart-column-headings">'
            '<span>Metabuscador</span><span>Cuota de sesiones</span>'
            '</div>'
        )
        slide = re.sub(
            r'(<div\b[^>]*\bclass=["\'][^"\']*\bchart-card\b[^"\']*["\'][^>]*>)',
            lambda m: m.group(1) + chart_intro,
            slide,
            count=1,
            flags=re.I
        )
    return html[:marker.start()] + slide + html[end:]


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
    if "rank-chart" in html:
        html = html.replace("</style>", RANKING_LAYOUT_CSS + "\n</style>", 1)
    html = patch_procedencia_html(html)
    html = html.replace("</style>", PROCEDENCIA_DASHBOARD_CSS + "\n" + CORPORATE_SELECTED_TABS_CSS + "\n</style>", 1)
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



def _audit_presentation_internals():
    """Temporary diagnostic restricted to structural HTML and requested slide headings."""
    try:
        h=get_html().decode("utf-8")
        r=re.search(r'<section\b[^>]*data-slug=["\']procedencia["\'][^>]*>',h,re.I)
        if not r:
            print("VERIFY_PROC missing-section",flush=True)
            return
        next_scene=re.search(r'<section\b[^>]*class=["\'][^"\']*scene',h[r.end():],re.I)
        segment=h[r.start():r.end()+(next_scene.start() if next_scene else len(h)-r.end())]
        head=re.search(r'<h2\b[^>]*>(.*?)</h2>',segment,re.I|re.S)
        print("VERIFY_PROC heading_html="+repr(head.group(1)[:380] if head else "MISSING"),flush=True)
        print("VERIFY_PROC two_col="+str("source-layout" in segment)+", title_span="+str('source-title-line' in segment)+", heading="+str('source-chart-heading' in segment)+", chart_colors="+str("--meta-chart-color" in h)+",styles="+str(len(re.findall(r'<style\b',h,re.I)))+", length="+str(len(h)),flush=True)
        for selector in ("chart-card","chart-name","chart-row","source-layout","seg-btn","selected","active","rank-chart"):
            print("VERIFY_PROC token "+selector+" "+str(len(re.findall(re.escape(selector),h))),flush=True)
        print("VERIFY_PROC color_style="+str(h.find("CORPORATE_SELECTED_TABS_CSS"))+", corporate_rule="+str(h.find(".segmented .seg-btn.selected"))+", css_end="+str(h.rfind("</style>")),flush=True)
    except Exception as ex:
        print("VERIFY_PROC failed "+type(ex).__name__,flush=True)

if __name__ == "__main__":
    if not USER or not PASSWORD:
        raise RuntimeError("Authentication credentials are required")

    _audit_presentation_internals()
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
