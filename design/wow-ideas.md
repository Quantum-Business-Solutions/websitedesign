# 20 ideas to make a customer website unforgettable (VAF showcase)

Shipped on the VAF build (live on the staging site), in the order they were built. Each is editable by the client or a theme-level setting, none needs a paid service.

| # | Idea | Status | Where it lives |
|---|------|--------|----------------|
| 1 | Technology Strength Assessment: yes/no steps, email capture, personalised results page, eliminate/optimize/leverage roadmap, branded PDF | Live | `js/vaf-assess.js`, questions and copy in HubDB |
| 2 | Lead-magnet popup ("27 Technology Tips for 2027") with smart triggers (delay plus scroll, exit intent, cooldown) and a branded PDF built in the browser | Live | `js/vaf-popup.js`, tips and rules in HubDB |
| 3 | Sticky-scroll service showcase: numbered list follows you, big image panels, proof stat per service | Live | `modules/vaf-showcase.module` |
| 4 | Company history as one horizontal rail, cards alternating above and below | Live | `modules/vaf-timeline.module` |
| 5 | Command palette: Ctrl/Cmd+K or "/" to jump to any page or action | Live | `js/vaf-wow.js` |
| 6 | "Open now" Customer Care status, computed in Indianapolis time, in the header and footer | Live | `js/vaf-wow.js` |
| 7 | Visit band: address, hours, directions, click-to-call, embedded map, plus matching LocalBusiness schema | Live | `templates/partials/vaf-footer.html` |
| 8 | Reading progress bar across the top | Live | `js/vaf-wow.js` |
| 9 | Pointer-following spotlight glow on cards and panels | Live | `js/vaf-wow.js`, `css/vaf-wow.css` |
| 10 | Smooth cross-fade between pages (View Transitions) | Live | `css/vaf-wow.css` |
| 11 | Branded print view: letterhead, link URLs, no chrome | Live | `css/vaf-wow.css` |
| 12 | Skip link and back-to-top button | Live | `js/vaf-wow.js` |
| 13 | Dark four-pillar wheel with icons, chips and proof lines | Live | `modules/vaf-wheel.module` |
| 14 | Legal pages as plain documents (no sales buttons, no stock photo, no sticky promo bar) | Live | layout and builder |
| 15 | "Pick your headache" router: three clicks to the right service and a tailored next step | Queued | new module |
| 16 | Savings estimator on the home page (the cost calculator already exists as its own page) | Queued | reuse `vaf-calculator` |
| 17 | Returning-visitor greeting that remembers the last service viewed | Queued | `js/vaf-wow.js` |
| 18 | Case-study metric cards that count up as they scroll into view | Queued | `vaf-casestudy` |
| 19 | Dark-mode toggle that follows the visitor's system setting | Queued | CSS variables |
| 20 | Floor-plan fly-through of the office with scroll-driven zoom | Queued | `vaf-hotspots` extension |

Reuse: items 1, 2, 5, 6, 7, 8, 9, 10, 11 and 12 are generic and can move into the base theme for every future build. Record: `process/website-program-template.md`.
