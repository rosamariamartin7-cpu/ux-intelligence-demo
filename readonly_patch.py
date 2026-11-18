from pathlib import Path

SOURCE = Path("latest_public_source.html")
ROOT = Path("app/ux-intelligence-demo-exact")
TARGET = ROOT / "index.html"

if not SOURCE.exists():
    raise SystemExit("ERROR: falta latest_public_source.html")

s = SOURCE.read_text(encoding="utf-8")
required = [
    'data-build="2026-11-18-v6-194-public-245-records"',
    'const publicDemoRows=',
    'Metabuscadores',
    'id="uxs-export"',
    'id="uxs-export-cro"',
    'insightRegisterSyncSnapshot'
]
missing = [item for item in required if item not in s]
if missing:
    raise SystemExit("ERROR public source incompleto: " + " | ".join(missing))

if 'ux-demo-readonly-badge' not in s:
    badge = '<span class="ux-demo-readonly-badge">Copia pública · solo consulta</span>'
    s = s.replace(
        '<span class="storage-save-status" id="storage-save-status"',
        badge + '\n        <span class="storage-save-status" id="storage-save-status"',
        1
    )

readonly_css = r'''
<style id="ux-demo-readonly-latest">
.ux-demo-readonly-badge{display:inline-flex;align-items:center;min-height:30px;padding:4px 10px;border:1px solid var(--border-secondary);border-radius:999px;background:#fff;color:var(--text-secondary);font-size:11px;font-weight:700;white-space:nowrap}
#add-document,#add-evidence,#document-upload,#insight-register-upload,
#import-workspace,#import-workspace-input,#import-workspace-confirm,
[data-doc-action="edit"],[data-doc-action="delete"],[data-doc-action="add-register"],
[data-doc-action="link-source"],[data-doc-action="relink-register"],[data-doc-action="replace"],
[data-source-update],[data-confirm-source-update],[data-add-insight-register],
[data-learning-suggestion-confirm],[data-learning-suggestion-edit],[data-learning-suggestion-evidence],
[data-approve-routine-clusters],[data-duplicate-decision],[data-learning-component-edit],
[data-finding-edit],[data-insight-edit],[data-open-publish-preview],[data-confirm-publish],
[data-publish],[data-edit],[data-delete],
#taxonomy .ux-taxonomy-header-actions,.ux-taxonomy-manage-v2,.taxonomy-inline-action,
[data-taxonomy-term-create],#taxonomy-vocabulary-create,[data-vocabulary-add],[data-glossary-create],
.glossary-kebab,[data-glossary-menu],[data-taxonomy-manager-v2],
[data-taxonomy-manager-v2-edit],[data-taxonomy-manager-v2-merge],[data-taxonomy-manager-v2-delete],
[data-taxonomy-edit],[data-taxonomy-delete],[data-propose-taxonomy],
#taxonomy-manager-v2-modal,#taxonomy-manager-v2-edit,#taxonomy-manager-v2-merge,
#taxonomy-manager-v2-confirm,#taxonomy-vocabulary-create-modal,
#taxonomy-manager-v2-edit-action,#taxonomy-manager-v2-merge-action,
#taxonomy-manager-v2-confirm-action,#delete-modal,[data-delete-confirm],
#storage-save-status{display:none!important}
#uxs-export,#uxs-export-cro,[data-download-insight-register],
[data-doc-download-direct],[data-doc-action="open"]{display:inline-flex!important}
@media(max-width:820px){.ux-demo-readonly-badge{display:none}}
</style>
'''
if 'id="ux-demo-readonly-latest"' not in s:
    s = s.replace('</head>', readonly_css + '\n</head>', 1)

readonly_js = r'''
<script id="ux-demo-readonly-latest-guard">
(() => {
  document.documentElement.dataset.demoMode='readonly';
  const writeSelectors = [
    '#add-document','#add-evidence','[data-doc-action="edit"]','[data-doc-action="delete"]',
    '[data-doc-action="add-register"]','[data-doc-action="link-source"]','[data-doc-action="relink-register"]',
    '[data-learning-suggestion-confirm]','[data-learning-suggestion-edit]','[data-learning-suggestion-evidence]',
    '[data-learning-component-edit]','[data-approve-routine-clusters]','[data-duplicate-decision]',
    '[data-finding-edit]','[data-insight-edit]','[data-open-publish-preview]','[data-confirm-publish]',
    '[data-taxonomy-term-create]','[data-taxonomy-manager-v2-edit]','[data-taxonomy-manager-v2-merge]',
    '[data-taxonomy-manager-v2-delete]','[data-taxonomy-edit]','[data-taxonomy-delete]',
    '[data-propose-taxonomy]','[data-source-update]','[data-confirm-source-update]',
    '[data-delete-confirm]','#import-workspace-confirm','#taxonomy-manager-v2-edit-action',
    '#taxonomy-manager-v2-merge-action','#taxonomy-manager-v2-confirm-action'
  ];
  document.addEventListener('click', e => {
    const target=e.target?.closest?.(writeSelectors.join(','));
    if(!target)return;
    e.preventDefault();
    e.stopImmediatePropagation();
  }, true);
})();
</script>
'''
if 'id="ux-demo-readonly-latest-guard"' not in s:
    s = s.replace('</body>', readonly_js + '\n</body>', 1)

s = s.replace(
    'data-build="2026-11-17-v6-192-excel-sync"',
    'data-build="2026-11-18-v6-194-public-245-records"',
    1
)

ROOT.mkdir(parents=True, exist_ok=True)
TARGET.write_text(s, encoding="utf-8")
print("UX Intelligence public snapshot installed")
print("v6-192 · 245 registros · read-only · filters + exports")