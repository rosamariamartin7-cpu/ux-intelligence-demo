from pathlib import Path
import json

ROOT = Path("app/ux-intelligence-demo-exact")
ROOT.mkdir(parents=True, exist_ok=True)

# Recupera el snapshot íntegro desde el index standalone del repo.
# Evita depender del antiguo data.js, que quedó truncado.
source_index = Path("index.html")
if not source_index.exists():
    raise SystemExit("ERROR: no se encuentra index.html fuente en el repo")
source_text = source_index.read_text(encoding="utf-8")
marker = "const HISTORY = "
start = source_text.find(marker)
if start < 0:
    raise SystemExit("ERROR: no se encuentra const HISTORY en index.html")
payload_text = source_text[start + len(marker):]
history, _ = json.JSONDecoder().raw_decode(payload_text)
(ROOT / "demo-data.json").write_text(
    json.dumps(history, ensure_ascii=False, separators=(",", ":")),
    encoding="utf-8"
)

html = r'''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex,nofollow,noarchive">
<title>Air Europa · UX Intelligence · Demo CRO</title>
<style>
:root{
  --navy:#031b4e;--navy2:#082a68;--blue:#2d69e1;--blue2:#1f58c7;--sky:#15a9e5;
  --ink:#181d27;--muted:#717680;--text2:#535862;--line:#e9eaeb;--line2:#d5d7da;
  --bg:#f6f8fb;--white:#fff;--soft:#f4f7ff;--success:#067647;--successbg:#ecfdf3;
  --warn:#b54708;--warnbg:#fff6ed;--danger:#b42318;--dangerbg:#fef3f2;
  --r:10px;--shadow:0 1px 2px rgba(10,13,18,.05);--side:252px;
}
*{box-sizing:border-box}
html{overflow-x:hidden}
body{margin:0;background:var(--bg);color:var(--ink);font:14px/1.5 Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
button,input,select{font:inherit}
button{cursor:pointer}
[hidden]{display:none!important}
.app{min-height:100vh}
.sidebar{position:fixed;inset:0 auto 0 0;width:var(--side);z-index:20;display:flex;flex-direction:column;background:linear-gradient(180deg,var(--navy),#03102f);color:#fff}
.brand{display:flex;align-items:center;gap:11px;padding:24px 20px 18px}
.mark{width:34px;height:34px;border-radius:9px;display:grid;place-items:center;background:linear-gradient(135deg,#fff,#b9edff);color:var(--navy);font-weight:800;box-shadow:0 6px 16px rgba(0,0,0,.15)}
.brand b,.brand span{display:block}.brand b{font-size:14px}.brand span{font-size:11px;color:rgba(255,255,255,.64);margin-top:2px}
.nav{padding:10px 12px}
.nav button{width:100%;min-height:44px;display:flex;align-items:center;gap:11px;padding:9px 10px;border:0;border-radius:9px;background:transparent;color:rgba(255,255,255,.72);text-align:left}
.nav button:hover,.nav button.active{color:#fff;background:rgba(255,255,255,.12)}
.ico{width:20px;height:20px;border:1px solid rgba(255,255,255,.3);border-radius:5px;display:grid;place-items:center;font-size:10px;font-weight:800}
.count{margin-left:auto;min-width:22px;padding:2px 6px;border-radius:999px;background:rgba(255,255,255,.1);font-size:10px;text-align:center}
.demo-note{margin:auto 16px 18px;padding-top:14px;border-top:1px solid rgba(255,255,255,.12);font-size:11px;color:rgba(255,255,255,.62)}
.main{min-height:100vh;margin-left:var(--side)}
.topbar{position:sticky;top:0;z-index:15;height:72px;display:flex;align-items:center;gap:14px;padding:0 28px;border-bottom:1px solid var(--line);background:rgba(255,255,255,.96);backdrop-filter:blur(10px)}
.menu{display:none;width:44px;height:44px;border:1px solid var(--line2);border-radius:8px;background:#fff}
.global{position:relative;width:min(520px,46vw);margin-left:auto}
.global input{width:100%;height:44px;padding:0 14px 0 40px;border:1px solid var(--line2);border-radius:8px;background:#fff;color:var(--ink);font-size:15px}
.global:before{content:"⌕";position:absolute;left:14px;top:9px;color:var(--muted);font-size:20px}
.readonly{display:inline-flex;align-items:center;min-height:30px;padding:4px 10px;border:1px solid var(--line);border-radius:999px;background:#fff;color:var(--text2);font-size:11px;font-weight:700;white-space:nowrap}
.content{max-width:1500px;margin:0 auto;padding:34px 32px 64px}
.head{margin-bottom:24px}.eyebrow{color:var(--blue2);font-size:12px;font-weight:800;text-transform:uppercase;letter-spacing:.06em}.head h1{margin:6px 0 6px;font-size:34px;line-height:1.15;letter-spacing:-.035em}.head p{margin:0;color:var(--muted);max-width:850px}
.cards{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px;margin:0 0 22px}
.card,.panel{border:1px solid var(--line);border-radius:12px;background:#fff;box-shadow:var(--shadow)}
.card{padding:18px}.card span{display:block;color:var(--muted);font-size:12px;font-weight:700}.card strong{display:block;margin-top:5px;font-size:28px;line-height:1.1}
.panel{padding:18px;margin-bottom:18px}
.panel-head{display:flex;align-items:flex-start;justify-content:space-between;gap:14px;margin-bottom:14px}.panel-head h2{margin:0;font-size:18px}.panel-head p{margin:3px 0 0;color:var(--muted)}
.filters{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;padding:16px;border:1px solid var(--line);border-radius:12px;background:#fff;margin-bottom:16px}
.field{display:grid;gap:5px}.field label{font-size:11px;font-weight:800;color:var(--muted);text-transform:uppercase;letter-spacing:.04em}
.field select,.field input{width:100%;height:42px;border:1px solid var(--line2);border-radius:8px;background:#fff;padding:0 11px;color:var(--ink)}
.toolbar{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin:0 0 14px}.toolbar .result{margin-left:auto;color:var(--muted);font-size:12px}
.btn{min-height:42px;padding:9px 13px;border-radius:8px;border:1px solid var(--line2);background:#fff;color:var(--ink);font-weight:700}.btn.primary{border-color:var(--blue);background:var(--blue);color:#fff}.btn:hover{filter:brightness(.98)}
.list{display:grid;gap:10px}
.item{border:1px solid var(--line);border-radius:11px;background:#fff;padding:15px 16px;display:grid;grid-template-columns:minmax(0,1fr) auto;gap:14px;align-items:start}
.meta{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:7px}.chip{display:inline-flex;align-items:center;min-height:24px;padding:3px 8px;border-radius:999px;background:#f2f4f7;color:var(--text2);font-size:11px;font-weight:700}.chip.blue{background:var(--soft);color:var(--blue2)}.chip.high{background:var(--dangerbg);color:var(--danger)}.chip.medium{background:var(--warnbg);color:var(--warn)}.chip.low{background:var(--successbg);color:var(--success)}
.item h3{margin:0;font-size:15px;line-height:1.45}.item p{margin:6px 0 0;color:var(--text2);font-size:13px}.link{border:0;background:transparent;color:var(--blue2);font-weight:750;min-height:40px;padding:6px 2px;white-space:nowrap}
.empty{padding:34px 18px;text-align:center;color:var(--muted);border:1px dashed var(--line2);border-radius:12px;background:#fff}
.doc-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px}
.doc{border:1px solid var(--line);border-radius:11px;background:#fff;padding:15px}.doc h3{margin:0 0 7px;font-size:15px}.doc p{margin:0;color:var(--muted);font-size:12px}
.tree{display:grid;gap:10px}.tree-group{border:1px solid var(--line);border-radius:11px;background:#fff;padding:14px}.tree-group h3{margin:0 0 10px;font-size:15px}.tree-row{display:flex;align-items:flex-start;gap:8px;flex-wrap:wrap;padding:7px 0;border-top:1px solid var(--line)}.tree-row:first-of-type{border-top:0}.tree-label{min-width:110px;color:var(--muted);font-size:11px;font-weight:800;text-transform:uppercase}.tree-values{display:flex;gap:6px;flex-wrap:wrap;flex:1}
.drawer-back{position:fixed;inset:0;z-index:40;background:rgba(3,16,47,.38)}
.drawer{position:fixed;z-index:45;right:0;top:0;bottom:0;width:min(620px,100vw);overflow:auto;background:#fff;box-shadow:-14px 0 44px rgba(10,13,18,.18)}
.drawer-head{padding:28px 24px 18px;border-bottom:1px solid var(--line)}.drawer-head h2{margin:8px 48px 0 0;font-size:23px;line-height:1.3}.close{position:absolute;right:16px;top:16px;width:44px;height:44px;border:1px solid var(--line2);border-radius:8px;background:#fff}
.drawer-body{padding:22px 24px 40px}.section{margin-bottom:24px}.section h4{margin:0 0 7px;font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:var(--muted)}.section p{margin:0;color:var(--text2);white-space:pre-wrap}
.error{margin:20px;padding:18px;border:1px solid #fda29b;border-radius:12px;background:#fff;color:#b42318}
.loading{padding:60px 20px;text-align:center;color:var(--muted)}
.backdrop{display:none}
@media(max-width:1050px){.cards{grid-template-columns:repeat(2,1fr)}.filters{grid-template-columns:repeat(2,1fr)}}
@media(max-width:820px){
  .sidebar{transform:translateX(-100%);transition:.2s}.sidebar.open{transform:none}.backdrop.open{display:block;position:fixed;inset:0;z-index:18;background:rgba(3,16,47,.4)}
  .main{margin-left:0}.menu{display:inline-grid;place-items:center}.topbar{height:64px;padding:0 12px}.global{width:auto;flex:1}.readonly{display:none}
  .content{padding:24px 16px 48px}.head h1{font-size:29px}.doc-grid{grid-template-columns:1fr}
}
@media(max-width:650px){.cards,.filters{grid-template-columns:1fr}.item{grid-template-columns:1fr}.item .link{justify-self:start}.toolbar{align-items:stretch}.toolbar .btn{width:100%}.toolbar .result{width:100%;margin-left:0}.drawer-head,.drawer-body{padding-left:18px;padding-right:18px}}
</style>
</head>
<body>
<div id="fatal" class="error" hidden></div>
<div class="app" id="app" hidden>
  <aside class="sidebar" id="sidebar">
    <div class="brand"><div class="mark">AE</div><div><b>UX Intelligence</b><span>Air Europa</span></div></div>
    <div class="nav">
      <button class="active" data-page="overview"><span class="ico">R</span>Resumen</button>
      <button data-page="explore"><span class="ico">E</span>Explorar <span class="count" id="nav-records">0</span></button>
      <button data-page="learnings"><span class="ico">L</span>Learnings <span class="count" id="nav-learnings">0</span></button>
      <button data-page="documents"><span class="ico">D</span>Documentos <span class="count" id="nav-docs">0</span></button>
      <button data-page="taxonomy"><span class="ico">T</span>Taxonomía</button>
    </div>
    <div class="demo-note">Herramienta interna UX · Demo solo consulta</div>
  </aside>
  <button class="backdrop" id="backdrop" aria-label="Cerrar menú"></button>
  <main class="main">
    <header class="topbar">
      <button class="menu" id="menu" aria-label="Abrir menú">☰</button>
      <div class="global"><input id="global-search" type="search" placeholder="Buscar en UX Intelligence"></div>
      <span class="readonly">Demo · solo consulta</span>
    </header>
    <div class="content">
      <section id="page-overview"></section>
      <section id="page-explore" hidden></section>
      <section id="page-learnings" hidden></section>
      <section id="page-documents" hidden></section>
      <section id="page-taxonomy" hidden></section>
    </div>
  </main>
</div>
<div class="loading" id="loading">Cargando UX Intelligence…</div>
<div id="drawer-root"></div>
<script>
const $=(s,r=document)=>r.querySelector(s);
const $$=(s,r=document)=>[...r.querySelectorAll(s)];
const esc=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const clean=v=>String(v??'').trim();
const norm=v=>clean(v).normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
let DATA={payload:null,documents:[],rows:[],learnings:[],evidence:[]};
let state={page:'overview',q:'',filters:{product:'',funnel:'',minifunnel:'',component:'',device:'',impact:''}};

async function decodePayload(){
  const response=await fetch('demo-data.json',{cache:'no-store'});
  if(!response.ok) throw new Error('No se pudo cargar el dataset de la demo ('+response.status+').');
  return await response.json();
}
function walk(obj,fn,seen=new Set()){
  if(!obj||typeof obj!=='object'||seen.has(obj))return;seen.add(obj);fn(obj);
  if(Array.isArray(obj)){for(const x of obj)walk(x,fn,seen);return}
  for(const v of Object.values(obj))walk(v,fn,seen);
}
function bestArray(root,names,shape=[]){
  const wanted=new Set(names.map(norm));let best=[];
  walk(root,o=>{
    if(Array.isArray(o))return;
    for(const [k,v] of Object.entries(o)){
      if(Array.isArray(v)&&wanted.has(norm(k))&&v.length>=best.length)best=v;
      if(Array.isArray(v)&&shape.length&&v.length>=best.length&&v.some(x=>x&&typeof x==='object'&&shape.some(key=>key in x)))best=v;
    }
  });
  return best;
}
function canonicalFunnel(row){
  const candidates=[row.funnel,row.minifunnel,row.screen].map(norm).filter(Boolean).join(' | ');
  if(/availability|disponibilidad|dispo/.test(candidates))return 'Availability';
  if(/shopping cart|summary|resumen|carrito/.test(candidates))return 'Shopping Cart';
  if(/passengers|pasajeros|paxes/.test(candidates))return 'Passengers';
  if(/payment|pago/.test(candidates))return 'Payment';
  if(/extras|ancillar|asiento|seat|maleta|equipaje|baggage|priority|men[uú]|wifi|mascota|deportivo/.test(candidates))return 'Extras';
  const f=clean(row.funnel);
  return ['Availability','Shopping Cart','Passengers','Extras','Payment'].find(x=>norm(x)===norm(f))||'';
}
function canonicalMini(row,funnel){
  if(funnel!=='Extras')return '';
  const c=[row.minifunnel,row.screen,row.component].map(norm).join(' | ');
  if(/asiento|seat/.test(c))return 'Reserva de asiento';
  if(/maleta|equipaje|baggage/.test(c))return 'Maletas';
  if(/priority/.test(c))return 'Priority Boarding';
  if(/men[uú]|comida|meal/.test(c))return 'Menú a bordo';
  if(/wifi/.test(c))return 'Wi-Fi';
  if(/mascota|pet/.test(c))return 'Mascotas';
  if(/deportivo|sport/.test(c))return 'Equipaje deportivo';
  const m=clean(row.minifunnel);
  return m && !/extras|ancillar/i.test(m)?m:'';
}
function normalizeRow(row,doc){
  const product=norm(row.product)==='home'?'Home':'Booking';
  const funnel=product==='Booking'?canonicalFunnel(row):'';
  return {
    ...row,product,funnel,minifunnel:canonicalMini(row,funnel),
    component:clean(row.component)||'',initiative:clean(row.initiative||doc?.initiative)||'',
    device:clean(row.device||row.channelEnvironment||row.dispositivo)||'',
    impact:clean(row.impactUx||row.impactUX||row.impact)||'',
    insight:clean(row.insight||row.title||row.finding||row.name)||'',
    evidence:clean(row.evidence||row.support||row.description)||'',
    recommendation:clean(row.recommendation||row.uxResponse||row.opportunity)||'',
    origin:clean(row.origin||row.sourceType)||'',
    source:clean(row.source||doc?.name)||'',
    recordType:clean(row.recordType||row.type)||''
  };
}
function initData(payload){
  const snapshot=payload?.snapshot||payload?.history?.snapshot||payload?.workspace||payload;
  let docs=bestArray(snapshot,['documents','sourceItems','sources'],['insightRegister','originalName','documentProfile']);
  docs=docs.filter(x=>x&&typeof x==='object'&&(x.insightRegister||x.name||x.originalName));
  const rows=[];
  docs.forEach(doc=>{
    const rs=doc?.insightRegister?.rows||doc?.rows||[];
    if(Array.isArray(rs))rs.forEach(r=>rows.push(normalizeRow(r,doc)));
  });
  const directRows=bestArray(snapshot,['records','insights','insightRows'],['insight','recordType','impactUx']);
  if(!rows.length&&directRows.length)directRows.forEach(r=>rows.push(normalizeRow(r,null)));
  let learn=bestArray(snapshot,['learnings','learningItems','publishedLearnings'],['confidence','whatWeKnow','learning']);
  let ev=bestArray(snapshot,['evidence','evidenceItems'],['confidence','evidenceType']);
  DATA={payload,snapshot,documents:docs,rows,learnings:learn,evidence:ev};
}
function vals(field,rows=DATA.rows){return [...new Set(rows.map(r=>clean(r[field])).filter(Boolean))].sort((a,b)=>a.localeCompare(b,'es'))}
function filteredRows(){
  const q=norm(state.q);const f=state.filters;
  return DATA.rows.filter(r=>{
    if(f.product&&r.product!==f.product)return false;if(f.funnel&&r.funnel!==f.funnel)return false;
    if(f.minifunnel&&r.minifunnel!==f.minifunnel)return false;if(f.component&&r.component!==f.component)return false;
    if(f.device&&r.device!==f.device)return false;if(f.impact&&r.impact!==f.impact)return false;
    if(q&&!norm([r.insight,r.evidence,r.recommendation,r.component,r.initiative,r.origin,r.source].join(' ')).includes(q))return false;
    return true;
  });
}
function chipImpact(v){const n=norm(v);return n.includes('alto')?'high':n.includes('medio')?'medium':n.includes('bajo')?'low':''}
function head(title,desc){return '<div class="head"><div class="eyebrow">UX Intelligence</div><h1>'+esc(title)+'</h1><p>'+esc(desc)+'</p></div>'}
function renderOverview(){
  const rows=DATA.rows,docs=DATA.documents,learn=DATA.learnings;
  const recent=docs.slice().sort((a,b)=>clean(b.ingestedAt).localeCompare(clean(a.ingestedAt))).slice(0,6);
  $('#page-overview').innerHTML=head('Resumen','Memoria transversal UX de Air Europa. Esta copia es de consulta para colaboración UX/CRO.')+
  '<div class="cards"><div class="card"><span>Registros estructurados</span><strong>'+rows.length+'</strong></div><div class="card"><span>Learnings</span><strong>'+learn.length+'</strong></div><div class="card"><span>Documentos</span><strong>'+docs.length+'</strong></div><div class="card"><span>Productos activos</span><strong>'+vals('product').length+'</strong></div></div>'+
  '<div class="panel"><div class="panel-head"><div><h2>Últimos documentos</h2><p>Fuentes disponibles en esta demo.</p></div></div><div class="doc-grid">'+
  (recent.length?recent.map(d=>'<div class="doc"><h3>'+esc(d.name||d.originalName||'Documento')+'</h3><p>'+esc([d.initiative,d.product,d.exactDate].filter(Boolean).join(' · '))+'</p></div>').join(''):'<div class="empty">No hay documentos disponibles.</div>')+
  '</div></div>';
}
function selectField(label,key,options){
  return '<div class="field"><label>'+label+'</label><select data-filter="'+key+'"><option value="">Todos</option>'+options.map(v=>'<option '+(state.filters[key]===v?'selected':'')+'>'+esc(v)+'</option>').join('')+'</select></div>'
}
function renderExplore(){
  let base=DATA.rows;
  const funnelRows=state.filters.product?base.filter(r=>r.product===state.filters.product):base;
  const miniRows=state.filters.funnel?funnelRows.filter(r=>r.funnel===state.filters.funnel):funnelRows;
  const compRows=state.filters.minifunnel?miniRows.filter(r=>r.minifunnel===state.filters.minifunnel):miniRows;
  const rows=filteredRows();
  $('#page-explore').innerHTML=head('Explorar','Consulta evidencias, insights, hipótesis, inferencias y oportunidades por contexto real del journey.')+
  '<div class="filters">'+selectField('Producto','product',vals('product'))+selectField('Funnel','funnel',vals('funnel',funnelRows))+selectField('Minifunnel','minifunnel',vals('minifunnel',miniRows))+selectField('Componente','component',vals('component',compRows))+
  selectField('Dispositivo','device',vals('device'))+selectField('Impacto UX','impact',vals('impact'))+'</div>'+
  '<div class="toolbar"><button class="btn" id="clear">Limpiar filtros</button><button class="btn" id="export">Exportar CSV</button><button class="btn primary" id="export-cro">Exportar para CRO</button><span class="result">'+rows.length+' resultados</span></div>'+
  '<div class="list">'+(rows.length?rows.map((r,i)=>'<article class="item"><div><div class="meta">'+
  [r.product,r.funnel,r.minifunnel,r.component].filter(Boolean).map(v=>'<span class="chip blue">'+esc(v)+'</span>').join('')+
  (r.impact?'<span class="chip '+chipImpact(r.impact)+'">'+esc(r.impact)+'</span>':'')+
  '</div><h3>'+esc(r.insight||'Registro sin título')+'</h3><p>'+esc(r.evidence).slice(0,360)+'</p></div><button class="link" data-row="'+i+'">Ver detalle →</button></article>').join(''):'<div class="empty">No hay resultados con estos filtros.</div>')+'</div>';
  $$('[data-filter]').forEach(el=>el.onchange=()=>{state.filters[el.dataset.filter]=el.value;if(el.dataset.filter==='product'){state.filters.funnel='';state.filters.minifunnel='';state.filters.component=''}if(el.dataset.filter==='funnel'){state.filters.minifunnel='';state.filters.component=''}if(el.dataset.filter==='minifunnel')state.filters.component='';renderExplore()});
  $('#clear').onclick=()=>{state.filters={product:'',funnel:'',minifunnel:'',component:'',device:'',impact:''};state.q='';$('#global-search').value='';renderExplore()};
  $('#export').onclick=()=>exportCsv(rows,false);$('#export-cro').onclick=()=>exportCsv(rows,true);
  $$('.link[data-row]').forEach(btn=>btn.onclick=()=>openRow(rows[Number(btn.dataset.row)]));
}
function learningTitle(x){return clean(x.title||x.name||x.learning||x.whatWeKnow||x.summary)}
function learningConfidence(x){return clean(x.confidence||x.confidenceLevel||x.level)}
function renderLearnings(){
  const q=norm(state.q);
  const items=(DATA.learnings||[]).filter(x=>!q||norm(JSON.stringify(x)).includes(q));
  $('#page-learnings').innerHTML=head('Learnings','Conocimiento UX consolidado. Un learning no equivale a un experimento aislado.')+
  '<div class="list">'+(items.length?items.map((x,i)=>'<article class="item"><div><div class="meta">'+
  (learningConfidence(x)?'<span class="chip">'+esc(learningConfidence(x))+'</span>':'')+
  '</div><h3>'+esc(learningTitle(x)||'Learning')+'</h3><p>'+esc(clean(x.description||x.summary||x.whatWeKnow||x.evidence)).slice(0,420)+'</p></div><button class="link" data-learning="'+i+'">Ver learning →</button></article>').join(''):'<div class="empty">Este snapshot no expone learnings consolidados como colección independiente. Los registros siguen disponibles en Explorar.</div>')+'</div>';
  $$('[data-learning]').forEach(btn=>btn.onclick=()=>openObject(items[Number(btn.dataset.learning)],'Learning'));
}
function renderDocuments(){
  const q=norm(state.q);const docs=DATA.documents.filter(d=>!q||norm(JSON.stringify(d)).includes(q));
  $('#page-documents').innerHTML=head('Documentos','Fuentes que alimentan UX Intelligence. Esta demo no permite subir, editar ni borrar.')+
  '<div class="filters">'+selectField('Producto','product',vals('product'))+'<div class="field"><label>Componente</label><select disabled><option>Todos</option></select></div><div class="field"><label>Tipo</label><select disabled><option>Todos</option></select></div></div>'+
  '<div class="doc-grid">'+(docs.length?docs.map((d,i)=>'<article class="doc"><h3>'+esc(d.name||d.originalName||'Documento')+'</h3><p>'+esc([d.type,d.initiative,d.product,d.exactDate].filter(Boolean).join(' · '))+'</p><button class="link" data-doc="'+i+'">Ver documento →</button></article>').join(''):'<div class="empty">No hay documentos.</div>')+'</div>';
  $$('[data-doc]').forEach(btn=>btn.onclick=()=>openObject(docs[Number(btn.dataset.doc)],'Documento'));
}
function renderTaxonomy(){
  const rows=DATA.rows;const products=vals('product',rows);
  const html=products.map(p=>{
    const pr=rows.filter(r=>r.product===p);const funnels=vals('funnel',pr);
    if(p==='Home'){
      return '<div class="tree-group"><h3>Home</h3><div class="tree-row"><div class="tree-label">Componentes</div><div class="tree-values">'+vals('component',pr).map(x=>'<span class="chip">'+esc(x)+'</span>').join('')+'</div></div></div>';
    }
    return '<div class="tree-group"><h3>'+esc(p)+'</h3>'+funnels.map(f=>{
      const fr=pr.filter(r=>r.funnel===f);const minis=vals('minifunnel',fr);const comps=vals('component',fr);
      return '<div class="tree-row"><div class="tree-label">'+esc(f)+'</div><div class="tree-values">'+
      minis.map(x=>'<span class="chip blue">'+esc(x)+'</span>').join('')+comps.slice(0,20).map(x=>'<span class="chip">'+esc(x)+'</span>').join('')+'</div></div>';
    }).join('')+'</div>';
  }).join('');
  $('#page-taxonomy').innerHTML=head('Taxonomía','Jerarquía activa: Producto → Funnel → Minifunnel → Componente. Los niveles inferiores son opcionales.')+
  '<div class="tree">'+(html||'<div class="empty">No hay taxonomía derivable en este snapshot.</div>')+'</div>';
}
function renderAll(){renderOverview();renderExplore();renderLearnings();renderDocuments();renderTaxonomy();updateNav()}
function updateNav(){
  $('#nav-records').textContent=DATA.rows.length;$('#nav-learnings').textContent=DATA.learnings.length;$('#nav-docs').textContent=DATA.documents.length;
  $$('.nav button').forEach(b=>b.classList.toggle('active',b.dataset.page===state.page));
  ['overview','explore','learnings','documents','taxonomy'].forEach(p=>$('#page-'+p).hidden=p!==state.page);
}
function go(page){state.page=page;updateNav();$('#sidebar').classList.remove('open');$('#backdrop').classList.remove('open');window.scrollTo({top:0,behavior:'smooth'})}
function openRow(r){openObject({Contexto:[r.product,r.funnel,r.minifunnel,r.component].filter(Boolean).join(' → '),Tipo:r.recordType,Insight:r.insight,Evidencia:r.evidence,'Posible respuesta UX':r.recommendation,Origen:r.origin,Dispositivo:r.device,'Impacto UX':r.impact,Fuente:r.source},'Detalle del registro')}
function openObject(obj,title){
  const body=Object.entries(obj||{}).filter(([k,v])=>v!==''&&v!=null&&!['id','extraFields'].includes(k)).slice(0,28).map(([k,v])=>'<div class="section"><h4>'+esc(k)+'</h4><p>'+esc(typeof v==='object'?JSON.stringify(v,null,2):v)+'</p></div>').join('');
  $('#drawer-root').innerHTML='<button class="drawer-back" id="drawer-back" aria-label="Cerrar"></button><aside class="drawer"><button class="close" id="drawer-close">✕</button><div class="drawer-head"><div class="eyebrow">Solo consulta</div><h2>'+esc(title)+'</h2></div><div class="drawer-body">'+body+'</div></aside>';
  $('#drawer-back').onclick=$('#drawer-close').onclick=()=>$('#drawer-root').innerHTML='';
}
function csvCell(v){const s=String(v??'').replace(/"/g,'""');return '"'+s+'"'}
function exportCsv(rows,cro){
  const cols=cro?
  [['Iniciativa','initiative'],['Producto','product'],['Funnel','funnel'],['Minifunnel','minifunnel'],['Componente','component'],['Dispositivo','device'],['Insight / hallazgo','insight'],['Evidencia','evidence'],['Posible respuesta UX','recommendation'],['Impacto UX','impact'],['Origen','origin']]:
  [['Iniciativa','initiative'],['Producto','product'],['Funnel','funnel'],['Minifunnel','minifunnel'],['Componente','component'],['Tipo','recordType'],['Insight / hallazgo','insight'],['Evidencia','evidence'],['Posible respuesta UX','recommendation'],['Origen','origin'],['Dispositivo','device'],['Impacto UX','impact'],['Fuente','source']];
  const csv=[cols.map(c=>csvCell(c[0])).join(','),...rows.map(r=>cols.map(c=>csvCell(r[c[1]])).join(','))].join('\n');
  const a=document.createElement('a');a.href=URL.createObjectURL(new Blob(['\ufeff'+csv],{type:'text/csv;charset=utf-8'}));a.download=cro?'ux-intelligence-cro.csv':'ux-intelligence.csv';a.click();setTimeout(()=>URL.revokeObjectURL(a.href),1000);
}
async function boot(){
  try{
    const payload=await decodePayload();initData(payload);renderAll();
    $('#loading').hidden=true;$('#app').hidden=false;
    $$('.nav button[data-page]').forEach(b=>b.onclick=()=>go(b.dataset.page));
    $('#menu').onclick=()=>{$('#sidebar').classList.add('open');$('#backdrop').classList.add('open')};
    $('#backdrop').onclick=()=>{$('#sidebar').classList.remove('open');$('#backdrop').classList.remove('open')};
    $('#global-search').oninput=e=>{state.q=e.target.value;if(state.page==='overview')go('explore');if(state.page==='explore')renderExplore();if(state.page==='learnings')renderLearnings();if(state.page==='documents')renderDocuments()};
  }catch(err){
    $('#loading').hidden=true;const f=$('#fatal');f.hidden=false;f.innerHTML='<strong>No se pudo cargar UX Intelligence.</strong><br>'+esc(err?.message||err);
    console.error(err);
  }
}
boot();
</script>
</body>
</html>'''

(ROOT / "index.html").write_text(html, encoding="utf-8")
print("UX Intelligence demo CRO standalone rebuilt")
print("Dataset rebuilt:", (ROOT / "demo-data.json").stat().st_size, "bytes")
