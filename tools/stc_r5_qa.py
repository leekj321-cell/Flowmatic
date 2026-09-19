"""Static and browser QA for the current Flowmatic Factory OS public homepage."""
from __future__ import annotations
import argparse,json,os,threading
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
RELEASE="2026.09.19-r6.1-value-loop"
LANGS=("ko","en","ar")
OUT=ROOT/"qa-artifacts";OUT.mkdir(exist_ok=True)
REPORT={"release":RELEASE,"checks":[],"limits":["Chromium viewport regression, not physical-device or Safari certification.","Arabic page is technically checked but not native-speaker proofread by this test.","Contact transport is not used to send a real inquiry during QA."]}
def check(name,ok,detail=None):
 REPORT["checks"].append({"name":name,"pass":bool(ok),"detail":detail})
 if not ok:print("FAIL",name,detail,flush=True)
def soup(text):return BeautifulSoup(text,"html.parser")
def static_checks():
 release=json.loads((ROOT/"release.json").read_text(encoding="utf-8"));check("release marker",release.get("release")==RELEASE,release)
 css=ROOT/"stc-lite-home-v1.css";check("homepage stylesheet exists",css.exists() and css.stat().st_size>1000)
 css_text=css.read_text(encoding="utf-8")
 check("value-loop stylesheet",all(x in css_text for x in (".stc-value-loop{","@keyframes stcValueFlow","@media(prefers-reduced-motion:reduce)")))
 ids=("hero","proof","journey","stack","progressive","outputs","loop","pilot","company","contact")
 for lang in LANGS:
  doc=soup((ROOT/lang/"index.html").read_text(encoding="utf-8"));tag=doc.select_one('meta[name="flowmatic-release"]')
  check(f"{lang}: release marker",bool(tag and tag.get("content")==RELEASE))
  check(f"{lang}: language",doc.html.get("lang")==lang)
  check(f"{lang}: one H1",len(doc.select("h1"))==1)
  check(f"{lang}: six nav items",len(doc.select(".site-nav a"))==6)
  check(f"{lang}: Factory OS title","Factory OS" in (doc.title.get_text() if doc.title else ""))
  check(f"{lang}: Factory OS navigation",bool(doc.select_one('#site-nav a[href="#journey"]')) and "Factory OS" in doc.select_one('#site-nav a[href="#journey"]').get_text())
  missing=[i for i in ids if not doc.find(id=i)];check(f"{lang}: complete homepage sequence",not missing,missing)
  raw=(ROOT/lang/"index.html").read_text(encoding="utf-8")
  positions=[raw.find(f'id="{i}"') for i in ids]
  check(f"{lang}: investor-first section order",all(x>=0 for x in positions) and positions==sorted(positions),positions)
  check(f"{lang}: proof immediately after hero",positions[0] < positions[1] < positions[2],positions[:3])
  check(f"{lang}: value loop exists",len(doc.select("#hero .stc-value-loop"))==1)
  check(f"{lang}: six value-loop segments",len(doc.select("#hero .stc-value-segment"))==6)
  check(f"{lang}: six accessible loop stages",len(doc.select("#hero .stc-value-loop-stage .sr-only li"))==6)
  check(f"{lang}: no legacy hero flow nodes",len(doc.select("#hero .stc-flow-node"))==0)
  check(f"{lang}: target loop boundary","TARGET · Factory OS" in doc.select_one("#hero .stc-value-loop-card").get_text(" ",strip=True))
  check(f"{lang}: two headline line spans",len(doc.select("#hero h1 .stc-hero-line"))==2)
  check(f"{lang}: journey eight steps",len(doc.select("#journey .stc-step"))==8)
  check(f"{lang}: two six-layer stacks",len(doc.select("#stack .stc-stack-card"))==2 and len(doc.select("#stack .stc-layer"))==12)
  flow=doc.select_one("#stack .stc-stack-card.flow");check(f"{lang}: L3-L6 core L1-L2 optional",bool(flow and len(flow.select('.stc-layer.core'))==4 and len(flow.select('.stc-layer.optional'))==2))
  check(f"{lang}: progressive bridge",len(doc.select("#progressive .stc-fallback-item"))==10)
  check(f"{lang}: eight deliverables",len(doc.select("#outputs .stc-output"))==8)
  check(f"{lang}: closed loop",len(doc.select("#loop .stc-loop article"))==4)
  check(f"{lang}: two proofs",len(doc.select("#proof .stc-proof"))==2)
  check(f"{lang}: public NC link",bool(doc.select_one(f'#proof a[href="/{lang}/nc/"]')))
  check(f"{lang}: CT video",bool(doc.select_one('#proof video source[src="/flowmatic_ct_demo.mp4"]')))
  text=doc.body.get_text(" ",strip=True)
  check(f"{lang}: current-target-pilot boundary",all(x in text for x in ("CURRENT","TARGET","PILOT")))
  forbidden=("STC-lite","Blueprint R2","L3–L6 CORE","CORE / OPTIONAL","INFERRED","Safety Contract","Full Factory OS target")
  exposed=[x for x in forbidden if x in text];check(f"{lang}: no internal public terms",not exposed,exposed)
  check(f"{lang}: pilot duration","4–8" in text)
  check(f"{lang}: ROI language","ROI" in text)
  check(f"{lang}: six-step pilot",len(doc.select("#pilot .stc-pilot article"))==6)
  check(f"{lang}: user and buyer",len(doc.select("#pilot .stc-audience article"))==2)
  check(f"{lang}: three-step expansion",len(doc.select("#company .stc-expansion article"))==3)
  check(f"{lang}: no unsupported percentage claim",not __import__("re").search(r"\b\d+(?:\.\d+)?\s*%",text))
  check(f"{lang}: ISA disclaimer","ISA-95" in text)
  primary=doc.select_one('#hero .stc-actions a.primary');secondary=doc.select_one('#hero .stc-actions a:not(.primary)')
  check(f"{lang}: primary CTA",bool(primary and primary.get('href')=='#proof'));check(f"{lang}: secondary CTA",bool(secondary and secondary.get('href')=='#contact'))
  check(f"{lang}: direction",doc.html.get('dir')==('rtl' if lang=='ar' else 'ltr'))
 root=(ROOT/'index.html').read_text(encoding='utf-8');r=soup(root);refresh=r.select_one('meta[http-equiv="refresh"]');check("root Factory OS redirect",bool(refresh and '/ko/' in refresh.get('content','') and 'Flowmatic Factory OS' in root))
 for rel in ('ko/nc/index.html','ko/ct/index.html','ko/platform/index.html'):check(f"detail route preserved: {rel}",(ROOT/rel).exists())
def _serve_local():
 handler=lambda *a,**kw:SimpleHTTPRequestHandler(*a,directory=str(ROOT),**kw);server=ThreadingHTTPServer(('127.0.0.1',0),handler);threading.Thread(target=server.serve_forever,daemon=True).start();return server,f"http://127.0.0.1:{server.server_address[1]}"
def browser_checks(base):
 from playwright.sync_api import sync_playwright
 errors=[];http=[];viewports=((360,800),(390,844),(768,1024),(1440,900))
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_PATH'));ctx=browser.new_context(viewport={'width':1440,'height':900},service_workers='block');page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('response',lambda r:http.append((r.status,r.url)) if r.status>=400 else None)
  for lang in LANGS:
   page.goto(base.rstrip('/')+f'/{lang}/',wait_until='domcontentloaded',timeout=45000);page.wait_for_timeout(350)
   check(f"{lang}: served marker",page.locator('meta[name="flowmatic-release"]').get_attribute('content')==RELEASE)
   check(f"{lang}: no internal acronym in visible page",'STC' not in page.locator('body').inner_text())
   check(f"{lang}: no internal acronym in browser title",'STC' not in page.title())
   for w,h in viewports:
    page.set_viewport_size({'width':w,'height':h});page.evaluate("scrollTo({top:0,behavior:'instant'})");page.wait_for_timeout(120);m=page.evaluate('({scroll:document.documentElement.scrollWidth,width:innerWidth})');check(f"{lang}: no overflow {w}",m['scroll']<=w+1,m);check(f"{lang}: H1 visible {w}",page.locator('#hero h1').is_visible());check(f"{lang}: value loop visible {w}",page.locator('#hero .stc-value-loop').is_visible());check(f"{lang}: stack visible {w}",page.locator('#stack .stc-stack-card').count()==2)
    if w==1440:
     lines=page.locator('#hero h1').evaluate("(el)=>{const s=getComputedStyle(el),lh=parseFloat(s.lineHeight),h=el.getBoundingClientRect().height;return {visual:h/lh,height:h,lineHeight:lh}}")
     check(f"{lang}: headline <=3 visual lines",lines['visual']<=3.15,lines)
    if w in (390,1440):page.screenshot(path=str(OUT/f'{lang}-factory-os-{w}.png'),full_page=True)
   page.emulate_media(reduced_motion="reduce");motion=page.locator('#hero .stc-value-flow-dash').evaluate("(el)=>getComputedStyle(el).animationName");check(f"{lang}: reduced motion disables loop animation",motion=="none",motion);page.emulate_media(reduced_motion="no-preference")
   page.locator('#hero a[href="#proof"]').click();check(f"{lang}: primary reaches proof",urlsplit(page.url).fragment=='proof');page.locator('#hero a[href="#contact"]').click();check(f"{lang}: secondary reaches contact",urlsplit(page.url).fragment=='contact')
  browser.close()
 check('no page errors',not errors,errors);relevant=[x for x in http if not any(y in x[1] for y in ('formspree','favicon'))];check('no relevant HTTP errors',not relevant,relevant)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--browser',action='store_true');ap.add_argument('--base',default='');args=ap.parse_args();static_checks();server=None
 try:
  if args.browser:
   if args.base:base=args.base
   else:server,base=_serve_local()
   browser_checks(base)
 finally:
  if server:server.shutdown()
 (OUT/'factory-os-qa.json').write_text(json.dumps(REPORT,ensure_ascii=False,indent=2),encoding='utf-8');fails=[x for x in REPORT['checks'] if not x['pass']];print(f"Factory OS QA: {len(REPORT['checks'])-len(fails)}/{len(REPORT['checks'])} passed");return 1 if fails else 0
if __name__=='__main__':raise SystemExit(main())
