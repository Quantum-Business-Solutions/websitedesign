"""Preview-only behaviours: a thin dismissible 'design preview' bar, and honest form handling (validation plus a clear
'preview only, not sent' message) so nobody believes a mock form reached the client."""

NOTICE_CSS = """
.pv-notice{position:relative;z-index:80;display:flex;gap:12px;align-items:center;justify-content:center;flex-wrap:wrap;background:#14171c;color:#fff;font:500 13px/1.4 var(--q-sans,system-ui);padding:8px 44px 8px 16px;text-align:center}
.pv-notice a{color:#ffd21f;text-decoration:underline;text-underline-offset:2px}
.pv-notice button{position:absolute;right:8px;top:50%;transform:translateY(-50%);width:32px;height:32px;border:0;background:transparent;color:#fff;font-size:20px;line-height:1;cursor:pointer;border-radius:50%}
.pv-notice button:hover{background:rgba(255,255,255,.14)}
.embedded .pv-notice{display:none}
.pv-fn{margin:14px 0 0;padding:14px 16px;border-radius:12px;border:1px solid #2f7d4f;background:#eaf6ee;color:#16331f;font:500 15px/1.5 var(--q-sans,system-ui)}
.pv-fn b{display:block;margin-bottom:2px}
.pv-fe{margin:6px 0 0;color:#a3271a;font:500 14px/1.4 var(--q-sans,system-ui)}
.q-form input[aria-invalid=true],.q-form select[aria-invalid=true],.q-form textarea[aria-invalid=true]{outline:2px solid #c8392b;outline-offset:1px}
[data-theme=dark] .pv-fn,:root[data-theme=dark] .pv-fn{background:#12301e;color:#d9f2e2;border-color:#3a9a62}
"""

NOTICE_JS = r"""
(function(){
var d=document,p=location.pathname,m=p.match(/\/(showcase|clean|press)\/(.*)$/);
var up=m?new Array((m[2].match(/\//g)||[]).length+2).join('../'):'';
var hub=(m?up:'')+'index.html';
try{if(sessionStorage.getItem('pv-notice')==='0'){}else if(!d.querySelector('.pv-notice')&&m){
var n=d.createElement('div');n.className='pv-notice';n.setAttribute('role','note');
n.innerHTML='<span><b>Design preview.</b> Forms, the dealer portal and sign-in are mock-ups and do not send anything yet.</span> <a href="'+hub+'#confirm">What is real and what DMP confirms</a><button type="button" aria-label="Dismiss this notice">&times;</button>';
d.body.insertBefore(n,d.body.firstChild);
n.querySelector('button').addEventListener('click',function(){n.remove();try{sessionStorage.setItem('pv-notice','0')}catch(e){}});}}catch(e){}
[].forEach.call(d.querySelectorAll('form.q-form'),function(f){
f.addEventListener('submit',function(e){
e.preventDefault();
[].forEach.call(f.querySelectorAll('.pv-fe,.pv-fn'),function(x){x.remove()});
var bad=null;
[].forEach.call(f.querySelectorAll('input,select,textarea'),function(i){
i.removeAttribute('aria-invalid');
var t=(i.type||'').toLowerCase();if(t==='submit'||t==='hidden'||t==='checkbox'||t==='radio')return;
var v=(i.value||'').trim(),isEmail=t==='email'||/email/i.test(i.id+i.name);
var ok=v.length>0;if(ok&&isEmail)ok=/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v);
if(i.required||isEmail||/name|first|last/i.test(i.id+i.name)){if(!ok){i.setAttribute('aria-invalid','true');if(!bad)bad=i;}}
});
var sub=f.querySelector('[type=submit]');
if(bad){var er=d.createElement('p');er.className='pv-fe';er.setAttribute('role','alert');er.textContent='Please fill in the highlighted fields (a name and a valid email).';(sub&&sub.parentNode===f?f:f).appendChild(er);bad.focus();return;}
var ok=d.createElement('div');ok.className='pv-fn';ok.setAttribute('role','status');
ok.innerHTML='<b>Preview only. This form did not send.</b>On the live site this goes to DMP’s team. For now, call 877-757-4367 (8 a.m. to 5 p.m. Central) or email InsideSales@DMP.com.';
f.appendChild(ok);
});
});
})();
"""
