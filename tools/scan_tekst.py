from playwright.sync_api import sync_playwright
import re,sys,os
PAGES=['overview','messages','events','notifications','surveys','schedule','audiences','users','delivery','team','settings']
T=r'\d{1,2}:\d{2}';D=r'\d{1,2}\.\d{2}(?:\.\d{2,4})?'
RX=[('time',re.compile(rf'({T})(\s*)([-–—])(\s*)({T})')),('date',re.compile(rf'({D})(\s*)([-–—])(\s*)({D})')),('dt',re.compile(rf'({D},?\s*{T})(\s*)([-–—])(\s*)({D}|{T})'))]
def run(path=os.environ.get('GAKKO_HTML','/home/claude/login/work.html')):
  with sync_playwright() as pw:
    b=pw.chromium.launch();errs=[];pg=b.new_page(viewport={'width':1440,'height':900});pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.route('**/fonts.googleapis.com/**',lambda r:r.fulfill(body='',content_type='text/css'))
    pg.goto('file://'+path);pg.evaluate("localStorage.clear();localStorage.setItem('gakko-admin-auth','{}')");pg.reload();pg.wait_for_timeout(900)
    bad={}
    def chk(tag):
        t=pg.evaluate("(()=>{const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT,{acceptNode:n=>n.parentElement.closest('script,style,svg')?NodeFilter.FILTER_REJECT:NodeFilter.FILTER_ACCEPT});let o=[];while(w.nextNode())o.push(w.currentNode.nodeValue);return o.join(' \\n')})()+' \\n'+[...document.querySelectorAll('[title],[aria-label],[data-tip],[placeholder]')].map(e=>(e.title||'')+' | '+(e.getAttribute('aria-label')||'')+' | '+(e.dataset.tip||'')+' | '+(e.placeholder||'')).join(' \\n')")
        for pat in ['·',r'(?<!•)•(?!•)',', ,',' ,',',,',' AM',' PM']:
            for m in re.finditer(pat if pat.startswith('(?') else re.escape(pat),t):bad.setdefault(('zakazane',repr(pat)),{}).setdefault(t[max(0,m.start()-40):m.end()+30].replace('\n','⏎'),tag)
        for kind,rx in RX:
            for m in rx.finditer(t):
                g=m.groups();sep=''.join(g[1:4])
                if sep==' – ':continue
                k=t[max(0,m.start()-30):m.end()+15].replace('\n','⏎')
                bad.setdefault((kind,repr(sep)),{}).setdefault(k,tag)
    for p in PAGES:
        pg.evaluate(f"navigate('{p}')");pg.wait_for_timeout(350);chk(p)
    S=[("navigate('schedule');ttOpenConf('s')",'conf')]
    for l in ['o','g','l','s']:S.append((f"navigate('schedule');tt.sheet=null;tt.lens='{l}';render()",'lens'+l))
    S+= [("navigate('schedule');tt.lens='g';render();document.querySelector('.tt-ev,[data-tt-open],.tt-item')?.click()",'ttsheet'),
         ("navigate('users');us.sheet=ttStuds()[0].id;us.tab='uni';render()",'usersheet'),
         ("navigate('users');us.sheet=ttStuds()[0].id;us.tab='log';render()",'userlog'),
         ("navigate('events');ev.id=state.events[0].id;render()",'eventdetail'),
         ("navigate('events');ev.id=null;ev.view='cal';render()",'evcal'),
         ("navigate('surveys');sv.id=state.surveys[0].id;render()",'surveydetail'),
         ("navigate('notifications');an.id=state.notifications[0].id;render()",'notifdetail')]
    for js,tag in S:
        try:pg.evaluate(js);pg.wait_for_timeout(350);chk(tag)
        except Exception as e:print('skip',tag,str(e)[:80])
    # wszystkie zdarzenia i ogłoszenia
    n=pg.evaluate("state.events.length")
    for i in range(n):
        pg.evaluate(f"navigate('events');ev.id=state.events[{i}].id;render()");pg.wait_for_timeout(120);chk('ev'+str(i))
    for key in ['notifications','surveys']:
        n=pg.evaluate(f"state.{key}.length")
        for i in range(n):
            pg.evaluate(f"navigate('{key}');{'an' if key=='notifications' else 'sv'}.id=state.{key}[{i}].id;render()");pg.wait_for_timeout(120);chk(key[:3]+str(i))
    for (kind,sep),d in sorted(bad.items()):
        print(f'== {kind} sep={sep}: {len(d)}')
        for k,tag in list(d.items())[:12]:print('   ',tag,'|',k)
    print('errors',errs[:3])
run(*sys.argv[1:])
