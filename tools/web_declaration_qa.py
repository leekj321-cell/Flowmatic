"""Fixed declaration + runtime regression. No tests are generated from website copy."""
import argparse, json, os, re, subprocess, sys, threading
from pathlib import Path
from urllib.parse import urlsplit, unquote
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from bs4 import BeautifulSoup
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
EXPECTED=['Elegant Engineering.','Intelligent Operations.','Flowmatic.']
RELEASE='2026.09.10-r3'
LANGS=['ko','en','ar']
SIZES=[(320,568),(360,800),(390,844),(768,1024),(1024,768),(1440,900)]
R2='ebe68b65290e356ffb9f739f83c4c28eb811a059'
R1='34faae11f9c63ecb031f0a727473c738b939d8fc'
OUT=ROOT/'qa-artifacts';OUT.mkdir(exist_ok=True)
REPORT={'release':RELEASE,'checks':[],'limits':['Author review and technical regression, not independent Strategy Office approval.','Chromium viewport tests, not physical handsets or Safari.','No Arabic native-speaker proofreading.','Contact transport is mocked; no real inquiry sent or receipt tested.']}
def check(name,ok,detail=None):
    REPORT['checks'].append({'name':name,'pass':bool(ok),'detail':detail})
    if not ok: print('FAIL',name,detail,flush=True)
def soup(text):return BeautifulSoup(text,'html.parser')
def original_contract(doc):
    h=doc.select_one('main #hero h1#hero-title')
    return bool(h and h.get_text('|')=='|'.join(EXPECTED))
def static_checks():
    import build_site as site
    policy=json.loads((ROOT/'homepage-declaration.json').read_text())
    check('locked canonical declaration equals owner-approved original',policy['lines']==EXPECTED and policy['approved_reference_commit']==R1)
    installer=(ROOT/'tools/apply_business_narrative.py').read_text()
    check('build installer cannot rewrite validators','write_text' not in installer and 'web_business_qa' not in installer and 'replace(' not in installer)
    files=sorted(set(list(ROOT.glob('*.html'))+list(ROOT.glob('ko/**/*.html'))+list(ROOT.glob('en/**/*.html'))+list(ROOT.glob('ar/**/*.html'))+list(ROOT.glob('html-vnext/*.html'))))
    broken=[];invalid=[];ownership=[]
    for f in files:
        doc=soup(f.read_text());rel=str(f.relative_to(ROOT));lang=doc.html.get('lang');tag=doc.select_one('meta[name="flowmatic-release"]')
        if not tag or tag.get('content')!=RELEASE:invalid.append((rel,'release'))
        ids=[x['id'] for x in doc.select('[id]')]
        if len(ids)!=len(set(ids)) or lang not in LANGS or len(doc.select('.site-nav a'))!=5:invalid.append((rel,'document contract'))
        if lang!='ko' and re.search('[가-힣]',doc.body.get_text()):invalid.append((rel,'locale leak'))
        if doc.select_one('#hero') and not original_contract(doc):invalid.append((rel,'WEB-019 compatibility entry'))
        if doc.select('[data-field-story]') and not ('operations-intelligence' in rel and len(doc.select('#operations-flow [data-field-story]'))==1):ownership.append(rel)
        for el in doc.select('[href],[src]'):
            value=el.get('href') or el.get('src');u=urlsplit(value)
            if not value or u.scheme or value.startswith('//'):continue
            path=(ROOT/u.path.lstrip('/')) if u.path.startswith('/') else f.parent/u.path
            if not u.path:path=f
            if path.is_dir():path=path/'index.html'
            if not path.exists():broken.append((rel,value))
            elif u.fragment and path.suffix=='.html':
                target=doc if path==f else soup(path.read_text())
                if not target.find(id=unquote(u.fragment)):broken.append((rel,value,'anchor'))
    check('all generated pages: release, language, navigation, IDs and declaration',not invalid,{'pages':len(files),'errors':invalid})
    check('all generated page links and local assets',not broken,broken)
    check('WEB-020 / RT-023 Operations-only animation ownership',not ownership,ownership)
    for lang in LANGS:
        doc=soup((ROOT/lang/'index.html').read_text());h=doc.select_one('#hero-title')
        check(lang+': original H1 exact three-line assertion',original_contract(doc))
        check(lang+': primary English declaration, not fallback paragraph',h.get('lang')=='en' and h.get('dir')=='ltr' and h.get('data-brand-contract')=='WEB-019' and len(doc.select('h1'))==1 and not doc.select('#brand-slogan'))
        order=[n.get('id') for n in doc.select('main [id]')];anchors=['hero','field-problem','workflow','products','demos','capability','preprocessing','architecture','growth','pilot','company','contact']
        check(lang+': approved post-declaration business sequence',all(a in order for a in anchors) and [order.index(a) for a in anchors]==sorted(order.index(a) for a in anchors))
        check(lang+': no NC-first CTA',doc.select_one('.hero-actions a.primary')['href']=='#products' and not doc.select('#hero a[href$="/nc/"]'))
        check(lang+': product and demo composition preserved',len(doc.select('#products .wr-product'))==4 and len(doc.select('#demos .wr-demo'))==2)
        check(lang+': home and platform do not duplicate Operations animation',not doc.select('[data-field-story]') and not soup((ROOT/lang/'platform/index.html').read_text()).select('[data-field-story]'))
        check(lang+': Operations contains original four-stage animation',len(soup((ROOT/lang/'operations-intelligence/index.html').read_text()).select('#operations-flow [data-story-stage]'))==4)
        for bad in ['<p id="hero-title">'+' '.join(EXPECTED)+'</p>','<h1 id="hero-title">'+' '.join(EXPECTED)+'</h1>','<h1 id="hero-title"><span>elegant Engineering.</span><span>Intelligent Operations.</span><span>Flowmatic.</span></h1>']:
            check(lang+': negative contract rejects demotion, line merge or case change',not original_contract(soup('<main><section id="hero">'+bad+'</section></main>')))
        for ref,want,label in [(R1,True,'approved r1'),(R2,False,'rejected r2')]:
            raw=subprocess.check_output(['git','show',ref+':'+lang+'/index.html']).decode()
            check(lang+': unchanged original assertion on '+label,original_contract(soup(raw))==want)
    check('approved Korean company definition retained','제조 현장의 기존 설비와 데이터를 활용해, 사람에 의존하던 생산·품질·관리 업무를 시스템화하는 제조 AI 플랫폼.' in (ROOT/'ko/index.html').read_text())

def browser_checks(base):
    from playwright.sync_api import sync_playwright
    import build_site as site
    errors=[];http=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_PATH'))
        ctx=browser.new_context(viewport={'width':1440,'height':900},service_workers='block');page=ctx.new_page()
        page.on('pageerror',lambda e:errors.append(str(e)));page.on('response',lambda r:http.append((r.status,r.url)) if r.status>=400 else None)
        def go(path):
            page.goto(base+path,wait_until='domcontentloaded',timeout=45000);page.evaluate('document.fonts.ready');page.wait_for_timeout(400)
            check('served r3 '+path,page.locator('meta[name="flowmatic-release"]').get_attribute('content')==RELEASE)
        for lang in LANGS:
            for slug in ['home']+list(site.PRODUCTS)+list(site.FACTORY_OS_PAGES):
                go('/'+lang+'/'+('' if slug=='home' else slug+'/'))
                for w,h in SIZES:
                    page.set_viewport_size({'width':w,'height':h});page.evaluate("scrollTo({top:0,behavior:'instant'})");page.wait_for_timeout(180)
                    bounds=page.evaluate('({scroll:document.documentElement.scrollWidth,width:innerWidth})')
                    check(f'{lang}/{slug}: no horizontal overflow {w}',bounds['scroll']<=w+1,bounds)
                    clipped=page.locator('h1,h2,h3,.brand-hero-title .copy-line').evaluate_all("els=>els.filter(e=>e.clientWidth>0&&getComputedStyle(e).display!=='none'&&e.scrollWidth>e.clientWidth+2).map(e=>e.textContent.slice(0,90))")
                    check(f'{lang}/{slug}: headings not clipped {w}',not clipped,clipped)
                    if slug=='home':
                        metrics=page.locator('#hero-title').evaluate("el=>{const s=getComputedStyle(el),r=el.getBoundingClientRect(),ls=[...el.querySelectorAll('.copy-line')].map(n=>{const q=n.getBoundingClientRect();const range=document.createRange();range.selectNodeContents(n);return {text:n.textContent,y:q.y,bottom:q.bottom,rects:range.getClientRects().length}});return {font:parseFloat(s.fontSize),weight:parseInt(s.fontWeight),display:s.display,visibility:s.visibility,opacity:s.opacity,direction:s.direction,align:s.textAlign,top:r.top,bottom:r.bottom,header:document.querySelector('.site-header').getBoundingClientRect().bottom,lines:ls,viewport:innerHeight}}")
                        visible=metrics['display']!='none' and metrics['visibility']=='visible' and float(metrics['opacity'])>0 and metrics['top']>=metrics['header']-1 and metrics['bottom']<=h+1
                        check(f'{lang}: WEB-019 first-screen primary hierarchy {w}',visible and metrics['font']>=23 and metrics['weight']>=800 and metrics['direction']=='ltr' and metrics['align']=='left',metrics)
                        check(f'{lang}: exactly three rendered declaration lines {w}',[x['text'] for x in metrics['lines']]==EXPECTED and len(set(round(x['y'],1) for x in metrics['lines']))==3 and all(x['rects']==1 for x in metrics['lines']),metrics['lines'])
                        if w in [320,390,1440]:page.screenshot(path=str(OUT/f'{lang}-home-{w}.png'))
                    if slug in ['nc','operations-intelligence'] and w in [390,1440]:page.screenshot(path=str(OUT/f'{lang}-{slug}-{w}.png'))
            for w,h in [(390,844),(1440,900)]:
                page.set_viewport_size({'width':w,'height':h});go('/'+lang+'/');root=page.locator('[data-composition-motion]')
                counts=root.evaluate("el=>[el.querySelectorAll('[data-token-kind=context]').length,el.querySelectorAll('[data-token-kind=engine]').length,el.querySelectorAll('[data-motion-module]').length,el.querySelectorAll('[data-motion-axis]').length]")
                check(f'{lang}: assembly counts {w}',counts==[10,12,12,4],counts);states=[]
                for progress in [0,.38,.68,1,0]:
                    root.evaluate("(el,p)=>scrollTo({top:scrollY+el.getBoundingClientRect().top+Math.max(0,el.getBoundingClientRect().height-innerHeight)*p,behavior:'instant'})",progress);page.wait_for_timeout(180);states.append(root.get_attribute('data-composition-state'))
                    if progress in [0,1]:page.screenshot(path=str(OUT/f'{lang}-assembly-{w}-{int(progress)}.png'))
                check(f'{lang}: assembly forward and reverse {w}',len(set(states))>=3 and states[0]==states[-1],states)
                pause=root.locator('[data-motion-pause]')
                if w>900:pause.click();check(lang+': assembly pause',pause.get_attribute('aria-pressed')=='true');pause.click()
                else:check(lang+': compact drift control',pause.is_hidden() and pause.is_disabled())
                go('/'+lang+'/operations-intelligence/');anim=page.locator('#operations-flow [data-field-story]');check(lang+': Operations animation single instance',anim.count()==1)
                anim.scroll_into_view_if_needed();a=anim.screenshot();page.wait_for_timeout(650);b=anim.screenshot();check(f'{lang}: Operations animation advances {w}',a!=b)
                page.locator('#operations-flow').screenshot(path=str(OUT/f'{lang}-operations-flow-{w}.png'),style='.site-header{visibility:hidden!important}')
            page.set_viewport_size({'width':390,'height':844});go('/'+lang+'/nc/')
            page.wait_for_function("document.querySelector('[data-nc-demo-lite]').ncViewerScene?.tools.length===3",timeout=20000)
            scene=page.locator('[data-nc-demo-lite]').evaluate('(el)=>({tools:el.ncViewerScene.tools.length,segments:el.ncViewerScene.segmentCount})');check(lang+': synthetic NC auto sample',scene['tools']==3 and scene['segments']>0,scene)
            canvas=page.locator('[data-viewer-canvas]');a=canvas.screenshot();page.locator('[data-viewer-next]').click();page.wait_for_timeout(150);b=canvas.screenshot();check(lang+': NC tool change',a!=b)
            canvas.focus();page.keyboard.press('ArrowLeft');page.wait_for_timeout(150);c=canvas.screenshot();check(lang+': NC keyboard orbit',b!=c)
            page.locator('[data-viewer-zoom-in]').click();page.wait_for_timeout(150);d=canvas.screenshot();check(lang+': NC zoom',c!=d)
            page.locator('[data-nc-reset]').click();check(lang+': NC reset',page.locator('[data-nc-demo-lite]').evaluate('(el)=>el.ncViewerScene===null'))
            page.locator('[data-nc-sample]').click();page.wait_for_function("document.querySelector('[data-nc-demo-lite]').ncViewerScene?.tools.length===3")
            posts=[]
            def track(r):
                if r.method=='POST':posts.append(r.url)
            ctx.on('request',track)
            page.locator('[data-nc-file]').set_input_files({'name':'public-local-test.nc','mimeType':'text/plain','buffer':b'G21 G90\nT1 M6\nG0 X0 Y0 Z5\nG1 X20 Y0 Z0 F100\nM30\n'})
            page.wait_for_function("document.querySelector('[data-nc-demo-lite]').ncViewerScene?.tools.length===1");check(lang+': local NC file sends no POST',not posts);ctx.remove_listener('request',track)
            go('/'+lang+'/');page.locator('.hero-actions a.primary').click();check(lang+': hero leads to products',urlsplit(page.url).fragment=='products');page.locator('#demos a.fm-button').first.click();check(lang+': contextual demo correct locale',urlsplit(page.url).path=='/'+lang+'/nc/')
            page.locator('[data-lang-link="en"]').click();check(lang+': language switch retains NC context',urlsplit(page.url).path=='/en/nc/')
            go('/'+lang+'/');video=page.locator('#demos video');video.scroll_into_view_if_needed();video.evaluate('(v)=>{v.muted=true;return v.play()}');page.wait_for_timeout(750)
            playback=video.evaluate('(v)=>({time:v.currentTime,paused:v.paused,error:v.error?.code||null})');check(lang+': CT recording actually plays',playback['time']>0 and not playback['paused'] and playback['error'] is None,playback);video.evaluate('(v)=>v.pause()')
            page.locator('#workflow').screenshot(path=str(OUT/f'{lang}-workflow-390.png'),style='.site-header{visibility:hidden!important}')
            page.locator('[data-nav-toggle]').click();check(lang+': mobile navigation opens',page.locator('[data-nav-toggle]').get_attribute('aria-expanded')=='true');page.locator('[data-nav-toggle]').click()
            form=page.locator('[data-contact-form]');form.scroll_into_view_if_needed();form.locator('button[type=submit]').click();check(lang+': blank contact blocked',bool(page.locator('[data-contact-form-status]').inner_text().strip()))
            ctx.route('https://formspree.io/**',lambda r:r.fulfill(status=200,content_type='application/json',body='{"ok":true}'))
            for key,val in [('organization','Release QA (mock only)'),('name','Release QA'),('reply','qa@example.invalid')]:form.locator('[name='+key+']').fill(val)
            form.locator('[name=brief]').fill('Mock transport. No inquiry sent.');form.locator('button[type=submit]').click();page.wait_for_timeout(100);check(lang+': contact mock success',site.CONTACT_FORM[lang]['sent'] in page.locator('[data-contact-form-status]').inner_text());ctx.unroute('https://formspree.io/**')
            reduced=browser.new_context(viewport={'width':390,'height':844},reduced_motion='reduce');rp=reduced.new_page();rp.goto(base+'/'+lang+'/',wait_until='domcontentloaded');rp.wait_for_timeout(500)
            check(lang+': reduced motion retains four domains',rp.locator('.composition-motion__fallback-axis').count()==4 and rp.locator('.composition-motion__fallback-axis').first.is_visible());reduced.close()
        check('browser uncaught exceptions',not errors,errors);check('HTTP errors',not http,http);browser.close()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--browser',action='store_true');ap.add_argument('--base');args=ap.parse_args();server=None
    try:
        static_checks()
        if args.browser:
            if not args.base:
                class Quiet(SimpleHTTPRequestHandler):
                    def __init__(self,*a,**kw):super().__init__(*a,directory=str(ROOT),**kw)
                    def log_message(self,*a):pass
                server=ThreadingHTTPServer(('127.0.0.1',8877),Quiet);threading.Thread(target=server.serve_forever,daemon=True).start()
            browser_checks(args.base or 'http://127.0.0.1:8877')
    except Exception as exc:check('suite execution',False,repr(exc))
    finally:
        if server:server.shutdown()
    REPORT['passed']=sum(c['pass'] for c in REPORT['checks']);REPORT['failed']=sum(not c['pass'] for c in REPORT['checks'])
    (OUT/'report.json').write_text(json.dumps(REPORT,ensure_ascii=False,indent=2));print(json.dumps({k:REPORT[k] for k in ['release','passed','failed']}),flush=True)
    return 1 if REPORT['failed'] else 0
if __name__=='__main__':raise SystemExit(main())
