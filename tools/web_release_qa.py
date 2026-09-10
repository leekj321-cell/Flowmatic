"""Executable release evidence. No real inquiry is sent; network and browser failures fail closed."""
import argparse, contextlib, hashlib, io, json, os, re, subprocess, sys, threading, time
from pathlib import Path
from urllib.parse import urlsplit, unquote
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import build_site as site
import web_release_content as wr
SIZES=[(320,568),(360,800),(390,844),(768,1024),(1024,768),(1440,900)]
REPORT={'release':wr.RELEASE,'checks':[],'limits':['Chromium simulated viewports, not physical handsets.','Arabic native-speaker proofreading not performed.','Contact form validation and transport mock tested; no real inquiry or receipt test.']}
OUT=ROOT/'qa-artifacts';OUT.mkdir(exist_ok=True)
def check(name,ok,detail=None):
 REPORT['checks'].append({'name':name,'pass':bool(ok),'detail':detail})
 if not ok: print('FAIL',name,detail,flush=True)
def static_checks():
 files=[ROOT/'index.html']+list(ROOT.glob('*.html'))+list(ROOT.glob('ko/**/*.html'))+list(ROOT.glob('en/**/*.html'))+list(ROOT.glob('ar/**/*.html'))+list(ROOT.glob('html-vnext/*.html'))
 files=sorted(set(files));errors=[];broken=[]
 for f in files:
  s=BeautifulSoup(f.read_text(),'html.parser');lang=s.html.get('lang');rel=str(f.relative_to(ROOT))
  if not s.select_one('meta[name="flowmatic-release"]'):errors.append((rel,'release missing'))
  if lang not in wr.LANGS:errors.append((rel,'locale missing'))
  if len(s.select('.site-nav a'))!=5:errors.append((rel,'navigation'))
  ids=[x['id'] for x in s.select('[id]')]
  if len(ids)!=len(set(ids)):errors.append((rel,'duplicate id'))
  if lang!='ko' and re.search('[가-힣]',s.body.get_text()):errors.append((rel,'Korean language leak'))
  for el in s.select('[href],[src]'):
   value=el.get('href') or el.get('src');u=urlsplit(value)
   if u.scheme or value.startswith('//') or not value:continue
   path=(ROOT/u.path.lstrip('/')) if u.path.startswith('/') else f.parent/u.path
   if not u.path:path=f
   if path.is_dir():path=path/'index.html'
   if not path.exists():broken.append((rel,value))
   elif u.fragment and path.suffix=='.html':
    target=s if path==f else BeautifulSoup(path.read_text(),'html.parser')
    if not target.find(id=unquote(u.fragment)):broken.append((rel,value,'anchor'))
 check('all static pages, locale isolation, navigation and unique IDs',not errors,{'pages':len(files),'errors':errors})
 check('all generated page links and local assets',not broken,{'errors':broken})
 check('approved Korean company definition',wr.TEXT['ko']['intro'] in (ROOT/'ko/index.html').read_text())
 for lang in wr.LANGS:
  h=BeautifulSoup((ROOT/lang/'index.html').read_text(),'html.parser')
  check(f'{lang}: 4 products, 2 demonstrations, 4 pilot steps',len(h.select('#products .wr-product'))==4 and len(h.select('#demos .wr-demo'))==2 and len(h.select('#pilot .wr-card'))==4)
  check(f'{lang}: canonical and hreflang',h.select_one('link[rel="canonical"]')['href']==f'https://flowmatic-os.com/{lang}/' and len(h.select('link[hreflang]'))==4)
  check(f'{lang}: slogan lines preserved',h.select_one('#hero-title').get_text('|')=='Elegant Engineering.|Intelligent Operations.|Flowmatic.')

def browser_checks(base,baseline=None,capture_assets=False):
 from playwright.sync_api import sync_playwright
 from PIL import Image
 errors=[]; responses=[]
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True)
  ctx=browser.new_context(viewport={'width':1440,'height':900},service_workers='block')
  page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('response',lambda r:responses.append((r.status,r.url)) if r.status>=400 else None)
  def go(path):
   page.goto(base+path,wait_until='domcontentloaded',timeout=45000);page.evaluate('document.fonts.ready');page.wait_for_timeout(400)
  if capture_assets:
   dest=ROOT/'media/web-release';dest.mkdir(exist_ok=True,parents=True)
   for lang in wr.LANGS:
    go(f'/{lang}/nc/');page.wait_for_function("document.querySelector('[data-nc-demo-lite]').ncViewerScene?.tools.length === 3",timeout=20000)
    page.locator('[data-viewer-canvas]').wait_for();page.wait_for_timeout(400)
    raw=page.locator('[data-nc-viewer]').screenshot(style='.site-header{visibility:hidden!important}')
    im=Image.open(io.BytesIO(raw)).convert('RGB');im.thumbnail((960,600))
    canvas=Image.new('RGB',(960,600),(16,24,32));canvas.paste(im,((960-im.width)//2,(600-im.height)//2));canvas.save(dest/f'nc-{lang}.webp',quality=90)
   subprocess.run(['ffmpeg','-y','-ss','8','-i',str(ROOT/'flowmatic_ct_demo.mp4'),'-frames:v','1','-vf','scale=960:600:force_original_aspect_ratio=decrease,pad=960:600:(ow-iw)/2:(oh-ih)/2','-c:v','libwebp',str(dest/'ct-program.webp')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
   check('real synthetic NC and existing CT media previews captured',True)
  for lang in wr.LANGS:
   go(f'/{lang}/nc/')
   page.wait_for_function("document.querySelector('[data-nc-demo-lite]').ncViewerScene?.tools.length === 3",timeout=20000)
   scene=page.locator('[data-nc-demo-lite]').evaluate('(el)=>({tools:el.ncViewerScene.tools.length,segments:el.ncViewerScene.segmentCount})')
   check(f'{lang}: automatic synthetic sample',scene['tools']==3 and scene['segments']>0,scene)
   a=page.locator('[data-viewer-canvas]').screenshot();page.locator('[data-viewer-next]').click();page.wait_for_timeout(100);b=page.locator('[data-viewer-canvas]').screenshot()
   check(f'{lang}: next tool changes rendered canvas',a!=b)
   page.locator('[data-viewer-canvas]').focus();page.keyboard.press('ArrowLeft');page.wait_for_timeout(100);c=page.locator('[data-viewer-canvas]').screenshot();check(f'{lang}: keyboard orbit changes canvas',b!=c)
   page.locator('[data-viewer-zoom-in]').click();page.wait_for_timeout(100);d=page.locator('[data-viewer-canvas]').screenshot();check(f'{lang}: zoom changes canvas',c!=d)
   page.locator('[data-nc-reset]').click();check(f'{lang}: reset stays empty',page.locator('[data-nc-demo-lite]').evaluate('(el)=>el.ncViewerScene===null'))
   page.locator('[data-nc-sample]').click();page.wait_for_function("document.querySelector('[data-nc-demo-lite]').ncViewerScene?.tools.length === 3")
   # Upload is browser-local; assert no POST requests are emitted.
   posts=[];ctx.on('request',lambda r: posts.append(r.url) if r.method=='POST' else None)
   page.locator('[data-nc-file]').set_input_files({'name':'public-local-test.nc','mimeType':'text/plain','buffer':b'G21 G90\nT1 M6\nG0 X0 Y0 Z5\nG1 X20 Y0 Z0 F100\nM30\n'})
   page.wait_for_function("document.querySelector('[data-nc-demo-lite]').ncViewerScene?.tools.length === 1")
   check(f'{lang}: local file analysis sends no POST',not posts)
   go(f'/{lang}/')
   page.locator('.hero-actions a.primary').click();check(f'{lang}: official home CTA opens same-locale NC',urlsplit(page.url).path==f'/{lang}/nc/')
   page.locator('[data-lang-link="en"]').click();check(f'{lang}: language switch retains NC context',urlsplit(page.url).path=='/en/nc/')
   # All canonical marketing/product pages across the six approved sizes.
   for slug in ['home']+list(site.PRODUCTS)+list(site.FACTORY_OS_PAGES):
    path=f'/{lang}/'+('' if slug=='home' else slug+'/');go(path)
    for w,h in SIZES:
     page.set_viewport_size({'width':w,'height':h});page.evaluate("window.scrollTo({top:0,behavior:'instant'})");page.wait_for_timeout(90)
     box=page.evaluate('({scroll:document.documentElement.scrollWidth, viewport:innerWidth})')
     check(f'{lang}/{slug}: no horizontal overflow {w}x{h}',box['scroll']<=w+1,box)
     if slug=='home':
      if w in (320,390,1440):page.screenshot(path=str(OUT/f'{lang}-home-{w}.png'))
      cta=page.locator('.hero-actions a.primary').bounding_box();check(f'{lang}: immediate first-screen CTA {w}x{h}',cta is not None and cta['y']+cta['height']<=h+1,cta)
     if slug in ('nc','platform','machining-intelligence','quality','operations-intelligence') and w in (390,1440):
      page.screenshot(path=str(OUT/f'{lang}-{slug}-{w}.png'))
   # Reversible assembly stages and same structural counts as baseline.
   for w,h in [(390,844),(1440,900)]:
    page.set_viewport_size({'width':w,'height':h});go(f'/{lang}/')
    root=page.locator('[data-composition-motion]');counts=root.evaluate("el=>[el.querySelectorAll('[data-token-kind=context]').length,el.querySelectorAll('[data-token-kind=engine]').length,el.querySelectorAll('[data-motion-module]').length,el.querySelectorAll('[data-motion-axis]').length]")
    check(f'{lang}: assembly counts {w}',counts==[10,12,12,4],counts)
    states=[]
    for progress in [0,.38,.68,1,0]:
     root.evaluate("(el,p)=>window.scrollTo({top:window.scrollY+el.getBoundingClientRect().top+Math.max(0,el.getBoundingClientRect().height-innerHeight)*p,behavior:\"instant\"})",progress);page.wait_for_timeout(180)
     states.append(root.get_attribute('data-composition-state'))
     if progress in [0,1]:page.screenshot(path=str(OUT/f'{lang}-assembly-{w}-{int(progress)}.png'))
    check(f'{lang}: reversible assembly {w}',len(set(states))>=3 and states[0]==states[-1],states)
    pause=root.locator('[data-motion-pause]')
    if w>900:
     pause.click();check(f'{lang}: animation pause {w}',pause.get_attribute('aria-pressed')=='true');pause.click()
    else:check(f'{lang}: compact animation omits disabled drift control',pause.is_hidden() and pause.is_disabled())
   page.set_viewport_size({'width':390,'height':844});go(f'/{lang}/operations-intelligence/');check(f'{lang}: Operations animation present',page.locator('[data-field-story]').count()==1)
   page.locator('[data-field-story]').scroll_into_view_if_needed();x=page.locator('[data-field-story]').screenshot();page.wait_for_timeout(650);y=page.locator('[data-field-story]').screenshot();check(f'{lang}: Operations animation advances',x!=y)
   # Responsive menu + non-delivery contact validation.
   go(f'/{lang}/');page.locator('[data-nav-toggle]').click();check(f'{lang}: mobile navigation opens',page.locator('[data-nav-toggle]').get_attribute('aria-expanded')=='true');page.locator('[data-nav-toggle]').click()
   form=page.locator('[data-contact-form]');form.scroll_into_view_if_needed();form.locator('button[type=submit]').click();check(f'{lang}: blank contact form blocked',bool(page.locator('[data-contact-form-status]').inner_text().strip()))
   ctx.route('https://formspree.io/**',lambda r:r.fulfill(status=200,content_type='application/json',body='{"ok":true}'))
   for key,val in [('organization','Release QA (mock only)'),('name','Release QA'),('reply','qa@example.invalid')]:form.locator(f'[name={key}]').fill(val)
   form.locator('[name=brief]').fill('Transport is mocked. No inquiry sent.');form.locator('button[type=submit]').click();page.wait_for_timeout(100)
   check(f'{lang}: contact success handler (mock only)',site.CONTACT_FORM[lang]['sent'] in page.locator('[data-contact-form-status]').inner_text())
   ctx.unroute('https://formspree.io/**')
  for lang in wr.LANGS:
   reduced=browser.new_context(viewport={'width':390,'height':844},reduced_motion='reduce');rp=reduced.new_page();rp.goto(base+f'/{lang}/',wait_until='domcontentloaded');rp.wait_for_timeout(500);check(f'{lang}: reduced motion retains 4 domains',rp.locator('.composition-motion__fallback-axis').count()==4 and rp.locator('.composition-motion__fallback-axis').first.is_visible());rp.locator('[data-composition-motion]').scroll_into_view_if_needed();rp.screenshot(path=str(OUT/f'{lang}-reduced-motion.png'));reduced.close()
  check('browser uncaught exceptions',not errors,errors)
  check('HTTP errors during browser tests',not responses,responses)
  browser.close()

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--browser',action='store_true');ap.add_argument('--base');ap.add_argument('--capture-assets',action='store_true');args=ap.parse_args()
 if args.browser:
  server=None
  if not args.base:
   class Quiet(SimpleHTTPRequestHandler):
    def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
    def log_message(self,*a):pass
   server=ThreadingHTTPServer(('127.0.0.1',8877),Quiet);threading.Thread(target=server.serve_forever,daemon=True).start()
  try:browser_checks(args.base or 'http://127.0.0.1:8877',capture_assets=args.capture_assets)
  except Exception as exc:check('browser suite execution',False,str(exc))
  finally:
   if server:server.shutdown()
 static_checks()
 REPORT['passed']=sum(c['pass'] for c in REPORT['checks']);REPORT['failed']=sum(not c['pass'] for c in REPORT['checks'])
 (OUT/'report.json').write_text(json.dumps(REPORT,ensure_ascii=False,indent=2))
 print(json.dumps({k:REPORT[k] for k in ('release','passed','failed')},ensure_ascii=False),flush=True)
 return 1 if REPORT['failed'] else 0
if __name__=='__main__':sys.exit(main())
