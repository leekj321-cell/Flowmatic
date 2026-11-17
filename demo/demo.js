const $=id=>document.getElementById(id);
const API="https://udkaqfqvptszlfjkmtrg.supabase.co/functions/v1/flowmatic-demo-planner";
const SUPA="https://udkaqfqvptszlfjkmtrg.supabase.co";
const KEY="sb_publishable_lnD7_RrBoKQDiJIK9htHpA_Fyfl_eUF";
let auth=null,plan=null,raf=0,lastFrame=0,sim=null;
const fmt=n=>Number(n).toLocaleString("en-US"),round=n=>Math.round(n*10)/10;
function message(text,error=false){$("status").textContent=text;$("status").className="status"+(error?" error":"");}
function escapeHtml(s){return String(s).replace(/[&<>"']/g,x=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[x]));}
async function authFetch(path,opts={}){return fetch(SUPA+path,{...opts,headers:{apikey:KEY,"Content-Type":"application/json",...(opts.headers||{})}});}
function getToken(){return sessionStorage.getItem("fm-demo-token");}
function setAuth(a){auth=a;$("authState").textContent=a?.user?.email?"Signed in: "+a.user.email:"Public evaluation";$("signOut").disabled=!a;$("sendOtp").disabled=!!a;}
async function restoreAuth(){
 const hash=new URLSearchParams(location.hash.slice(1)),at=hash.get("access_token"),rt=hash.get("refresh_token");
 if(at&&rt){sessionStorage.setItem("fm-demo-token",at);sessionStorage.setItem("fm-demo-refresh",rt);history.replaceState({},document.title,location.pathname);}
 const token=getToken();if(!token)return;
 try{const r=await authFetch("/auth/v1/user",{headers:{Authorization:"Bearer "+token}});if(!r.ok)throw Error();const user=await r.json();setAuth({user});}
 catch{sessionStorage.removeItem("fm-demo-token");sessionStorage.removeItem("fm-demo-refresh");setAuth(null);}
}
$("sendOtp").onclick=async()=>{
 const email=$("emailInput").value.trim();
 if(!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)){message("Enter a valid email address.",true);return;}
 $("sendOtp").disabled=true;message("Requesting a one-time sign-in code…");
 try{const r=await authFetch("/auth/v1/otp",{method:"POST",body:JSON.stringify({email,create_user:true})});
  const data=await r.json().catch(()=>({}));if(!r.ok)throw Error(data.msg||data.error_description||"Email login unavailable");
  $("otpRow").style.display="block";$("verifyOtp").style.display="inline-block";message("Check your email for the sign-in code. No password is required.");
 }catch(e){message(e.message,true);}finally{if(!auth)$("sendOtp").disabled=false;}
};
$("verifyOtp").onclick=async()=>{
 const email=$("emailInput").value.trim(),token=$("otpInput").value.trim();
 if(!email||!token){message("Enter email and verification code.",true);return;}
 $("verifyOtp").disabled=true;
 try{const r=await authFetch("/auth/v1/verify",{method:"POST",body:JSON.stringify({email,token,type:"email"})});
  const data=await r.json();if(!r.ok||!data.access_token)throw Error(data.msg||data.error_description||"Invalid or expired code");
  sessionStorage.setItem("fm-demo-token",data.access_token);if(data.refresh_token)sessionStorage.setItem("fm-demo-refresh",data.refresh_token);
  setAuth({user:data.user});message("Signed in. You may now analyze your own STEP files.");
 }catch(e){message(e.message,true);}finally{$("verifyOtp").disabled=false;}
};
$("signOut").onclick=()=>{sessionStorage.removeItem("fm-demo-token");sessionStorage.removeItem("fm-demo-refresh");setAuth(null);message("Signed out. Public sample remains available.");};
async function request(action,extra={}){
 const headers={"Content-Type":"application/json","apikey":KEY};
 if(action==="plan"&&getToken())headers.Authorization="Bearer "+getToken();
 const r=await fetch(API,{method:"POST",headers,body:JSON.stringify({action,annualVolume:+$("volume").value,options:{material:$("material").value,days:+$("days").value,shifts:+$("shifts").value,oee:+$("oee").value},...extra})});
 const data=await r.json();if(!r.ok||!data.ok)throw Error(data.error||"Planner request failed");
 return data;
}
function runButton(disabled){$("sampleBtn").disabled=disabled;$("planBtn").disabled=disabled;}
$("sampleBtn").onclick=async()=>{runButton(true);message("Generating a sample production plan…");try{const data=await request("sample");load(data.plan);message("Sample plan generated from STEP geometry. Change annual demand and run again to recalculate.");}catch(e){message(e.message,true);}finally{runButton(false);}};
$("planBtn").onclick=async()=>{
 const a=$("stockFile").files[0],b=$("productFile").files[0];
 if(!a||!b){message("Select both stock and finished product STEP files.",true);return;}
 if(a.size>330000||b.size>330000){message("Public evaluation limit: 330 KB per STEP file.",true);return;}
 if(!auth){message("Sign in with Google before analyzing your own STEP files. You can run the public sample without sign-in.",true);return;}
 runButton(true);message("Parsing STEP geometry and calculating the plan…");
 try{const data=await request("plan",{stockStep:await a.text(),productStep:await b.text()});load(data.plan);message("STEP geometry analyzed. Review estimates and engineering caveats before use.");}
 catch(e){message(e.message,true);}finally{runButton(false);}
};
function load(p){plan=p;stop();$("metricCt").textContent=fmt(p.metrics.estimatedCT);$("metricCapacity").textContent=fmt(p.metrics.estimatedCapacity);$("metricMachines").textContent=fmt(p.metrics.machineCount);$("metricTravel").textContent=p.toolpath.travelReductionPct+"%";
 $("operations").innerHTML=p.operations.map(o=>'<div class="op"><b>'+escapeHtml(o.id)+'</b><div><b>'+escapeHtml(o.name)+'</b><br><small>Annual capacity '+fmt(o.capacityAnnual)+'</small></div><span>'+o.seconds+' s</span><span class="badge">'+o.machines+' CNC</span></div>').join("");
 $("caveats").innerHTML=p.caveats.map(s=>"<p>• "+escapeHtml(s)+"</p>").join("");
 drawPath(p);initializeSimulation(p);$("startBtn").disabled=false;$("pauseBtn").disabled=false;$("resetBtn").disabled=false;$("exportBtn").disabled=false;$("csvBtn").disabled=false;
}
function drawPath(p){
 const b=p.part,ordered=p.toolpath.order,min=b.min,size=b.size;
 const x=v=>35+450*(v-min[0])/Math.max(size[0],1),y=v=>240-200*(v-min[1])/Math.max(size[1],1);
 const poly=ordered.map(q=>x(q.x)+","+y(q.y)).join(" ");
 let svg='<rect width="520" height="280" fill="#f7f9fc"/><rect x="35" y="40" width="450" height="200" fill="#eaf1f9" stroke="#b8c7da"/>';
 if(ordered.length)svg+='<polyline points="'+poly+'" fill="none" stroke="#1565d8" stroke-width="2.5" stroke-dasharray="7 4"/>';
 for(const q of ordered)svg+='<circle cx="'+x(q.x)+'" cy="'+y(q.y)+'" r="'+Math.max(4,Math.min(18,q.diameter/2))+'" fill="#fff" stroke="#1565d8" stroke-width="2"/><text x="'+(x(q.x)+9)+'" y="'+(y(q.y)-9)+'" font-size="11">'+escapeHtml(q.id)+'</text>';
 if(!ordered.length)svg+='<text x="260" y="130" text-anchor="middle" fill="#65768a">No cylindrical-face candidates found</text>';
 $("toolSvg").innerHTML=svg;
 $("pathNote").textContent="Baseline XY travel "+p.toolpath.baselineDistanceMm+" mm → nearest-neighbor candidate "+p.toolpath.candidateDistanceMm+" mm. Cylindrical candidates: "+p.geometry.cylindricalCandidates+". This is NOT validated drilling or production NC.";
}
function drawLayout(){
 if(!sim)return;const nodes=plan.layout.nodes,byId=Object.fromEntries(nodes.map(n=>[n.id,n]));
 let s='<defs><marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#a4b4c7"/></marker></defs><rect width="1050" height="450" fill="#f7f9fc"/>';
 for(const link of plan.layout.links){const a=byId[link.from],b=byId[link.to];s+='<path d="M '+a.x+' '+a.y+' L '+b.x+' '+b.y+'" fill="none" stroke="#a4b4c7" stroke-width="4" stroke-dasharray="8 6" marker-end="url(#arr)"/>';}
 for(const n of nodes){
  const isMachine=n.kind==="machine",w=isMachine?126:95,h=isMachine?70:60;
  const queue=sim.queues[n.id]?.length||0;
  s+='<rect x="'+(n.x-w/2)+'" y="'+(n.y-h/2)+'" width="'+w+'" height="'+h+'" rx="9" fill="'+(isMachine?"#fff":"#dcecfb")+'" stroke="'+(isMachine?"#1565d8":"#90a8c4")+'" stroke-width="2"/>';
  s+='<text x="'+n.x+'" y="'+(n.y-8)+'" font-size="14" text-anchor="middle" font-weight="800">'+escapeHtml(n.id)+'</text>';
  s+='<text x="'+n.x+'" y="'+(n.y+12)+'" font-size="11" text-anchor="middle">'+escapeHtml(n.name.length>17?n.name.slice(0,16)+"…":n.name)+'</text>';
  if(isMachine)s+='<text x="'+n.x+'" y="'+(n.y+28)+'" font-size="11" text-anchor="middle" fill="#627185">'+n.machines+' CNC · queue '+queue+'</text>';
 }
 const drawItem=(item,x,y)=>{s+='<circle cx="'+x+'" cy="'+y+'" r="7" fill="#e53935" stroke="#fff" stroke-width="2"/>';};
 for(const item of sim.items){
  if(item.state==="processing"){const n=byId[item.node];drawItem(item,n.x-43+(item.slot%4)*24,n.y-22);}
  if(item.state==="queued"){const n=byId[item.node];drawItem(item,n.x-30+(item.id%4)*16,n.y+48+Math.floor(item.id%8/4)*15);}
  if(item.state==="moving"){const a=byId[item.from],b=byId[item.to],t=Math.min(1,item.progress);drawItem(item,a.x+(b.x-a.x)*t,a.y+(b.y-a.y)*t);}
 }
 for(const rb of sim.robots){const link=plan.layout.links[rb.linkIndex||0],a=byId[link.from],b=byId[link.to],t=rb.item?rb.item.progress:0;
  const x=a.x+(b.x-a.x)*t,y=a.y+(b.y-a.y)*t;
  s+='<rect x="'+(x-14)+'" y="'+(y-14)+'" width="28" height="28" rx="7" fill="#1565d8" stroke="#fff" stroke-width="2"/><text x="'+x+'" y="'+(y+4)+'" font-size="10" fill="white" text-anchor="middle" font-weight="800">R'+rb.id+'</text>';
 }
 $("factorySvg").innerHTML=s;
}
function initializeSimulation(p){
 const queues={};p.layout.nodes.forEach(n=>queues[n.id]=[]);
 sim={time:0,items:[],queues,robots:[{id:1,item:null,linkIndex:0},{id:2,item:null,linkIndex:1}],running:false,produced:0,nextId:0,spawnAcc:0,
  processSlots:Object.fromEntries(p.operations.map(o=>[o.id,Array(o.machines).fill(null)]))};
 for(let i=0;i<3;i++)spawn();updateStatus();drawLayout();
}
function spawn(){if(sim.items.length>70)return;const id=sim.nextId++;const item={id,node:"RAW",state:"queued",progress:0,remaining:0,slot:0};sim.items.push(item);sim.queues.RAW.push(item);}
function tick(dt){
 sim.time+=dt;const steps=plan.operations,links=plan.layout.links;
 sim.spawnAcc+=dt;const feed=plan.operating.secondsPerMachine/Math.max(1,plan.annualDemand)*plan.layout.machines;
 while(sim.spawnAcc>Math.max(25,feed)&&sim.items.length<65){sim.spawnAcc-=Math.max(25,feed);spawn();}
 for(const op of steps){const slots=sim.processSlots[op.id];for(let k=0;k<slots.length;k++){
  const item=slots[k];if(item){item.remaining-=dt;if(item.remaining<=0){slots[k]=null;item.state="ready";}}
  if(!slots[k]&&sim.queues[op.id].length){const it=sim.queues[op.id].shift();slots[k]=it;it.node=op.id;it.state="processing";it.slot=k;it.remaining=op.seconds;}
 }}
 for(const robot of sim.robots){
  if(robot.item){const item=robot.item;item.progress+=dt/Math.max(7,20+robot.linkIndex*2);
   if(item.progress>=1){item.state=item.to==="DONE"?"complete":"queued";item.node=item.to;item.progress=0;
    if(item.to==="DONE"){sim.produced++;sim.items=sim.items.filter(x=>x!==item);}else sim.queues[item.to].push(item);
    robot.item=null;}}
  if(!robot.item){
   for(let i=0;i<links.length;i++){if(i%2+1!==robot.id)continue;const link=links[i];
    const item=sim.items.find(x=>x.node===link.from&&(x.state==="ready"||(link.from==="RAW"&&x.state==="queued")));
    if(item){if(link.from==="RAW")sim.queues.RAW=sim.queues.RAW.filter(x=>x!==item);
     item.state="moving";item.from=link.from;item.to=link.to;item.progress=0;robot.item=item;robot.linkIndex=i;break;}
   }
  }
 }
}
function updateStatus(){if(!sim)return;const t=Math.floor(sim.time),h=String(Math.floor(t/3600)).padStart(2,"0"),m=String(Math.floor(t%3600/60)).padStart(2,"0"),s=String(t%60).padStart(2,"0");
 $("simClock").textContent=h+":"+m+":"+s;
 $("simStatus").textContent="Produced "+sim.produced+" · WIP "+sim.items.length+" · Virtual time "+Math.floor(sim.time)+" s · Bottleneck "+plan.metrics.bottleneck+(plan.metrics.capacityShortfall?" · Capacity shortfall":"");
}
function frame(ts){if(!sim?.running)return;const elapsed=Math.min((ts-(lastFrame||ts))/1000,.12);lastFrame=ts;
 const scale=+$("speed").value;const substeps=Math.max(1,Math.ceil(elapsed*scale/3));
 for(let i=0;i<substeps;i++)tick(elapsed*scale/substeps);
 drawLayout();updateStatus();raf=requestAnimationFrame(frame);
}
function stop(){if(sim)sim.running=false;cancelAnimationFrame(raf);lastFrame=0;}
$("startBtn").onclick=()=>{if(!sim)return;if(sim.running)return;sim.running=true;lastFrame=0;raf=requestAnimationFrame(frame);};
$("pauseBtn").onclick=()=>stop();
$("resetBtn").onclick=()=>{if(plan){stop();initializeSimulation(plan);}};
$("exportBtn").onclick=()=>{if(plan)download("flowmatic-plan.json",JSON.stringify(plan,null,2),"application/json");};
$("csvBtn").onclick=()=>{if(!plan)return;const rows=[["operation","name","seconds","machines","annual_capacity"],...plan.operations.map(o=>[o.id,o.name,o.seconds,o.machines,o.capacityAnnual])];download("flowmatic-operations.csv",rows.map(x=>x.map(v=>'"'+String(v).replace(/"/g,'""')+'"').join(",")).join("\n"),"text/csv");};
function download(name,content,type){const blob=new Blob([content],{type}),url=URL.createObjectURL(blob),a=document.createElement("a");a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),2000);}
restoreAuth();
