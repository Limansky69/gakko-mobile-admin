import sys, asyncio, json
from playwright.async_api import async_playwright
# usage: flow.py file.html steps.json   steps: [{"js":..., "shot":"name", "w":1440,"h":900, "full":false, "click":"selector", "wait":300}]
async def main():
    f=sys.argv[1]; steps=json.load(open(sys.argv[2]))
    async with async_playwright() as p:
        import os; os.makedirs('/home/claude/shots',exist_ok=True)
        b=await p.chromium.launch(args=['--no-sandbox'])
        ctx=await b.new_context(locale='pl-PL',viewport={'width':steps[0].get('w',1440),'height':steps[0].get('h',900)})
        pg=await ctx.new_page(); errs=[]
        pg.on('pageerror',lambda e:errs.append('PAGEERROR '+str(e)))
        pg.on('console',lambda m:errs.append('console:'+m.text) if m.type=='error' and 'Failed to load resource' not in m.text else None)
        await pg.route('**/fonts.g*/**',lambda r:r.abort())
        await pg.goto('file://'+f); await pg.wait_for_timeout(400)
        if not steps[0].get('keep'): 
            await pg.evaluate("localStorage.clear();localStorage.setItem('gakko-admin-auth','{}')"); await pg.reload(); await pg.wait_for_timeout(500)
        for i,s in enumerate(steps):
            if 'w' in s and i>0: await pg.set_viewport_size({'width':s['w'],'height':s.get('h',900)})
            if 'click' in s:
                try: await pg.click(s['click'],timeout=3000)
                except Exception as e: print('CLICK FAIL',s['click'],str(e)[:120])
            if 'clickxy' in s: await pg.mouse.click(*s['clickxy'])
            if 'fill' in s:
                sel,val=s['fill']; await pg.fill(sel,val)
            if 'select' in s:
                sel,val=s['select']; await pg.select_option(sel,val)
            if 'press' in s: await pg.keyboard.press(s['press'])
            if 'js' in s:
                try:
                    r=await pg.evaluate(s['js'])
                    if r is not None: print(f'[{i}] JS:',json.dumps(r,ensure_ascii=False))
                except Exception as e: print(f'[{i}] JSERR',str(e)[:300])
            await pg.wait_for_timeout(s.get('wait',350))
            if 'shot' in s: await pg.screenshot(path=f"/home/claude/shots/{s['shot']}.png",full_page=s.get('full',False))
        print('errors:',errs[:12])
        await b.close()
asyncio.run(main())
