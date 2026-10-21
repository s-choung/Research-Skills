import sys
from playwright.sync_api import sync_playwright

path, outdir = sys.argv[1], sys.argv[2]
errs = []
with sync_playwright() as p:
    b = p.chromium.launch()
    for w in (1440, 1280, 1024):
        pg = b.new_page(viewport={"width": w, "height": 900})
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.route("**/*", lambda r: r.abort() if r.request.url.startswith("http") else r.continue_())
        pg.goto("file://" + path)
        pg.wait_for_timeout(800)
        r = pg.evaluate("""() => ({
          sw: document.documentElement.scrollWidth - window.innerWidth,
          font: document.fonts.check('16px Inter'),
          imgs: Array.from(document.images).every(i => i.naturalWidth > 0),
          nimg: document.images.length,
          hidden: document.querySelectorAll('.fv[hidden]').length,
          shown: document.querySelectorAll('.fv:not([hidden])').length})""")
        print(w, r)
        if w == 1440:
            pg.screenshot(path=f"{outdir}/top.png")
            pg.click("#f2 .btngrp:nth-child(1) button:nth-child(4)")
            pg.click("#f2 .btngrp:nth-child(2) button:nth-child(3)")
            print("f2 after click", pg.evaluate("() => Array.from(document.querySelectorAll('#f2 .fv:not([hidden])')).map(d => d.getAttribute('data-key'))"))
            pg.click("#f5 .btngrp:nth-child(2) button:nth-child(2)")
            print("f5 after click", pg.evaluate("() => Array.from(document.querySelectorAll('#f5 .fv:not([hidden])')).map(d => d.getAttribute('data-key'))"))
            pg.query_selector("#f2").screenshot(path=f"{outdir}/f2.png")
            pg.query_selector("#f5").screenshot(path=f"{outdir}/f5.png")
            pg.evaluate("() => document.querySelector('h1.sec').scrollIntoView()")
            pg.screenshot(path=f"{outdir}/summary.png")
            pg.evaluate("() => document.querySelector('#f4').scrollIntoView()")
            pg.screenshot(path=f"{outdir}/f4.png")
            # paragraph right edge vs table right edge
            print("edges", pg.evaluate("() => [document.querySelector('.note').getBoundingClientRect().right, document.querySelector('table').getBoundingClientRect().right, document.querySelector('.wrap').getBoundingClientRect().right]"))
            print("page height", pg.evaluate("() => document.documentElement.scrollHeight"))
        pg.close()
    b.close()
print("js errors", errs)
