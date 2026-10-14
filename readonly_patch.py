from pathlib import Path

p = Path("app/ux-intelligence-demo-exact/index.html")
s = p.read_text(encoding="utf-8")

marker = "</head>"
style = r"""
<style id="ux-demo-strict-readonly">
/* Shared review build: consult, filter and download only. */
#add-document,
#add-evidence,
#document-upload,
#insight-register-upload,
#import-workspace,
#import-workspace-input,
#export-workspace,

/* Document / knowledge editing */
[data-doc-action="edit"],
[data-doc-action="delete"],
[data-doc-action="add-register"],
[data-doc-action="link-source"],
[data-doc-action="relink-register"],
[data-learning-suggestion-confirm],
[data-learning-suggestion-edit],
[data-learning-component-edit],
[data-finding-edit],
[data-insight-edit],
[data-open-publish-preview],
[data-confirm-publish],
[data-confirm-source-update],
[data-add-insight-register],

/* Taxonomy editing */
#taxonomy .ux-taxonomy-header-actions,
.ux-taxonomy-manage-v2,
.taxonomy-inline-action,
[data-taxonomy-term-create],
#taxonomy-vocabulary-create,
[data-vocabulary-add],
[data-glossary-create],
.glossary-kebab,
[data-glossary-menu],
#taxonomy-detail button:not([data-taxonomy-explore-context]),
[data-taxonomy-manager-v2],
[data-taxonomy-manager-v2-edit],
[data-taxonomy-manager-v2-merge],
[data-taxonomy-manager-v2-delete],
[data-taxonomy-edit],
[data-taxonomy-delete],
[data-propose-taxonomy],
[data-vocabulary-add],
[data-glossary-create],
#taxonomy-manager-v2-modal,
#taxonomy-manager-v2-edit,
#taxonomy-manager-v2-merge,
#taxonomy-manager-v2-confirm,

/* Backup/import controls are not part of the shared demo */
#import-workspace-modal {
  display:none !important;
}
</style>
"""

if 'id="ux-demo-strict-readonly"' in s:
    start = s.index('<style id="ux-demo-strict-readonly">')
    end = s.index('</style>', start) + len('</style>')
    s = s[:start] + style.strip() + s[end:]
else:
    s = s.replace(marker, style + marker, 1)

p.write_text(s, encoding="utf-8")
print("Strict read-only UI applied")
