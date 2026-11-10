"""Visual detail pass (final CSS layer). Loads last. No em or en dashes."""

VIS_CSS = r"""
/* ===== visual detail pass (preview_vis.py): loads last ===== */
p,li,dd,blockquote,figcaption{text-wrap:pretty}
h1,h2,h3,h4,.q-h1,.q-h2,.q-h3{text-wrap:balance}
"""
VIS_CSS += r"""
/* Cutout images in aspect-ratio boxes: percent max-height never resolved, so tall products overflowed and were clipped.
   Absolute + auto margins centres them and makes the percentages resolve against the box. */
.lf-wk-img:not(.cover) img,.pp-nc-m:not(.cover) img,.pp-r-i img,.pp-cn-i img,.mo-fc-img img{position:absolute;inset:0;margin:auto}
.lf-wk-img:not(.cover) img{width:auto;height:auto;max-width:76%;max-height:80%;object-fit:contain}
.pp-nc-m:not(.cover) img{max-width:80%;max-height:84%}
.pp-nc.big .pp-nc-m:not(.cover) img{max-height:86%}
.pp-cn-i{position:relative}
.mo-fc-img{position:relative}
.mo-fc-img img{width:auto;height:auto;max-width:100%;max-height:100%;object-fit:contain}
"""
VIS_CSS += r"""
/* Mega menu panel: same edges as the header content (logo to search), not a fixed 1180 */
.q-header .dw-mega{width:min(1240px,calc(100vw - 80px))}
"""
VIS_CSS += r"""
/* Product hero buttons: ghost buttons were 6px-radius rectangles beside pill primaries; one height, full-width stack on phones */
.lf-ps .pv-btns .q-btn-ghost{border-radius:999px;min-height:52px;padding:0 24px;display:inline-flex;align-items:center;justify-content:center}
@media(max-width:520px){.lf-ps .pv-btns{flex-direction:column;align-items:stretch}.lf-ps .pv-btns > a{width:100%;justify-content:center;text-align:center}}
/* footer legal links share the copyright's left edge */
@media(max-width:480px){.q-footer.dw2-foot .dw2-fl a:first-child{padding-left:0}}
"""
VIS_CSS += r"""
/* condensed header: 84% let hero text show through the logo row */
.q-header.dw-cond::before{background:color-mix(in srgb,var(--chrome-bg) 95%,transparent)}
"""
VIS_CSS += r"""
/* Leadership cards: monogram was absolute, so a long name or title rode up over the initials. Now it is a normal block. */
.p2-lp{justify-content:flex-start}
.p2-lmono{position:static;margin:-20px -20px 14px;height:128px;flex:none}
@media(max-width:768px){.p2-lmono{height:96px;margin-bottom:12px}}
/* Timeline entries with no photo: a short band, not a full-height empty card, on phones */
@media(max-width:767px){.pv-tl2 li .img.ph{aspect-ratio:auto;height:64px}}
@media(max-width:768px){.p2-lgrid > li:last-child:nth-child(odd){grid-column:1/-1}}
"""
VIS_CSS += r"""
/* FAQ and section header icon badges sit on the heading's axis (they were hugging the left edge above centred headings) */
.dw2-hbw.c{display:flex;justify-content:center}
/* fast-lane card: an odd last link spans the row instead of leaving a hole */
.pv-lh .fcard.b .links a:last-child:nth-child(odd){grid-column:1/-1}
/* phone footer: link lists in two columns instead of one 2000px column */
@media(max-width:480px){.q-footer.dw2-foot .dw2-fgrid{grid-template-columns:repeat(2,minmax(0,1fr));gap:28px 18px}.q-footer.dw2-foot .dw2-fbrand{grid-column:1/-1}.q-footer.dw2-foot .dw2-fc:nth-of-type(odd){}.q-footer.dw2-foot .q-footer-head{font-size:12.5px}}
"""
VIS_CSS += r"""
/* Tablet 768 to 1024: the systems explorer rail became five tall empty cards beside a squeezed panel. Pill row above a full-width panel instead. */
@media(min-width:768px) and (max-width:1024px){
.ex-grid{grid-template-columns:minmax(0,1fr);gap:16px}.ex-rail li{flex:none;display:block}.ex-rail li .ex-tab{flex:none}
.ex-rail ol{flex-direction:row;flex-wrap:wrap;gap:8px}
.ex-tab{grid-template-columns:auto auto;min-height:44px;padding:6px 16px 6px 8px;gap:8px;font-size:15px;border-radius:99px}
.ex-tab:hover{transform:none}.ex-tab::before,.ex-num{display:none}
.ex-ico{width:36px;height:36px}.ex-ico .ex-ic{width:19px;height:19px}
}
/* Three-up card grids are 215px wide at 768 and broke words; two across until 900, an odd last card spans */
@media(min-width:768px) and (max-width:900px){
.pv-grid-3,.pv-res,.pv-values{grid-template-columns:repeat(2,minmax(0,1fr))}
.pv-grid-3 > :last-child:nth-child(odd),.pv-res > :last-child:nth-child(odd),.pv-values > :last-child:nth-child(odd){grid-column:1/-1}
}
"""
VIS_CSS += r"""
/* phone: the cookie notice sat 18px under the compare tray; lift it above the tray when the tray is open */
@media(max-width:767px){body:has(.p2-tray:not([hidden])) .pp3-cc{bottom:160px;max-height:calc(100vh - 240px)}}
"""
VIS_CSS += r"""
/* phone tap targets: contact email links were 24px tall; chip links get an invisible 44px hit area */
.cd-mail{display:inline-flex;align-items:center;min-height:44px}
.pv-chip-a{position:relative}.pv-chip-a::after{content:"";position:absolute;inset:-12px -8px}
"""
VIS_CSS += r"""
/* decorative glow and mesh layers may extend past the viewport: clip (not hidden, so sticky keeps working) */
body{overflow-x:clip}
"""
VIS_CSS += r"""
/* phones: the fixed Directions pill and sticky bar must never cover the last footer links, and the pill text must hold AA contrast */
@media(max-width:640px){body:has(.pv-switch-m) .q-footer{padding-bottom:calc(140px + env(safe-area-inset-bottom,0px))}
.pv-switch-m summary{color:#fff}}
"""
