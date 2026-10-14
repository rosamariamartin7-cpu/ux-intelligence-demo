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
.ux-taxonomy-manage-v2,
[data-doc-action="edit"],
[data-doc-action="delete"],
[data-doc-action="add-register"],
[data-doc-action="link-source"],
[data-doc-action="relink-register"],
[data-taxonomy-edit],
[data-taxonomy-delete],
[data-propose-taxonomy],
[data-learning-suggestion-confirm],
[data-learning-suggestion-edit],
[data-learning-component-edit],
[data-finding-edit],
[data-insight-edit],
[data-open-publish-preview],
[data-confirm-publish],
[data-confirm-source-update],
[data-add-insight-register],
#taxonomy-manager-v2-modal,
#import-workspace-modal {
  display:none !important;
}
</style>
"""

if 'id="ux-demo-strict-readonly"' not in s:
    s = s.replace(marker, style + marker, 1)

p.write_text(s, encoding="utf-8")
print("Strict read-only UI applied")
