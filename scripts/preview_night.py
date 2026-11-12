"""Night shift: one illustrated building after dark, eight DMP products on duty, and a test alarm you can run.

Showcase home page only, and only for DMP (the section type pn-night is named by brands/dmp_night.py alone).

  RENDER_NIGHT   {"pn-night": renderer}
  assets         brands/digital-monitoring-products.assets/night/night.css and night.js (linked from the section, so the
                 other pages and the other two directions carry nothing)

Every word on the scene comes from the section data (brands/dmp_night.py), which copies product facts already in the repo.
The scene itself is an illustration and says so. Nothing about the test alarm is a real event: no time, place, zone or cause.

Performance and fallbacks
  * no JS: the scene is a still picture, the eight products are a plain list with links, the six steps are a readable list;
  * reduced motion: no parallax or tween, and the test alarm becomes six steps advanced by hand;
  * the parallax loop runs only while the section is on screen, and a frame-time guard switches it off for good on a machine
    that cannot hold the frame rate (class ns-lite); CSS animations are paused while the section is off screen (ns-off).

STAGE is the prototype scene (ids prefixed ns-, the nine class names that collided with the site renamed ns-*).
"""
from __future__ import annotations

from preview_panel import MARK_A, MARK_B

STAGE = r'''<div class="ns" id="ns-ns" data-seq="idle">

  <div class="ns-stage" id="ns-stage">
    <div class="ns-top">
      <p class="status" id="ns-status" role="status"><i aria-hidden="true"></i><span id="ns-statusText">Armed</span></p>
      <div class="tod" role="group" aria-label="Lighting">
        <button type="button" class="tod-b" data-t="0">Day</button>
        <input type="range" id="ns-tod" min="0" max="100" step="1" value="100" aria-label="Time of day, from day to night">
        <button type="button" class="tod-b" data-t="1">Night</button>
      </div>
    </div>

    @@TITLE@@
    <svg id="ns-scene" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice" role="group" aria-label="Illustrated building at night with eight protection points you can open">
      <defs>
        <linearGradient id="ns-gSky" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0" style="stop-color:var(--sky0)"/>
          <stop offset=".52" style="stop-color:var(--sky1)"/>
          <stop offset=".78" style="stop-color:var(--sky2)"/>
        </linearGradient>
        <radialGradient id="ns-gMoonGlow"><stop offset="0" stop-color="#cfdcff" stop-opacity=".55"/><stop offset=".25" stop-color="#9db4ff" stop-opacity=".18"/><stop offset="1" stop-color="#9db4ff" stop-opacity="0"/></radialGradient>
        <radialGradient id="ns-gSunGlow"><stop offset="0" stop-color="#fff3c4" stop-opacity=".95"/><stop offset=".3" stop-color="#ffd27a" stop-opacity=".35"/><stop offset="1" stop-color="#ffb060" stop-opacity="0"/></radialGradient>
        <radialGradient id="ns-gHorizon"><stop offset="0" stop-color="#ff9a52" stop-opacity=".85"/><stop offset="1" stop-color="#ff9a52" stop-opacity="0"/></radialGradient>
        <radialGradient id="ns-gHalo"><stop offset="0" stop-color="#ffd23d" stop-opacity=".55"/><stop offset=".55" stop-color="#ffd23d" stop-opacity=".14"/><stop offset="1" stop-color="#ffd23d" stop-opacity="0"/></radialGradient>
        <radialGradient id="ns-gWarm"><stop offset="0" stop-color="#ffd58a" stop-opacity=".9"/><stop offset=".5" stop-color="#ffb24a" stop-opacity=".28"/><stop offset="1" stop-color="#ffb24a" stop-opacity="0"/></radialGradient>
        <radialGradient id="ns-gPool"><stop offset="0" stop-color="#ffdf9e" stop-opacity=".55"/><stop offset="1" stop-color="#ffdf9e" stop-opacity="0"/></radialGradient>
        <linearGradient id="ns-gCone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe6ad" stop-opacity=".6"/><stop offset=".55" stop-color="#ffd98f" stop-opacity=".16"/><stop offset="1" stop-color="#ffd98f" stop-opacity="0"/></linearGradient>
        <linearGradient id="ns-gSpill" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffd27a" stop-opacity=".5"/><stop offset="1" stop-color="#ffd27a" stop-opacity="0"/></linearGradient>
        <radialGradient id="ns-gFog"><stop offset="0" style="stop-color:var(--fog)" stop-opacity=".6"/><stop offset="1" style="stop-color:var(--fog)" stop-opacity="0"/></radialGradient>
        <linearGradient id="ns-gFace" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".28"/></linearGradient>
        <linearGradient id="ns-gDrop" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity=".32"/><stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>
        <linearGradient id="ns-gLot" x1="0" y1="0" x2="0" y2="1"><stop offset="0" style="stop-color:var(--asphalt)"/><stop offset="1" style="stop-color:var(--asphalt2)"/></linearGradient>
        <linearGradient id="ns-gRim" x1="0" y1="0" x2="1" y2="0"><stop offset="0" style="stop-color:var(--rim)" stop-opacity=".95"/><stop offset="1" style="stop-color:var(--rim)" stop-opacity="0"/></linearGradient>
        <pattern id="ns-pBrick" width="22" height="12" patternUnits="userSpaceOnUse"><path d="M0 .5H22M0 6.5H22M5 .5V6.5M16 6.5V12" stroke="#000" stroke-opacity=".1" fill="none"/></pattern>
        <pattern id="ns-pStripe" width="24" height="10" patternUnits="userSpaceOnUse"><rect width="24" height="10" fill="#ffd23d"/><path d="M12 0H22L10 10H0Z" fill="#101114"/></pattern>
        <filter id="ns-fBloom" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="13"/></filter>
        <filter id="ns-fSoft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="5"/></filter>
        <g id="ns-cloudShape"><ellipse cx="0" cy="0" rx="74" ry="26"/><ellipse cx="-50" cy="9" rx="46" ry="19"/><ellipse cx="54" cy="10" rx="52" ry="19"/><ellipse cx="-16" cy="-20" rx="38" ry="25"/><ellipse cx="26" cy="-13" rx="34" ry="21"/></g>
      </defs>

      <!-- plane 0: sky -->
      <g class="pl" data-d="0.05">
        <rect x="-500" y="-400" width="2700" height="1400" fill="url(#ns-gSky)"/>
        <ellipse id="ns-horizonGlow" cx="1120" cy="650" rx="760" ry="230" fill="url(#ns-gHorizon)"/>
        <g id="ns-stars"><path d="M1547 54h0M-132 424h0M668 -4h0M1407 71h0M1883 278h0M578 288h0M724 274h0M350 178h0M1830 483h0M-145 -35h0M698 402h0M225 -1h0M1645 232h0M1699 59h0M219 535h0M927 -48h0M938 496h0M-184 418h0M-152 -2h0M1854 353h0M1984 -59h0M24 482h0M1528 5h0M585 116h0M1288 495h0M673 353h0M923 64h0M1915 164h0M826 244h0M-19 535h0M-23 258h0M-207 135h0M1018 220h0M1881 -15h0M1387 20h0M459 267h0M1642 216h0M1565 200h0M657 -59h0M167 11h0M1471 264h0M-90 371h0M1187 205h0M-158 163h0M1560 378h0M1792 233h0" stroke="#fff" stroke-width="1.4" stroke-linecap="round" opacity="0.5"/><path d="M15 38h0M1660 307h0M538 70h0M992 434h0M1898 312h0M1347 -27h0M1771 318h0M751 145h0M1788 509h0M131 160h0M1946 429h0M1481 260h0M1929 147h0M1045 91h0M1848 59h0M1910 108h0M226 483h0M1673 398h0M-264 195h0M1381 328h0M1810 225h0M719 132h0M-244 43h0M829 487h0M129 -58h0M1049 36h0M87 203h0M1754 -59h0M217 554h0M1118 312h0M264 103h0M34 439h0M984 277h0M1229 484h0" stroke="#fff" stroke-width="2.2" stroke-linecap="round" opacity="0.7"/><path d="M860 97h0M708 -33h0M202 332h0M1884 502h0M488 499h0M216 110h0M-10 459h0M726 491h0M723 325h0M-73 120h0M1147 -3h0M1212 313h0M222 358h0M393 -53h0M1023 344h0M622 173h0M1028 484h0M342 106h0" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity="0.9"/><path class="tw" d="M804 397h0M1021 144h0M-12 -50h0M512 155h0M1252 308h0M1705 455h0M1214 4h0M1494 -21h0M460 190h0M838 222h0M1527 439h0M-53 -14h0M811 359h0M-120 100h0M1415 -12h0M142 291h0" stroke="#fff" stroke-width="2.4" stroke-linecap="round" opacity="0.9"/><path class="tw tw2" d="M387 515h0M488 278h0M1569 506h0M1416 135h0M633 303h0M1832 -48h0M509 -47h0M226 558h0M1788 257h0M539 499h0M1263 324h0M938 -12h0" stroke="#fff" stroke-width="3.2" stroke-linecap="round" opacity="1"/></g>
        <g id="ns-sun"><circle r="230" fill="url(#ns-gSunGlow)"/><circle r="40" fill="#fff7dc"/></g>
        <g id="ns-moon" transform="translate(1340 168)"><circle r="170" fill="url(#ns-gMoonGlow)"/><circle r="29" fill="#f2efe2"/><circle cx="-9" cy="-7" r="6" fill="#d9d5c4" opacity=".7"/><circle cx="9" cy="8" r="8" fill="#d9d5c4" opacity=".55"/><circle cx="8" cy="-13" r="3.5" fill="#d9d5c4" opacity=".6"/></g>
      </g>

      <!-- plane 1: clouds -->
      <g class="pl" data-d="0.14">
        <g id="ns-farClouds" class="cl">
          <ellipse cx="260" cy="330" rx="250" ry="12" opacity=".35"/><ellipse cx="420" cy="350" rx="160" ry="8" opacity=".3"/>
          <ellipse cx="1500" cy="300" rx="220" ry="10" opacity=".3"/><ellipse cx="640" cy="118" rx="130" ry="7" opacity=".22"/>
        </g>
        <g id="ns-cloud" transform="translate(1085 262)">
          <use href="#ns-cloudShape" class="cl-glow" filter="url(#ns-fBloom)"/>
          <ellipse cx="0" cy="17" rx="98" ry="13" class="cl-sh"/>
          <use href="#ns-cloudShape" class="cl"/>
          <path d="M-52 -28Q-30 -50 -6 -42Q16 -40 30 -30" class="cl-rim"/>
          <g class="cl-icon"><path d="M-14 4a9 9 0 0 1 2-17 12 12 0 0 1 23 2 8 8 0 0 1 2 15z" /><path d="M-5 -4l4 4 7-8" class="cl-check"/></g>
        </g>
      </g>

      <!-- plane 2: distant skyline -->
      <g class="pl" data-d="0.26">
        <path d="M-500 600C-250 560 -60 590 140 574S520 540 760 580S1180 550 1420 572S1900 560 2200 596V700H-500Z" style="fill:var(--far2)"/>
        <g id="ns-skyline"><path d="M-420 533h76v132h-76zM-382 519h2v14h-2zM-341 516h33v149h-33zM-325 502h2v14h-2zM-306 522h34v143h-34zM-269 560h49v105h-49zM-218 506h30v159h-30zM-185 514h71v151h-71zM-112 556h35v109h-35zM-95 542h2v14h-2zM-63 548h27v117h-27zM-34 549h26v116h-26zM-22 535h2v14h-2zM8 555h26v110h-26zM20 541h2v14h-2zM37 502h51v163h-51zM62 488h2v14h-2zM91 568h57v97h-57zM150 569h55v96h-55zM207 497h62v168h-62zM271 586h66v79h-66zM343 529h53v136h-53zM398 546h32v119h-32zM413 532h2v14h-2zM433 537h58v128h-58zM493 540h56v125h-56zM551 566h72v99h-72zM626 585h31v80h-31zM659 572h62v93h-62zM724 590h33v75h-33zM759 592h44v73h-44zM805 566h28v99h-28zM818 552h2v14h-2zM835 570h45v95h-45zM896 555h46v110h-46zM918 541h2v14h-2zM944 594h77v71h-77zM1024 587h40v78h-40zM1066 566h61v99h-61zM1130 568h28v97h-28zM1160 568h44v97h-44zM1207 575h27v90h-27zM1220 561h2v14h-2zM1237 572h47v93h-47zM1259 558h2v14h-2zM1286 562h44v103h-44zM1332 597h73v68h-73zM1368 583h2v14h-2zM1425 576h59v89h-59zM1486 585h73v80h-73zM1562 557h39v108h-39zM1580 543h2v14h-2zM1618 520h68v145h-68zM1689 547h28v118h-28zM1702 533h2v14h-2zM1731 502h27v163h-27zM1743 488h2v14h-2zM1775 575h63v90h-63zM1805 561h2v14h-2zM1840 570h46v95h-46zM1888 571h43v94h-43zM1932 523h40v142h-40zM1951 509h2v14h-2zM1975 519h72v146h-72zM2010 505h2v14h-2zM2049 539h31v126h-31zM2083 509h51v156h-51zM2107 495h2v14h-2z" style="fill:var(--far)"/><path class="sw" d="M-415 539h3v4h-3zM-391 539h3v4h-3zM-383 539h3v4h-3zM-375 539h3v4h-3zM-359 539h3v4h-3zM-351 548h3v4h-3zM-407 557h3v4h-3zM-351 557h3v4h-3zM-375 566h3v4h-3zM-415 575h3v4h-3zM-407 575h3v4h-3zM-383 575h3v4h-3zM-367 575h3v4h-3zM-415 584h3v4h-3zM-367 593h3v4h-3zM-351 593h3v4h-3zM-328 549h3v4h-3zM-336 567h3v4h-3zM-328 576h3v4h-3zM-320 576h3v4h-3zM-285 528h3v4h-3zM-301 537h3v4h-3zM-285 537h3v4h-3zM-301 546h3v4h-3zM-293 555h3v4h-3zM-293 564h3v4h-3zM-285 564h3v4h-3zM-285 573h3v4h-3zM-293 591h3v4h-3zM-248 575h3v4h-3zM-240 584h3v4h-3zM-232 593h3v4h-3zM-197 512h3v4h-3zM-205 539h3v4h-3zM-197 539h3v4h-3zM-213 548h3v4h-3zM-213 557h3v4h-3zM-197 557h3v4h-3zM-205 575h3v4h-3zM-197 575h3v4h-3zM-213 584h3v4h-3zM-172 529h3v4h-3zM-148 529h3v4h-3zM-140 529h3v4h-3zM-164 547h3v4h-3zM-156 547h3v4h-3zM-164 556h3v4h-3zM-156 556h3v4h-3zM-148 556h3v4h-3zM-156 565h3v4h-3zM-140 565h3v4h-3zM-172 574h3v4h-3zM-140 574h3v4h-3zM-124 574h3v4h-3zM-172 583h3v4h-3zM-91 562h3v4h-3zM-99 571h3v4h-3zM-99 589h3v4h-3zM-50 563h3v4h-3zM-50 572h3v4h-3zM-42 572h3v4h-3zM-58 581h3v4h-3zM-42 581h3v4h-3zM-21 564h3v4h-3zM-29 573h3v4h-3zM-21 573h3v4h-3zM-29 582h3v4h-3zM13 597h3v4h-3zM29 597h3v4h-3zM50 508h3v4h-3zM66 517h3v4h-3zM82 517h3v4h-3zM42 526h3v4h-3zM66 526h3v4h-3zM74 526h3v4h-3zM50 535h3v4h-3zM82 535h3v4h-3zM66 544h3v4h-3zM74 544h3v4h-3zM42 562h3v4h-3zM58 571h3v4h-3zM82 571h3v4h-3zM58 580h3v4h-3zM66 580h3v4h-3zM74 580h3v4h-3zM58 589h3v4h-3zM42 598h3v4h-3zM50 598h3v4h-3zM82 598h3v4h-3zM96 574h3v4h-3zM136 574h3v4h-3zM104 583h3v4h-3zM112 583h3v4h-3zM128 583h3v4h-3zM120 592h3v4h-3zM155 575h3v4h-3zM195 575h3v4h-3zM155 584h3v4h-3zM195 584h3v4h-3zM155 593h3v4h-3zM187 593h3v4h-3zM195 593h3v4h-3zM212 503h3v4h-3zM244 503h3v4h-3zM260 503h3v4h-3zM220 512h3v4h-3zM212 521h3v4h-3zM220 521h3v4h-3zM220 530h3v4h-3zM228 530h3v4h-3zM228 539h3v4h-3zM244 539h3v4h-3zM228 548h3v4h-3zM252 548h3v4h-3zM260 548h3v4h-3zM228 557h3v4h-3zM236 557h3v4h-3zM244 557h3v4h-3zM236 566h3v4h-3zM260 566h3v4h-3zM252 584h3v4h-3zM260 593h3v4h-3zM308 592h3v4h-3zM364 544h3v4h-3zM388 544h3v4h-3zM380 553h3v4h-3zM388 553h3v4h-3zM364 562h3v4h-3zM380 562h3v4h-3zM388 562h3v4h-3zM372 571h3v4h-3zM356 598h3v4h-3zM403 570h3v4h-3zM419 570h3v4h-3zM411 588h3v4h-3zM403 597h3v4h-3zM470 543h3v4h-3zM478 543h3v4h-3zM486 543h3v4h-3zM470 552h3v4h-3zM446 561h3v4h-3zM462 561h3v4h-3zM470 561h3v4h-3zM462 570h3v4h-3zM470 570h3v4h-3zM438 579h3v4h-3zM446 579h3v4h-3zM446 588h3v4h-3zM478 588h3v4h-3zM438 597h3v4h-3zM454 597h3v4h-3zM498 546h3v4h-3zM498 555h3v4h-3zM514 555h3v4h-3zM522 564h3v4h-3zM498 573h3v4h-3zM514 573h3v4h-3zM522 582h3v4h-3zM498 591h3v4h-3zM514 591h3v4h-3zM538 591h3v4h-3zM564 572h3v4h-3zM572 572h3v4h-3zM604 572h3v4h-3zM612 572h3v4h-3zM556 581h3v4h-3zM580 581h3v4h-3zM604 581h3v4h-3zM556 590h3v4h-3zM580 590h3v4h-3zM588 590h3v4h-3zM612 599h3v4h-3zM672 587h3v4h-3zM680 587h3v4h-3zM688 587h3v4h-3zM704 587h3v4h-3zM680 596h3v4h-3zM772 598h3v4h-3zM780 598h3v4h-3zM818 572h3v4h-3zM826 581h3v4h-3zM826 590h3v4h-3zM810 599h3v4h-3zM872 576h3v4h-3zM848 585h3v4h-3zM856 585h3v4h-3zM864 585h3v4h-3zM840 594h3v4h-3zM856 594h3v4h-3zM864 594h3v4h-3zM909 561h3v4h-3zM925 561h3v4h-3zM901 570h3v4h-3zM901 579h3v4h-3zM901 597h3v4h-3zM1071 581h3v4h-3zM1103 581h3v4h-3zM1087 590h3v4h-3zM1087 599h3v4h-3zM1151 574h3v4h-3zM1143 583h3v4h-3zM1135 592h3v4h-3zM1143 592h3v4h-3zM1151 592h3v4h-3zM1197 583h3v4h-3zM1228 599h3v4h-3zM1242 578h3v4h-3zM1274 578h3v4h-3zM1274 596h3v4h-3zM1291 577h3v4h-3zM1299 577h3v4h-3zM1307 586h3v4h-3zM1430 582h3v4h-3zM1438 582h3v4h-3zM1462 582h3v4h-3zM1478 582h3v4h-3zM1438 591h3v4h-3zM1491 591h3v4h-3zM1499 591h3v4h-3zM1523 591h3v4h-3zM1531 591h3v4h-3zM1547 591h3v4h-3zM1567 563h3v4h-3zM1575 563h3v4h-3zM1567 572h3v4h-3zM1583 572h3v4h-3zM1583 581h3v4h-3zM1591 590h3v4h-3zM1639 526h3v4h-3zM1671 526h3v4h-3zM1631 535h3v4h-3zM1671 535h3v4h-3zM1679 535h3v4h-3zM1631 544h3v4h-3zM1655 544h3v4h-3zM1631 553h3v4h-3zM1639 553h3v4h-3zM1623 562h3v4h-3zM1647 562h3v4h-3zM1655 562h3v4h-3zM1671 562h3v4h-3zM1679 562h3v4h-3zM1639 571h3v4h-3zM1631 580h3v4h-3zM1623 589h3v4h-3zM1631 589h3v4h-3zM1639 589h3v4h-3zM1655 589h3v4h-3zM1679 598h3v4h-3zM1702 562h3v4h-3zM1710 580h3v4h-3zM1710 598h3v4h-3zM1736 535h3v4h-3zM1744 535h3v4h-3zM1744 553h3v4h-3zM1736 562h3v4h-3zM1744 562h3v4h-3zM1752 562h3v4h-3zM1736 571h3v4h-3zM1752 580h3v4h-3zM1744 589h3v4h-3zM1736 598h3v4h-3zM1744 598h3v4h-3zM1752 598h3v4h-3zM1812 581h3v4h-3zM1780 590h3v4h-3zM1812 599h3v4h-3zM1845 576h3v4h-3zM1869 576h3v4h-3zM1853 585h3v4h-3zM1869 594h3v4h-3zM1925 577h3v4h-3zM1909 586h3v4h-3zM1925 586h3v4h-3zM1893 595h3v4h-3zM1945 529h3v4h-3zM1961 538h3v4h-3zM1945 547h3v4h-3zM1945 556h3v4h-3zM1953 556h3v4h-3zM1945 565h3v4h-3zM1961 592h3v4h-3zM1980 525h3v4h-3zM2020 525h3v4h-3zM1988 534h3v4h-3zM2036 543h3v4h-3zM1980 552h3v4h-3zM2004 570h3v4h-3zM1988 579h3v4h-3zM2028 579h3v4h-3zM1980 588h3v4h-3zM2012 597h3v4h-3zM2036 597h3v4h-3zM2054 581h3v4h-3zM2062 581h3v4h-3zM2062 590h3v4h-3zM2070 590h3v4h-3zM2088 515h3v4h-3zM2112 515h3v4h-3zM2112 524h3v4h-3zM2088 533h3v4h-3zM2104 533h3v4h-3zM2112 542h3v4h-3zM2096 560h3v4h-3zM2128 560h3v4h-3zM2104 569h3v4h-3zM2112 569h3v4h-3zM2088 578h3v4h-3zM2088 587h3v4h-3zM2104 587h3v4h-3zM2096 596h3v4h-3zM2104 596h3v4h-3zM2112 596h3v4h-3z"/></g>
        <g style="fill:var(--far)"><rect x="150" y="512" width="5" height="70"/><rect x="186" y="512" width="5" height="70"/><path d="M138 480h64l-6 34h-52z"/><path d="M146 480q24-22 48 0z"/></g>
      </g>

      <!-- plane 3: treeline and far fog -->
      <g class="pl" data-d="0.42">
        <g id="ns-treeline"><circle cx="-420" cy="623" r="36"/><circle cx="-379" cy="617" r="36"/><circle cx="-338" cy="613" r="31"/><circle cx="-297" cy="617" r="49"/><circle cx="-256" cy="616" r="46"/><circle cx="-215" cy="610" r="43"/><circle cx="-174" cy="621" r="28"/><circle cx="-133" cy="625" r="36"/><circle cx="-92" cy="614" r="35"/><circle cx="-51" cy="624" r="36"/><circle cx="-10" cy="624" r="32"/><circle cx="31" cy="624" r="34"/><circle cx="72" cy="610" r="30"/><circle cx="113" cy="622" r="42"/><circle cx="154" cy="615" r="24"/><circle cx="195" cy="617" r="38"/><circle cx="236" cy="620" r="34"/><circle cx="277" cy="625" r="34"/><circle cx="318" cy="613" r="26"/><circle cx="359" cy="620" r="38"/><circle cx="400" cy="619" r="49"/><circle cx="441" cy="613" r="33"/><circle cx="482" cy="612" r="25"/><circle cx="523" cy="613" r="44"/><circle cx="564" cy="612" r="47"/><circle cx="605" cy="624" r="29"/><circle cx="646" cy="614" r="47"/><circle cx="687" cy="622" r="41"/><circle cx="728" cy="623" r="41"/><circle cx="769" cy="617" r="27"/><circle cx="810" cy="627" r="41"/><circle cx="851" cy="623" r="26"/><circle cx="892" cy="618" r="41"/><circle cx="933" cy="614" r="29"/><circle cx="974" cy="613" r="34"/><circle cx="1015" cy="625" r="35"/><circle cx="1056" cy="611" r="38"/><circle cx="1097" cy="618" r="34"/><circle cx="1138" cy="613" r="32"/><circle cx="1179" cy="624" r="47"/><circle cx="1220" cy="627" r="42"/><circle cx="1261" cy="625" r="40"/><circle cx="1302" cy="625" r="43"/><circle cx="1343" cy="623" r="25"/><circle cx="1384" cy="612" r="44"/><circle cx="1425" cy="624" r="35"/><circle cx="1466" cy="611" r="25"/><circle cx="1507" cy="615" r="28"/><circle cx="1548" cy="623" r="24"/><circle cx="1589" cy="616" r="46"/><circle cx="1630" cy="619" r="25"/><circle cx="1671" cy="618" r="32"/><circle cx="1712" cy="627" r="41"/><circle cx="1753" cy="612" r="37"/><circle cx="1794" cy="619" r="26"/><circle cx="1835" cy="616" r="28"/><circle cx="1876" cy="623" r="48"/><circle cx="1917" cy="616" r="41"/><circle cx="1958" cy="612" r="26"/><circle cx="1999" cy="610" r="27"/><circle cx="2040" cy="614" r="34"/><circle cx="2081" cy="611" r="38"/></g>
        <rect x="-500" y="628" width="2700" height="60" style="fill:var(--treeFar)"/>
        <ellipse class="fog fogA" cx="700" cy="628" rx="820" ry="70" fill="url(#ns-gFog)"/>
        <ellipse class="fog fogB" cx="1500" cy="640" rx="620" ry="54" fill="url(#ns-gFog)"/>
      </g>

      <!-- plane 4: the building -->
      <g class="pl" data-d="0.68" id="ns-plB">
        <path d="M-500 652C200 640 1000 640 2200 652V720H-500Z" style="fill:var(--lawn)"/>
        <!-- tree left -->
        <g id="ns-treeL">
          <rect x="449" y="556" width="12" height="98" style="fill:var(--trunk)"/>
          <g style="fill:var(--tree)"><circle cx="455" cy="514" r="60"/><circle cx="410" cy="548" r="42"/><circle cx="500" cy="544" r="46"/><circle cx="452" cy="470" r="40"/></g>
          <g style="fill:var(--treeHi)"><circle cx="432" cy="486" r="26"/><circle cx="398" cy="534" r="20"/><circle cx="470" cy="456" r="18"/></g>
          
        </g>
        <!-- tree right, behind gym -->
        <g>
          <rect x="1492" y="560" width="12" height="94" style="fill:var(--trunk)"/>
          <g style="fill:var(--tree)"><circle cx="1498" cy="512" r="64"/><circle cx="1548" cy="552" r="44"/><circle cx="1458" cy="556" r="38"/><circle cx="1510" cy="462" r="38"/></g>
          <g style="fill:var(--treeHi)"><circle cx="1476" cy="488" r="26"/><circle cx="1500" cy="446" r="16"/></g>
        </g>

        <!-- gym wing -->
        <g id="ns-gym">
          <rect x="1180" y="455" width="272" height="197" style="fill:var(--wallC)"/>
          <rect x="1180" y="455" width="272" height="197" fill="url(#ns-pBrick)"/>
          <rect x="1180" y="455" width="272" height="197" fill="url(#ns-gFace)"/>
          <rect x="1176" y="447" width="280" height="9" style="fill:var(--trim)"/>
          <rect x="1180" y="456" width="272" height="16" fill="url(#ns-gDrop)"/>
          <rect x="1180" y="532" width="272" height="5" style="fill:var(--wallB)" opacity=".5"/>
          <rect x="1338" y="584" width="36" height="68" style="fill:var(--trim)"/>
          <rect x="1343" y="590" width="26" height="24" class="w-off"/>
          <rect x="1366" y="622" width="4" height="10" fill="#ffd23d" opacity=".8"/>
          <g class="nightglow"><circle cx="1356" cy="574" r="46" fill="url(#ns-gWarm)"/><path d="M1340 580L1372 580L1396 652L1316 652Z" fill="url(#ns-gSpill)"/></g>
          <rect x="1349" y="570" width="14" height="6" rx="2" class="lampHead"/>
        </g>

        <!-- main block -->
        <g id="ns-main">
          <rect x="600" y="385" width="260" height="267" style="fill:var(--wallA)"/>
          <rect x="940" y="385" width="240" height="267" style="fill:var(--wallA)"/>
          <rect x="600" y="385" width="580" height="267" fill="url(#ns-pBrick)"/>
          <rect x="940" y="385" width="240" height="267" fill="url(#ns-gFace)"/>
          <rect x="600" y="385" width="260" height="267" fill="url(#ns-gFace)" opacity=".45"/>
          <rect x="600" y="386" width="580" height="18" fill="url(#ns-gDrop)"/>
          <rect x="600" y="518" width="580" height="7" style="fill:var(--wallB)" opacity=".7"/>
          <rect x="594" y="377" width="272" height="9" style="fill:var(--trim)"/>
          <rect x="934" y="377" width="252" height="9" style="fill:var(--trim)"/>
          <!-- roof kit -->
          <rect x="1030" y="356" width="72" height="22" style="fill:var(--trim)"/><rect x="1038" y="350" width="22" height="7" style="fill:var(--trim)"/>
          <path d="M1040 362h52M1040 367h52M1040 372h52" stroke="#000" stroke-opacity=".3"/>
          <rect x="960" y="366" width="26" height="12" style="fill:var(--trim)"/>
          <g id="ns-mast">
            <rect x="747" y="360" width="26" height="18" rx="2" style="fill:var(--wallB)"/>
            <rect x="751" y="364" width="8" height="4" fill="#ffd23d"/>
            <path d="M760 360V314M750 330h20M753 340h14" style="stroke:var(--trim)" stroke-width="3" fill="none"/>
            <circle id="ns-mastTip" cx="760" cy="312" r="3.4" class="led"/>
            <circle cx="760" cy="312" r="16" fill="url(#ns-gHalo)" class="ledGlow"/>
          </g>
          <!-- stair tower -->
          <rect x="860" y="335" width="80" height="317" style="fill:var(--wallB)"/>
          <rect x="860" y="335" width="80" height="317" fill="url(#ns-gFace)" opacity=".5"/>
          <rect x="854" y="327" width="92" height="9" style="fill:var(--trim)"/>
          <g class="bloom"><rect x="872" y="352" width="56" height="196"/><rect x="872" y="570" width="56" height="82"/></g>
          <rect x="872" y="352" width="56" height="196" class="w-hot"/>
          <g style="stroke:var(--trim)" stroke-width="3" fill="none" opacity=".85">
            <path d="M872 401H928M872 450H928M872 499H928M900 352V548"/>
            <path d="M876 548L924 499L876 450L924 401L876 352" stroke-width="5" opacity=".55"/>
          </g>
          <!-- entrance -->
          <rect x="868" y="568" width="64" height="84" style="fill:var(--trim)"/>
          <rect x="873" y="573" width="25" height="79" class="w-hot"/><rect x="902" y="573" width="25" height="79" class="w-hot"/>
          <path d="M894 610v14M906 610v14" style="stroke:var(--trim)" stroke-width="3"/>
          <rect x="834" y="556" width="132" height="9" style="fill:var(--trim)"/>
          <rect x="934" y="590" width="7" height="12" rx="1.5" fill="#15171c"/><circle cx="937.5" cy="594" r="1.6" fill="#ffd23d"/>
          <g class="nightglow"><path d="M868 652L932 652L986 700L814 700Z" fill="url(#ns-gSpill)"/><ellipse cx="900" cy="566" rx="70" ry="16" fill="url(#ns-gWarm)" opacity=".6"/></g>
          <g id="ns-wins"><g class="bloom"><rect x="680" y="548" width="44" height="72"></rect><rect x="622" y="420" width="44" height="72"></rect><rect x="738" y="420" width="44" height="72"></rect><rect x="738" y="548" width="44" height="72"></rect><rect x="1012" y="420" width="44" height="72"></rect><rect x="1120" y="420" width="44" height="72"></rect><rect x="958" y="548" width="44" height="72"></rect><rect x="1252" y="482" width="38" height="30"></rect><rect x="1304" y="482" width="38" height="30"></rect></g><g class="nightglow"><path d="M738 652h44l22 44h-88z" fill="url(#ns-gSpill)" opacity="0.7"></path><path d="M958 652h44l22 44h-88z" fill="url(#ns-gSpill)" opacity="0.7"></path></g><rect x="618" y="416" width="52" height="80" style="fill:var(--trim)"></rect><rect x="622" y="420" width="44" height="72" class="w-lit"></rect><rect x="634" y="470" width="14" height="22" class="ws"></rect><path d="M644 420v72M622 456h44" class="wm"></path><rect x="616" y="496" width="56" height="4" style="fill:var(--wallB)" opacity="0.8"></rect><rect x="676" y="416" width="52" height="80" style="fill:var(--trim)"></rect><rect x="680" y="420" width="44" height="72" class="w-off"></rect><path d="M702 420v72M680 456h44" class="wm"></path><rect x="674" y="496" width="56" height="4" style="fill:var(--wallB)" opacity="0.8"></rect><rect x="734" y="416" width="52" height="80" style="fill:var(--trim)"></rect><rect x="738" y="420" width="44" height="72" class="w-lit"></rect><path d="M738 425h44M738 431h44M738 437h44M738 443h44M738 449h44M738 455h44M738 461h44" class="wb"></path><rect x="744" y="470" width="14" height="22" class="ws"></rect><path d="M760 420v72M738 456h44" class="wm"></path><rect x="732" y="496" width="56" height="4" style="fill:var(--wallB)" opacity="0.8"></rect><rect x="792" y="416" width="52" height="80" style="fill:var(--trim)"></rect><rect x="796" y="420" width="44" height="72" class="w-off"></rect><path d="M818 420v72M796 456h44" class="wm"></path><rect x="790" y="496" width="56" height="4" style="fill:var(--wallB)" opacity="0.8"></rect><rect x="618" y="544" width="52" height="80" style="fill:var(--trim)"></rect><rect x="622" y="548" width="44" height="72" class="w-off"></rect><path d="M644 548v72M622 584h44" class="wm"></path><rect x="616" y="624" width="56" height="4" style="fill:var(--wallB)" opacity="0.8"></rect><rect x="734" y="544" width="52" height="80" style="fill:var(--trim)"></rect><rect x="738" y="548" width="44" height="72" class="w-lit"></rect><rect x="744" y="598" width="14" height="22" class="ws"></rect><path d="M760 548v72M738 584h44" class="wm"></path><rect x="732" y="624" width="56" height="4" style="fill:var(--wallB)" opacity="0.8"></rect><rect x="792" y="544" width="52" height="80" style="fill:var(--trim)"></rect><rect x="796" y="548" width="44" height="72" class="w-off"></rect><path d="M796 553h44M796 559h44M796 565h44M796 571h44M796 577h44M796 583h44M796 589h44" class="wb"></path><path d="M818 548v72M796 584h44" class="wm"></path><rect x="790" y="624" width="56" height="4" style="fill:var(--wallB)" opacity="0.8"></rect><rect x="954" y="416" width="52" height="80" style="fill:var(--trim)"></rect><rect x="958" y="420" width="44" height="72" class="w-off"></rect><path d="M980 420v72M958 456h44" class="wm"></path><rect x="952" y="496" width="56" height="4" style="fill:var(--wallB)" opacity="0.8"></rect><rect x="1008" y="416" width="52" height="80" style="fill:var(--trim)"></rect><rect x="1012" y="420" width="44" height="72" class="w-lit"></rect><rect x="1024" y="470" width="14" height="22" class="ws"></rect><path d="M1034 420v72M1012 456h44" class="wm"></path><rect x="1006" y="496" width="56" height="4" style="fill:var(--wallB)" opacity="0.8"></rect><rect x="1062" y="416" width="52" height="80" style="fill:var(--trim)"></rect><rect x="1066" y="420" width="44" height="72" class="w-off"></rect><path d="M1088 420v72M1066 456h44" class="wm"></path><rect x="1060" y="496" width="56" height="4" style="fill:var(--wallB)" opacity="0.8"></rect><rect x="1116" y="416" width="52" height="80" style="fill:var(--trim)"></rect><rect x="1120" y="420" width="44" height="72" class="w-lit"></rect><path d="M1120 425h44M1120 431h44M1120 437h44M1120 443h44M1120 449h44M1120 455h44M1120 461h44" class="wb"></path><rect x="1132" y="470" width="14" height="22" class="ws"></rect><path d="M1142 420v72M1120 456h44" class="wm"></path><rect x="1114" y="496" width="56" height="4" style="fill:var(--wallB)" opacity="0.8"></rect><rect x="954" y="544" width="52" height="80" style="fill:var(--trim)"></rect><rect x="958" y="548" width="44" height="72" class="w-lit"></rect><rect x="970" y="598" width="14" height="22" class="ws"></rect><path d="M980 548v72M958 584h44" class="wm"></path><rect x="952" y="624" width="56" height="4" style="fill:var(--wallB)" opacity="0.8"></rect><rect x="1030" y="544" width="52" height="80" style="fill:var(--trim)"></rect><rect x="1034" y="548" width="44" height="72" class="w-off"></rect><path d="M1056 548v72M1034 584h44" class="wm"></path><rect x="1028" y="624" width="56" height="4" style="fill:var(--wallB)" opacity="0.8"></rect><rect x="1196" y="478" width="46" height="38" style="fill:var(--trim)"></rect><rect x="1200" y="482" width="38" height="30" class="w-off"></rect><path d="M1219 482v30" class="wm"></path><rect x="1194" y="516" width="50" height="4" style="fill:var(--wallB)" opacity="0.8"></rect><rect x="1248" y="478" width="46" height="38" style="fill:var(--trim)"></rect><rect x="1252" y="482" width="38" height="30" class="w-lit"></rect><path d="M1271 482v30" class="wm"></path><rect x="1246" y="516" width="50" height="4" style="fill:var(--wallB)" opacity="0.8"></rect><rect x="1300" y="478" width="46" height="38" style="fill:var(--trim)"></rect><rect x="1304" y="482" width="38" height="30" class="w-lit"></rect><path d="M1323 482v30" class="wm"></path><rect x="1298" y="516" width="50" height="4" style="fill:var(--wallB)" opacity="0.8"></rect><rect x="1352" y="478" width="46" height="38" style="fill:var(--trim)"></rect><rect x="1356" y="482" width="38" height="30" class="w-off"></rect><path d="M1375 482v30" class="wm"></path><rect x="1350" y="516" width="50" height="4" style="fill:var(--wallB)" opacity="0.8"></rect><rect x="1404" y="478" width="46" height="38" style="fill:var(--trim)"></rect><rect x="1408" y="482" width="38" height="30" class="w-off"></rect><path d="M1427 482v30" class="wm"></path><rect x="1402" y="516" width="50" height="4" style="fill:var(--wallB)" opacity="0.8"></rect></g>
          <!-- panel room -->
          <g id="ns-panelRoom">
            <rect x="1108" y="544" width="60" height="80" style="fill:var(--trim)"/>
            <rect x="1112" y="548" width="52" height="72" class="w-panel"/>
            <rect x="1124" y="562" width="28" height="38" rx="2" fill="#8d939e"/><rect x="1124" y="562" width="28" height="38" rx="2" fill="none" stroke="#2a2d36"/>
            <rect x="1129" y="568" width="10" height="5" fill="#ffd23d"/><circle cx="1146" cy="592" r="2" class="led"/>
            <path d="M1138 600V620M1132 600V612H1118V620" stroke="#2a2d36" stroke-width="1.5" fill="none"/>
            <circle class="panelGlow" cx="1138" cy="582" r="40" fill="url(#ns-gHalo)"/>
          </g>
          <!-- break window -->
          <g id="ns-breakWin">
            <rect x="676" y="544" width="52" height="80" style="fill:var(--trim)"/>
            <rect x="680" y="548" width="44" height="72" class="w-lit bw-glass"/>
            <path d="M702 548V620M680 584H724" style="stroke:var(--trim)" stroke-width="2.5"/>
            <g class="bw-broken">
              <polygon points="687,556 703,552 718,563 713,584 721,600 705,611 690,604 684,584" fill="#04060c"/>
              <path d="M687 556L680 549M718 563L724 556M721 600L724 612M690 604L681 616M705 611L706 620M684 584L680 580M713 584L724 580" stroke="#fff" stroke-opacity=".85" stroke-width="1.1" fill="none"/>
            </g>
            <g class="shards" fill="#e9f3ff">
              <polygon points="690,580 698,572 696,588"/><polygon points="706,566 714,574 704,578"/><polygon points="700,596 710,590 708,604"/><polygon points="694,560 700,566 692,568"/><polygon points="712,596 718,590 716,602"/><polygon points="702,582 708,586 700,590"/>
            </g>
            
            <rect x="718" y="552" width="5" height="9" rx="1" fill="#f2f2f2"/>
          </g>
          <!-- rim light -->
          <g class="rim">
            <rect x="594" y="377" width="272" height="2"/><rect x="934" y="377" width="252" height="2"/><rect x="854" y="327" width="92" height="2"/><rect x="1176" y="447" width="280" height="2"/>
            <rect x="600" y="386" width="2" height="266" opacity=".6"/><rect x="860" y="336" width="2" height="50" opacity=".6"/><rect x="1030" y="356" width="72" height="1.5" opacity=".7"/>
          </g>
          <!-- hotspots on building plane -->
          <g class="hs" id="ns-hs-roof" data-k="roof" tabindex="0" role="button" aria-label="Roof: 263LTE cellular communicator" transform="translate(760 340)"><circle class="hs-hit" r="34"/><circle class="hs-halo" r="34"/><circle class="hs-ping" r="13"/><circle class="hs-focus" r="21"/><circle class="hs-ring" r="13"/><circle class="hs-dot" r="5"/></g>
          <g class="hs" id="ns-hs-stair" data-k="stair" tabindex="0" role="button" aria-label="Stairwell: XF6 fire control panel" transform="translate(900 426)"><circle class="hs-hit" r="34"/><circle class="hs-halo" r="34"/><circle class="hs-ping" r="13"/><circle class="hs-focus" r="21"/><circle class="hs-ring" r="13"/><circle class="hs-dot" r="5"/></g>
          <g class="hs" id="ns-hs-win" data-k="win" tabindex="0" role="button" aria-label="Windows: 1128 glassbreak detector" transform="translate(702 584)"><circle class="hs-hit" r="34"/><circle class="hs-halo" r="34"/><circle class="hs-ping" r="13"/><circle class="hs-focus" r="21"/><circle class="hs-ring" r="13"/><circle class="hs-dot" r="5"/></g>
          <g class="hs" id="ns-hs-door" data-k="door" tabindex="0" role="button" aria-label="Main door: X1 single-door access controller" transform="translate(900 612)"><circle class="hs-hit" r="34"/><circle class="hs-halo" r="34"/><circle class="hs-ping" r="13"/><circle class="hs-focus" r="21"/><circle class="hs-ring" r="13"/><circle class="hs-dot" r="5"/></g>
          <g class="hs" id="ns-hs-panel" data-k="panel" tabindex="0" role="button" aria-label="Panel room: XR550 control panel" transform="translate(1138 582)"><circle class="hs-hit" r="34"/><circle class="hs-halo" r="34"/><circle class="hs-ping" r="13"/><circle class="hs-focus" r="21"/><circle class="hs-ring" r="13"/><circle class="hs-dot" r="5"/></g>
          <g class="hs" id="ns-hs-side" data-k="side" tabindex="0" role="button" aria-label="Side entrance: Digital Key credential" transform="translate(1356 618)"><circle class="hs-hit" r="34"/><circle class="hs-halo" r="34"/><circle class="hs-ping" r="13"/><circle class="hs-focus" r="21"/><circle class="hs-ring" r="13"/><circle class="hs-dot" r="5"/></g>
        </g>
      </g>

      <!-- plane 5: lot, lamps, gate -->
      <g class="pl" data-d="1" id="ns-plL">
        <path d="M-500 664H2200V1100H-500Z" fill="url(#ns-gLot)"/>
        <rect x="-500" y="660" width="2700" height="11" style="fill:var(--walk)"/>
        <g id="ns-lotLines" style="stroke:var(--paint)" stroke-width="3" opacity=".7" fill="none"><path d="M430 772L237 940"></path><path d="M550 772L407 940"></path><path d="M670 772L578 940"></path><path d="M790 772L748 940"></path><path d="M910 772L918 940"></path><path d="M1030 772L1089 940"></path><path d="M1150 772L1259 940"></path><path d="M1270 772L1430 940"></path><path d="M1390 772L1600 940"></path></g>
        <path d="M-500 760H2200" style="stroke:var(--paint)" stroke-width="2" stroke-dasharray="46 40" opacity=".28"/>
        <!-- lamp pools and cones -->
        <g class="nightglow">
          <ellipse cx="580" cy="708" rx="150" ry="20" fill="url(#ns-gPool)"/>
          <ellipse cx="1224" cy="716" rx="150" ry="20" fill="url(#ns-gPool)"/>
          <g filter="url(#ns-fSoft)"><polygon points="570,470 588,470 706,708 454,708" fill="url(#ns-gCone)"/><polygon points="1215,478 1233,478 1350,716 1098,716" fill="url(#ns-gCone)"/></g>
          <circle cx="579" cy="470" r="42" fill="url(#ns-gWarm)"/><circle cx="1224" cy="478" r="42" fill="url(#ns-gWarm)"/>
        </g>
        <!-- car -->
        <g id="ns-car">
          <ellipse cx="1018" cy="742" rx="100" ry="7" fill="#000" opacity=".35"/>
          <path d="M930 738V716Q934 706 952 703L975 684Q982 678 995 678H1048Q1060 678 1068 686L1086 704Q1102 706 1104 716V738Z" style="fill:var(--car)"/>
          <path d="M960 703L979 687Q984 683 994 683H1014V703ZM1020 683H1046Q1056 683 1062 689L1076 703H1020Z" class="w-off"/>
          <circle cx="960" cy="738" r="12" fill="#06070b"/><circle cx="1074" cy="738" r="12" fill="#06070b"/><circle cx="960" cy="738" r="5" fill="#3a3d47"/><circle cx="1074" cy="738" r="5" fill="#3a3d47"/>
          <path d="M952 703L975 684Q982 678 995 678H1048Q1060 678 1068 686L1086 704Q1102 706 1104 716" class="rimline"/>
          <rect x="929" y="712" width="4" height="9" fill="#ff4a3d" class="tail"/>
        </g>
        <!-- lamps -->
        <g style="fill:var(--trim)">
          <rect x="545" y="470" width="5" height="236"/><path d="M546 474Q552 462 580 464V469Q556 468 550 478Z"/><rect x="540" y="700" width="15" height="8"/>
          <rect x="1250" y="478" width="5" height="236"/><path d="M1254 482Q1248 470 1222 472V477Q1244 476 1250 486Z"/><rect x="1245" y="708" width="15" height="8"/>
        </g>
        <rect x="566" y="462" width="26" height="7" rx="3" class="lampHead"/><rect x="1211" y="470" width="26" height="7" rx="3" class="lampHead"/>
        <path d="M545 470V706" class="rimline"/><path d="M1255 478V714" class="rimline"/>
        <!-- gate -->
        <g id="ns-gate">
          <rect x="298" y="556" width="5" height="152" style="fill:var(--trim)"/>
          <g transform="translate(301 560) rotate(16)"><rect x="-4" y="-9" width="40" height="15" rx="3" fill="#e9ebef"/><rect x="30" y="-7" width="9" height="11" rx="2" fill="#15171c"/><rect x="-6" y="-12" width="38" height="4" rx="2" fill="#c9ccd3"/><circle cx="34" cy="-1.5" r="2.2" class="led"/></g>
          <polygon class="camcone" points="338,572 520,640 520,706 360,706" fill="url(#ns-gHalo)"/>
          <rect x="322" y="628" width="36" height="80" rx="2" style="fill:var(--trim)"/><rect x="326" y="636" width="28" height="8" fill="#ffd23d"/><circle cx="340" cy="656" r="3" class="led"/>
          <g transform="rotate(-2.5 356 664)"><rect x="356" y="659" width="172" height="9" rx="2" fill="url(#ns-pStripe)"/><rect x="356" y="659" width="172" height="9" rx="2" class="dim"/></g>
          <rect x="524" y="646" width="8" height="62" style="fill:var(--trim)"/>
          <path d="M300 556V708" class="rimline"/>
          <path d="M368 716H520" style="stroke:var(--paint)" stroke-width="6" opacity=".7"/>
        </g>
        <ellipse class="fog fogC" cx="900" cy="700" rx="900" ry="46" fill="url(#ns-gFog)"/>
        <g class="hs" id="ns-hs-gate" data-k="gate" tabindex="0" role="button" aria-label="Parking gate: VUE Plus bullet camera" transform="translate(338 592)"><circle class="hs-hit" r="34"/><circle class="hs-halo" r="34"/><circle class="hs-ping" r="13"/><circle class="hs-focus" r="21"/><circle class="hs-ring" r="13"/><circle class="hs-dot" r="5"/></g>
      </g>

      <!-- plane 6: foreground silhouettes -->
      <g class="pl" data-d="1.7" id="ns-plF">
        <g style="fill:var(--fg)">
          <path d="M-500 1100V832Q-420 800 -340 826Q-300 786 -236 812Q-190 770 -120 804Q-70 778 -20 812Q30 790 84 824Q130 806 176 838Q230 830 262 862Q320 862 352 900V1100Z"/>
          <path d="M1700 -60Q1560 -30 1452 36M1640 -20Q1560 30 1500 104M1560 0Q1520 -8 1470 -2" stroke-width="9" fill="none" style="stroke:var(--fg)" stroke-linecap="round"/>
          <g><ellipse cx="1452" cy="38" rx="26" ry="10" transform="rotate(-28 1452 38)"/><ellipse cx="1500" cy="106" rx="28" ry="10" transform="rotate(-52 1500 106)"/><ellipse cx="1470" cy="-2" rx="24" ry="9" transform="rotate(8 1470 -2)"/><ellipse cx="1546" cy="58" rx="26" ry="10" transform="rotate(-40 1546 58)"/><ellipse cx="1600" cy="10" rx="28" ry="10" transform="rotate(-20 1600 10)"/><ellipse cx="1520" cy="20" rx="22" ry="8" transform="rotate(-10 1520 20)"/><ellipse cx="1590" cy="70" rx="26" ry="9" transform="rotate(-60 1590 70)"/><ellipse cx="1650" cy="40" rx="30" ry="11" transform="rotate(-35 1650 40)"/></g>
          <!-- owner -->
          <path d="M1150 1100V920C1156 860 1182 824 1228 812C1244 808 1252 802 1254 792H1292C1294 802 1302 808 1318 812C1364 824 1392 864 1398 920V1100Z"/>
          <ellipse cx="1273" cy="760" rx="32" ry="37"/>
          <path d="M1180 900Q1160 850 1168 816" stroke-width="30" fill="none" style="stroke:var(--fg)" stroke-linecap="round"/>
        </g>
        <path d="M1245 742Q1252 722 1273 723Q1296 724 1302 744" class="rimline" stroke-width="2.2"/>
        <path d="M1318 812C1364 824 1392 864 1398 920" class="rimline" stroke-width="2.2"/>
        <g id="ns-phone" transform="rotate(-9 1166 786)">
          <circle class="phoneGlow" cx="1166" cy="786" r="80" fill="url(#ns-gHalo)"/>
          <rect x="1145" y="746" width="42" height="80" rx="7" fill="#07080c" stroke="#3a3d47" stroke-width="1.5"/>
          <rect x="1149" y="752" width="34" height="66" rx="3" class="phoneScreen"/>
          <rect x="1153" y="758" width="26" height="9" rx="2" fill="#ffd23d"/><rect x="1153" y="771" width="18" height="3" rx="1.5" fill="#fff" opacity=".7"/><rect x="1153" y="778" width="22" height="3" rx="1.5" fill="#fff" opacity=".4"/>
        </g>
        <g class="hs" id="ns-hs-phone" data-k="phone" tabindex="0" role="button" aria-label="Phone: Virtual Keypad" transform="translate(1166 790)"><circle class="hs-hit" r="34"/><circle class="hs-halo" r="34"/><circle class="hs-ping" r="13"/><circle class="hs-focus" r="21"/><circle class="hs-ring" r="13"/><circle class="hs-dot" r="5"/></g>
      </g>
    </svg>

    <div class="fx scrim" aria-hidden="true"></div>
    <div class="fx vignette" aria-hidden="true"></div>
    <div class="fx wash" aria-hidden="true"></div>
    <div class="fx grain" id="ns-grain" aria-hidden="true"></div>
    <div class="fx flash" aria-hidden="true"></div>

    <div class="pcard" id="ns-pcard" role="group" aria-label="Product on duty" hidden>
      <div class="pc-img"><img id="ns-pcImg" src="" alt="" width="240" height="240"></div>
      <div class="pc-body">
        <p class="pc-where" id="ns-pcWhere"></p>
        <h3 id="ns-pcName"></h3>
        <p class="pc-kind" id="ns-pcKind"></p>
        <p class="pc-fact" id="ns-pcFact"></p>
        <a class="pc-go" id="ns-pcGo" href="#">View product <span aria-hidden="true">&rarr;</span></a>
      </div>
      <button type="button" class="pc-x" id="ns-pcClose" aria-label="Close product card"><svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path d="M3 3l10 10M13 3L3 13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button>
    </div>
  </div>

  <div class="spots" id="ns-spots" role="group" aria-label="Protection points">
    <p class="spots-h">Eight points on duty</p>
    <ul id="ns-chipList"></ul>
  </div>

  <div class="console" id="ns-console" role="group" aria-label="Test alarm">
    <div class="run">
      <button type="button" class="btn" id="ns-runBtn"><svg viewBox="0 0 20 20" width="18" height="18" aria-hidden="true"><path d="M5 3.5v13l11-6.5z" fill="currentColor"/></svg><span id="ns-runLabel">Run a test alarm</span></button>
      <button type="button" class="btn ns-ghost" id="ns-resetBtn" hidden>Reset</button>
      <span class="ill">Illustrative, 12 seconds</span>
    </div>
    <div class="stepnav" id="ns-stepnav" hidden>
      <button type="button" class="btn ns-ghost" id="ns-prevBtn">Back</button>
      <button type="button" class="btn" id="ns-nextBtn">Next step</button>
      <button type="button" class="btn ns-ghost" id="ns-exitBtn">Close</button>
      <span class="ill">Illustrative, 6 steps</span>
    </div>
    @@RAIL@@
  </div>

  <div class="cards" id="ns-cards">
    <div class="sc" id="ns-cMc" aria-hidden="true">
      <p class="sc-hd"><span class="sc-k">Monitoring center</span><span class="sc-ill">Illustrative</span></p>
      <p class="sc-big"><i class="ns-dot" aria-hidden="true"></i>Signal received</p>
      <dl>
        <div><dt>Event</dt><dd>Glassbreak</dd></div>
        <div><dt>Path</dt><dd>LTE cellular, 263LTE</dd></div>
        <div><dt>Demo</dt><dd>No signal is sent</dd></div>
      </dl>
    </div>
    <div class="sc" id="ns-cPh" aria-hidden="true">
      <p class="sc-hd"><span class="sc-k">Phone</span><span class="sc-ill">Virtual Keypad</span></p>
      <p class="sc-big"><i class="ns-dot" aria-hidden="true"></i><span class="a0">System in alarm</span><span class="a1">Alarm cancelled</span></p>
      <p class="sc-q">Is This A False Alarm?</p>
      <div class="sc-btns" aria-hidden="true"><span class="pb pb-cancel">False Alarm</span><span class="pb">Real Alarm</span></div>
      <p class="sc-done">Cancelled from the phone</p>
    </div>
    <div class="sc" id="ns-cCam" aria-hidden="true">
      <p class="sc-hd"><span class="sc-k">VUE Plus camera</span><span class="sc-ill">AlarmVision</span></p>
      <div class="feed">
        <svg viewBox="0 0 240 120" aria-hidden="true" preserveAspectRatio="xMidYMid slice">
          <rect width="240" height="120" fill="#0b1712"/>
          <rect y="0" width="240" height="92" fill="#16291f"/>
          <path d="M0 92H240V120H0Z" fill="#0e1c15"/>
          <g stroke="#0b1712" stroke-opacity=".5"><path d="M0 20H240M0 40H240M0 60H240M0 80H240"/></g>
          <rect x="24" y="22" width="44" height="58" fill="#3c6a50"/><rect x="24" y="22" width="44" height="58" fill="none" stroke="#0b1712" stroke-width="3"/>
          <rect x="96" y="18" width="52" height="66" fill="#0b1712"/><rect x="100" y="22" width="44" height="58" fill="#8fd6ad"/>
          <polygon points="108,30 124,26 138,37 133,56 140,70 124,78 110,72 105,54" fill="#07100c"/>
          <path d="M108 30l-8-8M138 37l6-8M140 70l4 10M110 72l-10 8" stroke="#d9ffe9" stroke-width="1"/>
          <rect x="176" y="22" width="44" height="58" fill="#3c6a50"/><rect x="176" y="22" width="44" height="58" fill="none" stroke="#0b1712" stroke-width="3"/>
          
          <g class="box" fill="none" stroke="#ffd23d" stroke-width="2"><path d="M90 24V12H102M142 12H154V24M154 78V90H142M102 90H90V78"/></g>
          <rect class="scan" x="0" y="0" width="240" height="14" fill="#baffd8" opacity=".16"/>
          <g font-family="ui-monospace,Menlo,Consolas,monospace" font-size="8" fill="#d9ffe9"><text x="208" y="12">LIVE</text></g>
          <circle cx="201" cy="9" r="3" fill="#ff4a3d" class="ns-rec"/>
        </svg>
      </div>
      <p class="sc-ver"><span class="v0">Checking live footage</span><span class="v1"><svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path d="M3 8.5l3.2 3.2L13 4.8" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>Live footage viewed</span></p>
    </div>
  </div>

  <svg id="ns-wire" aria-hidden="true"></svg>

@@POINTS@@
</div>'''


def _night(s, ctx):
    E, L, rel = ctx["E"], ctx["L"], ctx["rel"]
    hid = s.get("id", "night")
    h = s.get("heading") or ["Night", "shift"]
    title = (f'<div class="title" id="ns-title"><p class="eyebrow">{E(s.get("eyebrow", ""))}</p>'
             f'<h2 id="{E(hid)}-h" class="ns-h">{E(h[0])} <em>{E(h[1])}</em></h2><p class="lede">{E(s.get("lede", ""))}</p></div>')
    steps = "".join(f"<li><b>{E(k)}</b><span>{E(t)}</span></li>" for k, t in s.get("steps", []))
    rail = (f'<p class="caption" id="ns-caption" aria-live="polite">{E(s.get("caption", ""))}</p>'
            f'<ol class="ns-rail" id="ns-rail">{steps}</ol>')
    pts = ""
    for p in s.get("points", []):
        pts += (f'<li data-k="{E(p["k"])}" data-chip="{E(p["chip"])}" data-where="{E(p["where"])}" data-name="{E(p["name"])}" data-kind="{E(p["kind"])}" '
                f'data-img="{E(rel(p["image"]))}" data-alt="{E(p["alt"])}" data-fact="{E(p["fact"])}" data-href="{E(L(p["href"]))}">'
                f'<b>{E(p["where"])}</b><a href="{E(L(p["href"]))}">{E(p["name"])}</a><p>{E(p["kind"])}. {E(p["fact"])}</p></li>')
    points = f'<ul class="ns-points" id="ns-points">{pts}</ul><p class="ns-cap">{E(s.get("note", "Illustrative scene"))}</p>'
    more = "".join(f'<a href="{E(L(h))}">{E(t)} <span aria-hidden="true">&rarr;</span></a>' for t, h in s.get("more", []))
    more = f'<p class="ns-more"><span>On the systems page</span>{more}</p>' if more else ""
    stage = STAGE.replace("@@TITLE@@", title).replace("@@RAIL@@", rail).replace("@@POINTS@@", points)
    return (MARK_A + f'<section class="pn-night" id="{E(hid)}" aria-labelledby="{E(hid)}-h">'
            f'<link rel="stylesheet" href="{E(rel("assets/night/night.css"))}">{stage}{more}'
            f'<script src="{E(rel("assets/night/night.js"))}" defer></script></section>' + MARK_B)


RENDER_NIGHT = {"pn-night": _night}
