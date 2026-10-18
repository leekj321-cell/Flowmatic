"""Deterministic multilingual build for the owner-approved product-first homepage."""
from __future__ import annotations
import json
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from content.investor_home import COPY, FILES, IDS, RELEASE

def e(value):
    return escape(str(value), quote=True)

def eyebrow(text, state=''):
    return f'<p class="eyebrow"><span class="square" aria-hidden="true"></span>{f"<bdi>{state}</bdi> · " if state else ""}{e(text)}</p>'

def paragraphs(items):
    return ''.join(f'<p>{e(s)}</p>' for s in items)

def build_home(lang):
    c = COPY[lang]
    logo = 'flowmatic-ci-ko-horizontal.png' if lang == 'ko' else 'flowmatic-ci-global-horizontal.svg'
    keys = ['label','title','description','input','output','next','status','caption','boundary','alt']
    shots = [dict(zip(keys, row), id=IDS[i], number=f'{i+1:02}', src='/media/product-20261018/'+FILES[i]) for i,row in enumerate(c['shots'])]
    first = shots[0]
    image = lambda s, cls='', lazy=True: f'<img class="{cls}" src="{e(s["src"])}" alt="{e(s["alt"])}" width="2304" height="1294" {"loading=lazy" if lazy else "fetchpriority=high"} decoding="async">'
    links = ''.join(f'<a href="#{target}">{e(label)}</a>' for target,label in zip(['problem','product','readiness','adoption'],c['nav']))
    locales = ''.join(f'<a href="/{code}/" lang="{code}" hreflang="{code}" data-lang-link="{code}" {"aria-current=page" if code==lang else ""}>{label}</a>' for code,label in [('ko','한국어'),('en','EN'),('ar','العربية')])
    steps = []
    for s in shots:
        fields = ''.join(f'<div><dt>{e(label)}</dt><dd>{e(s[key])}</dd></div>' for label,key in zip(c['fields'],['input','output','next']))
        steps.append(f'''<article class="story-step" id="step-{s['id']}" data-step="{s['id']}" aria-labelledby="title-{s['id']}">
<div class="story-card"><p class="step-number"><bdi>{s['number']} / 04</bdi><span>{e(s['label'])}</span></p>
<h3 id="title-{s['id']}">{e(s['title'])}</h3><p class="step-description">{e(s['description'])}</p>
<figure class="step-image"><button type="button" class="image-open" data-open-shot="{s['id']}" aria-label="{e(c['zoom'])}">{image(s)}</button><figcaption>{e(s['caption'])}</figcaption></figure>
<dl class="step-handoff">{fields}</dl><p class="step-boundary">{e(s['boundary'])}</p></div></article>''')
    tabs = ''.join(f'<a class="step-tab" href="#step-{s["id"]}" data-shot="{s["id"]}" aria-controls="product-panel" {"aria-current=step" if i==0 else ""}><bdi>{s["number"]}</bdi><span>{e(s["label"])}</span></a>' for i,s in enumerate(shots))
    values = ''.join(f'<div class="value-row"><span>{e(a)}</span><div><h3>{e(b)}</h3><p>{e(d)}</p></div></div>' for a,b,d in c['values'])
    readiness = ''.join(f'<div class="readiness-block">{eyebrow(c[title],state)}<ul>'+''.join(f'<li>{e(x)}</li>' for x in c[key])+'</ul></div>' for state,title,key in [('CURRENT','currentTitle','current'),('PILOT','pilotTitle','pilot')])
    rows = ''.join(f'<tr><th scope="row"><bdi>{e(level)}</bdi> {e(label)}</th><td>{e(c["traditionalTop" if i<4 else "traditionalBottom"])}</td><td>{e(c["flowTop" if i<4 else "flowBottom"])}</td></tr>' for i,(level,label) in enumerate(c['layers']))
    pilot = ''.join(f'<article class="adoption-step"><span class="num">{i+1:02}</span><h3>{e(a)}</h3><p>{e(b)}</p></article>' for i,(a,b) in enumerate(c['adoptionSteps']))
    audience = ''.join(f'<article><h3>{e(a)}</h3><p>{e(b)}</p></article>' for a,b in c['audience'])
    loop = ''.join(f'<article><h3><bdi>{e(a)}</bdi></h3><p>{e(b)}</p></article>' for a,b in c['loop'])
    form_copy = {
        'ko':['회사 / 이름','이메일','검토할 내용','검토 요청 보내기','전송 중입니다.','요청이 접수되었습니다.','전송하지 못했습니다. 이메일로 문의해 주세요.'],
        'en':['Company / name','Email','Scope for review','Send review request','Sending…','Request received.','Unable to send. Please contact the email address.'],
        'ar':['الشركة / الاسم','البريد الإلكتروني','النطاق المطلوب مراجعته','إرسال طلب المراجعة','جارٍ الإرسال…','تم استلام الطلب.','تعذر الإرسال. يرجى التواصل عبر البريد الإلكتروني.']
    }[lang]
    html = f'''<!doctype html>
<html lang="{lang}" dir="{'rtl' if lang=='ar' else 'ltr'}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{e(c['meta'])}"><meta name="color-scheme" content="light">
<meta name="flowmatic-release" content="{RELEASE}"><title>{e(c['title'])}</title>
<link rel="canonical" href="https://flowmatic-os.com/{lang}/">
{''.join(f'<link rel="alternate" hreflang="{code}" href="https://flowmatic-os.com/{code}/">' for code in COPY)}
<link rel="alternate" hreflang="x-default" href="https://flowmatic-os.com/ko/">
<meta property="og:title" content="{e(c['title'])}"><meta property="og:description" content="{e(c['meta'])}">
<meta property="og:image" content="https://flowmatic-os.com{first['src']}"><meta property="og:type" content="website">
<link rel="stylesheet" href="/stc-lite-home-v1.css?v={RELEASE}">
<script src="/investor-home.js?v={RELEASE}" defer></script></head>
<body><a class="skip" href="#main">{e(c['skip'])}</a>
<header class="site-header"><div class="wrap nav"><a class="brand" href="/{lang}/#hero" aria-label="Flowmatic"><img src="/assets/branding/canonical/{logo}" alt="Flowmatic" width="220"></a>
<button type="button" class="menu-toggle" id="menu-toggle" aria-controls="navigation" aria-expanded="false">{e(c['menu'])}</button>
<nav class="nav-links" id="navigation" aria-label="{e(c['menu'])}">{links}<div class="lang-switcher">{locales}</div></nav></div></header>
<main id="main"><section class="hero wrap" id="hero" aria-labelledby="hero-title">
<div class="hero-top">{eyebrow(c['kind'])}<span class="tag">{e(c['stage'])}</span></div>
<div class="hero-grid"><div class="hero-copy"><h1 id="hero-title">{''.join(f'<span>{e(t)}</span>' for t in c['headline'])}</h1>
<p class="lead">{e(c['lead'])}</p><p class="sub">{e(c['sub'])}</p><div class="actions"><a class="btn btn-primary" href="#product">{e(c['view'])} <span aria-hidden="true">↓</span></a><a class="btn" href="#adoption">{e(c['adopt'])}</a></div></div>
<figure class="hero-visual"><div class="visual-head"><strong>{e(first['label'])}</strong><span><bdi>CURRENT</bdi></span></div>
<button type="button" class="image-open" data-open-shot="machining" aria-label="{e(c['zoom'])}">{image(first,lazy=False)}</button>
<figcaption class="visual-foot"><span>{e(c['actual'])}</span><span class="zoom-hint">{e(c['zoom'])} ↗</span></figcaption></figure></div>
<div class="hero-summary">{''.join(f'<div><small>{e(a)}</small><strong>{e(b)}</strong></div>' for a,b in c['summary'])}</div></section>
<section class="problem" id="problem" aria-labelledby="problem-title"><div class="wrap problem-grid"><div>{eyebrow(c['nav'][0])}<h2 id="problem-title">{e(c['problemTitle'])}</h2></div><div class="problem-copy">{paragraphs(c['problem'])}<div class="problem-bottom">{''.join(f'<div><strong>{e(a)}</strong><span>{e(b)}</span></div>' for a,b in c['problemBottom'])}</div></div></div></section>
<section class="product wrap" id="product" aria-labelledby="product-title"><span id="proof" class="anchor-alias"></span><span id="journey" class="anchor-alias"></span>
<div class="section-intro"><div>{eyebrow(c['nav'][1],'CURRENT')}<h2 id="product-title">{e(c['productTitle'])}</h2></div><p>{e(c['productIntro'])}</p></div>
<div class="product-input"><strong>{e(c['inputTitle'])}</strong><span>{e(c['inputText'])}</span></div>
<p class="scroll-hint">{e(c['scrollHint'])}</p>
<div class="product-story" id="product-story"><div class="product-visual" id="product-panel" aria-label="{e(c['nav'][1])}" data-active-shot="machining">
<nav class="step-nav" aria-label="{e(c['nav'][1])}">{tabs}</nav>
<figure class="scroll-figure"><div class="evidence-label"><span class="status" id="shot-status">{e(first['status'])}</span><span class="zoom-hint">{e(c['zoom'])} ↗</span></div>
<button type="button" class="image-open" id="gallery-open" data-open-shot="machining" aria-label="{e(c['zoom'])}">{image(first,cls='shot-image')}</button>
<figcaption class="caption"><strong id="shot-caption">{e(first['caption'])}</strong><p class="interface-note">{e(c['interface'])}</p></figcaption></figure></div>
<div class="story-steps">{''.join(steps)}</div></div><p class="sequence-note">{e(c['sequence'])}</p>
<div class="additional-proof"><div><h3>{e(c['proofTitle'])}</h3><article><p class="proof-tag"><bdi>CURRENT · NC</bdi></p><h4>{e(c['ncTitle'])}</h4><p>{e(c['ncText'])}</p><a class="text-link" href="/{lang}/nc/">{e(c['ncLink'])} ↗</a></article><article><p class="proof-tag"><bdi>CURRENT · CT</bdi></p><h4>{e(c['ctTitle'])}</h4><p>{e(c['ctText'])}</p><a class="text-link" href="/{lang}/ct/">{e(c['ctLink'])} ↗</a></article></div><video controls playsinline preload="none" aria-label="{e(c['ctTitle'])}"><source src="/flowmatic_ct_demo.mp4" type="video/mp4"></video></div>
</section>
<section class="value" id="value" aria-labelledby="value-title"><div class="wrap value-grid"><div>{eyebrow(c['valueKicker'])}<h2 id="value-title">{e(c['valueTitle'])}</h2><p class="value-lead">{e(c['valueLead'])}</p></div><div><div class="value-list">{values}</div><p class="value-note">{e(c['valueNote'])}</p></div></div></section>
<section class="readiness wrap" id="readiness" aria-labelledby="readiness-title"><h2 id="readiness-title">{e(c['readinessTitle'])}</h2><div class="readiness-grid">{readiness}</div><p class="scope-line">{e(c['boundary'])}</p></section>
<section class="architecture wrap" id="stack" aria-labelledby="stack-title">{eyebrow('Factory OS','TARGET')}<h2 id="stack-title">{e(c['stackTitle'])}</h2><p class="architecture-intro">{e(c['stackIntro'])}</p>
<details class="stack-detail"><summary>{e(c['stackOpen'])}</summary><div class="table-scroll" tabindex="0"><table><thead><tr>{''.join(f'<th scope="col">{e(t)}</th>' for t in c['stackHeaders'])}</tr></thead><tbody>{rows}</tbody></table></div><p class="scope-line">{e(c['stackNote'])}</p></details>
<div id="loop" class="target-loop"><h3>{e(c['loopTitle'])}</h3><div class="loop-grid">{loop}</div><p class="scope-line">{e(c['loopNote'])}</p></div></section>
<section class="adoption wrap" id="adoption" aria-labelledby="adoption-title"><span id="pilot" class="anchor-alias"></span><div class="adoption-top"><div>{eyebrow('4–8 '+('주' if lang=='ko' else 'weeks' if lang=='en' else 'أسابيع'),'PILOT')}<h2 id="adoption-title">{e(c['adoptionTitle'])}</h2></div><p>{e(c['adoptionIntro'])}</p></div><div class="adoption-steps">{pilot}</div><div class="audience">{audience}</div><div class="model" id="company"><strong>{e(c['modelTitle'])}</strong><p>{e(c['model'])}</p></div>
<div class="contact" id="contact"><div><h3>{e(c['contactTitle'])}</h3><p>{e(c['contactText'])}</p><a class="btn" href="mailto:contact@flowmatic-os.com">{e(c['contactLink'])} ↗</a></div>
<form action="https://formspree.io/f/xojgorkl" method="post" data-contact-form data-sending="{e(form_copy[4])}" data-success="{e(form_copy[5])}" data-failed="{e(form_copy[6])}">
<label for="contact-name">{e(form_copy[0])}</label><input id="contact-name" name="name" autocomplete="organization" required>
<label for="contact-email">{e(form_copy[1])}</label><input id="contact-email" name="email" type="email" autocomplete="email" required>
<label for="contact-brief">{e(form_copy[2])}</label><textarea id="contact-brief" name="brief" rows="3" required></textarea><button class="btn" type="submit">{e(form_copy[3])}</button><p class="form-status" role="status"></p></form></div></section>
</main><footer><div class="wrap footer-inner"><div><strong>Flowmatic</strong><p>{e(c['footer'])}</p><div class="color-rule" aria-hidden="true"><span></span><span></span><span></span></div></div><div class="footer-right"><p><a href="mailto:contact@flowmatic-os.com">contact@flowmatic-os.com</a></p><p>© 2026 Flowmatic</p></div></div></footer>
<dialog id="image-dialog" aria-labelledby="dialog-title"><div class="dialog-head"><h2 id="dialog-title">{e(c['nav'][1])}</h2><button type="button" id="dialog-close">{e(c['close'])} ×</button></div><div class="dialog-image" dir="ltr"><img id="dialog-image" alt="" width="2304" height="1294"></div><p class="dialog-note" id="dialog-note"></p></dialog>
<script id="product-evidence" type="application/json">{json.dumps(shots,ensure_ascii=False).replace('</','<\\/')}</script></body></html>
'''
    (ROOT/lang/'index.html').write_text(html,encoding='utf-8')

def main():
    for lang in COPY:
        build_home(lang)
    (ROOT/'index.html').write_text(f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="flowmatic-release" content="{RELEASE}"><meta http-equiv="refresh" content="0;url=/ko/"><link rel="canonical" href="https://flowmatic-os.com/ko/"><title>Flowmatic Factory OS</title></head><body><a href="/ko/">Flowmatic Factory OS · 한국어</a> · <a href="/en/">English</a> · <a href="/ar/">العربية</a></body></html>\n''',encoding='utf-8')
    (ROOT/'release.json').write_text(json.dumps({'release':RELEASE,'scope':'approved-investor-home-product-scroll','base_release':'2026.09.20-r6.2-formal-copy','locales':list(COPY),'canonical_build':'python tools/build_stc_r5_site.py','canonical_qa':'python tools/stc_r5_qa.py --browser'},ensure_ascii=False,indent=2)+'\n')
    print('PASS: product-first homepages generated for KO / EN / AR.')

if __name__ == '__main__':
    main()
