"use strict";function lock(e){e.preventDefault(),post({lock:askForPassword("Re-enter password to lock")},!0)}function save(e){e.preventDefault(),post({save:askForPassword("Re-enter password to save")}).then(e=>{200==e.code&&error("Cache was successfully saved")})}
"use strict";async function reloadIndex(){const e=await postOrPreload({recent:""});0!=e.length?replaceTemplate({params:e,builder:e=>makeNewCard({uuid:e.hash,name:e.id,message:e.msgs[e.msgs.length-1].msg,isClickable:!0,usePointer:!0})}):replaceTemplate({start:blank("Add a friend to start talking!")})}
"use strict";function url(e){history.replaceState({},"","/"+e)}function cookie(e){return document.cookie.replace(new RegExp("(?:(?:^|.*;\\s*)"+e+"\\s*\\=\\s*([^;]*).*$)|^.*$"),"$1")}
"use strict";const setting={button:function(e){const o=e.innerText.toLowerCase().trim()||e.id;"change password"==o?post({"change pwd":{old:askForPassword("Enter old password"),new:askForPassword("Enter new password")}}):"generate new key"==o?(askForConfirmation("Are you sure? Generating new key will make your friends unable to talk to you until your new public key is sent out"),post({"new key":askForPassword("Enter password to confirm")},!0)):"devmode"==o?post({devmode:isChecked(e)}).then(()=>{window.location.reload(!0)}):"nuke cache"==o?(askForConfirmation("Are you sure you want to delete cache?"),post({nuke:askForPassword("Enter password to confirm")},!0)):"fresh js"==o?post({"fresh js":isChecked(e)}).then(()=>{window.location.reload(!0)}):"fresh css"==o&&post({"fresh css":isChecked(e)}).then(()=>{window.location.reload(!0)})},dropdown:function(e){const o=(e.getAttribute("data-type")||"").toLowerCase();"expiration timer"==o?post({"expiration timer":e.value}):"msg deletion"==o?post({"msg policy":e.value}):"theme"==o&&post({theme:e.value}).then(()=>{window.location.reload(!0)})}};function isChecked(e){return e.className.includes("-unchecked")}
"use strict";
/*! MIT Licnse for nu available at -> https://github.com/dosisod/nu */function nu(n,e,t,r){if(!e)return document.getElementById(n);let o=document.createElement(n);for(const n in e)o[n]=e[n];const c=o;function i(n){n instanceof HTMLElement?o=n.appendChild(o).parentNode:"string"==typeof n&&(o=nu(n).appendChild(o).parentNode)}return t&&(Array.isArray(t)?t.forEach((function(n){i(n)})):i(t)),r?c:o}
"use strict";const tray=nu("tray");var friends=[];async function checkFriends(){friends.length||(friends=(await post({friends:""})).msg)}function realname(e){for(const n of friends)if(n.id==e)return n.name;return""}async function postOrPreload(e){if(await checkFriends(),preload){const e=preload;return preload=!1,e}return(await post(e)).msg}function replaceTemplate(e){tray.innerHTML="",addAppendable(tray,e.start),e.params&&e.params.forEach((n,a)=>{n.index=a,e.builder&&tray.appendChild(e.builder(n))}),addAppendable(tray,e.end)}function addAppendable(e,n){"string"==typeof n?e.innerHTML+=n:n&&e.appendChild(n)}function makeNewCard(e){const n=realname(e.name),a=nu("ol",{});a.appendChild(nu("li",{className:"name title hide",innerText:n})),a.appendChild(nu("li",{className:"msg hide",innerText:e.message||""}));const i=nu("div",{className:e.usePointer?"holder point":"holder"});e.isClickable&&(i.onclick=()=>{window.location.href="/@"+e.name}),i.appendChild(makeProfilePic(e.uuid,n)),i.appendChild(document.createTextNode("\n")),i.appendChild(a);const r=nu("li",{className:"item"});return r.appendChild(i),r}function makeProfilePic(e,n){const a=nu("div",{className:"profile-pic-img",innerText:n[0]}),i=e.slice(0,6);return a.style.background="#"+i,a.style.color=parseInt(i,16)>8388607.5?"#000":"#fff",a}function blank(e){return nu("span",{className:"title center",innerText:e},nu("div",{className:"holder nopoint blank"})).outerHTML}
"use strict";function askForPassword(r){const o=prompt(r);if(o)return o;throw new Error("User cancelled or used blank password.")}function askForConfirmation(r){if(!confirm(r))throw new Error("User cancelled or declined confirmation.")}
"use strict";async function send(e){const s=e.target;"Enter"==e.key&&s.value&&(await post({"send msg":{uname:cookie("uname"),msg:s.value}}).then(e=>{400!=e.code&&reloadMsgs()}),s.value="")}async function reloadMsgs(){const e=cookie("uname"),s=await postOrPreload({allfor:e});if(0==s.length)return;const a=s.msgs,n=s.id;0!=a.length?(replaceTemplate({start:makeNewCard({uuid:s.hash,name:e,isClickable:!1}),params:a,builder:e=>createMsg(e,n)}),nu("reload").scrollIntoView()):replaceTemplate({start:makeNewCard({uuid:s.hash,name:e,isClickable:!1}).outerHTML+blank(`Say hi to ${realname(e)}!`)})}function createMsg(e,s){const a=nu("span",{className:e.sending?"x-sending":"x-receiving",innerText:"x",onclick:()=>{post({status:""}).then(a=>{if(0==a.msg["msg policy"])askForConfirmation("Are you sure you want to delete this message?");else if(1==a.msg["msg policy"])var n=askForPassword("Enter Password");else 2!=a.msg["msg policy"]&&error("Invalid Request");post({"delete msg":{id:s,index:e.index,pwd:n||""}}),reloadMsgs()})}},nu("li",{className:"item"}));return nu("span",{className:"msg",innerText:e.msg},[nu("div",{className:"holder block "+(e.sending?"sending":"receiving")}),a]),a}
"use strict";var lastError=0;const API_WAIT=5e3;async function post(e,r=!1){if(clearError(),e.redirect=!!r,!r)return fetch("/api/",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(e)}).then(e=>e.json()).catch(e=>{if("NetworkError when attempting to fetch resource."==e.message||"Failed to fetch"==e.message)throw error("Network Disconnected"),new Error("Network Disconnect: "+e.message);if(e.message.startsWith("JSON.parse: unexpected character at"))throw error("Could Not Handle Request"),new Error("Could Not Handle Request: "+e.message)}).then(r=>{if(200!=r.code&&error(r.msg),""!=r.rethrow)return r;post(e,!0)});{const r=nu("form",{id:"api-form",action:"/api/",method:"POST"});nu("input",{type:"hidden",name:"json",value:JSON.stringify(e)},r),nu("input",{type:"submit",style:"visibility: hidden;"},[r,document.body],!0).click(),nu("api-form").remove()}}async function heartbeat(){"NetworkError when attempting to fetch resource."==(await post({ping:""})).message?error("Network Disconnected"):clearError()}async function setHeartbeat(e){e?setInterval(e,5e3):setInterval(heartbeat,5e3)}function clearError(){error(!1)}function error(e){"string"==typeof e?(lastError=Date.now(),nu("error").style.display="block",nu("error").innerText=e):Date.now()>lastError+5e3&&(nu("error").style.display="none",nu("error").innerText="")}
