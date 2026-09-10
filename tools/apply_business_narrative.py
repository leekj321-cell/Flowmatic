"""Idempotent build hook and role-aware regression suite, based on existing QA."""
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'build_site.py';s=p.read_text()
if '\nimport business_narrative\n' not in s:
    s=s.replace('web_release.configure(globals())','web_release.configure(globals())\nimport business_narrative\nbusiness_narrative.configure(globals())')
s=s.replace('page_path(lang, "platform"), home+"#company", home+"#pilot"]','page_path(lang, "platform"), home+"#company", home+"#contact"]')
p.write_text(s)
# Always derive from the preserved r1 suite; no repeated patch accumulation.
s=(ROOT/'tools/web_release_qa.py').read_text()
s=s.replace('browser=p.chromium.launch(headless=True)','browser=p.chromium.launch(headless=True, executable_path=os.environ.get("CHROMIUM_PATH"))')
s=s.replace("check(f'{lang}: slogan lines preserved',h.select_one('#hero-title').get_text('|')=='Elegant Engineering.|Intelligent Operations.|Flowmatic.')",'''check(f'{lang}: approved brand slogan preserved',h.select_one('#brand-slogan').get_text()=='Elegant Engineering. Intelligent Operations. Flowmatic.')
  import business_narrative as bn
  check(f'{lang}: business-first heading',h.select_one('#hero-title').get_text('|')==bn.COPY[lang]['hero'])
  order=[n.get('id') for n in h.select('main [id]')]
  anchors=['hero','field-problem','workflow','products','demos','capability','preprocessing','architecture','growth','pilot','company','contact']
  check(f'{lang}: narrative reading order',all(a in order for a in anchors) and [order.index(a) for a in anchors]==sorted(order.index(a) for a in anchors),order)
  check(f'{lang}: hero offers product context, not NC execution',h.select_one('.hero-actions a.primary')['href']=='#products' and not h.select('#hero a[href$="/nc/"]'))
  check(f'{lang}: company definition before first action',str(h.select_one('.hero-copy')).find('bn-definition')<str(h.select_one('.hero-copy')).find('hero-actions'))
  check(f'{lang}: one preserved field-principle animation',len(h.select('#workflow [data-field-story]'))==1)
  check(f'{lang}: CT recording has explicit playback controls',h.select_one('#demos video').has_attr('controls'))''')
s=s.replace("page.locator('.hero-actions a.primary').click();check(f'{lang}: official home CTA opens same-locale NC',urlsplit(page.url).path==f'/{lang}/nc/')", "page.locator('.hero-actions a.primary').click();check(f'{lang}: company CTA leads to product explanation',urlsplit(page.url).fragment=='products')\n   page.locator('#demos a.fm-button').first.click();check(f'{lang}: contextual demonstration opens same-locale NC',urlsplit(page.url).path==f'/{lang}/nc/')")
s=s.replace("cta=page.locator('.hero-actions a.primary').bounding_box();check(f'{lang}: immediate first-screen CTA {w}x{h}',cta is not None and cta['y']+cta['height']<=h+1,cta)","cta=page.locator('.hero-actions a.primary');check(f'{lang}: product CTA available without animation prerequisite {w}x{h}',cta.is_visible() and cta.is_enabled())")
s=s.replace("page.set_viewport_size({'width':390,'height':844});go(f'/{lang}/operations-intelligence/');check(f'{lang}: Operations animation present',page.locator('[data-field-story]').count()==1)", "page.set_viewport_size({'width':390,'height':844});go(f'/{lang}/');check(f'{lang}: cross-workflow animation within principle explanation',page.locator('#workflow [data-field-story]').count()==1)")
s=s.replace("f'{lang}: Operations animation advances'", "f'{lang}: field-principle animation advances'")
s=s.replace("   # Responsive menu + non-delivery contact validation.",'''   go(f'/{lang}/operations-intelligence/');check(f'{lang}: purchasing is not misrepresented by generic field animation',page.locator('[data-field-story]').count()==0)
   for width in [390,1440]:
    page.set_viewport_size({'width':width,'height':900});go(f'/{lang}/')
    for ident in ['field-problem','workflow','products','demos','capability','growth','pilot']:
     el=page.locator('#'+ident);el.scroll_into_view_if_needed();page.wait_for_timeout(120);el.screenshot(path=str(OUT/f'{lang}-{ident}-{width}.png'),style='.site-header{visibility:hidden!important}')
   page.set_viewport_size({'width':390,'height':844})
   go(f'/{lang}/');video=page.locator('#demos video');video.scroll_into_view_if_needed()
   video.evaluate('(v)=>{v.muted=true;return v.play()}');page.wait_for_timeout(700)
   playback=video.evaluate('(v)=>({time:v.currentTime,duration:v.duration,paused:v.paused,error:v.error?.code||null})')
   check(f'{lang}: contextual CT recording actually plays',playback['time']>0 and not playback['paused'] and playback['error'] is None,playback)
   video.evaluate('(v)=>v.pause()')
   # Responsive menu + non-delivery contact validation.''')
s=s.replace("'Contact form validation and transport mock tested; no real inquiry or receipt test.'", "'Contact form validation and transport mock tested; no real inquiry or receipt test.','Business content reviewed by the author against owner-approved narrative; no independent reader study.'")
(ROOT/'tools/web_business_qa.py').write_text(s)
# The abandoned transfer staging files are not part of the public release.
if (ROOT/'.release-transfer').exists():shutil.rmtree(ROOT/'.release-transfer')
print('Business narrative and regression suite installed; protected animation renderers unchanged.')
