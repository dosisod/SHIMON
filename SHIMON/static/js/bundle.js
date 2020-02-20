"use strict";var lastError=0;const API_WAIT=5e3;async function post(e,r=!1){if(clearError(),e.redirect=!!r,!r)return fetch("/api/",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(e)}).then(e=>e.json()).catch(e=>{console.log({error:e.message}),"NetworkError when attempting to fetch resource."==e.message?error("Network Disconnected"):"JSON.parse: unexpected character at line 1 column 1 of the JSON data"==e.message&&error("Could Not Handle Request")}).then(r=>{if(200!=r.code&&error(r.msg),""!=r.rethrow)return r;post(e,!0)});{const r=nu("form",{id:"api-form",action:"/api/",method:"POST"});nu("input",{type:"hidden",name:"json",value:JSON.stringify(e)},r),nu("input",{type:"submit",style:"visibility: hidden;"},[r,document.body],!0).click(),nu("api-form").remove()}}async function heartbeat(){"NetworkError when attempting to fetch resource."==(await post({ping:""})).message?error("Network Disconnected"):clearError()}async function setHeartbeat(e){e?setInterval(e,API_WAIT):setInterval(heartbeat,API_WAIT)}function clearError(){error(!1)}function error(e){"string"==typeof e?(lastError=Date.now(),nu("error").style.display="block",nu("error").innerText=e):Date.now()>lastError+API_WAIT&&(nu("error").style.display="none",nu("error").innerText="")}
"use strict";function askForPassword(r){const o=prompt(r);if(o)return o;throw new Error("User cancelled or used blank password.")}function askForConfirmation(r){if(!confirm(r))throw new Error("User cancelled or declined confirmation.")}
"use strict";function lock(e){e.preventDefault(),post({lock:askForPassword("Re-enter password to lock")},!0)}function save(e){e.preventDefault(),post({save:askForPassword("Re-enter password to save")}).then(e=>{200==e.code&&error("Cache was successfully saved")})}
"use strict";async function send(e){const s=e.target;"Enter"==e.key&&s.value&&(await post({"send msg":{uname:document.cookie.replace(/(?:(?:^|.*;\s*)uname\s*\=\s*([^;]*).*$)|^.*$/,"$1"),msg:s.value}}).then(e=>{400!=e.code&&reloadMsgs()}),s.value="")}
"use strict";
/*! MIT Licnse for nu available at -> https://github.com/dosisod/nu */function nu(n,e,t,r){if(!e)return document.getElementById(n);let o=document.createElement(n);for(const n in e)o[n]=e[n];const c=o;function i(n){n instanceof HTMLElement?o=n.appendChild(o).parentNode:"string"==typeof n&&(o=nu(n).appendChild(o).parentNode)}return t&&(Array.isArray(t)?t.forEach((function(n){i(n)})):i(t)),r?c:o}
"use strict";const setting={button:function(e){const o=e.innerText.toLowerCase()||e.id;"change password"==o?post({"change pwd":{old:askForPassword("Enter old password"),new:askForPassword("Enter new password")}}):"generate new key"==o?(askForConfirmation("Are you sure? Generating new key will make your friends unable to talk to you until your new public key is sent out"),post({"new key":askForPassword("Enter password to confirm")},!0)):"devmode"==o?post({devmode:e.className.includes("-unchecked")}).then(()=>{window.location.reload(!0)}):"nuke cache"==o?(askForConfirmation("Are you sure you want to delete cache?"),post({nuke:askForPassword("Enter password to confirm")},!0)):"fresh js"==o?post({"fresh js":isChecked(e)}).then(()=>{window.location.reload(!0)}):"fresh css"==o&&post({"fresh css":isChecked(e)}).then(()=>{window.location.reload(!0)})},dropdown:function(e){const o=e.getAttribute("data-type");if(!o)return;const s=o.toLowerCase();"expiration timer"==s?post({"expiration timer":e.value}):"msg deletion"==s?post({"msg policy":e.value}):"theme"==s&&post({theme:e.value}).then(()=>{window.location.reload(!0)})}};function isChecked(e){return e.className.includes("-unchecked")}
"use strict";const tray=nu("tray");var friends=[];async function checkFriends(){friends.length||(friends=(await post({friends:""})).msg)}function realname(e){for(const n of friends)if(n.id==e)return n.name;return""}async function reloadMsgs(){const e=document.cookie.replace(/(?:(?:^|.*;\s*)uname\s*\=\s*([^;]*).*$)|^.*$/,"$1"),n=await postOrPreload({allfor:e});if(0==n.length)return;const a=n.msgs,t=n.id;0!=a.length?(replaceTemplate(newCard(n.hash,e,"",!1),reloadButton(reloadMsgs),a,e=>createMsg(e,t)),nu("reload").scrollIntoView()):replaceTemplate(newCard(n.hash,e,"",!1).outerHTML+blank("Say hi to "+realname(e)+"!"),reloadButton(reloadMsgs))}function createMsg(e,n){const a=nu("span",{className:e.sending?"x-sending":"x-receiving",innerText:"x",onclick:()=>{post({status:""}).then(a=>{if(0==a.msg["msg policy"])askForConfirmation("Are you sure you want to delete this message?");else if(1==a.msg["msg policy"])var t=askForPassword("Enter Password");else 2!=a.msg["msg policy"]&&error("Invalid Request");post({"delete msg":{id:n,index:e.index,pwd:t||""}}),reloadMsgs()})}},nu("li",{className:"item"}));return nu("span",{className:"msg",innerText:e.msg},[nu("div",{className:"holder block "+(e.sending?"sending":"receiving")}),a]),a}async function reloadIndex(){const e=await postOrPreload({recent:""});0!=e.length?replaceTemplate(void 0,reloadButton(reloadIndex),e,e=>newCard(e.hash,e.id,e.msgs[e.msgs.length-1].msg,!0,!0)):replaceTemplate(blank("Add a friend to start talking!"),reloadButton(reloadIndex))}async function postOrPreload(e){if(await checkFriends(),preload){const e=preload;return preload=!1,e}return(await post(e)).msg}async function replaceTemplate(e,n,a,t){tray.innerHTML='<div class="rightbar"><a class="rightitem name point" href="/add">ADD FRIEND</a><br><a class="rightitem name point" href="/account">ACCOUNT</a><br><span class="rightitem name point" onclick="save(event)">SAVE</span></div>',"string"==typeof e?tray.innerHTML+=e:e&&tray.appendChild(e),a&&t&&a.forEach((e,n)=>{e.index=n,tray.appendChild(t(e))}),"string"==typeof n?tray.innerHTML+=n:n&&tray.appendChild(n)}function newCard(e,n,a,t=!1,s=!1){const r=realname(n),i=nu("ol",{});i.appendChild(nu("li",{className:"name title hide",innerText:r})),i.appendChild(nu("li",{className:"msg hide",innerText:a}));const o=nu("div",{className:s?"holder point":"holder"});t&&(o.onclick=()=>{window.location.href="/@"+n}),o.appendChild(makeProfilePic(e,r)),o.appendChild(document.createTextNode("\n")),o.appendChild(i);const l=nu("li",{className:"item"});return l.appendChild(o),l}function reloadButton(e){return nu("span",{className:"center name point",id:"reload",innerText:"RELOAD",onclick:()=>e()})}function makeProfilePic(e,n){const a=nu("div",{className:"profile-pic-img",innerText:n[0]}),t=e.slice(0,6);return a.style.background="#"+e.slice(0,6),a.style.color=parseInt(t,16)>8388607.5?"#000":"#fff",a}function blank(e){return`<div class="holder nopoint blank"><span class="title center">${e}</span></div>`}
"use strict";function url(t){history.replaceState({},"","/"+t)}
