from pathlib import Path

ROOT = Path("app/ux-intelligence-demo-exact")
ROOT.mkdir(parents=True, exist_ok=True)

parts_dir = Path("v6184_parts")
target = ROOT / "index.html"
parts = sorted(parts_dir.glob("part_*.txt"))
if len(parts) != 18:
    raise SystemExit(f"ERROR: se esperaban 18 partes de v6-184 y hay {len(parts)}")

chunks = [part.read_text(encoding="utf-8") for part in parts]
s = ""
for chunk in chunks:
    if s and chunk and not s.endswith("\n") and not chunk.startswith("\n"):
        s += "\n"
    s += chunk

expected_build = 'data-build="2026-10-27-v6-184-strict-learning-taxonomy"'
if expected_build not in s:
    raise SystemExit("ERROR: la fuente ensamblada no es la build v6-184 esperada")

# La copia pública debe conservar exactamente la Dimensión UX ya presente en
# los registros originales. No inferimos ni rellenamos dimensiones nuevas.
# Exponemos un mapa por texto de hallazgo y lo usamos solo como fallback cuando
# la capa pública pierde uxLine durante la normalización.
public_rows_anchor = "const publicDemoRows=["
anchor_pos = s.find(public_rows_anchor)
if anchor_pos < 0:
    raise SystemExit("ERROR: no se encuentra publicDemoRows")

rows_start = anchor_pos + len("const publicDemoRows=")
rows_end = s.find("];", rows_start)
if rows_end < 0:
    raise SystemExit("ERROR: no se puede cerrar publicDemoRows")
rows_literal = s[rows_start:rows_end+1]

import json
try:
    public_rows = json.loads(rows_literal)
except Exception as exc:
    raise SystemExit(f"ERROR: publicDemoRows no es JSON válido: {exc}")

dimension_by_insight = {
    str(row.get("insight") or "").strip(): str(row.get("uxLine") or "").strip()
    for row in public_rows
    if str(row.get("insight") or "").strip() and str(row.get("uxLine") or "").strip()
}
dimension_map_js = json.dumps(dimension_by_insight, ensure_ascii=False, separators=(",",":"))

inject_after = rows_literal + ";"
replacement = rows_literal + ";globalThis.__UX_PUBLIC_DIMENSIONS_BY_INSIGHT=" + dimension_map_js + ";"
if "__UX_PUBLIC_DIMENSIONS_BY_INSIGHT" not in s:
    s = s[:rows_start] + replacement + s[rows_end+2:]

structured_old = "uxLine:row.uxLine||'',"
structured_new = "uxLine:row.uxLine||globalThis.__UX_PUBLIC_DIMENSIONS_BY_INSIGHT?.[String(row.insight||'').trim()]||'',"
if structured_old in s:
    s = s.replace(structured_old, structured_new, 1)

fallback_old = "uxLine:first(row,['Dimensión','Dimension','dimensión','dimension','Dimensión UX','Dimension UX','dimensión ux','dimension ux','Línea UX','Linea UX','línea ux','linea ux','Línea UX / agrupación','Linea UX / agrupacion','línea ux / agrupación','linea ux / agrupacion']),"
fallback_new = "uxLine:first(row,['Dimensión','Dimension','dimensión','dimension','Dimensión UX','Dimension UX','dimensión ux','dimension ux','Línea UX','Linea UX','línea ux','linea ux','Línea UX / agrupación','Linea UX / agrupacion','línea ux / agrupación','linea ux / agrupacion'])||globalThis.__UX_PUBLIC_DIMENSIONS_BY_INSIGHT?.[String(first(row,['Insight / hallazgo','Insight','insight','Hallazgo','hallazgo'])||'').trim()]||'',"
if fallback_old in s:
    s = s.replace(fallback_old, fallback_new, 1)

# La demo pública no tiene el estado local persistido de Taxonomía.
# Inyectamos exclusivamente el canon ya definido en v6-184; no se infiere nada nuevo.
canonical_terms = [
    {"id":"ux-product-home","level":"product","canonicalName":"Home","name":"Home","parentId":"","status":"canonical","governed":True,"aliases":[],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-component-home-header","level":"component","canonicalName":"Header","name":"Header","parentId":"ux-product-home","status":"canonical","governed":True,"aliases":[],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-component-home-buscador","level":"component","canonicalName":"Buscador","name":"Buscador","parentId":"ux-product-home","status":"canonical","governed":True,"aliases":["Buscador de vuelos","Calendario"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-component-home-banner-promocional","level":"component","canonicalName":"Banner promocional","name":"Banner promocional","parentId":"ux-product-home","status":"canonical","governed":True,"aliases":["Banner","Banners promocionales"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-component-home-avisos","level":"component","canonicalName":"Avisos","name":"Avisos","parentId":"ux-product-home","status":"canonical","governed":True,"aliases":["Aviso","Mensajes de aviso"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-component-home-accesos-rapidos","level":"component","canonicalName":"Accesos rápidos","name":"Accesos rápidos","parentId":"ux-product-home","status":"canonical","governed":True,"aliases":["Accesos rapidos","Accesos de autogestión","Accesos de autogestion"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-component-home-hero-banner","level":"component","canonicalName":"Hero Banner","name":"Hero Banner","parentId":"ux-product-home","status":"canonical","governed":True,"aliases":["Hero","Hero / contenido comercial"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-component-home-claim","level":"component","canonicalName":"Claim","name":"Claim","parentId":"ux-product-home","status":"canonical","governed":True,"aliases":["Contenido comercial","Claim principal","H1 principal"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},

    {"id":"ux-product-booking","level":"product","canonicalName":"Booking","name":"Booking","parentId":"","status":"canonical","governed":True,"aliases":[],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-funnel-booking-availability","level":"funnel","canonicalName":"Availability","name":"Availability","parentId":"ux-product-booking","status":"canonical","governed":True,"aliases":["Disponibilidad","Availability/Dispo","Dispo"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-component-availability-fare-families","level":"component","canonicalName":"Fare Families","name":"Fare Families","parentId":"ux-funnel-booking-availability","status":"canonical","governed":True,"aliases":[],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-component-availability-upsell-panel","level":"component","canonicalName":"Upsell Panel","name":"Upsell Panel","parentId":"ux-funnel-booking-availability","status":"canonical","governed":True,"aliases":["Upsell","Panel de upsell"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},

    {"id":"ux-funnel-booking-shopping-cart","level":"funnel","canonicalName":"Shopping Cart","name":"Shopping Cart","parentId":"ux-product-booking","status":"canonical","governed":True,"aliases":["Carrito","Summary","Resumen","Resumen / Shopping Cart","Summary / Shopping Cart"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-component-shopping-cart-slider-de-millas","level":"component","canonicalName":"Slider de Millas","name":"Slider de Millas","parentId":"ux-funnel-booking-shopping-cart","status":"canonical","governed":True,"aliases":["Slider Millas","Cash & Miles"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-component-shopping-cart-footer","level":"component","canonicalName":"Footer","name":"Footer","parentId":"ux-funnel-booking-shopping-cart","status":"canonical","governed":True,"aliases":["Footer Millas","Footer de Millas"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},

    {"id":"ux-funnel-booking-passengers","level":"funnel","canonicalName":"Passengers","name":"Passengers","parentId":"ux-product-booking","status":"canonical","governed":True,"aliases":["Pasajeros","Passengers/Paxes","Paxes"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-component-passengers-card-confirmacion-pasajero-suma","level":"component","canonicalName":"Card confirmación pasajero SUMA","name":"Card confirmación pasajero SUMA","parentId":"ux-funnel-booking-passengers","status":"canonical","governed":True,"aliases":["Card Confirmación del pasajero","Card Confirmación del pasajero SUMA","Confirmación del pasajero","Confirmación del pasajero SUMA","¿Eres tú el que viaja?"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-component-passengers-card-datos-del-pasajero","level":"component","canonicalName":"Card Datos del pasajero","name":"Card Datos del pasajero","parentId":"ux-funnel-booking-passengers","status":"canonical","governed":True,"aliases":["Datos Pasajero","Datos del pasajero","Card Datos Pasajero"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-component-passengers-card-pasajero-suma","level":"component","canonicalName":"Card pasajero SUMA","name":"Card pasajero SUMA","parentId":"ux-funnel-booking-passengers","status":"canonical","governed":True,"aliases":["Card Pasajero frecuente","Pasajero frecuente","Tarjeta pasajero frecuente","Tarjeta de pasajero frecuente","Card Tarjeta pasajero frecuente"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},

    {"id":"ux-funnel-booking-extras","level":"funnel","canonicalName":"Extras","name":"Extras","parentId":"ux-product-booking","status":"canonical","governed":True,"aliases":[],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-component-extras-cards-de-extras","level":"component","canonicalName":"Cards de extras","name":"Cards de extras","parentId":"ux-funnel-booking-extras","status":"canonical","governed":True,"aliases":["Cards Extras","Card Extras"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-component-extras-detalle-del-vuelo","level":"component","canonicalName":"Detalle del vuelo","name":"Detalle del vuelo","parentId":"ux-funnel-booking-extras","status":"canonical","governed":True,"aliases":["Detalle vuelo"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-component-extras-card-asiento","level":"component","canonicalName":"Card Asiento","name":"Card Asiento","parentId":"ux-funnel-booking-extras","status":"canonical","governed":True,"aliases":["Card Asientos"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-component-extras-card-equipaje","level":"component","canonicalName":"Card Equipaje","name":"Card Equipaje","parentId":"ux-funnel-booking-extras","status":"canonical","governed":True,"aliases":["Card Maletas"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-component-extras-card-priority-boarding","level":"component","canonicalName":"Card Priority Boarding","name":"Card Priority Boarding","parentId":"ux-funnel-booking-extras","status":"canonical","governed":True,"aliases":["Card Embarque prioritario"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-component-extras-card-wi-fi","level":"component","canonicalName":"Card Wi-Fi","name":"Card Wi-Fi","parentId":"ux-funnel-booking-extras","status":"canonical","governed":True,"aliases":["Card WiFi","Card Wifi"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-component-extras-card-menu-a-bordo","level":"component","canonicalName":"Card Menú a bordo","name":"Card Menú a bordo","parentId":"ux-funnel-booking-extras","status":"canonical","governed":True,"aliases":["Card Menu a bordo","Card Menu"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-component-extras-card-mascotas","level":"component","canonicalName":"Card Mascotas","name":"Card Mascotas","parentId":"ux-funnel-booking-extras","status":"canonical","governed":True,"aliases":["Card Mascota"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},

    {"id":"ux-minifunnel-extras-asientos","level":"minifunnel","canonicalName":"Asientos","name":"Asientos","parentId":"ux-funnel-booking-extras","status":"canonical","governed":True,"aliases":["Reserva de asiento","Reserva de asientos"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-component-asientos-selector-por-pasajero","level":"component","canonicalName":"Selector por pasajero","name":"Selector por pasajero","parentId":"ux-minifunnel-extras-asientos","status":"canonical","governed":True,"aliases":["Selección por pasajero","Seleccion por pasajero"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-minifunnel-extras-equipaje","level":"minifunnel","canonicalName":"Equipaje","name":"Equipaje","parentId":"ux-funnel-booking-extras","status":"canonical","governed":True,"aliases":["Maletas"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-component-equipaje-selector-por-pasajero","level":"component","canonicalName":"Selector por pasajero","name":"Selector por pasajero","parentId":"ux-minifunnel-extras-equipaje","status":"canonical","governed":True,"aliases":["Selección por pasajero","Seleccion por pasajero"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-minifunnel-extras-priority-boarding","level":"minifunnel","canonicalName":"Priority Boarding","name":"Priority Boarding","parentId":"ux-funnel-booking-extras","status":"canonical","governed":True,"aliases":["Embarque prioritario"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-component-priority-boarding-selector-por-pasajero","level":"component","canonicalName":"Selector por pasajero","name":"Selector por pasajero","parentId":"ux-minifunnel-extras-priority-boarding","status":"canonical","governed":True,"aliases":["Selección por pasajero","Seleccion por pasajero"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-minifunnel-extras-wi-fi","level":"minifunnel","canonicalName":"Wi-Fi","name":"Wi-Fi","parentId":"ux-funnel-booking-extras","status":"canonical","governed":True,"aliases":["WiFi","Wifi","Wi Fi"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-component-wi-fi-selector-por-pasajero","level":"component","canonicalName":"Selector por pasajero","name":"Selector por pasajero","parentId":"ux-minifunnel-extras-wi-fi","status":"canonical","governed":True,"aliases":["Selección por pasajero","Seleccion por pasajero"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-minifunnel-extras-menu-a-bordo","level":"minifunnel","canonicalName":"Menú a bordo","name":"Menú a bordo","parentId":"ux-funnel-booking-extras","status":"canonical","governed":True,"aliases":["Menu a bordo","Menu"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-component-menu-a-bordo-selector-por-pasajero","level":"component","canonicalName":"Selector por pasajero","name":"Selector por pasajero","parentId":"ux-minifunnel-extras-menu-a-bordo","status":"canonical","governed":True,"aliases":["Selección por pasajero","Seleccion por pasajero"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-minifunnel-extras-mascotas","level":"minifunnel","canonicalName":"Mascotas","name":"Mascotas","parentId":"ux-funnel-booking-extras","status":"canonical","governed":True,"aliases":["Mascota","Pets"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-component-mascotas-selector-por-pasajero","level":"component","canonicalName":"Selector por pasajero","name":"Selector por pasajero","parentId":"ux-minifunnel-extras-mascotas","status":"canonical","governed":True,"aliases":["Selección por pasajero","Seleccion por pasajero"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-minifunnel-extras-equipaje-deportivo","level":"minifunnel","canonicalName":"Equipaje deportivo","name":"Equipaje deportivo","parentId":"ux-funnel-booking-extras","status":"canonical","governed":True,"aliases":["Equipajes deportivos"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-component-equipaje-deportivo-selector-por-pasajero","level":"component","canonicalName":"Selector por pasajero","name":"Selector por pasajero","parentId":"ux-minifunnel-extras-equipaje-deportivo","status":"canonical","governed":True,"aliases":["Selección por pasajero","Seleccion por pasajero"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},

    {"id":"ux-funnel-booking-payment","level":"funnel","canonicalName":"Payment","name":"Payment","parentId":"ux-product-booking","status":"canonical","governed":True,"aliases":["Pago"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-funnel-booking-transversal","level":"funnel","canonicalName":"Transversal","name":"Transversal","parentId":"ux-product-booking","status":"canonical","governed":True,"aliases":["Booking transversal"],"origin":"UX Intelligence · criterio canónico 2026-10-22"},
    {"id":"ux-component-transversal-login-autenticacion","level":"component","canonicalName":"Login / autenticación","name":"Login / autenticación","parentId":"ux-funnel-booking-transversal","status":"canonical","governed":True,"aliases":["Login","Login contextual"],"origin":"UX Intelligence · criterio canónico 2026-10-22"}
]

import json
canonical_terms_js = json.dumps(canonical_terms, ensure_ascii=False, separators=(",",":"))
needle = "terms:[],"
if needle not in s:
    raise SystemExit("ERROR: no se encuentra publicTaxonomyState con terms vacío")
s = s.replace(needle, "terms:" + canonical_terms_js + ",", 1)

# Taxonomía de consulta: se prerenderiza en build para no depender del renderer editable.
def _taxonomy_ordered_rows(terms):
    by_parent = {}
    by_id = {str(item.get("id","")): item for item in terms}
    for item in terms:
        if item.get("status") != "canonical" or item.get("governed") is False:
            continue
        by_parent.setdefault(str(item.get("parentId","")), []).append(item)
    level_order = {"product":0,"funnel":1,"minifunnel":2,"component":3}
    for items in by_parent.values():
        items.sort(key=lambda x: (level_order.get(x.get("level"),9), str(x.get("canonicalName") or x.get("name") or "").lower()))
    rows = []
    def visit(parent="", depth=0):
        for item in by_parent.get(str(parent), []):
            rows.append((item, depth))
            visit(item.get("id",""), depth+1)
    visit()
    return rows, by_id

_tax_rows, _tax_by_id = _taxonomy_ordered_rows(canonical_terms)
_tax_tree_html = "".join(
    '<button type="button" class="ux-ro-static-taxonomy-term" '
    f'data-ro-static-taxonomy-id="{item.get("id","")}" '
    f'data-taxonomy-level="{item.get("level","")}" '
    f'style="--ux-ro-depth:{depth}">'
    f'<span>{item.get("canonicalName") or item.get("name") or ""}</span></button>'
    for item, depth in _tax_rows
)
_first_tax = next((item for item, _depth in _tax_rows if item.get("level")=="product"), _tax_rows[0][0] if _tax_rows else None)
_first_name = (_first_tax or {}).get("canonicalName") or (_first_tax or {}).get("name") or ""
_first_level = (_first_tax or {}).get("level") or ""
_tax_detail_html = (
    '<div class="ux-ro-static-taxonomy-detail">'
    f'<span class="eyebrow">{_first_level.capitalize()}</span>'
    f'<h2>{_first_name}</h2>'
    f'<p>{_first_name}</p>'
    '</div>'
)

s = s.replace(
    '<nav class="taxonomy-tree" id="taxonomy-tree" aria-label="Árbol de taxonomía"></nav>',
    '<nav class="taxonomy-tree" id="taxonomy-tree" aria-label="Árbol de taxonomía">' + _tax_tree_html + '</nav>',
    1
)
s = s.replace(
    '<article class="taxonomy-detail" id="taxonomy-detail"></article>',
    '<article class="taxonomy-detail" id="taxonomy-detail">' + _tax_detail_html + '</article>',
    1
)


# Vista pública independiente: no reutiliza el contenedor controlado por el renderer editable.
_public_taxonomy_html = (
    '<div id="ux-public-taxonomy-static" class="ux-public-taxonomy-static">'
    '<nav class="ux-public-taxonomy-static-tree" aria-label="Taxonomía canónica de solo lectura">' + _tax_tree_html + '</nav>'
    '<article class="ux-public-taxonomy-static-detail">' + _tax_detail_html + '</article>'
    '</div>'
)
s = s.replace(
    '<div class="taxonomy-layout">',
    _public_taxonomy_html + '<div class="taxonomy-layout ux-public-taxonomy-editable-layout">',
    1
)

static_taxonomy_guard_js = f"""
<script id="ux-demo-static-taxonomy-guard">
(() => {{
  const TREE_HTML={json.dumps(_tax_tree_html, ensure_ascii=False)};
  const TERMS={canonical_terms_js};

  function bindIndependentPublicTaxonomy(){{
    const root=document.getElementById('ux-public-taxonomy-static');
    if(!root||root.dataset.bound==='true')return;
    root.dataset.bound='true';
    const tree=root.querySelector('.ux-public-taxonomy-static-tree');
    const detail=root.querySelector('.ux-public-taxonomy-static-detail');
    if(!tree||!detail)return;

    const map=new Map(TERMS.map(item=>[String(item.id||''),item]));
    const pathFor=term=>{{
      const out=[];let current=term;let guard=0;
      while(current&&guard++<20){{
        out.unshift(String(current.canonicalName||current.name||''));
        current=current.parentId?map.get(String(current.parentId)):null;
      }}
      return out;
    }};
    const show=term=>{{
      if(!term)return;
      const aliases=Array.isArray(term.aliases)?term.aliases.filter(Boolean):[];
      detail.innerHTML='<div class="ux-ro-static-taxonomy-detail">'+
        '<span class="eyebrow">'+String(term.level||'')+'</span>'+
        '<h2>'+String(term.canonicalName||term.name||'')+'</h2>'+
        '<p>'+pathFor(term).join(' › ')+'</p>'+
        (aliases.length?'<div class="ux-ro-static-taxonomy-aliases"><strong>Aliases</strong><p>'+aliases.join(' · ')+'</p></div>':'')+
        '</div>';
      tree.querySelectorAll('[data-ro-static-taxonomy-id]').forEach(node=>node.classList.toggle('active',String(node.dataset.roStaticTaxonomyId||'')===String(term.id||'')));
    }};
    tree.addEventListener('click',event=>{{
      const btn=event.target.closest('[data-ro-static-taxonomy-id]');
      if(!btn)return;
      event.preventDefault();event.stopImmediatePropagation();
      show(map.get(String(btn.dataset.roStaticTaxonomyId||'')));
    }},true);
    const first=tree.querySelector('[data-ro-static-taxonomy-id]');
    if(first)show(map.get(String(first.dataset.roStaticTaxonomyId||'')));
  }}

  function pathFor(term){{
    const map=new Map(TERMS.map(item=>[String(item.id||''),item]));
    const out=[]; let current=term; let guard=0;
    while(current&&guard++<20){{
      out.unshift(String(current.canonicalName||current.name||''));
      current=current.parentId?map.get(String(current.parentId)):null;
    }}
    return out;
  }}

  function show(term){{
    const detail=document.getElementById('taxonomy-detail');
    if(!detail||!term)return;
    const aliases=Array.isArray(term.aliases)?term.aliases.filter(Boolean):[];
    detail.innerHTML=
      '<div class="ux-ro-static-taxonomy-detail">'+
      '<span class="eyebrow">'+String(term.level||'')+'</span>'+
      '<h2>'+String(term.canonicalName||term.name||'')+'</h2>'+
      '<p>'+pathFor(term).join(' › ')+'</p>'+
      (aliases.length?'<div class="ux-ro-static-taxonomy-aliases"><strong>Aliases</strong><p>'+aliases.join(' · ')+'</p></div>':'')+
      '</div>';
  }}

  function ensure(){{
    const tree=document.getElementById('taxonomy-tree');
    if(!tree)return;
    if(!tree.querySelector('[data-ro-static-taxonomy-id]')) tree.innerHTML=TREE_HTML;
    if(!tree.dataset.roStaticBound){{
      tree.dataset.roStaticBound='true';
      tree.addEventListener('click',event=>{{
        const btn=event.target.closest('[data-ro-static-taxonomy-id]');
        if(!btn)return;
        event.preventDefault();
        event.stopImmediatePropagation();
        const term=TERMS.find(item=>String(item.id||'')===String(btn.dataset.roStaticTaxonomyId||''));
        tree.querySelectorAll('[data-ro-static-taxonomy-id]').forEach(node=>node.classList.toggle('active',node===btn));
        show(term);
      }},true);
    }}
    const active=tree.querySelector('[data-ro-static-taxonomy-id].active')||tree.querySelector('[data-ro-static-taxonomy-id]');
    if(active&&!document.getElementById('taxonomy-detail')?.textContent?.trim()){{
      const term=TERMS.find(item=>String(item.id||'')===String(active.dataset.roStaticTaxonomyId||''));
      show(term);
    }}
  }}

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',()=>{{ensure();bindIndependentPublicTaxonomy();}},{{once:true}});
  else {{ensure();bindIndependentPublicTaxonomy();}}
  window.addEventListener('load',()=>{{ensure();setTimeout(ensure,300);setTimeout(ensure,1200);setTimeout(ensure,3000);}},{{once:true}});
  setInterval(()=>{{
    const taxonomy=document.getElementById('taxonomy');
    if(taxonomy&&!taxonomy.hidden)ensure();
  }},1000);
}})();
</script>
"""

# Restauración robusta para la demo pública:
# La taxonomía read-only se representa directamente desde el canon embebido.
# No se crean, recuperan ni modifican learnings en la demo.
taxonomy_runtime_js = f"""
<script id="ux-demo-taxonomy-runtime-restore-v6184">
(() => {{
  const TERMS={canonical_terms_js};

  function renderReadonlyTaxonomy(){{
    try{{
      const tree=document.getElementById('taxonomy-tree');
      const detail=document.getElementById('taxonomy-detail');
      if(!tree||!detail)return;

      const all=TERMS.filter(term=>term.status==='canonical'&&term.governed===true);
      const byParent=new Map();
      all.forEach(term=>{{
        const key=String(term.parentId||'');
        if(!byParent.has(key))byParent.set(key,[]);
        byParent.get(key).push(term);
      }});

      const levelLabel={{product:'Producto',funnel:'Funnel',minifunnel:'Minifunnel',component:'Componente'}};
      const levelClass={{product:'is-product',funnel:'is-funnel',minifunnel:'is-minifunnel',component:'is-component'}};
      const rank={{product:0,funnel:1,minifunnel:2,component:3}};

      function orderedChildren(parentId){{
        return [...(byParent.get(String(parentId||''))||[])].sort((a,b)=>
          (rank[a.level]??9)-(rank[b.level]??9)||
          String(a.canonicalName||a.name||'').localeCompare(String(b.canonicalName||b.name||''),'es')
        );
      }}

      function buildBranch(parentId,depth){{
        const frag=document.createDocumentFragment();
        orderedChildren(parentId).forEach(term=>{{
          const wrap=document.createElement('div');
          wrap.className='ux-ro-taxonomy-node';
          wrap.style.setProperty('--ux-depth',String(depth));

          const btn=document.createElement('button');
          btn.type='button';
          btn.className='ux-ro-taxonomy-term '+(levelClass[term.level]||'');
          btn.dataset.roTaxonomyId=String(term.id||'');

          const level=document.createElement('span');
          level.className='ux-ro-taxonomy-level';
          level.textContent=levelLabel[term.level]||term.level||'';

          const strong=document.createElement('strong');
          strong.textContent=String(term.canonicalName||term.name||'');

          btn.append(level,strong);
          wrap.append(btn);

          const children=orderedChildren(term.id);
          if(children.length){{
            const childWrap=document.createElement('div');
            childWrap.className='ux-ro-taxonomy-children';
            childWrap.append(buildBranch(term.id,depth+1));
            wrap.append(childWrap);
          }}
          frag.append(wrap);
        }});
        return frag;
      }}

      function pathFor(term){{
        const map=new Map(all.map(x=>[String(x.id||''),x]));
        const parts=[];let current=term;const seen=new Set();
        while(current){{
          const id=String(current.id||'');
          if(id&&seen.has(id))break;
          if(id)seen.add(id);
          parts.unshift(String(current.canonicalName||current.name||''));
          current=current.parentId?map.get(String(current.parentId)):null;
        }}
        return parts;
      }}

      function show(term){{
        detail.innerHTML='';
        const box=document.createElement('div');
        box.className='ux-ro-taxonomy-detail';

        const kicker=document.createElement('span');
        kicker.className='ux-ro-taxonomy-kicker';
        kicker.textContent=levelLabel[term.level]||term.level||'';

        const h=document.createElement('h3');
        h.textContent=String(term.canonicalName||term.name||'');

        const p=document.createElement('p');
        p.className='ux-ro-taxonomy-path';
        p.textContent=pathFor(term).join(' / ');

        box.append(kicker,h,p);

        const aliases=Array.isArray(term.aliases)?term.aliases.filter(Boolean):[];
        if(aliases.length){{
          const a=document.createElement('div');
          a.className='ux-ro-taxonomy-aliases';
          const st=document.createElement('strong');
          st.textContent='Alias históricos';
          const ap=document.createElement('p');
          ap.textContent=aliases.join(' · ');
          a.append(st,ap);
          box.append(a);
        }}
        detail.append(box);

        tree.querySelectorAll('[data-ro-taxonomy-id]').forEach(node=>
          node.classList.toggle('active',node.dataset.roTaxonomyId===String(term.id||''))
        );
      }}

      tree.innerHTML='';
      tree.append(buildBranch('',0));
      tree.onclick=event=>{{
        const btn=event.target.closest('[data-ro-taxonomy-id]');
        if(!btn)return;
        const term=all.find(x=>String(x.id||'')===btn.dataset.roTaxonomyId);
        if(term)show(term);
      }};

      const first=all.find(term=>term.level==='product')||all[0];
      if(first)show(first);
    }}catch(e){{
      console.error('[UX Intel readonly taxonomy render]',e);
    }}
  }}

  function restoreTaxonomy(){{
    renderReadonlyTaxonomy();
    try{{
      if(typeof taxonomyProject==='undefined' || !taxonomyProject) return;
      taxonomyProject.state = taxonomyProject.state || {{}};
      taxonomyProject.state.terms = JSON.parse(JSON.stringify(TERMS));
      if(!taxonomyProject.state.controlledVocabularies && typeof publicTaxonomyState!=='undefined'){{
        taxonomyProject.state.controlledVocabularies = JSON.parse(JSON.stringify(publicTaxonomyState.controlledVocabularies||{{}}));
      }}
      if(!taxonomyProject.state.glossaryTerms && typeof publicTaxonomyState!=='undefined'){{
        taxonomyProject.state.glossaryTerms = JSON.parse(JSON.stringify(publicTaxonomyState.glossaryTerms||[]));
      }}
      try{{ refreshAllTaxonomyFilters?.(); }}catch(_e){{}}
      try{{ renderTaxonomy?.(); }}catch(_e){{}}
      renderReadonlyTaxonomy();
      try{{ renderLearnings?.(); }}catch(_e){{}}
      try{{ renderOverview?.(); }}catch(_e){{}}
    }}catch(e){{
      console.error('[UX Intel public taxonomy restore]',e);
    }}
  }}

  let taxonomyRepairing=false;
  function taxonomyLooksEmpty(){{
    const tree=document.getElementById('taxonomy-tree');
    if(!tree)return false;
    return !tree.querySelector('[data-ro-taxonomy-id]');
  }}

  function keepReadonlyTaxonomyStable(){{
    const tree=document.getElementById('taxonomy-tree');
    const detail=document.getElementById('taxonomy-detail');
    if(!tree||!detail)return;
    const observer=new MutationObserver(()=>{{
      if(taxonomyRepairing||!taxonomyLooksEmpty())return;
      taxonomyRepairing=true;
      queueMicrotask(()=>{{
        try{{ renderReadonlyTaxonomy(); }}
        finally{{ taxonomyRepairing=false; }}
      }});
    }});
    observer.observe(tree,{{childList:true,subtree:true}});
    observer.observe(detail,{{childList:true,subtree:true}});
  }}

  function run(){{
    restoreTaxonomy();
    keepReadonlyTaxonomyStable();
  }}

  if(document.readyState==='loading'){{
    document.addEventListener('DOMContentLoaded',()=>setTimeout(run,250),{{once:true}});
  }}else{{
    setTimeout(run,250);
  }}
  window.addEventListener('load',()=>{{
    setTimeout(restoreTaxonomy,600);
    setTimeout(restoreTaxonomy,1600);
    setTimeout(restoreTaxonomy,3200);
    setTimeout(restoreTaxonomy,6000);
  }},{{once:true}});
}})();
</script>
"""

# Identificación visual de la copia compartida.
badge = '<span class="ux-demo-readonly-badge">Demo · solo consulta</span>'
if 'ux-demo-readonly-badge' not in s:
    s = s.replace(
        '<span class="storage-save-status" id="storage-save-status"',
        badge + '\n        <span class="storage-save-status" id="storage-save-status"',
        1
    )

# Solo lectura: misma UI, mismos filtros, navegación y descargas.
# Ocultamos exclusivamente acciones que modifican datos o taxonomía.
readonly_css = r'''
<style id="ux-demo-taxonomy-readonly-fallback">
#taxonomy .taxonomy-layout{grid-template-columns:minmax(320px,.9fr) minmax(360px,1.1fr)!important;align-items:start}
#taxonomy .taxonomy-tree,#taxonomy .taxonomy-detail{background:#fff;border:1px solid var(--border-secondary);border-radius:14px}

/* En demo pública usamos una vista estática independiente del renderer editable */
#taxonomy .ux-public-taxonomy-editable-layout{display:none!important;}
#taxonomy .ux-public-taxonomy-static{
  display:grid;grid-template-columns:minmax(320px,.9fr) minmax(360px,1.1fr);
  gap:18px;align-items:start;
}
#taxonomy .ux-public-taxonomy-static-tree,
#taxonomy .ux-public-taxonomy-static-detail{
  background:#fff;border:1px solid var(--border-secondary);border-radius:14px;
}
#taxonomy .ux-public-taxonomy-static-tree{padding:12px;}
#taxonomy .ux-public-taxonomy-static-detail{padding:22px;min-height:180px;}
#taxonomy .ux-public-taxonomy-static-tree .ux-ro-static-taxonomy-term{
  display:flex;align-items:center;width:calc(100% - (var(--ux-ro-depth,0) * 14px));
  margin-left:calc(var(--ux-ro-depth,0) * 14px);
  min-height:42px;padding:8px 10px;border:0;border-bottom:1px solid var(--border-secondary);
  background:transparent;text-align:left;color:var(--text-primary);font:inherit;font-weight:600;cursor:pointer;
}
#taxonomy .ux-public-taxonomy-static-tree .ux-ro-static-taxonomy-term::before{
  content:"";width:4px;height:22px;border-radius:999px;margin-right:10px;background:#d0d5dd;flex:0 0 auto;
}
#taxonomy .ux-public-taxonomy-static-tree [data-taxonomy-level="product"]::before{background:#2d69e1;}
#taxonomy .ux-public-taxonomy-static-tree [data-taxonomy-level="funnel"]::before{background:#17b26a;}
#taxonomy .ux-public-taxonomy-static-tree [data-taxonomy-level="minifunnel"]::before{background:#f79009;}
#taxonomy .ux-public-taxonomy-static-tree [data-taxonomy-level="component"]::before{background:#7a5af8;}
#taxonomy .ux-public-taxonomy-static-tree .ux-ro-static-taxonomy-term:hover,
#taxonomy .ux-public-taxonomy-static-tree .ux-ro-static-taxonomy-term.active{background:#f5f8ff;}
@media(max-width:820px){
  #taxonomy .ux-public-taxonomy-static{grid-template-columns:1fr;}
}
#taxonomy .taxonomy-tree{padding:12px}
#taxonomy .taxonomy-detail{padding:22px;min-height:180px}
.ux-ro-taxonomy-node{margin-left:calc(var(--ux-depth,0) * 18px)}
.ux-ro-taxonomy-term{width:100%;display:flex;align-items:center;gap:10px;padding:9px 10px;border:0;background:transparent;border-radius:9px;text-align:left;color:var(--text-primary);cursor:pointer}
.ux-ro-taxonomy-term:hover,.ux-ro-taxonomy-term.active{background:#f5f8ff}
.ux-ro-taxonomy-level{font-size:10px;font-weight:800;letter-spacing:.03em;text-transform:uppercase;min-width:72px}
.ux-ro-taxonomy-term.is-product .ux-ro-taxonomy-level{color:#2563eb}
.ux-ro-taxonomy-term.is-funnel .ux-ro-taxonomy-level{color:#16803c}
.ux-ro-taxonomy-term.is-minifunnel .ux-ro-taxonomy-level{color:#b45309}
.ux-ro-taxonomy-term.is-component .ux-ro-taxonomy-level{color:#6d28d9}
.ux-ro-taxonomy-children{border-left:1px solid #e5e7eb;margin-left:11px}
.ux-ro-taxonomy-kicker{font-size:11px;font-weight:800;text-transform:uppercase;color:var(--text-secondary)}
.ux-ro-taxonomy-detail h3{margin:8px 0 8px;font-size:22px}
.ux-ro-taxonomy-path,.ux-ro-taxonomy-aliases p{color:var(--text-secondary)}
@media(max-width:820px){
  #taxonomy .taxonomy-layout{grid-template-columns:1fr!important}
  .ux-ro-taxonomy-node{margin-left:calc(var(--ux-depth,0) * 10px)}
}
</style>
<style id="ux-demo-readonly-final">
.ux-demo-readonly-badge{
  display:inline-flex;align-items:center;min-height:30px;padding:4px 10px;
  border:1px solid var(--border-secondary);border-radius:999px;background:#fff;
  color:var(--text-secondary);font-size:11px;font-weight:700;white-space:nowrap;
}

/* Topbar: no ingesta */
#add-document,#add-evidence,#document-upload,#insight-register-upload{display:none!important;}

/* Workspace / backup: no import ni restauración */
#import-workspace,#import-workspace-input,#import-workspace-confirm,[data-import-workspace],[data-workspace-restore]{display:none!important;}

/* Documentos: consultar/abrir/descargar sí; editar/borrar/revincular no */
[data-doc-action="edit"],
[data-doc-action="delete"],
[data-doc-action="add-register"],
[data-doc-action="link-source"],
[data-doc-action="relink-register"],
[data-doc-action="replace"],
[data-source-update],
[data-confirm-source-update],
[data-add-insight-register]{display:none!important;}

/* Learnings / evidence / findings: lectura sí; edición/publicación no */
[data-learning-suggestion-confirm],
[data-learning-suggestion-edit],
[data-learning-suggestion-evidence],
[data-approve-routine-clusters],
[data-duplicate-decision],
[data-learning-component-edit],
[data-finding-edit],
[data-insight-edit],
[data-open-publish-preview],
[data-confirm-publish],
[data-publish],
[data-edit],
[data-delete]{display:none!important;}

/* Taxonomía: consulta sí; gestión no */
#taxonomy .ux-taxonomy-header-actions,
.ux-taxonomy-manage-v2,
.taxonomy-inline-action,
[data-taxonomy-term-create],
#taxonomy-vocabulary-create,
[data-vocabulary-add],
[data-glossary-create],
.glossary-kebab,
[data-glossary-menu],
[data-taxonomy-manager-v2],
[data-taxonomy-manager-v2-edit],
[data-taxonomy-manager-v2-merge],
[data-taxonomy-manager-v2-delete],
[data-taxonomy-edit],
[data-taxonomy-delete],
[data-propose-taxonomy],
#taxonomy-manager-v2-modal,
#taxonomy-manager-v2-edit,
#taxonomy-manager-v2-merge,
#taxonomy-manager-v2-confirm,
#taxonomy-vocabulary-create-modal,
#taxonomy-manager-v2-edit-action,
#taxonomy-manager-v2-merge-action,
#taxonomy-manager-v2-confirm-action,
#delete-modal,
[data-delete-confirm]{display:none!important;}

/* Estado de guardado no tiene sentido en una demo sin escritura */
#storage-save-status{display:none!important;}

/* Taxonomía pública prerenderizada y estable */
#taxonomy-tree .ux-ro-static-taxonomy-term{
  display:flex;align-items:center;width:calc(100% - (var(--ux-ro-depth,0) * 14px));
  margin-left:calc(var(--ux-ro-depth,0) * 14px);
  min-height:42px;padding:8px 10px;border:0;border-bottom:1px solid var(--border-secondary);
  background:transparent;text-align:left;color:var(--text-primary);font:inherit;font-weight:600;cursor:pointer;
}
#taxonomy-tree .ux-ro-static-taxonomy-term::before{
  content:"";width:4px;height:22px;border-radius:999px;margin-right:10px;background:#d0d5dd;flex:0 0 auto;
}
#taxonomy-tree .ux-ro-static-taxonomy-term[data-taxonomy-level="product"]::before{background:#2d69e1;}
#taxonomy-tree .ux-ro-static-taxonomy-term[data-taxonomy-level="funnel"]::before{background:#17b26a;}
#taxonomy-tree .ux-ro-static-taxonomy-term[data-taxonomy-level="minifunnel"]::before{background:#f79009;}
#taxonomy-tree .ux-ro-static-taxonomy-term[data-taxonomy-level="component"]::before{background:#7a5af8;}
#taxonomy-tree .ux-ro-static-taxonomy-term:hover,
#taxonomy-tree .ux-ro-static-taxonomy-term.active{background:#f5f8ff;}
#taxonomy-detail .ux-ro-static-taxonomy-detail{padding:20px;}
#taxonomy-detail .ux-ro-static-taxonomy-detail h2{margin:6px 0 8px;font-size:22px;}
#taxonomy-detail .ux-ro-static-taxonomy-detail>p,
#taxonomy-detail .ux-ro-static-taxonomy-aliases p{color:var(--text-secondary);}
#taxonomy-detail .ux-ro-static-taxonomy-aliases{margin-top:18px;padding-top:14px;border-top:1px solid var(--border-secondary);}


/* Mantener explícitamente visibles las acciones de consulta/export */
#uxs-export,#uxs-export-cro,
[data-download-insight-register],
[data-doc-download-direct],
[data-doc-action="open"]{display:inline-flex!important;}

@media(max-width:820px){
  .ux-demo-readonly-badge{display:none;}
}
</style>
'''
if 'id="ux-demo-readonly-final"' not in s:
    s = s.replace('</head>', readonly_css + '\n</head>', 1)

readonly_js = r'''
<script id="ux-demo-readonly-guard">
(() => {
  document.documentElement.dataset.demoMode='readonly';

  // Las acciones de escritura quedan bloqueadas incluso si algún control legacy
  // llegara a mostrarse por código dinámico. Descargas y exports no se bloquean.
  const writeSelectors = [
    '#add-document','#add-evidence','[data-doc-action="edit"]','[data-doc-action="delete"]',
    '[data-doc-action="add-register"]','[data-doc-action="link-source"]','[data-doc-action="relink-register"]',
    '[data-learning-suggestion-confirm]','[data-learning-suggestion-edit]','[data-learning-suggestion-evidence]','[data-learning-component-edit]',
    '[data-approve-routine-clusters]','[data-duplicate-decision]',
    '[data-finding-edit]','[data-insight-edit]','[data-open-publish-preview]','[data-confirm-publish]',
    '[data-taxonomy-term-create]','[data-taxonomy-manager-v2-edit]','[data-taxonomy-manager-v2-merge]',
    '[data-taxonomy-manager-v2-delete]','[data-taxonomy-edit]','[data-taxonomy-delete]',
    '[data-propose-taxonomy]','[data-source-update]','[data-confirm-source-update]',
    '[data-delete-confirm]','#import-workspace-confirm','#taxonomy-manager-v2-edit-action',
    '#taxonomy-manager-v2-merge-action','#taxonomy-manager-v2-confirm-action'
  ];
  document.addEventListener('click', e => {
    const target = e.target?.closest?.(writeSelectors.join(','));
    if(!target) return;
    e.preventDefault();
    e.stopImmediatePropagation();
  }, true);
})();
</script>
'''
if 'id="ux-demo-readonly-guard"' not in s:
    s = s.replace('</body>', readonly_js + '\n' + taxonomy_runtime_js + '\n</body>', 1)
else:
    s = s.replace('</body>', taxonomy_runtime_js + '\n</body>', 1)

if 'id="ux-demo-static-taxonomy-guard"' not in s:
    s = s.replace('</body>', static_taxonomy_guard_js + '\n</body>', 1)

# UX_INTEL_SYNC_2026_10_29_BEGIN
# Capa incremental: replica exclusivamente mejoras validadas en la app local.
# No modifica la base documental, taxonomía canónica, learnings ni contenido.
import re as _ux_re

def _ux_required_replace(old, new, label, count=1):
    global s
    if old not in s:
        raise SystemExit(f'ERROR UX sync: no se encuentra {label}')
    s = s.replace(old, new, count)

# 1) Fecha histórica de incorporación en los 198 registros públicos.
_m = _ux_re.search(r'const publicDemoRows=(\[.*?\]);', s, _ux_re.S)
if not _m:
    raise SystemExit('ERROR UX sync: no se encuentra publicDemoRows para fechas')
_rows = json.loads(_m.group(1))
def _inc_date(row):
    initiative=str(row.get('initiative') or '')
    origin=str(row.get('origin') or '')
    rid=str(row.get('id') or '')
    try:
        n=int(rid.split('-')[-1])
    except Exception:
        n=-1
    if initiative=='SUMA Frequent Flyer':
        if 1 <= n <= 36: return '2026-10'
        if 37 <= n <= 87: return '2026-07'
        if 88 <= n <= 101: return '2026-09'
    if initiative=='Buscador':
        if 144 <= n <= 153: return '2026-06'
        if origin in ('Auditoría UX','Desk research'): return '2026-05'
        if origin in ('Análisis de datos','Análisis conductual','Benchmark'): return '2026-06'
    if initiative=='Header':
        if 164 <= n <= 167: return '2026-06'
        if 168 <= n <= 170: return '2026-07'
        return {'Benchmark':'2026-06','Test con usuarios':'2026-05','Análisis de datos':'2026-04','Auditoría UX':'2026-06','Desk research':'2026-04'}.get(origin,'')
    return ''
for _row in _rows:
    _row['incorporationDate']=_inc_date(_row)
if len(_rows)!=198 or any(not str(r.get('incorporationDate') or '').strip() for r in _rows):
    raise SystemExit('ERROR UX sync: las fechas públicas no cubren 198/198 registros')
_rows_json=json.dumps(_rows,ensure_ascii=False,separators=(',',':'))
s=s[:_m.start(1)]+_rows_json+s[_m.end(1):]

# 2) Propagar la fecha al registro normalizado.
_ux_required_replace("          ingestedAt:row.ingestedAt||rowDoc?.ingestedAt||''", "          ingestedAt:row.ingestedAt||rowDoc?.ingestedAt||'',\n          incorporationDate:row.incorporationDate||rowDoc?.incorporationDate||'',\n          reportDate:(row.reportDate||((rowDoc&&typeof documentDate==='function')?documentDate(rowDoc):''))", 'normalización principal')
_ux_required_replace("          ingestedAt:doc.ingestedAt||'',", "          ingestedAt:doc.ingestedAt||'',\n          incorporationDate:row.incorporationDate||doc.incorporationDate||'',\n          reportDate:(row.reportDate||((typeof documentDate==='function')?documentDate(doc):'')),", 'normalización secundaria')

# 3) Helper de presentación: mes/año histórico, sin usar el 23/10 del master.
_helper_anchor='  function compactContextPath(record){'
_helper=r'''
  function incorporationTemporalValue(record){
    const explicit=clean(record?.incorporationDate||'');
    if(explicit)return explicit;
    const report=clean(record?.reportDate||'');
    if(report&&!['No especificada','No especificado'].includes(report))return report;
    const workbook=clean(record?.workbook||'');
    if(workbook==='UX_Intelligence_CRO_master_final.xlsx')return '';
    return clean(record?.ingestedAt||'');
  }

  function incorporationDateDisplay(record){
    const raw=incorporationTemporalValue(record);
    if(!raw)return 'Sin fecha registrada';
    const isoMonth=raw.match(/^(\d{4})-(\d{2})$/);
    if(isoMonth){
      const labels={'01':'ene','02':'feb','03':'mar','04':'abr','05':'may','06':'jun','07':'jul','08':'ago','09':'sept','10':'oct','11':'nov','12':'dic'};
      return `${labels[isoMonth[2]]||isoMonth[2]} ${isoMonth[1]}`;
    }
    const isoDay=raw.match(/^(\d{4})-(\d{2})-(\d{2})(?:T.*)?$/);
    if(isoDay)return `${isoDay[3]}/${isoDay[2]}/${isoDay[1]}`;
    const parsed=new Date(raw);
    if(Number.isFinite(parsed.getTime())&&/T/.test(raw))return parsed.toLocaleDateString('es-ES',{day:'2-digit',month:'2-digit',year:'numeric'});
    return raw;
  }

'''
if _helper_anchor not in s: raise SystemExit('ERROR UX sync: helper anchor')
s=s.replace(_helper_anchor,_helper+_helper_anchor,1)

# 4) Mostrar Fecha de incorporación en cada hallazgo.
_old_meta="""      clean(r.origin)?`<div><span>Tipo de análisis</span><strong>${escapeHtml(r.origin)}</strong></div>`:'',
      clean(r.impactUx)?`<div><span>Impacto UX</span><strong><span class=\"status-badge ${impactClass(r.impactUx)}\">${escapeHtml(r.impactUx)}</span></strong></div>`:''"""
_new_meta="""      clean(r.origin)?`<div><span>Tipo de análisis</span><strong>${escapeHtml(r.origin)}</strong></div>`:'',
      `<div><span>Fecha de incorporación</span><strong>${escapeHtml(incorporationDateDisplay(r))}</strong></div>`,
      clean(r.impactUx)?`<div><span>Impacto UX</span><strong><span class=\"status-badge ${impactClass(r.impactUx)}\">${escapeHtml(r.impactUx)}</span></strong></div>`:''"""
_ux_required_replace(_old_meta,_new_meta,'meta detalle hallazgo')

# 5) Exportaciones: misma Fecha de incorporación en general y CRO.
_export_anchor='  function fullExportValue(record,key){'
if _export_anchor not in s: raise SystemExit('ERROR UX sync: fullExportValue')
s=s.replace(_export_anchor,_export_anchor+"\n    if(key==='incorporationDateDisplay')return incorporationDateDisplay(record);",1)
if "['Incluido en UX Intelligence','ingestedAt']" in s:
    s=s.replace("['Incluido en UX Intelligence','ingestedAt']","['Fecha de incorporación','incorporationDateDisplay']",1)
elif "['Fecha de incorporación','incorporationDateDisplay']" not in s:
    raise SystemExit('ERROR UX sync: columna general fecha')
_cro_old="""      ['Iniciativa','initiative'],['Producto','product'],['Funnel','funnel'],['Minifunnel','minifunnel'],['Componente','component'],
      ['Dispositivo','device'],['Tipo de registro','recordType'],['Insight / hallazgo','insight'],['Evidencia','evidence'],"""
_cro_new="""      ['Iniciativa','initiative'],['Producto','product'],['Funnel','funnel'],['Minifunnel','minifunnel'],['Componente','component'],
      ['Fecha de incorporación','incorporationDateDisplay'],
      ['Dispositivo','device'],['Tipo de registro','recordType'],['Insight / hallazgo','insight'],['Evidencia','evidence'],"""
_ux_required_replace(_cro_old,_cro_new,'columnas CRO')
s=s.replace('const widths=[18,14,18,18,24,16,18,55,60,50,13,22,30,16,60,65,20,20];','const widths=[18,14,18,18,24,18,16,18,55,60,50,13,22,30,16,60,65,20,20];',1)

# 6) Learnings: visibles solo Producto · Funnel · Minifunnel · Componente.
_lp_old='''            <div class="primary-filters">
              <label class="filter-field">Producto<select class="filter-select hierarchy-product" data-hierarchy-level="product" id="learning-product"></select></label>
              <label class="filter-field">Funnel<select class="filter-select hierarchy-funnel" data-hierarchy-level="funnel" id="learning-funnel"></select></label>
              <label class="filter-field">Componente<select class="filter-select hierarchy-component" data-hierarchy-level="component" id="learning-component"></select></label>
              <label class="filter-field">Impacto UX<select class="filter-select" id="learning-impact"></select></label>
            </div>
            <div class="secondary-filters" id="learning-secondary-filters" hidden>
              <label class="filter-field">Minifunnel<select class="filter-select hierarchy-minifunnel" data-hierarchy-level="minifunnel" id="learning-minifunnel"></select></label>'''
_lp_new='''            <div class="primary-filters">
              <label class="filter-field">Producto<select class="filter-select hierarchy-product" data-hierarchy-level="product" id="learning-product"></select></label>
              <label class="filter-field">Funnel<select class="filter-select hierarchy-funnel" data-hierarchy-level="funnel" id="learning-funnel"></select></label>
              <label class="filter-field">Minifunnel<select class="filter-select hierarchy-minifunnel" data-hierarchy-level="minifunnel" id="learning-minifunnel"></select></label>
              <label class="filter-field">Componente<select class="filter-select hierarchy-component" data-hierarchy-level="component" id="learning-component"></select></label>
            </div>
            <div class="secondary-filters" id="learning-secondary-filters" hidden>
              <label class="filter-field">Impacto UX<select class="filter-select" id="learning-impact"></select></label>'''
_ux_required_replace(_lp_old,_lp_new,'filtros visibles Learnings')

# 7) Learnings: Iniciativa limita Producto/Funnel/Minifunnel/Componente.
_h_start=s.find("    function hierarchyValues(product='Todos',funnel='Todos',minifunnel='Todos',group=''){")
_h_end=s.find('    const renderers={',_h_start)
if _h_start<0 or _h_end<0: raise SystemExit('ERROR UX sync: hierarchyValues')
_h_new=r'''    function learningInitiativeScope(){
      const selected=document.getElementById('learning-initiative')?.value||'Todos';
      const exact=(actual,target)=>['Todos','Todas',''].includes(target)||normalizeText(actual||'')===normalizeText(target);
      return learnings.filter(item=>{
        if(['Todos','Todas',''].includes(selected))return true;
        return governedLearningInitiatives(item).some(value=>exact(value,selected));
      });
    }
    function learningProductValues(){
      return [...new Set(learningInitiativeScope().map(item=>governedTaxonomyRecord(item).product).filter(Boolean))].sort((a,b)=>a.localeCompare(b,'es'));
    }
    function hierarchyValues(product='Todos',funnel='Todos',minifunnel='Todos',group=''){
      const exact=(actual,selected)=>['Todos','Todas',''].includes(selected)||normalizeText(actual||'')===normalizeText(selected);
      const sort=(values)=>[...new Set(values.filter(Boolean))].sort((a,b)=>a.localeCompare(b,'es'));
      if(group==='learning'){
        const contexts=learningInitiativeScope().map(item=>({item,current:governedTaxonomyRecord(item)}));
        const inProduct=contexts.filter(({current})=>exact(current.product,product));
        const funnels=sort(inProduct.map(({current})=>current.funnel));
        const inFunnel=inProduct.filter(({current})=>exact(current.funnel,funnel));
        const minifunnels=sort(inFunnel.map(({current})=>current.minifunnel));
        const hasProduct=!['Todos','Todas',''].includes(product);
        const hasFunnel=!['Todos','Todas',''].includes(funnel);
        const hasMinifunnel=!['Todos','Todas',''].includes(minifunnel);
        let componentItems=[];
        if(hasMinifunnel)componentItems=inFunnel.filter(({current})=>exact(current.minifunnel,minifunnel));
        else if(hasFunnel)componentItems=inFunnel.filter(({current})=>!String(current.minifunnel||'').trim());
        else if(hasProduct&&normalizeText(product)==='home')componentItems=inProduct.filter(({current})=>!String(current.funnel||'').trim()&&!String(current.minifunnel||'').trim());
        return {funnels,minifunnels,components:sort(componentItems.flatMap(({item})=>governedComponentNames(item)))};
      }
      const contexts=taxonomyContexts();
      const inProduct=contexts.filter(ctx=>exact(ctx.product,product));
      const funnels=sort(inProduct.map(ctx=>ctx.funnel));
      const inFunnel=inProduct.filter(ctx=>exact(ctx.funnel,funnel));
      const minifunnels=sort(inFunnel.map(ctx=>ctx.minifunnel));
      const hasProduct=!['Todos','Todas',''].includes(product);
      const hasFunnel=!['Todos','Todas',''].includes(funnel);
      const hasMinifunnel=!['Todos','Todas',''].includes(minifunnel);
      let componentContexts=[];
      if(hasMinifunnel)componentContexts=inFunnel.filter(ctx=>exact(ctx.minifunnel,minifunnel));
      else if(hasFunnel)componentContexts=inFunnel.filter(ctx=>!String(ctx.minifunnel||'').trim());
      else if(hasProduct&&normalizeText(product)==='home')componentContexts=inProduct.filter(ctx=>!String(ctx.funnel||'').trim()&&!String(ctx.minifunnel||'').trim());
      return {funnels,minifunnels,components:sort(componentContexts.map(ctx=>ctx.component).filter(Boolean))};
    }
'''
s=s[:_h_start]+_h_new+s[_h_end:]

# Producto de Learnings se repuebla según iniciativa.
_prod_init="      optionSet(system.querySelector('.hierarchy-product'),'Todos',[...new Set(taxonomyContexts().map(ctx=>ctx.product).filter(Boolean))]);"
_prod_new="      optionSet(system.querySelector('.hierarchy-product'),'Todos',group==='learning'?learningProductValues():[...new Set(taxonomyContexts().map(ctx=>ctx.product).filter(Boolean))]);"
_ux_required_replace(_prod_init,_prod_new,'producto Learnings por iniciativa')
_nonhier="      system.querySelectorAll('select:not([data-hierarchy-level])').forEach(select=>select.addEventListener('change',()=>{renderers[group]();updateActiveFilters(group);}));"
_nonhier_new="""      system.querySelectorAll('select:not([data-hierarchy-level])').forEach(select=>select.addEventListener('change',()=>{
        if(group==='learning'&&select.id==='learning-initiative'){
          const product=document.getElementById('learning-product'),funnel=document.getElementById('learning-funnel'),minifunnel=document.getElementById('learning-minifunnel'),component=document.getElementById('learning-component');
          if(product)optionSet(product,'Todos',learningProductValues(),'Todos');
          if(funnel)funnel.value='Todos';if(minifunnel)minifunnel.value='Todos';if(component)component.value='Todos';
          refreshHierarchy('learning');return;
        }
        renderers[group]();updateActiveFilters(group);
      }));"""
_ux_required_replace(_nonhier,_nonhier_new,'listener iniciativa Learnings')

# Habilitación jerárquica de Learnings y refresco de Producto.
_refresh_anchor="""    function refreshHierarchy(group,changed){
      const product=document.getElementById(`${group}-product`);
      const funnel=document.getElementById(`${group}-funnel`);
      const minifunnel=document.getElementById(`${group}-minifunnel`);
      const component=document.getElementById(`${group}-component`);
      if(!product||!component)return;
"""
_refresh_new=_refresh_anchor+"""
      if(group==='learning'){
        const validProducts=learningProductValues();
        const currentProduct=product.value;
        optionSet(product,'Todos',validProducts,currentProduct);
        if(!validProducts.some(value=>normalizeText(value)===normalizeText(currentProduct)))product.value='Todos';
        product.disabled=validProducts.length===0;
      }
"""
_ux_required_replace(_refresh_anchor,_refresh_new,'refresh Learnings')

# 8) Explorar: Iniciativa limita toda la cascada.
_fo_old="""  function filterOptions(field){
    const fromData=unique(field);
    if(field==='funnel'&&norm(filters.product||'')==='home')return [];
    if(field==='minifunnel'&&!norm(filters.funnel||''))return [];
    if(journeyLevels.has(field)){
      // Nunca convertir valores observados en datos/Excel en vocabulario canónico.
      // Si el canon no está disponible todavía, el filtro espera al canon.
      return dedupe(taxonomyValues(field));
    }
    const governed=dedupe(controlledTaxonomyValues(field));
    if(governed.length)return governed;
    if(controlledFilterValues[field])return dedupe(controlledFilterValues[field]);
    return fromData;
  }"""
_fo_new=r'''  function initiativeScopedJourneyValues(field,canonicalValues){
    const selectedInitiative=norm(filters.initiative||'');
    if(!selectedInitiative)return canonicalValues;
    const selectedProduct=norm(filters.product||''),selectedFunnel=norm(filters.funnel||''),selectedMinifunnel=norm(filters.minifunnel||'');
    const scoped=records.filter(record=>[...(record.initiatives||[]),record.initiative].filter(Boolean).map(norm).includes(selectedInitiative));
    const observed=new Set();
    scoped.forEach(record=>{
      const product=norm(record.product||''),funnel=norm(record.funnel||''),minifunnel=norm(record.minifunnel||'');
      if(field==='product'){if(record.product)observed.add(norm(record.product));return;}
      if(selectedProduct&&product!==selectedProduct)return;
      if(field==='funnel'){if(record.funnel)observed.add(norm(record.funnel));return;}
      if(selectedFunnel&&funnel!==selectedFunnel)return;
      if(field==='minifunnel'){if(record.minifunnel)observed.add(norm(record.minifunnel));return;}
      if(field==='component'){
        if(selectedMinifunnel){if(minifunnel!==selectedMinifunnel)return;}
        else if(selectedFunnel){if(minifunnel)return;}
        else if(selectedProduct==='home'){if(funnel||minifunnel)return;}
        else return;
        componentsOf(record).forEach(value=>{if(value)observed.add(norm(value));});
      }
    });
    return canonicalValues.filter(value=>observed.has(norm(value)));
  }
  function filterOptions(field){
    const fromData=unique(field);
    if(field==='funnel'&&norm(filters.product||'')==='home')return [];
    if(field==='minifunnel'&&!norm(filters.funnel||''))return [];
    if(journeyLevels.has(field))return dedupe(initiativeScopedJourneyValues(field,taxonomyValues(field)));
    const governed=dedupe(controlledTaxonomyValues(field));
    if(governed.length)return governed;
    if(controlledFilterValues[field])return dedupe(controlledFilterValues[field]);
    return fromData;
  }'''
_ux_required_replace(_fo_old,_fo_new,'filterOptions Explorar')

_hd_old=r'''  function hierarchyFilterDisabled(field){
    if(field==='funnel')return norm(filters.product||'')==='home';
    if(field==='minifunnel'){
      if(!norm(filters.funnel||''))return true;
      return taxonomyValues('minifunnel').length===0;
    }
    return false;
  }'''
_hd_new=r'''  function hierarchyFilterDisabled(field){
    if(field==='product'){if(norm(filters.initiative||''))return filterOptions('product').length===0;return false;}
    if(field==='funnel')return !norm(filters.product||'')||norm(filters.product||'')==='home';
    if(field==='minifunnel'){if(!norm(filters.product||'')||!norm(filters.funnel||''))return true;return filterOptions('minifunnel').length===0;}
    if(field==='component'){
      if(!norm(filters.product||''))return true;
      if(norm(filters.product||'')==='home')return filterOptions('component').length===0;
      if(!norm(filters.funnel||''))return true;
      return filterOptions('component').length===0;
    }
    return false;
  }'''
_ux_required_replace(_hd_old,_hd_new,'bloqueo jerárquico Explorar')

_init_old="""        if(field==='product'){
          filters.funnel='';
          filters.minifunnel='';
          filters.component='';
          fillSelect('uxs-funnel','funnel','funnel');
          fillSelect('uxs-minifunnel','minifunnel','minifunnel');
          fillSelect('uxs-component','component','component');
          try{globalThis.__dsSyncSelects?.();}catch(_){}
        }else if(field==='funnel'){"""
_init_new="""        if(field==='initiative'){
          filters.product='';filters.funnel='';filters.minifunnel='';filters.component='';
          fillSelect('uxs-product','product','product');fillSelect('uxs-funnel','funnel','funnel');fillSelect('uxs-minifunnel','minifunnel','minifunnel');fillSelect('uxs-component','component','component');
          try{globalThis.__dsSyncSelects?.();}catch(_){}
        }else if(field==='product'){
          filters.funnel='';
          filters.minifunnel='';
          filters.component='';
          fillSelect('uxs-funnel','funnel','funnel');
          fillSelect('uxs-minifunnel','minifunnel','minifunnel');
          fillSelect('uxs-component','component','component');
          try{globalThis.__dsSyncSelects?.();}catch(_){}
        }else if(field==='funnel'){"""
_ux_required_replace(_init_old,_init_new,'cambio iniciativa Explorar')

# 9) Marcador de build sincronizada.
s=s.replace('data-build="2026-10-27-v6-184-strict-learning-taxonomy"','data-build="2026-10-29-v6-192-public-sync"',1)
if '2026-10-29-v6-192-public-sync' not in s:
    raise SystemExit('ERROR UX sync: no se pudo actualizar build')

# Checks estructurales antes de escribir.
if s.count('id="learning-minifunnel"') != 1: raise SystemExit('ERROR UX sync: learning-minifunnel duplicado')
if "['Fecha de incorporación','incorporationDateDisplay']" not in s: raise SystemExit('ERROR UX sync: export fecha ausente')
if 'initiativeScopedJourneyValues' not in s or 'learningInitiativeScope' not in s: raise SystemExit('ERROR UX sync: cascada iniciativa ausente')
print('UX sync 2026-10-29 OK · fechas + exports + filtros jerárquicos')
# UX_INTEL_SYNC_2026_10_29_END


target.write_text(s, encoding="utf-8")
print("UX Intelligence consolidated UI installed in read-only mode")
print("Same UI · filters/search/downloads enabled · writes hidden")
