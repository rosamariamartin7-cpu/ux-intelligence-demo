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

# Restauración robusta para la demo pública:
# 1) reaplica la taxonomía DESPUÉS de loadTaxonomyProject(), que puede sobrescribirla;
# 2) recupera los dos learnings históricos que ya existían en el workspace local,
#    usando únicamente evidencia presente en los 198 registros públicos.
taxonomy_runtime_js = f"""
<script id="ux-demo-taxonomy-runtime-restore-v6184">
(() => {{
  const TERMS={canonical_terms_js};

  function restoreTaxonomy(){{
    try{{
      if(!globalThis.taxonomyProject) return;
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
      try{{ renderLearnings?.(); }}catch(_e){{}}
      try{{ renderOverview?.(); }}catch(_e){{}}
    }}catch(e){{
      console.error('[UX Intel public taxonomy restore]',e);
    }}
  }}

  function ensureHistoricalLearnings(){{
    try{{
      if(!Array.isArray(globalThis.learnings)) return;

      const specs = [
        {{
          id:'L-SUMA-04',
          initiative:'SUMA Frequent Flyer',
          initiatives:['SUMA Frequent Flyer'],
          product:'Booking',
          funnel:'Passengers',
          minifunnel:'',
          component:'Card Datos del pasajero',
          components:['Card Datos del pasajero'],
          impactUx:'Alto',
          title:'Si el usuario ya está logado en SUMA, aprovechemos los datos que ya tenemos',
          know:'Si ya conocemos sus datos y beneficios, volver a pedirlos añade esfuerzo.',
          text:'Podemos recuperar la información disponible y aplicar sus ventajas, dejando claro qué se ha recuperado o aplicado.',
          forEvidence:[
            'DEMO-051 · La identificación SUMA puede reducir esfuerzo si evita volver a introducir datos ya conocidos.',
            'DEMO-077 · La recuperación automática de datos personales y número SUMA reduce esfuerzo en Paxes.'
          ],
          sourceNames:['UX_Intelligence_CRO_master_final.xlsx'],
          status:'Learning consolidado'
        }},
        {{
          id:'L-SUMA-05',
          initiative:'SUMA Frequent Flyer',
          initiatives:['SUMA Frequent Flyer'],
          product:'Booking',
          funnel:'Shopping Cart',
          minifunnel:'',
          component:'Slider de Millas',
          components:['Slider de Millas'],
          impactUx:'Alto',
          title:'No queda claro qué representa la cifra de Millas',
          know:'La cifra puede parecer el saldo total cuando quizá sea el máximo que se puede usar en esa reserva. Esa diferencia cambia cómo se entiende el canje.',
          text:'Antes de usar el slider, tiene que quedar claro qué significa esa cifra y qué cantidad puede aplicarse realmente.',
          forEvidence:[
            'DEMO-059 · El mensaje inicial no deja claro si las Millas mostradas son saldo total o máximo aplicable a la reserva.'
          ],
          sourceNames:['UX_Intelligence_CRO_master_final.xlsx'],
          status:'Learning consolidado'
        }}
      ];

      let changed=false;
      for(const spec of specs){{
        const exists=learnings.some(item =>
          String(item?.id||'')===spec.id ||
          String(item?.title||'').trim()===spec.title
        );
        if(!exists){{
          learnings.push(JSON.parse(JSON.stringify(spec)));
          changed=true;
        }}
      }}
      if(changed){{
        try{{ renderLearnings?.(); }}catch(_e){{}}
        try{{ renderOverview?.(); }}catch(_e){{}}
        try{{ refreshAllTaxonomyFilters?.(); }}catch(_e){{}}
      }}
    }}catch(e){{
      console.error('[UX Intel public learning restore]',e);
    }}
  }}

  function run(){{
    restoreTaxonomy();
    ensureHistoricalLearnings();
  }}

  if(document.readyState==='loading'){{
    document.addEventListener('DOMContentLoaded',()=>setTimeout(run,250),{{once:true}});
  }}else{{
    setTimeout(run,250);
  }}
  window.addEventListener('load',()=>{{
    setTimeout(run,600);
    setTimeout(run,1600);
    setTimeout(run,3200);
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

target.write_text(s, encoding="utf-8")
print("UX Intelligence consolidated UI installed in read-only mode")
print("Same UI · filters/search/downloads enabled · writes hidden")
