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
/* Rendimiento dashboard: fixed height and dimensions across all three selected metrics. */
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) {
  box-sizing: border-box !important;
  display: grid !important;
  grid-template-columns: minmax(0,1fr) 306px !important;
  align-items: stretch !important;
  grid-auto-flow: row !important;
  gap: 18px !important;
  width: 100% !important;
  height: 460px !important;
  min-height: 460px !important;
  max-height: 460px !important;
  margin: 0 auto !important;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .chart-panel,
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading {
  box-sizing: border-box !important;
  position: relative !important;
  display: flex !important;
  flex-direction: column !important;
  width: 100% !important;
  min-width: 0 !important;
  max-width: 100% !important;
  height: 100% !important;
  min-height: 0 !important;
  max-height: 100% !important;
  margin: 0 !important;
  border: 1px solid #eaecf0 !important;
  border-radius: 14px !important;
  background-color: #ffffff !important;
  box-shadow: 0 1px 2px rgba(16,24,40,.05) !important;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .chart-panel {
  overflow: hidden !important;
  padding: 22px 26px !important;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) .panel-top {
  box-sizing: border-box;
  width: 100%;
  min-width: 0;
  max-width: 100%;
  flex-wrap: nowrap !important;
  gap: 12px !important;
}
/* Same divider used by the Procedencia chart heading. */
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .chart-panel > .panel-top {
  padding-bottom: 15px !important;
  border-bottom: 1px solid #eaecf0 !important;
  flex: 0 0 auto !important;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) .segmented {
  flex-wrap: nowrap !important;
  flex: 0 0 auto !important;
  min-width: 0 !important;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) .seg-btn {
  white-space: nowrap !important;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) #rank-chart {
  box-sizing: border-box !important;
  width: 100% !important;
  max-width: 100% !important;
  min-width: 0 !important;
  min-height: 0;
  flex: 1 1 0 !important;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading {
  justify-content: flex-start !important;
  align-items: stretch !important;
  gap: 0 !important;
  padding: 20px 22px !important;
  overflow: hidden !important;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading > * {
  box-sizing: border-box;
  min-width: 0;
  max-width: 100%;
  flex-shrink: 0;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) .ranking-main-value {
  margin: 0 0 12px !important;
  font-size: 32px !important;
  line-height: 1.12 !important;
  letter-spacing: -.035em;
  font-variant-numeric: tabular-nums;
  white-space: nowrap !important;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) .ranking-winner {
  margin: 0 0 12px !important;
  font-size: clamp(18px,1.65vw,23px) !important;
  line-height: 1.2 !important;
  text-wrap: pretty;
  overflow-wrap: break-word;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading p {
  font-size: 13px !important;
  line-height: 1.4 !important;
  margin: 6px 0 !important;
  color: #475467 !important;
  overflow-wrap: break-word;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) .reading-divider {
  box-sizing: border-box;
  width: 100%;
  height: 1px !important;
  min-height: 1px !important;
  max-height: 1px !important;
  margin: 14px 0 !important;
  flex: 0 0 1px !important;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading p:last-child {
  margin-bottom: 0 !important;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading.metrics-compact {
  padding: 16px 18px !important;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading.metrics-compact .ranking-main-value {
  font-size: 29px !important;
  margin-bottom: 8px !important;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading.metrics-compact .ranking-winner {
  font-size: 19px !important;
  margin-bottom: 8px !important;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading.metrics-compact p {
  font-size: 12px !important;
  line-height: 1.32 !important;
  margin: 4px 0 !important;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading.metrics-compact .reading-divider {
  margin: 8px 0 !important;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading.metrics-tight {
  padding: 14px 16px !important;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading.metrics-tight .ranking-main-value {
  font-size: 27px !important;
  margin-bottom: 6px !important;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading.metrics-tight .ranking-winner {
  font-size: 18px !important;
  margin-bottom: 6px !important;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading.metrics-tight p {
  font-size: 11.5px !important;
  line-height: 1.29 !important;
  margin: 3px 0 !important;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading.metrics-tight .reading-divider {
  margin: 6px 0 !important;
}
@media (max-width: 950px) {
  .scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) {
    grid-template-columns: minmax(0,1fr) !important;
    height: auto !important;
    min-height: 0 !important;
    max-height: none !important;
    gap: 16px !important;
  }
  .scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .chart-panel {
    height: 350px !important;
    min-height: 350px !important;
    max-height: 350px !important;
    padding: 18px !important;
  }
  .scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading {
    height: 390px !important;
    min-height: 390px !important;
    max-height: 390px !important;
  }
}
@media (max-width: 540px) {
  .scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .chart-panel {
    height: 330px !important;
    min-height: 330px !important;
    max-height: 330px !important;
    padding: 14px !important;
  }
  .scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading {
    height: 420px !important;
    min-height: 420px !important;
    max-height: 420px !important;
  }
}

/* Legible metric reading: the figure and one key insight, without repeated text. */
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading {
  justify-content:center !important;
  align-items:flex-start !important;
  padding:25px 24px !important;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) .ranking-main-value {
  font-size:46px !important;
  line-height:1.1 !important;
  margin:0 0 10px !important;
  letter-spacing:-.045em !important;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) .ranking-winner {
  font-size:24px !important;
  line-height:1.25 !important;
  margin:0 0 22px !important;
  font-weight:700 !important;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading #rank-explanation {
  font-size:16px !important;
  line-height:1.5 !important;
  color:#475467 !important;
  margin:0 !important;
  overflow-wrap:break-word;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading #rank-implication,
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading .reading-divider {
  display:none !important;
}
.scene[data-slug="rendimiento"] #rank-chart .chart-name,
.scene[data-slug="rendimiento"] #rank-chart .bar-label { font-size:18px !important; }
.scene[data-slug="rendimiento"] #rank-chart .chart-value,
.scene[data-slug="rendimiento"] #rank-chart .bar-value {
  font-size:19px !important;
  font-weight:700 !important;
  font-variant-numeric:tabular-nums;
}
@media(max-width:540px) {
  .scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) .ranking-main-value {font-size:42px !important;}
  .scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) .ranking-winner {font-size:22px !important;}
}

/* Consistent KPI scale in Procedencia and Rendimiento. Numbers stay fully visible. */
.scene[data-slug="procedencia"] .hero-count,
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) .ranking-main-value,
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) .metrics-compact .ranking-main-value,
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) .metrics-tight .ranking-main-value {
  font-size: 64px !important;
  line-height: 1.08 !important;
  font-weight: 800 !important;
  letter-spacing: -.055em !important;
  font-variant-numeric: tabular-nums !important;
  white-space: nowrap !important;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) .ranking-main-value {
  box-sizing: border-box !important;
  display: block !important;
  width: 100% !important;
  min-width: 0 !important;
  max-width: 100% !important;
  margin: 0 0 11px !important;
  overflow: visible !important;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading,
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading.metrics-compact,
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading.metrics-tight {
  justify-content: center !important;
  align-items: stretch !important;
  padding: 20px 22px !important;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) .ranking-winner,
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) .metrics-compact .ranking-winner,
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) .metrics-tight .ranking-winner {
  font-size: 23px !important;
  line-height: 1.22 !important;
  margin: 0 0 13px !important;
  font-weight: 700 !important;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading p,
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading #rank-explanation,
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading #rank-implication {
  font-size: 14px !important;
  line-height: 1.45 !important;
  margin: 0 !important;
  color: #475467 !important;
  overflow-wrap: break-word;
  display: block !important;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading .reading-divider {
  display: block !important;
  box-sizing: border-box !important;
  height: 1px !important;
  min-height: 1px !important;
  margin: 15px 0 !important;
  background: #eaecf0 !important;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading.metrics-compact .ranking-winner {
  margin-bottom: 10px !important;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading.metrics-compact p,
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading.metrics-compact #rank-explanation,
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading.metrics-compact #rank-implication {
  font-size: 13.5px !important;
  line-height: 1.36 !important;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading.metrics-compact .reading-divider {
  margin: 10px 0 !important;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading.metrics-tight .ranking-winner {
  font-size: 21px !important;
  margin-bottom: 8px !important;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading.metrics-tight p,
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading.metrics-tight #rank-explanation,
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading.metrics-tight #rank-implication {
  font-size: 12.5px !important;
  line-height: 1.32 !important;
}
.scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) > .ranking-reading.metrics-tight .reading-divider {
  margin: 8px 0 !important;
}
@media (max-width: 540px) {
  .scene[data-slug="procedencia"] .hero-count,
  .scene[data-slug="rendimiento"] .interactive-grid:has(#rank-chart) .ranking-main-value {
    font-size: 56px !important;
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
  background-image: none !important;
  opacity: 1 !important;
  border-radius: 5px;
}
.scene[data-slug="procedencia"] .chart-row:nth-child(1) { --meta-chart-color: #2563eb; }
.scene[data-slug="procedencia"] .chart-row:nth-child(2) { --meta-chart-color: #0d9488; }
.scene[data-slug="procedencia"] .chart-row:nth-child(3) { --meta-chart-color: #f97316; }
.scene[data-slug="procedencia"] .chart-row:nth-child(4) { --meta-chart-color: #94a3b8; }
.scene[data-slug="procedencia"] .chart-value {
  min-width: 0;
  text-align: right !important;
  white-space: nowrap !important;
  font-variant-numeric: tabular-nums;
  color: #101f46 !important;
  font-weight: 700 !important;
}
.scene[data-slug="procedencia"] .section-head h2 .source-title-line {
  display: block !important;
  white-space: nowrap !important;
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
/* Selected metrics and segmented tabs use the Air Europa corporate blue. */
.segmented .seg-btn.selected,
.segmented .seg-btn.active,
.segmented .seg-btn.is-active,
.segmented .seg-btn[aria-selected="true"],
.segmented .seg-btn[aria-pressed="true"],
.segmented button[data-state="active"],
.tabs button.selected,
.tabs button.active,
.tabs button[aria-selected="true"],
.tab-list [role="tab"][aria-selected="true"],
.tab-bar button.active,
.tab-buttons button.active {
  background: #1659bd !important;
  background-color: #1659bd !important;
  background-image: none !important;
  color: #fff !important;
  border-color: #1659bd !important;
  box-shadow: inset 0 0 0 1px #1659bd, 0 2px 5px rgba(18,66,145,.16) !important;
  font-weight: 700 !important;
}
.segmented .seg-btn.selected:hover,
.segmented .seg-btn.active:hover,
.tabs button.active:hover,
.tab-bar button.active:hover {
  background: #0f469f !important;
  background-color: #0f469f !important;
}
.segmented .seg-btn:focus-visible,
.tabs button:focus-visible,
.tab-list [role="tab"]:focus-visible,
.tab-bar button:focus-visible {
  outline: 3px solid #9cc4fa !important;
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
    # The final editorial fixes may change this heading before the slide is rendered.
    # Target the heading element itself, not an outdated literal string.
    intended_title = (
        'Google Flights y Skyscanner reúnen el 82,9 %'
        '<span class="source-title-line" style="display:block!important">de las sesiones</span>'
    )
    slide = re.sub(
        r'(<h2\b[^>]*>)(.*?)(</h2>)',
        lambda m: m.group(1) + intended_title + m.group(3),
        slide, count=1, flags=re.I | re.S
    )
    # Explicit inline colors guarantee the four bars retain their distinct palette
    # even when legacy styles or theme variables override backgrounds.
    for legacy_color, dashboard_color in (
        ("var(--gflights)", "#2563eb"),
        ("var(--sky)", "#0d9488"),
        ("var(--kayak)", "#f97316"),
        ("var(--other)", "#94a3b8"),
    ):
        slide = slide.replace("background:" + legacy_color, "background:" + dashboard_color + " !important")
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



RANKING_FIT_JS = r"""
(function () {
  "use strict";
  // Keep the original text from the presentation for each metric.
  // Only adjust the KPI size when the number is too wide for its fixed card.
  function setup() {
    const scene = document.querySelector('.scene[data-slug="rendimiento"]');
    const card = scene && scene.querySelector('.ranking-reading');
    const value = card && card.querySelector('.ranking-main-value');
    if (!card || !value) return;
    let queued = false;
    function fit() {
      queued = false;
      card.classList.remove('metrics-compact', 'metrics-tight');
      value.style.removeProperty('font-size');
      const initial = window.innerWidth <= 540 ? 56 : 64;
      let size = initial;
      value.style.setProperty('font-size', size + 'px', 'important');
      // Numerals differ in length: e.g. 11,5 % and 52,82 M€.
      while (size > 42 && value.scrollWidth > value.clientWidth + 1) {
        size -= 2;
        value.style.setProperty('font-size', size + 'px', 'important');
      }
      if (card.scrollHeight > card.clientHeight + 2) {
        card.classList.add('metrics-compact');
      }
      if (card.scrollHeight > card.clientHeight + 2) {
        card.classList.add('metrics-tight');
      }
    }
    function schedule() {
      if (queued) return;
      queued = true;
      window.requestAnimationFrame(fit);
    }
    new MutationObserver(schedule).observe(card, {
      childList: true,
      characterData: true,
      subtree: true
    });
    scene.querySelectorAll('.seg-btn').forEach(function (btn) {
      btn.addEventListener('click', schedule);
    });
    if (window.ResizeObserver) new ResizeObserver(schedule).observe(card);
    window.addEventListener('resize', schedule);
    schedule();
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setup, {once: true});
  } else {
    setup();
  }
})();
"""


PROCEDENCIA_HEADING_FIX_JS = r"""
(function () {
  "use strict";
  const lead = "Google Flights y Skyscanner reúnen el 82,9 %";
  const tail = "de las sesiones";
  const init = function () {
    const scene = document.querySelector('.scene[data-slug="procedencia"]');
    if (!scene) return;
    const ensureLineBreak = function () {
      const heading = scene.querySelector('.section-head h2');
      if (!heading) return;
      const span = heading.firstElementChild;
      const correct = heading.childNodes.length === 2 &&
        heading.firstChild.nodeType === 3 &&
        heading.firstChild.textContent === lead &&
        span && span.classList.contains('source-title-line') &&
        span.textContent === tail;
      if (correct) return;
      const newSpan = document.createElement("span");
      newSpan.className = "source-title-line";
      newSpan.textContent = tail;
      newSpan.style.setProperty("display", "block", "important");
      heading.replaceChildren(document.createTextNode(lead), newSpan);
    };
    const observer = new MutationObserver(ensureLineBreak);
    observer.observe(scene, {childList: true, characterData: true, subtree: true});
    ensureLineBreak();
    window.addEventListener("hashchange", ensureLineBreak);
  };
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, {once: true});
  } else {
    init();
  }
})();
"""


CONTEXTO_REFINED_CSS = r"""
/* Contexto only. A sober three-column editorial composition using the verified
   Untitled UI Metric item surface: neutral border, 12px radius, subtle shadow. */
.scene[data-slug="contexto"] .center-block {
  width: 100%;
  max-width: 1070px;
  margin-inline: auto;
}
.scene[data-slug="contexto"] .center-block > .flow {
  box-sizing: border-box !important;
  display: grid !important;
  grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
  align-items: stretch !important;
  gap: 18px !important;
  width: 100% !important;
  max-width: 100%;
  padding: 0 !important;
  margin: 0 !important;
  background: transparent !important;
  border: 0 !important;
}
.scene[data-slug="contexto"] .center-block > .flow > .flow-step,
.scene[data-slug="contexto"] .center-block > .flow > .flow-step + .flow-step {
  box-sizing: border-box !important;
  display: flex !important;
  flex-direction: column !important;
  justify-content: flex-start !important;
  align-items: stretch !important;
  min-width: 0 !important;
  width: 100% !important;
  min-height: 260px !important;
  height: auto !important;
  padding: 26px 26px 28px !important;
  margin: 0 !important;
  border: 1px solid #eaecf0 !important;
  border-radius: 12px !important;
  background: #ffffff !important;
  box-shadow: 0 1px 2px rgba(16, 24, 40, .055) !important;
  overflow: visible !important;
}
.scene[data-slug="contexto"] .flow-step-title {
  display: block !important;
  min-width: 0;
  font-size: clamp(21px, 1.65vw, 24px) !important;
  line-height: 1.25 !important;
  font-weight: 700 !important;
  letter-spacing: -.025em !important;
  color: #101f46 !important;
  margin: 0 !important;
  text-wrap: balance;
}
.scene[data-slug="contexto"] .flow-step p {
  min-width: 0;
  max-width: 100%;
  font-size: 16px !important;
  line-height: 1.52 !important;
  font-weight: 400 !important;
  color: #475467 !important;
  margin: 15px 0 0 !important;
  overflow-wrap: break-word !important;
  text-wrap: pretty;
}
.scene[data-slug="contexto"] .center-block > .takeaway {
  box-sizing: border-box !important;
  display: block !important;
  width: 100% !important;
  max-width: 100% !important;
  margin: 22px 0 0 !important;
  padding: 18px 1px 0 !important;
  border: 0 !important;
  border-top: 1px solid #eaecf0 !important;
  border-radius: 0 !important;
  background: transparent !important;
  box-shadow: none !important;
  color: #101f46 !important;
  font-size: clamp(18px, 1.45vw, 21px) !important;
  font-weight: 650 !important;
  line-height: 1.4 !important;
  letter-spacing: -.015em !important;
  text-align: left !important;
}
@media (max-width: 900px) {
  .scene[data-slug="contexto"] .center-block > .flow {
    grid-template-columns: minmax(0, 1fr) !important;
    gap: 14px !important;
  }
  .scene[data-slug="contexto"] .center-block > .flow > .flow-step,
  .scene[data-slug="contexto"] .center-block > .flow > .flow-step + .flow-step {
    min-height: 0 !important;
    padding: 22px 24px !important;
  }
  .scene[data-slug="contexto"] .center-block > .takeaway {
    margin-top: 18px !important;
  }
}
@media (min-width: 901px) and (max-height: 750px) {
  .scene[data-slug="contexto"] .center-block > .flow > .flow-step,
  .scene[data-slug="contexto"] .center-block > .flow > .flow-step + .flow-step {
    min-height: 242px !important;
    padding: 21px 23px 22px !important;
  }
  .scene[data-slug="contexto"] .flow-step p {
    font-size: 15px !important;
    margin-top: 11px !important;
  }
  .scene[data-slug="contexto"] .center-block > .takeaway {
    margin-top: 15px !important;
    padding-top: 14px !important;
  }
}
"""


def patch_contexto_copy(html):
    """Improve the narrative, keeping only source-supported facts and the same DOM."""
    from html import escape as _escape
    start = re.search(r'<section\b[^>]*data-slug=["\']contexto["\'][^>]*>', html, re.I)
    if not start:
        return html
    next_scene = re.search(r'<section\b[^>]*class=["\'][^"\']*\bscene\b', html[start.end():], re.I)
    end = start.end() + next_scene.start() if next_scene else len(html)
    section = html[start.start():end]
    step_pattern = re.compile(
        r'(<div\b[^>]*class=["\'][^"\']*\bflow-step\b[^"\']*["\'][^>]*>\s*'
        r'<div\b[^>]*class=["\'][^"\']*\bflow-step-title\b[^"\']*["\'][^>]*>.*?</div>\s*'
        r'<p\b[^>]*>)(.*?)(</p>)', re.I | re.S
    )
    matches = list(step_pattern.finditer(section))
    if len(matches) != 3:
        return html
    # Avoid editing a different slide layout or unexpected content.
    expected = ('Metabuscador', 'Amadeus MetaConnect', 'Booking de Air Europa')
    if any(name not in matches[i].group(0) for i, name in enumerate(expected)):
        return html
    descriptions = (
        'El usuario compara vuelos, precios y, según la plataforma, alternativas de tarifa. Al hacer clic, llega con una oferta concreta como referencia.',
        'MetaConnect conecta el metabuscador con la oferta y la búsqueda en Air Europa. Aquí importa qué información se conserva al pasar de un entorno a otro.',
        'Ejemplo actual: desde Skyscanner se aterriza en Availability. La entrada a Shopping Cart con la selección recuperada sigue en desarrollo.',
    )
    count = iter(descriptions)
    section = step_pattern.sub(lambda m: m.group(1) + _escape(next(count)) + m.group(3), section, count=3)
    return html[:start.start()] + section + html[end:]

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
    if "rank-chart" in html:
        html = html.replace("</body>", "<script>\n" + RANKING_FIT_JS + "\n</script></body>", 1)
    if 'data-slug="procedencia"' in html or "data-slug='procedencia'" in html:
        html = html.replace("</body>", "<script>\n" + PROCEDENCIA_HEADING_FIX_JS + "\n</script></body>", 1)
    html = patch_contexto_copy(html)
    html = html.replace("</style>", CONTEXTO_REFINED_CSS + "\n</style>", 1)
    return html.encode("utf-8")




PREVIEW_V2_VERTICAL_CSS = r"""
/* Metabuscadores: vertical, content-first landing. Applied ONLY to /preview-v2. */
:root {scroll-behavior:smooth}
html,body {height:auto!important;min-height:100%!important;overflow-x:hidden!important;overflow-y:auto!important;background:#fff!important;}
.workspace {display:block!important;height:auto!important;min-height:100vh!important;overflow:visible!important;}
.toolbar,.navigation {display:none!important;}
.viewport {display:block!important;flex:none!important;width:100%!important;height:auto!important;min-height:0!important;padding:0!important;margin:0!important;overflow:visible!important;position:relative!important;}
.stage {display:block!important;position:relative!important;width:100%!important;max-width:none!important;height:auto!important;transform:none!important;margin:0!important;box-shadow:none!important;border-radius:0!important;overflow:visible!important;}
.slide,.slide.is-active {
  box-sizing:border-box!important;display:block!important;position:relative!important;
  visibility:visible!important;opacity:1!important;pointer-events:auto!important;
  width:100%!important;height:auto!important;min-height:0!important;inset:auto!important;
}
.slide-cover {
  display:flex!important;flex-direction:column!important;
  min-height:100vh!important;min-height:100svh!important;
  padding:clamp(28px,4vw,62px) clamp(26px,7.1vw,122px) clamp(34px,4.1vw,66px)!important;
  background:#031B4E!important;isolation:isolate;color:white!important;
}
.slide-cover::before {content:"";position:absolute;z-index:-1;pointer-events:none;top:0;right:0;bottom:0;width:43%;background:radial-gradient(ellipse at 100% 48%,rgba(45,105,225,.21) 0%,rgba(45,105,225,.055) 48%,transparent 78%);}
.cover-corner,.cover-sheen,.cover-swatch,.cover-visual,.rule-top,.cover-bottom-line {display:none!important;}
.cover-nav {display:flex!important;position:relative!important;top:auto!important;left:auto!important;right:auto!important;width:100%!important;align-items:center!important;justify-content:space-between!important;gap:24px!important;z-index:2;}
.cover-nav .logo {width:230px!important;height:56px!important;object-fit:contain!important;object-position:left center!important;filter:brightness(0) invert(1)!important;}
.edition {font-weight:650!important;font-size:13px!important;letter-spacing:.11em!important;}
.cover-copy {
  display:block!important;position:relative!important;top:auto!important;left:auto!important;
  z-index:2!important;width:min(1070px,100%)!important;max-width:100%!important;
  margin:auto 0!important;padding:clamp(70px,10vh,124px) 0 clamp(80px,11vh,140px)!important;
}
.cover-copy .eyebrow {font-size:12px!important;letter-spacing:.14em!important;gap:14px!important;color:rgba(255,255,255,.76)!important;}
.cover-copy .eyebrow .dash {width:36px!important;background:#2D69E1!important;height:4px!important;}
.cover-copy h1 {font-size:clamp(70px,9.2vw,132px)!important;line-height:1.02!important;letter-spacing:-.067em!important;font-weight:790!important;margin:26px 0 30px!important;max-width:100%!important;white-space:normal!important;text-wrap:balance!important;}
.cover-subtitle {font-size:clamp(25px,3.2vw,41px)!important;line-height:1.26!important;letter-spacing:-.038em!important;font-weight:520!important;color:white!important;max-width:850px!important;margin:0!important;text-wrap:balance!important;}
.cover-subtitle span {color:#82ACFF!important;}
.cover-description {font-size:clamp(16px,1.4vw,20px)!important;max-width:720px!important;color:#B9CBE8!important;line-height:1.56!important;margin-top:24px!important;}
.cover-bottom {position:relative!important;left:auto!important;right:auto!important;bottom:auto!important;display:flex!important;justify-content:space-between!important;gap:20px!important;color:#C8D5EA!important;font-size:12px!important;font-weight:600!important;letter-spacing:.065em!important;}
.slide-context {padding:clamp(50px,5.9vw,104px) clamp(26px,7.1vw,122px) clamp(66px,6.7vw,104px)!important;min-height:100vh!important;min-height:100svh!important;background:white!important;}
.context-top,.context-kicker,.context-title,.context-lead,.journey,.context-rule,.context-foot {
  position:relative!important;top:auto!important;bottom:auto!important;left:auto!important;right:auto!important;width:100%!important;height:auto!important;
}
.context-top{display:flex!important;align-items:center!important;justify-content:space-between!important;gap:30px!important;}
.context-top .logo{width:210px!important;height:51px!important;object-fit:contain!important;}
.context-ref{font-size:12px!important;letter-spacing:.09em!important;}
.context-kicker{margin-top:clamp(72px,8vh,112px)!important;font-size:13px!important;letter-spacing:.14em!important;}
.context-title {font-size:clamp(45px,5.6vw,78px)!important;line-height:1.14!important;max-width:1200px!important;letter-spacing:-.061em!important;margin:27px 0 0!important;}
.context-title em{color:#2D69E1!important;}
.context-lead{font-size:clamp(18px,1.65vw,23px)!important;line-height:1.56!important;max-width:1060px!important;margin:27px 0 0!important;color:#475467!important;}
.journey{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:20px!important;margin-top:clamp(48px,6vw,86px)!important;}
.journey-card {box-shadow:0 1px 2px rgba(16,24,40,.045)!important;border:1px solid #E4E7EC!important;border-radius:14px!important;min-height:242px!important;padding:26px 27px 28px!important;overflow-wrap:break-word!important;}
.journey-card::before{height:4px!important;}
.journey-card h3{font-size:clamp(19px,1.9vw,24px)!important;line-height:1.18!important;letter-spacing:-.025em!important;}
.journey-card p{font-size:15px!important;line-height:1.55!important;}
.journey-card .fine{font-size:12px!important;}
.context-rule{margin-top:clamp(45px,5.5vw,72px)!important;min-height:1px!important;background:#E4E7EC!important;}
.context-foot {display:flex!important;align-items:flex-start!important;justify-content:space-between!important;gap:22px!important;flex-wrap:wrap!important;margin-top:23px!important;line-height:1.55!important;}
.context-foot>span:first-child{max-width:70%;}
@media (max-width:900px){
  .slide-cover{min-height:780px!important;}
  .journey{grid-template-columns:1fr!important;gap:13px!important;}
  .journey-card{min-height:0!important;padding:21px 23px!important;}
  .context-title br{display:none!important;}
  .context-foot>span:first-child{max-width:100%;}
  .context-kicker{margin-top:75px!important;}
}
@media (max-width:560px){
  .cover-nav .logo{width:180px!important;height:46px!important;}
  .edition{font-size:10px!important;}
  .cover-copy{padding:75px 0 84px!important;}
  .cover-copy h1{font-size:clamp(46px,13vw,72px)!important;margin-top:25px!important;overflow-wrap:break-word!important;}
  .cover-copy .eyebrow{font-size:10px!important;line-height:1.5!important;letter-spacing:.075em!important;}
  .cover-subtitle{font-size:clamp(25px,6.8vw,34px)!important;}
  .cover-description{font-size:16px!important;}
  .cover-bottom{font-size:10px!important;}
  .context-top .logo{width:170px!important;height:44px!important;}
  .context-ref{font-size:10px!important;text-align:right!important;}
  .context-title{font-size:clamp(40px,9.5vw,56px)!important;}
  .context-lead{font-size:18px!important;}
  .context-foot{font-size:12px!important;}
}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto!important;}}
"""

def render_vertical_preview(prototype):
    """Reflow only the self-contained preview into a vertical landing.
    Keep the private content in environment configuration unchanged.
    """
    prototype = re.sub(r'<header class="toolbar">.*?</header>', '', prototype, count=1, flags=re.S)
    prototype = re.sub(r'<nav class="navigation"[^>]*>.*?</nav>', '', prototype, count=1, flags=re.S)
    # Remove the preview's slide keyboard/scale controls. No legacy main-page scripts are touched.
    prototype = re.sub(r'<script>\s*\(function\(\).*?</script>', '', prototype, count=1, flags=re.S)
    prototype = prototype.replace('aria-hidden="true"', 'aria-hidden="false"')
    prototype = prototype.replace(
        '<p class="cover-subtitle">De la intención de búsqueda a la experiencia de compra</p>',
        '<p class="cover-subtitle">De la intención de búsqueda a la <span>experiencia de compra</span></p>'
    )
    prototype = prototype.replace('EDICIÓN DE TRABAJO</span>', 'DESLIZA PARA EXPLORAR ↓</span>')
    prototype = prototype.replace('</style>', PREVIEW_V2_VERTICAL_CSS + '\n</style>', 1)
    return prototype


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
        # Optional, authenticated two-slide visual prototype.
        # The private HTML stays in Render environment configuration, not in Git.
        if path in ("/preview-v2", "/preview-v2/"):
            if os.environ.get("METAS_PRESENTATION_V2_ENABLED") != "1":
                self._send_body(404, b"Preview disabled", "text/plain")
                return
            prototype = os.environ.get("METAS_PRESENTATION_V2_HTML", "")
            if not prototype:
                self._send_body(503, b"Preview not configured", "text/plain")
            else:
                self._send_body(200, render_vertical_preview(prototype).encode("utf-8"))
            return
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

    # Safe structural startup check, without private data or user information.
    rendered = get_html().decode("utf-8")
    proc_start = rendered.find('data-slug="procedencia"')
    if proc_start < 0:
        proc_start = rendered.find("data-slug='procedencia'")
    proc_chunk = rendered[proc_start:proc_start + 17000] if proc_start >= 0 else ""
    title_ok = '82,9 %<span class="source-title-line" style="display:block!important">de las sesiones</span>' in proc_chunk
    cards_ok = 'source-chart-heading' in proc_chunk and 'source-chart-column-headings' in proc_chunk
    color_ok = all("background:" + c + " !important" in proc_chunk for c in ("#2563eb", "#0d9488", "#f97316", "#94a3b8"))
    tabs_ok = '.segmented .seg-btn.selected' in rendered and 'background-color: #1659bd' in rendered
    print("METAS_LAYOUT_VERIFY title_split=" + str(title_ok) + " chart_labels=" + str(cards_ok) + " distinct_bars=" + str(color_ok) + " tabs_blue=" + str(tabs_ok), flush=True)
    context_ok = all(snippet in rendered for snippet in (
        'El usuario compara vuelos, precios',
        'MetaConnect conecta el metabuscador',
        'Ejemplo actual: desde Skyscanner se aterriza en Availability',
    ))
    context_style_ok = ('CONTEXTO_REFINED_CSS' not in rendered and
                        '.scene[data-slug="contexto"] .center-block > .flow' in rendered)
    print("CONTEXT_REFINEMENT_VERIFY copy=" + str(context_ok) +
          " styles=" + str(context_style_ok), flush=True)
    # Temporary private diagnostic: only first-slide markup, never image assets.
    if os.environ.get("METAS_PORTADA_AUDIT") == "1":
        start = re.search(r'<section\b[^>]*data-slug=["\']portada["\'][^>]*>', rendered, re.I)
        if start:
            boundary = re.search(r'<section\b[^>]*\bclass=["\'][^"\']*\bscene\b', rendered[start.end():], re.I)
            end = start.end() + boundary.start() if boundary else len(rendered)
            fragment = rendered[start.start():end][:24000]
            fragment = re.sub(r'<img\b[^>]*>', '<IMG/>', fragment, flags=re.I | re.S)
            fragment = re.sub(r'<svg\b.*?</svg>', '<SVG/>', fragment, flags=re.I | re.S)
            fragment = re.sub(r'data:image/[^"\']+', 'data:image:omitted', fragment, flags=re.I)
            fragment = re.sub(r'\s+', ' ', fragment)
            print("METAS_PORTADA_AUDIT " + fragment[:7500], flush=True)
            relevant = []
            first_style = rendered.split('</style>',1)[0]
            for match in re.finditer(r'([^{}]+)\{([^{}]*)\}', first_style):
                selector, body = match.group(1).strip(), match.group(2).strip()
                if any(token in selector for token in ('.cover', '.cover-inner', '.brand-logo', '.scene {', '.scene,', 'html,body')):
                    relevant.append(selector[:230] + ' {' + body[:900] + '}')
                if len(relevant) >= 20:
                    break
            print("METAS_COVER_CSS_AUDIT " + " || ".join(relevant)[:9500], flush=True)
        else:
            print("METAS_PORTADA_AUDIT missing_portada", flush=True)
    ThreadingHTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
