"""Canonical R7 static and browser regression for the approved investor homepage.

Run browser checks in the existing GitHub Actions website QA environment.
No live contact submission is made.
"""
from __future__ import annotations
import argparse, hashlib, json, os, re, threading, sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from bs4 import BeautifulSoup
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from content.investor_home import RELEASE, COPY, IDS, FILES
OUT = ROOT/'qa-artifacts'
OUT.mkdir(exist_ok=True)
REPORT = {'release':RELEASE,'checks':[],'limits':['Chromium viewport regression, not physical-device or Safari certification.','Arabic is checked for equivalent meaning and layout; native-speaker proofreading is not claimed.','No real contact request is submitted.']}
def check(name, ok, detail=None):
    REPORT['checks'].append({'name':name,'pass':bool(ok),'detail':detail})
    if not ok: print('FAIL',name,detail,flush=True)

def static_checks():
    check('release marker',json.loads((ROOT/'release.json').read_text())['release']==RELEASE)
    provenance=json.loads((ROOT/'media/product-20261018/provenance.json').read_text())
    check('four actual product images',len(provenance['assets'])==4)
    for asset in provenance['assets']:
        path=ROOT/'media/product-20261018'/asset['file']
        check('unaltered actual image: '+asset['file'],hashlib.sha256(path.read_bytes()).hexdigest()==asset['sha256'])
    css=(ROOT/'stc-lite-home-v1.css').read_text()
    check('reduced motion and short-viewport fallback',all(s in css for s in ['prefers-reduced-motion:reduce','@media(max-height:610px)','.step-image']))
    for lang in COPY:
        raw=(ROOT/lang/'index.html').read_text()
        doc=BeautifulSoup(raw,'html.parser')
        check(f'{lang}: release marker',doc.select_one('meta[name="flowmatic-release"]').get('content')==RELEASE)
        check(f'{lang}: locale and direction',doc.html.get('lang')==lang and doc.html.get('dir')==('rtl' if lang=='ar' else 'ltr'))
        check(f'{lang}: Factory OS title','Factory OS' in doc.title.text)
        check(f'{lang}: one H1',len(doc.select('h1'))==1)
        ids=['hero','problem','product','value','readiness','stack','adoption','contact']
        pos=[raw.find('id="'+x+'"') for x in ids]
        check(f'{lang}: approved narrative order',min(pos)>=0 and pos==sorted(pos))
        check(f'{lang}: real product hero before architecture',bool(doc.select_one('#hero [data-open-shot="machining"] img')))
        check(f'{lang}: four scroll steps',[x.get('data-step') for x in doc.select('[data-step]')]==IDS)
        check(f'{lang}: optional manual jump links',[x.get('href') for x in doc.select('[data-shot]')]==['#step-'+i for i in IDS])
        shots=json.loads(doc.select_one('#product-evidence').text)
        check(f'{lang}: equivalent evidence identities',[s['id'] for s in shots]==IDS and [s['src'] for s in shots]==['/media/product-20261018/'+x for x in FILES])
        check(f'{lang}: no-JS product images',len(doc.select('.step-image img'))==4)
        check(f'{lang}: public NC and CT links',all(doc.select_one(f'a[href="/{lang}/{route}/"]') for route in ['nc','ct']))
        check(f'{lang}: existing CT video',bool(doc.select_one('video source[src="/flowmatic_ct_demo.mp4"]')))
        check(f'{lang}: claim states',all(x in doc.get_text() for x in ['CURRENT','PILOT','TARGET']))
        check(f'{lang}: six-layer stack',len(doc.select('#stack tbody tr'))==6 and 'ISA-95' in doc.get_text())
        check(f'{lang}: Design Build Run Improve',[x.text.strip() for x in doc.select('.loop-grid h3')]==['DESIGN','BUILD','RUN','IMPROVE'])
        check(f'{lang}: pilot duration and ROI',all(x in doc.get_text() for x in ['4–8','ROI','KPI']))
        check(f'{lang}: six-step pilot and users/buyers',len(doc.select('.adoption-step'))==6 and len(doc.select('.audience article'))==2)
        check(f'{lang}: no internal public labels',not any(x in doc.get_text() for x in ['STC-lite','Blueprint R2','L3–L6 CORE','CORE / OPTIONAL','INFERRED','Safety Contract']))
        percentages=re.findall(r'\d+(?:\.\d+)?\s*%',doc.get_text())
        check(f'{lang}: only documented demo percentage',set(percentages)<= {'30%'},percentages)
        check(f'{lang}: canonical brand asset',doc.select_one('.brand img')['src']=='/assets/branding/canonical/'+('flowmatic-ci-ko-horizontal.png' if lang=='ko' else 'flowmatic-ci-global-horizontal.svg'))
        check(f'{lang}: locale switcher',set(a['href'] for a in doc.select('[data-lang-link]'))=={'/ko/','/en/','/ar/'})
        check(f'{lang}: localized contact form',bool(doc.select_one('form[action="https://formspree.io/f/xojgorkl"]')) and all(doc.find(id='contact-'+x) for x in ['name','email','brief']))
        # All local assets and anchors in generated pages must resolve.
        missing=[]
        for tag in doc.select('[src],a[href],link[rel=stylesheet]'):
            target=tag.get('src') or tag.get('href','')
            if target.startswith('#') and not doc.find(id=target[1:]): missing.append(target)
            if target.startswith('/'):
                path=ROOT/target.split('?',1)[0].split('#',1)[0].lstrip('/')
                if not path.exists(): missing.append(target)
        check(f'{lang}: local links and assets',not missing,missing)
    doc=BeautifulSoup((ROOT/'index.html').read_text(),'html.parser')
    check('root locale redirect','/ko/' in doc.select_one('meta[http-equiv=refresh]')['content'])
    for lang in COPY:
        for route in ['nc','ct','platform']:
            check(f'{lang}: preserved {route} route',(ROOT/lang/route/'index.html').exists())

def serve():
    handler=lambda *a,**kw:SimpleHTTPRequestHandler(*a,directory=str(ROOT),**kw)
    server=ThreadingHTTPServer(('127.0.0.1',0),handler)
    threading.Thread(target=server.serve_forever,daemon=True).start()
    return server,f'http://127.0.0.1:{server.server_address[1]}'

SCROLL_TO_STEP = '''(id) => {
 const panel=document.querySelector('#product-panel');
 const h=document.querySelector('.site-header').offsetHeight;
 const sticky=innerWidth<=820&&getComputedStyle(panel).position==='sticky';
 const bottom=h+10+panel.offsetHeight;
 const line=sticky?Math.min(innerHeight-60,bottom+Math.max(32,(innerHeight-bottom)*.25)):Math.max(h+50,innerHeight*.46);
 const el=document.getElementById('step-'+id);
 scrollTo({top:Math.max(0,scrollY+el.getBoundingClientRect().top-line+24),behavior:'instant'});
}'''

def browser_checks(base):
    from playwright.sync_api import sync_playwright
    errors=[]; http=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_PATH'))
        ctx=browser.new_context(viewport={'width':1440,'height':900},service_workers='block')
        page=ctx.new_page()
        page.on('pageerror',lambda err:errors.append(str(err)))
        page.on('response',lambda response:http.append([response.status,response.url]) if response.status>=400 else None)
        for lang in COPY:
            page.goto(base.rstrip('/')+f'/{lang}/',wait_until='networkidle',timeout=60000)
            check(f'{lang}: served release',page.locator('meta[name="flowmatic-release"]').get_attribute('content')==RELEASE)
            for w,h in [(360,800),(390,844),(768,1024),(1440,900),(1920,1080),(844,390)]:
                page.set_viewport_size({'width':w,'height':h})
                page.evaluate("scrollTo({top:0,behavior:'instant'})")
                page.wait_for_timeout(180)
                metrics=page.evaluate('({width:innerWidth,scroll:document.documentElement.scrollWidth})')
                check(f'{lang} {w}x{h}: no horizontal overflow',metrics['scroll']<=w+1,metrics)
                check(f'{lang} {w}x{h}: canonical CI minimum width',page.locator('.brand img').bounding_box()['width']>=219)
                if w==1440:
                    lines=page.locator('h1').evaluate('(el)=>el.offsetHeight/parseFloat(getComputedStyle(el).lineHeight)')
                    check(f'{lang}: desktop headline within three lines',lines<=3.15,lines)
                if w<=1000:
                    page.locator('#menu-toggle').click()
                    check(f'{lang} {w}: mobile navigation opens',page.locator('#navigation').is_visible())
                    check(f'{lang} {w}: three locale controls',page.locator('#navigation [data-lang-link]:visible').count()==3)
                    page.keyboard.press('Escape')
                    check(f'{lang} {w}: mobile navigation closes',not page.locator('#navigation').is_visible())
                for id in IDS:
                    page.evaluate(SCROLL_TO_STEP,id)
                    page.wait_for_timeout(180)
                    check(f'{lang} {w}x{h}: forward {id}',page.locator('#product-panel').get_attribute('data-active-shot')==id)
                    check(f'{lang} {w}x{h}: image follows {id}',page.locator('.shot-image').get_attribute('src').endswith(FILES[IDS.index(id)]))
                    if h>610:
                        box=page.locator('#product-panel').bounding_box()
                        check(f'{lang} {w}x{h}: product panel readable {id}',box['y']>=-1 and box['y']+box['height']<=h-45,box)
                    if w in [390,1440]:
                        page.screenshot(path=str(OUT/f'{lang}-{w}-step-{id}.png'))
                for id in reversed(IDS):
                    page.evaluate(SCROLL_TO_STEP,id);page.wait_for_timeout(100)
                    check(f'{lang} {w}x{h}: reverse {id}',page.locator('#product-panel').get_attribute('data-active-shot')==id)
                if h<=610:
                    check(f'{lang}: landscape inline evidence fallback',page.locator('.step-image').first.is_visible())
                if w in [390,1440]:
                    page.evaluate("scrollTo({top:0,behavior:'instant'})")
                    page.screenshot(path=str(OUT/f'{lang}-home-{w}.png'),full_page=True)
            # Manual selection aligns the narrative; reduced motion removes the smooth scroll.
            page.set_viewport_size({'width':390,'height':844})
            page.emulate_media(reduced_motion='reduce')
            page.evaluate(SCROLL_TO_STEP,'machining');page.wait_for_timeout(150)
            page.locator('[data-shot=handover]').click();page.wait_for_timeout(150)
            check(f'{lang}: manual step selection',page.locator('#product-panel').get_attribute('data-active-shot')=='handover')
            page.locator('[data-shot=handover]').focus()
            page.keyboard.press('End');page.wait_for_timeout(150)
            check(f'{lang}: keyboard last step',page.locator('#product-panel').get_attribute('data-active-shot')=='operations')
            page.keyboard.press('Home');page.wait_for_timeout(150)
            check(f'{lang}: keyboard first step',page.locator('#product-panel').get_attribute('data-active-shot')=='machining')
            check(f'{lang}: reduced motion',page.evaluate("getComputedStyle(document.documentElement).scrollBehavior")=='auto')
            page.locator('#gallery-open').click()
            check(f'{lang}: real image dialog',page.locator('#image-dialog').is_visible() and page.locator('#dialog-image').get_attribute('src').endswith(FILES[0]))
            page.keyboard.press('Escape');page.wait_for_timeout(100)
            check(f'{lang}: dialog closes and focus returns',not page.locator('#image-dialog').is_visible() and page.locator('#gallery-open').evaluate('(el)=>el===document.activeElement'))
            page.emulate_media(reduced_motion='no-preference')
            page.locator('.stack-detail summary').click()
            check(f'{lang}: stack comparison expands',page.locator('#stack table').is_visible())
            # Form behavior is tested against a local intercepted success, never the live endpoint.
            calls=[]
            def mock_contact(route):
                calls.append(route.request.method)
                route.fulfill(status=200,content_type='application/json',body='{"ok":true}')
            page.route('https://formspree.io/f/xojgorkl',mock_contact)
            page.locator('#contact-name').fill('Website QA')
            page.locator('#contact-email').fill('qa@example.invalid')
            page.locator('#contact-brief').fill('Intercepted test; never sent')
            page.locator('[data-contact-form] button').click()
            page.wait_for_timeout(200)
            check(f'{lang}: preserved contact behavior (intercepted)',calls==['POST'] and page.locator('.form-status').inner_text()==page.locator('form').get_attribute('data-success'))
            page.unroute('https://formspree.io/f/xojgorkl')
            # A direct step link is useful when sharing a specific product stage.
            page.goto(base.rstrip('/')+f'/{lang}/#step-handover',wait_until='networkidle')
            page.wait_for_timeout(1000)
            check(f'{lang}: direct step link',page.locator('#product-panel').get_attribute('data-active-shot')=='handover')
        nojs=browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844})
        fallback=nojs.new_page()
        for lang in COPY:
            fallback.goto(base.rstrip('/')+f'/{lang}/',wait_until='domcontentloaded')
            check(f'{lang}: all four images available without JS',all(fallback.locator('.step-image').nth(i).is_visible() for i in range(4)))
        browser.close()
    check('no browser errors',not errors,errors)
    relevant=[x for x in http if 'favicon' not in x[1]]
    check('no HTTP errors',not relevant,relevant)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--browser',action='store_true');ap.add_argument('--base',default='');args=ap.parse_args()
    static_checks();server=None
    try:
        if args.browser:
            if args.base: base=args.base
            else: server,base=serve()
            browser_checks(base)
    finally:
        if server: server.shutdown()
        (OUT/'factory-os-qa.json').write_text(json.dumps(REPORT,ensure_ascii=False,indent=2))
    fails=[x for x in REPORT['checks'] if not x['pass']]
    print(f'Factory OS QA: {len(REPORT["checks"])-len(fails)}/{len(REPORT["checks"])} passed')
    return int(bool(fails))
if __name__=='__main__': raise SystemExit(main())
