import os
from playwright.sync_api import sync_playwright
def setup(b,W=1440):
    pg=b.new_page(viewport={'width':W,'height':900});pg.route('**/fonts.g*/**',lambda r:r.abort())
    pg.goto('file://'+os.environ.get('GAKKO_HTML','/home/claude/login/work.html'));pg.evaluate("localStorage.clear();localStorage.setItem('gakko-admin-auth','{}')");pg.reload();pg.wait_for_timeout(1200)
    pg.evaluate("navigate('overview')");pg.wait_for_timeout(300);pg.click('[data-dash=edit]');pg.wait_for_timeout(300);return pg
def lay(pg):return pg.evaluate("[...document.querySelectorAll('#dashGrid .dw')].map(w=>{const r=w.getBoundingClientRect();return [w.dataset.w,Math.round(r.left),Math.round(r.top+scrollY),Math.round(r.width),Math.round(r.height)]})")
def drag(pg,k,tx,ty,steps=25,hold=600,release=True):
    g=pg.locator(f'[data-dgrip="{k}"]');g.scroll_into_view_if_needed();bb=g.bounding_box();x0,y0=bb['x']+bb['width']/2,bb['y']+bb['height']/2
    pg.mouse.move(x0,y0);pg.mouse.down()
    for i in range(1,steps+1):pg.mouse.move(x0+(tx-x0)*i/steps,y0+(ty-y0)*i/steps);pg.wait_for_timeout(16)
    pg.wait_for_timeout(hold)
    if release:pg.mouse.up();pg.wait_for_timeout(400)
