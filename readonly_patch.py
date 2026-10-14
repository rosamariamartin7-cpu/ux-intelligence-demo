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



cascade_marker = "</body>"
cascade_script = r"""
<script id="ux-demo-cascading-taxonomy-filters">
(function(){
  const fields=['product','funnel','minifunnel','screen','component','element'];
  const ids=Object.fromEntries(fields.map(field=>[field,'uxs-'+field]));
  const norm=value=>String(value??'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').trim().toLowerCase();
  let suppress=false;

  function fieldValues(record,field){
    if(!record)return [];
    if(field==='component'){
      const values=[record.component,...(Array.isArray(record.components)?record.components:[])];
      return [...new Set(values.map(v=>String(v||'').trim()).filter(Boolean))];
    }
    const value=record[field];
    if(Array.isArray(value))return [...new Set(value.map(v=>String(v||'').trim()).filter(Boolean))];
    return String(value||'').trim()?[String(value).trim()]:[];
  }

  function records(){
    try{
      if(typeof currentStructuredRecords==='function'){
        const rows=currentStructuredRecords()||[];
        return rows.map(row=>globalThis.UXGovernedTaxonomy?.normalizeRecord?.(row)||row);
      }
    }catch(_){}
    try{
      if(Array.isArray(globalThis.sourceItems)){
        return globalThis.sourceItems.flatMap(item=>(item.insightRegister?.rows||[]))
          .map(row=>globalThis.UXGovernedTaxonomy?.normalizeRecord?.(row)||row);
      }
    }catch(_){}
    return [];
  }

  function selected(field){
    const el=document.getElementById(ids[field]);
    return String(el?.value||'').trim();
  }

  function matches(record,field,value){
    if(!value)return true;
    return fieldValues(record,field).some(candidate=>norm(candidate)===norm(value));
  }

  function availableValues(targetField){
    const targetIndex=fields.indexOf(targetField);
    let rows=records();
    fields.slice(0,targetIndex).forEach(parent=>{
      const value=selected(parent);
      if(value)rows=rows.filter(row=>matches(row,parent,value));
    });
    const out=[];
    const seen=new Set();
    rows.forEach(row=>fieldValues(row,targetField).forEach(value=>{
      const key=norm(value);
      if(key&&!seen.has(key)){seen.add(key);out.push(value);}
    }));
    return out.sort((a,b)=>a.localeCompare(b,'es'));
  }

  function setOptions(field,{preserve=true}={}){
    const el=document.getElementById(ids[field]);
    if(!el)return;
    const current=preserve?String(el.value||''):'';
    const values=availableValues(field);
    el.innerHTML='<option value="">Todos</option>'+values.map(value=>'<option value="'+escapeHtml(value)+'">'+escapeHtml(value)+'</option>').join('');
    if(current&&values.some(value=>norm(value)===norm(current))){
      const matched=values.find(value=>norm(value)===norm(current));
      el.value=matched||'';
    }else{
      el.value='';
    }
  }

  function resetDescendants(field){
    const index=fields.indexOf(field);
    suppress=true;
    fields.slice(index+1).forEach(child=>{
      const el=document.getElementById(ids[child]);
      if(!el)return;
      if(el.value!==''){
        el.value='';
        el.dispatchEvent(new Event('change',{bubbles:true}));
      }
    });
    suppress=false;
  }

  function updateAll(){
    fields.forEach(field=>setOptions(field,{preserve:true}));
    try{globalThis.__dsSyncSelects?.();}catch(_){}
  }

  function onChange(event){
    const field=fields.find(name=>event.target?.id===ids[name]);
    if(!field||suppress)return;
    resetDescendants(field);
    fields.slice(fields.indexOf(field)+1).forEach(child=>setOptions(child,{preserve:false}));
    try{globalThis.__dsSyncSelects?.();}catch(_){}
  }

  function escapeHtml(value){
    return String(value??'').replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  }

  function init(){
    fields.forEach(field=>document.getElementById(ids[field])?.addEventListener('change',onChange));
    updateAll();
    setTimeout(updateAll,350);
    setTimeout(updateAll,1200);

    const prev=globalThis.__uxSimpleExploreRefresh;
    if(typeof prev==='function'&&!prev.__uxCascadeWrapped){
      const wrapped=function(){
        const result=prev.apply(this,arguments);
        setTimeout(updateAll,0);
        return result;
      };
      wrapped.__uxCascadeWrapped=true;
      globalThis.__uxSimpleExploreRefresh=wrapped;
    }
  }

  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);
  else init();
})();
</script>
"""

if 'id="ux-demo-cascading-taxonomy-filters"' not in s:
    s = s.replace(cascade_marker, cascade_script + cascade_marker, 1)


p.write_text(s, encoding="utf-8")
print("Strict read-only UI applied")
