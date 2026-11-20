"""Records the Seatmate walkthrough: Playwright drives the real app, an in-page
cursor moves on eased curves, and a caption appears beside each action.
Frames come from the Chrome screencast; run.sh resets the data first."""

import base64
import os
import random
import shutil

from playwright.sync_api import sync_playwright

B = "http://localhost:5173"
FR = "frames"
shutil.rmtree(FR, ignore_errors=True)
os.makedirs(FR)
random.seed(7)

OVERLAY = r"""
(() => {
  try { localStorage.setItem('shotgun.theme','light') } catch(e){}
  const css = `
  #__vue-devtools-container__,[id^="vue-devtools"],[class*="vue-devtools"]{display:none!important}
  #rec-cap{position:absolute;left:0;top:0;z-index:2147483646;pointer-events:none;white-space:nowrap;
    background:#0f172a;color:#fff;font:500 19px/1.25 'Geist Variable',Geist,system-ui,sans-serif;letter-spacing:-.005em;
    padding:11px 18px;border-radius:12px;box-shadow:0 12px 32px rgba(15,23,42,.28),0 2px 6px rgba(15,23,42,.18);
    opacity:0;transform:scale(.94);transition:opacity .22s ease,transform .22s cubic-bezier(.2,.8,.2,1)}
  #rec-cap.on{opacity:1;transform:scale(1)}
  #rec-cap::before{content:'';position:absolute;width:12px;height:12px;background:#0f172a;transform:rotate(45deg);border-radius:2px}
  #rec-cap[data-side=right]::before{left:-5px;top:calc(50% - 6px)}
  #rec-cap[data-side=left]::before{right:-5px;top:calc(50% - 6px)}
  #rec-cap[data-side=top]::before{bottom:-5px;left:calc(50% - 6px)}
  #rec-cap[data-side=bottom]::before{top:-5px;left:calc(50% - 6px)}
  #rec-cur{position:fixed;left:0;top:0;z-index:2147483647;pointer-events:none;will-change:transform}
  #rec-cur svg{position:absolute;display:none;transition:transform .08s}
  #rec-cur[data-k=arrow] .k-arrow,#rec-cur[data-k=hand] .k-hand,#rec-cur[data-k=text] .k-text{display:block}
  #rec-cur.down svg{transform:scale(.88)}`;
  const SVG = `
   <svg class="k-arrow" width="26" height="26" viewBox="0 0 24 24" style="left:-6px;top:-3px;filter:drop-shadow(0 1px 1.5px rgba(0,0,0,.4))">
     <path d="M6 3v17.2l4.3-4.2 2.8 6.3 2.7-1.2-2.8-6.2h6.1z" fill="#000" stroke="#fff" stroke-width="1.4" stroke-linejoin="round"/></svg>
   <svg class="k-hand" width="28" height="28" viewBox="0 0 24 24" style="left:-9px;top:-2px;filter:drop-shadow(0 1px 1.5px rgba(0,0,0,.4))">
     <path d="M9 2c-1 0-1.7.8-1.7 1.7v9.6l-1.4-1.4c-.7-.7-1.9-.7-2.5 0-.6.6-.7 1.6-.1 2.3l4.5 5.5c1 1.2 2.4 1.8 3.9 1.8h3.3c2.6 0 4.7-2.1 4.7-4.7v-5c0-.9-.8-1.7-1.7-1.7-.4 0-.8.1-1.1.4-.1-.9-.8-1.6-1.7-1.6-.5 0-1 .2-1.3.6-.3-.7-.9-1.2-1.7-1.2-.4 0-.8.1-1.1.4V3.7C10.7 2.8 10 2 9 2z" fill="#fff" stroke="#000" stroke-width="1.3" stroke-linejoin="round"/>
     <path d="M10.7 10.5v4M13.8 10.9v3.6M16.9 11.6v2.9" stroke="#000" stroke-width="1.1" stroke-linecap="round"/></svg>
   <svg class="k-text" width="22" height="26" viewBox="0 0 22 26" style="left:-11px;top:-13px">
     <path d="M7 3.5c2 0 3.2.6 4 1.6.8-1 2-1.6 4-1.6M11 5.1v15.8M7 22.5c2 0 3.2-.6 4-1.6.8 1 2 1.6 4 1.6M8.6 13h4.8" fill="none" stroke="#fff" stroke-width="3.6" stroke-linecap="round"/>
     <path d="M7 3.5c2 0 3.2.6 4 1.6.8-1 2-1.6 4-1.6M11 5.1v15.8M7 22.5c2 0 3.2-.6 4-1.6.8 1 2 1.6 4 1.6M8.6 13h4.8" fill="none" stroke="#000" stroke-width="1.5" stroke-linecap="round"/></svg>`;
  const S = window.__rec = { x: 1500, y: 820 };
  function kindAt(x, y) {
    const el = document.elementFromPoint(x, y); if (!el) return 'arrow';
    const t = el.closest('input,textarea,select');
    if (t && (t.tagName === 'TEXTAREA' || (t.tagName === 'INPUT' && /^(text|email|password|search|tel|number|)$/.test(t.type)))) return 'text';
    const c = getComputedStyle(el).cursor;
    if (c === 'pointer') return 'hand';
    if (c === 'text') return 'text';
    return 'arrow';
  }
  function draw() {
    const cur = document.getElementById('rec-cur'); if (!cur) return;
    cur.style.transform = `translate(${S.x}px,${S.y}px)`;
    cur.dataset.k = kindAt(S.x, S.y);
  }
  function mount() {
    if (document.getElementById('rec-cur')) return;
    const s = document.createElement('style'); s.textContent = css; document.head.appendChild(s);
    const c = document.createElement('div'); c.id = 'rec-cap'; document.body.appendChild(c);
    const cur = document.createElement('div'); cur.id = 'rec-cur'; cur.innerHTML = SVG; document.body.appendChild(cur);
    draw();
    document.addEventListener('scroll', draw, { passive: true });
    document.addEventListener('mousedown', () => cur.classList.add('down'), true);
    document.addEventListener('mouseup', () => cur.classList.remove('down'), true);
  }
  document.addEventListener('DOMContentLoaded', mount);

  // Minimum-jerk easing along a gently curved cubic Bezier, like a real hand.
  window.__moveTo = (tx, ty, dur, bend) => new Promise(res => {
    const x0 = S.x, y0 = S.y, dx = tx - x0, dy = ty - y0, d = Math.hypot(dx, dy) || 1;
    const nx = -dy / d, ny = dx / d, k = d * bend;
    const c1 = [x0 + dx * .3 + nx * k, y0 + dy * .3 + ny * k];
    const c2 = [x0 + dx * .75 + nx * k * .5, y0 + dy * .75 + ny * k * .5];
    const t0 = performance.now();
    function step(now) {
      let t = Math.min(1, (now - t0) / dur);
      const e = t * t * t * (10 - 15 * t + 6 * t * t), u = 1 - e;
      S.x = u*u*u*x0 + 3*u*u*e*c1[0] + 3*u*e*e*c2[0] + e*e*e*tx;
      S.y = u*u*u*y0 + 3*u*u*e*c1[1] + 3*u*e*e*c2[1] + e*e*e*ty;
      draw();
      t < 1 ? requestAnimationFrame(step) : res();
    }
    requestAnimationFrame(step);
  });

  // Caption next to a rect (document coordinates), on the side with room.
  window.__cap = (text, r, pref, fixed) => {
    const c = document.getElementById('rec-cap'); if (!c) return;
    if (!text) { c.classList.remove('on'); setTimeout(() => { if (!c.classList.contains('on')) { c.style.position = 'fixed'; c.style.left = '-9999px'; c.style.top = '0px'; } }, 260); return; }
    c.textContent = text;
    c.style.position = fixed ? 'fixed' : 'absolute';
    const w = c.offsetWidth, h = c.offsetHeight, vw = innerWidth, sy = scrollY, sx = fixed ? 0 : scrollX, g = 18;
    const top = r.y - sy, fits = {
      right: r.x + r.w + g + w < vw - 24, left: r.x - g - w > 24,
      top: top - g - h > 76, bottom: top + r.h + g + h < innerHeight - 20 };
    const order = [pref, 'right', 'left', 'top', 'bottom'].filter(Boolean);
    const side = order.find(o => fits[o]) || 'bottom';
    let x, y;
    if (side === 'right') { x = r.x + r.w + g; y = r.y + r.h / 2 - h / 2; }
    if (side === 'left') { x = r.x - g - w; y = r.y + r.h / 2 - h / 2; }
    if (side === 'top') { x = r.x + r.w / 2 - w / 2; y = r.y - g - h; }
    if (side === 'bottom') { x = r.x + r.w / 2 - w / 2; y = r.y + r.h + g; }
    x = Math.max(24, Math.min(x, vw - w - 24));
    c.dataset.side = side;
    c.style.left = (x + sx) + 'px'; c.style.top = (fixed ? y - sy : y) + 'px';
    c.classList.add('on');
  };
})();
"""

frames = []
with sync_playwright() as p:
    b = p.chromium.launch(args=["--font-render-hinting=none"])
    ctx = b.new_context(
        viewport={"width": 1920, "height": 1080},
        device_scale_factor=1,
        color_scheme="light",
    )
    ctx.add_init_script(OVERLAY)
    pg = ctx.new_page()
    pg.goto(B + "/")
    pg.wait_for_load_state("networkidle")
    pg.wait_for_timeout(800)
    pg.mouse.move(1500, 820)

    cdp = ctx.new_cdp_session(pg)

    def on_frame(ev):
        frames.append((ev["metadata"]["timestamp"], ev["data"]))
        try:
            cdp.send("Page.screencastFrameAck", {"sessionId": ev["sessionId"]})
        except Exception:  # noqa: BLE001, S110
            pass

    cdp.on("Page.screencastFrame", on_frame)
    cdp.send(
        "Page.startScreencast",
        {
            "format": "jpeg",
            "quality": 95,
            "maxWidth": 1920,
            "maxHeight": 1080,
            "everyNthFrame": 1,
        },
    )

    W = pg.wait_for_timeout

    def rect(loc):
        """Document-coordinate rect of a locator."""
        return pg.evaluate(
            "el => { const r = el.getBoundingClientRect(); return {x:r.left, y:r.top+scrollY, w:r.width, h:r.height} }",
            loc.element_handle(),
        )

    def say(text, loc=None, side=None):
        if not text:
            pg.evaluate("window.__cap('')")
            return
        fixed = pg.evaluate("el => !!el.closest('header')", loc.element_handle())
        pg.evaluate(
            "([t,r,s,f]) => window.__cap(t,r,s,f)", [text, rect(loc), side, fixed]
        )

    def hide():
        say("")

    def scroll(y, ms=900):
        pg.evaluate("y => window.scrollTo({top:y,behavior:'smooth'})", y)
        W(ms)

    def ensure_visible(loc, top=110, bottom=140, place=0.42):
        if pg.evaluate("el => !!el.closest('header')", loc.element_handle()):
            return
        r = loc.bounding_box()
        if r["y"] < top or r["y"] + r["height"] > 1080 - bottom:
            y = pg.evaluate(
                "([el,p]) => el.getBoundingClientRect().top + scrollY - innerHeight*p",
                [loc.element_handle(), place],
            )
            scroll(max(0, y), 700)

    def move(loc, speed=1.0):
        ensure_visible(loc)
        r = loc.bounding_box()
        # aim somewhere natural inside the element, not dead centre
        tx = (
            r["x"] + r["width"] * random.uniform(0.38, 0.62)
            if r["width"] < 220
            else r["x"] + min(r["width"] * 0.5, random.uniform(90, 200))
        )
        ty = r["y"] + r["height"] * random.uniform(0.4, 0.6)
        sx, sy = pg.evaluate("[__rec.x, __rec.y]")
        d = ((tx - sx) ** 2 + (ty - sy) ** 2) ** 0.5
        dur = (240 + 120 * (1 + d / 30) ** 0.5 * 1.4) * speed if d > 4 else 0
        dur = min(dur, 900)
        bend = random.choice([-1, 1]) * random.uniform(0.05, 0.14)
        if dur:
            pg.evaluate("([x,y,t,b]) => window.__moveTo(x,y,t,b)", [tx, ty, dur, bend])
        pg.mouse.move(tx, ty)  # real pointer for hover states
        W(random.randint(90, 160))

    def click(loc, speed=1.0, after=220):
        move(loc, speed)
        pg.mouse.down()
        W(75)
        pg.mouse.up()
        W(after)

    def menu(name, label):
        av = pg.locator("header button[aria-haspopup=menu]")
        click(av)
        W(200)
        item = pg.locator("header a", has_text=name).first
        say(label, item, "left")
        move(item, 0.8)
        W(250)
        pg.evaluate(
            "() => { const c = document.getElementById('rec-cap'); c.style.transition = 'none'; c.classList.remove('on'); c.style.position = 'fixed'; c.style.left = '-9999px'; c.offsetHeight; c.style.transition = '' }"
        )
        pg.mouse.down()
        W(75)
        pg.mouse.up()
        W(220)
        pg.wait_for_load_state("networkidle")
        W(300)

    # 1. Landing + login
    W(600)
    email = pg.locator("input[type=email]")
    say("Log in with email and password", email, "right")
    click(email)
    pg.keyboard.type("ana@shotgun.app", delay=26)
    click(pg.locator("input[type=password]"), 0.7)
    pg.keyboard.type("Geslo123", delay=33)
    W(150)
    click(pg.locator('button:has-text("Log in")'))
    hide()
    pg.wait_for_url("**/app")
    pg.wait_for_load_state("networkidle")
    W(1500)

    # 2. Home
    find = pg.locator(".card").filter(has_text="Find a ride").first
    pg.evaluate("""() => [...document.querySelectorAll('button')].filter(x=>x.textContent.includes('Book a seat'))
        .find(x=>{const t=x.closest('.card')?.textContent||''; return t.includes('Ljubljana')&&t.includes('Milan')&&t.includes('Luka')})
        .closest('.card').dataset.rec='milan'""")
    milan = pg.locator("[data-rec=milan]")
    heading = pg.locator("h2", has_text="Available drivers")
    scroll(
        pg.evaluate(
            "el => el.getBoundingClientRect().top + scrollY - 120",
            heading.element_handle(),
        ),
        700,
    )
    say("Search and browse drivers: price, seats, CO₂ saved", heading, "right")
    W(900)
    hide()
    scroll(
        pg.evaluate(
            "el => el.getBoundingClientRect().top + scrollY - 160",
            milan.element_handle(),
        ),
        1000,
    )

    # 3. Book
    book = milan.locator('button:has-text("Book a seat")')
    say("Book a seat", book, "top")
    click(book, after=400)
    hide()
    scroll(
        pg.evaluate(
            "el => el.getBoundingClientRect().top + scrollY - 100",
            milan.element_handle(),
        ),
        650,
    )
    seats = pg.get_by_role("button", name="More: Seats to book")
    say(
        "Choose seats and luggage",
        pg.get_by_role("button", name="More: Seats to book"),
        "right",
    )
    click(seats, after=300)
    click(pg.get_by_role("button", name="More: Small bags"), 0.8, after=350)
    hide()
    confirm = milan.locator('button:has-text("Book 2 seats")')
    say("Confirm the booking", confirm, "top")
    click(confirm, after=120)
    hide()
    pg.wait_for_load_state("networkidle")
    W(1300)

    # 4. Bookings
    menu("My bookings", "Open My bookings")
    milanb = pg.locator(".card").filter(has_text="Milan").first
    if milanb.count():
        scroll(
            pg.evaluate(
                "el => el.getBoundingClientRect().top + scrollY - 260",
                milanb.element_handle(),
            ),
            700,
        )
        say("See the new booking is added", milanb.locator("text=Milan").first, "right")
        W(900)
    hide()

    # 5. Offer a ride
    scroll(0, 450)
    menu("My rides", "Open My rides")
    offer = pg.locator('button:has-text("Offer a ride")')
    say("Offer a ride as a driver", offer, "left")
    click(offer, after=350)
    hide()
    say("Route, date and seats", pg.locator("#ride-form-from-country"), "top")
    for sel, val in [
        ("#ride-form-from-country", "Italy"),
        ("#ride-form-from-city", "Milan"),
        ("#ride-form-to-country", "Italy"),
        ("#ride-form-to-city", "Rome"),
    ]:
        move(pg.locator(sel), 0.7)
        pg.select_option(sel, val)
        W(160)
    move(pg.locator("#ride-form-date"), 0.7)
    pg.fill("#ride-form-date", "2026-11-28")
    W(150)
    move(pg.locator("#ride-form-time"), 0.7)
    pg.fill("#ride-form-time", "09:30")
    W(150)
    click(pg.get_by_role("button", name="More: Free seats"), 0.7, after=250)
    hide()
    save = pg.locator("#ride-form-save-btn")
    say("Publish the ride", save, "right")
    click(save, after=120)
    hide()
    W(700)

    # 6. Rate
    comp = pg.locator('button:has-text("Completed rides")')
    scroll(
        pg.evaluate(
            "el => el.getBoundingClientRect().top + scrollY - 300",
            comp.element_handle(),
        ),
        650,
    )
    click(comp, after=450)
    rate = pg.locator('button:has-text("Rate")').first
    say("Rate passengers after the trip", rate, "left")
    click(rate, after=450)
    hide()
    star = pg.locator('[aria-label="5 stars"]')
    say("5 stars and a comment", star, "right")
    click(star, after=150)
    click(pg.locator("textarea"), 0.7)
    pg.keyboard.type("Great company!", delay=18)
    W(150)
    hide()
    submit = pg.locator("[role=dialog] button[type=submit]").first
    click(submit, after=700)

    # 7. Profile + dark mode
    scroll(0, 450)
    menu("My profile", "Open your profile")
    car = pg.locator("h2, h3").filter(has_text="Car and environmental impact").first
    say("Your profile details", pg.locator("h1", has_text="My profile"), "right")
    W(1000)
    hide()
    W(150)
    say("Your car and its CO₂ per km", car, "right")
    W(1000)
    hide()
    toggle = pg.locator("header").get_by_role("button", name="Switch to dark")
    say("Switch to dark mode", toggle, "left")
    click(toggle, after=150)
    hide()
    W(650)

    # 8. Impact
    link = pg.locator("header a", has_text="Sustainability impact")
    say("Sustainability impact", link, "bottom")
    click(link)
    hide()
    pg.wait_for_load_state("networkidle")
    W(700)
    scroll(480, 1300)
    W(700)
    pg.mouse.move(1880, 1000)

    cdp.send("Page.stopScreencast")
    W(300)
    b.close()

frames.sort(key=lambda f: f[0])
with open("list.txt", "w") as lst:
    for i, (ts, data) in enumerate(frames):
        fn = f"{FR}/f{i:05d}.jpg"
        open(fn, "wb").write(base64.b64decode(data))  # noqa: SIM115
        nxt = frames[i + 1][0] if i + 1 < len(frames) else ts + 0.5
        lst.write(f"file '{fn}'\nduration {max(nxt - ts, 0.001):.4f}\n")
    lst.write(f"file '{FR}/f{len(frames) - 1:05d}.jpg'\n")
print("frames", len(frames), "duration", round(frames[-1][0] - frames[0][0], 1))
