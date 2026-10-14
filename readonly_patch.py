from pathlib import Path

ROOT = Path("app/ux-intelligence-demo-exact")
p = ROOT / "index.html"
s = p.read_text(encoding="utf-8")

# Identificación de la copia compartida.
s = s.replace(
    '>Demo · solo consulta</span>',
    '>Herramienta interna UX · Demo solo consulta</span>',
    1
)

marker = "</head>"
style = r"""
<style id="ux-demo-strict-readonly">
/* Demo compartida: consultar, filtrar y descargar. Nunca editar ni subir. */
#add-document,
#add-evidence,
#document-upload,
#insight-register-upload,
#import-workspace,
#import-workspace-input,
#export-workspace,
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

/* Taxonomía: consulta pura. */
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
#taxonomy-manager-v2-modal,
#taxonomy-manager-v2-edit,
#taxonomy-manager-v2-merge,
#taxonomy-manager-v2-confirm,
#taxonomy-vocabulary-create-modal,
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

body_marker = "</body>"
script = r"""
<script id="ux-demo-controlled-journey-filters">
(function(){
  const hierarchy=['product','funnel','minifunnel','screen','component','element'];
  const ids=Object.fromEntries(hierarchy.map(field=>[field,'uxs-'+field]));
  const BOOKING_FUNNELS=['Availability','Shopping Cart','Passengers','Extras','Payment'];
  const EXTRA_FALLBACK=['Asientos','Maletas','Priority Boarding','Menú a bordo','Wi-Fi','Mascotas','Equipaje deportivo'];
  const SUPPORTED_PRODUCTS=new Set(['home','booking']);
  let internal=false;

  const clean=value=>String(value??'').trim();
  const norm=value=>clean(value).normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLocaleLowerCase('es');
  const esc=value=>String(value??'').replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));

  function taxonomyTerms(){
    try{
      const terms=Array.isArray(taxonomyProject?.state?.terms)?taxonomyProject.state.terms:[];
      return terms.filter(term=>{
        const status=norm(term?.status||'canonical');
        const origin=clean(term?.origin);
        const canonical=['canonical','canonico'].includes(status);
        const governed=term?.governed===true||!/^excel revisado\s*·/i.test(origin);
        return canonical&&governed;
      });
    }catch(_){return [];}
  }
  const termId=term=>clean(term?.id||term?.termId||term?.key);
  const parentId=term=>clean(term?.parentId||term?.parentTermId||term?.parent?.id||term?.parent);
  const termName=term=>clean(term?.canonicalName||term?.name||term?.label||term?.value);

  function ancestry(term){
    const terms=taxonomyTerms();
    const byId=new Map(terms.map(item=>[termId(item),item]).filter(([id])=>id));
    const out=[];
    const seen=new Set();
    let current=term;
    while(current){
      const id=termId(current);
      if(id&&seen.has(id))break;
      if(id)seen.add(id);
      out.unshift(termName(current));
      const pid=parentId(current);
      current=pid?byId.get(pid):null;
    }
    return out.filter(Boolean);
  }

  function canonicalProducts(){
    return [...new Set(taxonomyTerms()
      .filter(term=>clean(term?.level)==='product')
      .map(termName).filter(Boolean))]
      .sort((a,b)=>a.localeCompare(b,'es'));
  }

  function bookingExtraMinifunnels(){
    const values=taxonomyTerms()
      .filter(term=>clean(term?.level)==='minifunnel')
      .filter(term=>{
        const path=ancestry(term).map(norm);
        return path.includes('booking')&&path.includes('extras');
      })
      .map(termName).filter(Boolean);
    const unique=[...new Set(values)];
    return unique.length?unique.sort((a,b)=>a.localeCompare(b,'es')):EXTRA_FALLBACK.slice();
  }

  function structuredRecords(){
    try{
      if(typeof currentStructuredRecords==='function'){
        return (currentStructuredRecords()||[]).map(row=>globalThis.UXGovernedTaxonomy?.normalizeRecord?.(row)||row);
      }
    }catch(_){}
    try{
      return (Array.isArray(globalThis.sourceItems)?globalThis.sourceItems:[])
        .flatMap(item=>(item.insightRegister?.rows||[]))
        .map(row=>globalThis.UXGovernedTaxonomy?.normalizeRecord?.(row)||row);
    }catch(_){return [];}
  }

  function valuesOf(row,field){
    if(!row)return [];
    if(field==='component'){
      return [...new Set([row.component,...(Array.isArray(row.components)?row.components:[])]
        .map(clean).filter(Boolean))];
    }
    const value=row[field];
    if(Array.isArray(value))return [...new Set(value.map(clean).filter(Boolean))];
    return clean(value)?[clean(value)]:[];
  }

  function selected(field){
    return clean(document.getElementById(ids[field])?.value);
  }

  function funnelMatches(rowValue,selectedValue){
    const rv=norm(rowValue),sv=norm(selectedValue);
    if(rv===sv)return true;
    const aliases={
      'availability':['availability','disponibilidad','availability/dispo','dispo'],
      'shopping cart':['shopping cart','resumen','resumen / shopping cart','summary / shopping cart'],
      'passengers':['passengers','pasajeros','passengers/paxes','paxes'],
      'extras':['extras'],
      'payment':['payment','pago']
    };
    return (aliases[sv]||[sv]).includes(rv);
  }

  function rowMatches(row,field,value){
    if(!value)return true;
    const candidates=valuesOf(row,field);
    if(field==='funnel')return candidates.some(candidate=>funnelMatches(candidate,value));
    return candidates.some(candidate=>norm(candidate)===norm(value));
  }

  function productAllowsDetails(product){
    return !product||SUPPORTED_PRODUCTS.has(norm(product));
  }

  function dataValues(field){
    const product=selected('product');
    if(!productAllowsDetails(product))return [];

    let rows=structuredRecords();
    const parents={
      screen:['product','funnel','minifunnel'],
      component:['product','funnel','minifunnel','screen'],
      element:['product','funnel','minifunnel','screen','component']
    }[field]||[];

    parents.forEach(parent=>{
      const value=selected(parent);
      if(value)rows=rows.filter(row=>rowMatches(row,parent,value));
    });

    const out=[];
    const seen=new Set();
    rows.forEach(row=>valuesOf(row,field).forEach(value=>{
      const key=norm(value);
      if(key&&!seen.has(key)){seen.add(key);out.push(value);}
    }));
    return out.sort((a,b)=>a.localeCompare(b,'es'));
  }

  function desiredOptions(field){
    const product=selected('product');
    if(field==='product')return canonicalProducts();

    if(!productAllowsDetails(product))return [];

    if(field==='funnel'){
      return !product||norm(product)==='booking' ? BOOKING_FUNNELS.slice() : [];
    }

    if(field==='minifunnel'){
      const funnel=selected('funnel');
      return (!product||norm(product)==='booking')&&norm(funnel)==='extras'
        ? bookingExtraMinifunnels()
        : [];
    }

    if(field==='screen'||field==='component'||field==='element'){
      return dataValues(field);
    }
    return [];
  }

  function setSelect(field,{preserve=true}={}){
    const el=document.getElementById(ids[field]);
    if(!el)return;
    const current=preserve?clean(el.value):'';
    const options=desiredOptions(field);
    el.innerHTML='<option value="">Todos</option>'+options.map(value=>'<option value="'+esc(value)+'">'+esc(value)+'</option>').join('');

    const matched=current&&options.find(value=>norm(value)===norm(current));
    el.value=matched||'';
  }

  function clearField(field){
    const el=document.getElementById(ids[field]);
    if(!el||!el.value)return;
    el.value='';
    el.dispatchEvent(new Event('change',{bubbles:true}));
  }

  function refreshFrom(field){
    const index=hierarchy.indexOf(field);
    internal=true;
    try{
      hierarchy.slice(index+1).forEach(child=>clearField(child));
      hierarchy.slice(index+1).forEach(child=>setSelect(child,{preserve:false}));
      if(field==='product')setSelect('product',{preserve:true});
      globalThis.__dsSyncSelects?.();
    }finally{
      internal=false;
    }
  }

  function refreshAll(){
    internal=true;
    try{
      setSelect('product',{preserve:true});
      setSelect('funnel',{preserve:true});
      setSelect('minifunnel',{preserve:true});
      setSelect('screen',{preserve:true});
      setSelect('component',{preserve:true});
      setSelect('element',{preserve:true});
      globalThis.__dsSyncSelects?.();
    }finally{
      internal=false;
    }
  }

  function onHierarchyChange(event){
    if(internal)return;
    const field=hierarchy.find(name=>event.target?.id===ids[name]);
    if(!field)return;
    setTimeout(()=>refreshFrom(field),0);
  }

  function init(){
    hierarchy.forEach(field=>document.getElementById(ids[field])?.addEventListener('change',onHierarchyChange));
    refreshAll();
    setTimeout(refreshAll,300);
    setTimeout(refreshAll,1000);

    const previous=globalThis.__uxSimpleExploreRefresh;
    if(typeof previous==='function'&&!previous.__uxDemoControlled){
      const wrapped=function(){
        const result=previous.apply(this,arguments);
        setTimeout(refreshAll,0);
        return result;
      };
      wrapped.__uxDemoControlled=true;
      globalThis.__uxSimpleExploreRefresh=wrapped;
    }
  }

  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);
  else init();
})();
</script>
"""

# Replace any previous demo-specific hierarchy patch with the current one.
for old_id in [
    'ux-demo-cascading-taxonomy-filters',
    'ux-demo-controlled-journey-filters'
]:
    token = f'<script id="{old_id}">'
    if token in s:
        start = s.index(token)
        end = s.index('</script>', start) + len('</script>')
        s = s[:start] + s[end:]

s = s.replace(body_marker, script + body_marker, 1)

p.write_text(s, encoding="utf-8")
print("Read-only demo filters aligned with UX review rules")
