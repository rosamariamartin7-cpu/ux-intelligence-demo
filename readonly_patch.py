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
    s = s.replace('</body>', readonly_js + '\n</body>', 1)

target.write_text(s, encoding="utf-8")
print("UX Intelligence consolidated UI installed in read-only mode")
print("Same UI · filters/search/downloads enabled · writes hidden")
