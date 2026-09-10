"""One-time r2 -> r3 content repair. Never edits validation code or motion assets."""
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def replace_once(text, old, new):
    if text.count(old)!=1: raise SystemExit('Unexpected source; refusing repair: '+old[:90])
    return text.replace(old,new,1)
def main():
    p=ROOT/'business_narrative.py';s=p.read_text()
    if "RELEASE='2026.09.10-r3'" in s:
        print('r3 content already installed; no mutation');return
    if "RELEASE='2026.09.10-r2'" not in s: raise SystemExit('Expected reviewed r2 source')
    s=replace_once(s,"RELEASE='2026.09.10-r2'", "RELEASE='2026.09.10-r3'\nfrom pathlib import Path\nimport json\nDECLARATION='|'.join(json.loads((Path(__file__).parent/'homepage-declaration.json').read_text())['lines'])")
    s=replace_once(s,".update(h1=t['hero'],primary=", ".update(h1=DECLARATION,primary=")
    s=replace_once(s,'<h1 id="hero-title">{e(t["hero"]).replace("|","<br>")}</h1>', '<h1 id="hero-title" class="hero-title semantic-copy brand-hero-title" lang="en" dir="ltr" data-brand-contract="WEB-019">{site["lines"](DECLARATION)}</h1>')
    s=replace_once(s,'<p class="bn-brand-slogan" id="brand-slogan" lang="en" dir="ltr">Elegant Engineering. Intelligent Operations. Flowmatic.</p>','')
    old=next(line for line in s.splitlines() if "return f'<section class=\"field-flow section-grid bn-workflow\" id=\"workflow\"" in line)
    s=replace_once(s,old,"        return section('workflow',t['workflow'],t['workflow_body'],cards(t['workflow_steps']))")
    helper='''    def operations_motion(lang):
        t=COPY[lang]
        html=site['operations_story_section'](lang).replace('class="field-flow section-grid"','class="field-flow section-grid bn-workflow"')
        visual=site['field_story'](lang)
        return html.replace(visual+'</div>',visual+f'<p class="wr-label">{e(t["principle"])}</p><p class="wr-footnote">{e(t["principle_note"])}</p></div>')
'''
    s=replace_once(s,'    def composition(lang):',helper+'    def composition(lang):')
    s=replace_once(s,"+section('operating-resources',t['resources'],t['resources_body'])+end(lang,slug)","+section('operating-resources',t['resources'],t['resources_body'])+operations_motion(lang)+end(lang,slug)")
    s=s.replace('Original field animation explains cross-workflow connection, not purchasing.','WEB-019 / RT-022: canonical first-screen English declaration is the primary three-line H1 in all locales. WEB-020 / RT-023: original operational animation belongs only to the Operations page, with an illustrative integration boundary.')
    p.write_text(s)
    p=ROOT/'business-narrative.css';css=p.read_text()
    css+='''
/* WEB-019 / RT-022: approved primary declaration; content copy cannot replace it. */
body.bn-page .bn-hero #hero-title{font-size:clamp(24px,3.7vw,56px)!important;line-height:1.08!important;font-weight:800!important;letter-spacing:-.035em!important;direction:ltr!important;text-align:left!important;unicode-bidi:isolate;max-width:none!important;width:100%;margin:10px 0 28px;word-break:normal!important;overflow-wrap:normal!important}
body.bn-page .bn-hero #hero-title .copy-lines{display:block!important;width:100%!important;min-width:0;max-width:100%}
body.bn-page .bn-hero #hero-title .copy-line{display:block!important;white-space:nowrap!important;width:auto!important;max-width:100%;font-size:inherit!important;line-height:inherit!important;letter-spacing:inherit!important;word-break:normal!important;overflow-wrap:normal!important}
@media(max-width:768px){body.bn-page .bn-hero #hero-title{font-size:clamp(24px,7.2vw,52px)!important}.bn-hero .bn-promise h2{font-size:clamp(24px,6.5vw,38px)}}
@media(max-width:359px){body.bn-page .bn-hero #hero-title{font-size:23px!important}}
@media(min-width:769px) and (max-width:1180px){body.bn-page .bn-hero .hero-copy,body.bn-page .bn-hero .bn-promise{grid-column:span 12!important}body.bn-page .bn-hero .hero-copy{min-height:0}body.bn-page .bn-hero #hero-title{font-size:clamp(40px,5.5vw,60px)!important}}
'''
    p.write_text(css)
    print('Restored approved declaration and Operations ownership; validators and motion assets untouched')
if __name__=='__main__':main()
