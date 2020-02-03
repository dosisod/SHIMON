var lastError=0;const API_WAIT=5e3;async function post(e,r=!1){clearError(),e.session=document.cookie.replace(/(?:(?:^|.*;\s*)session\s*\=\s*([^;]*).*$)|^.*$/,"$1"),e.redirect=!!r;const t=function(e){if("object"==typeof e)try{return JSON.stringify(e)}catch{}return e};if(!r){var o=new FormData;for(const r in e)o.append(r,t(e[r]));return fetch("/api/",{method:"POST",body:o}).then(e=>e.json()).catch(e=>{console.log({error:e.message}),"NetworkError when attempting to fetch resource."==e.message?error("Network Disconnected"):"JSON.parse: unexpected character at line 1 column 1 of the JSON data"==e.message&&error("Could Not Handle Request")}).then(r=>{if(200!=r.code&&error(r.msg),""!=r.rethrow)return r;post(e,!0)})}{const r=nu("form",{id:"api-form",action:"/api/",method:"POST"});for(const o in e)nu("input",{type:"hidden",name:o,value:t(e[o])},r);nu("input",{type:"submit",style:"visibility: hidden;"},[r,document.body],!0).click(),nu("api-form").remove()}}async function heartbeat(){"NetworkError when attempting to fetch resource."==(await post({ping:""})).message?error("Network Disconnected"):clearError()}async function setHeartbeat(e){e?setInterval(e,API_WAIT):setInterval(heartbeat,API_WAIT)}function clearError(){error(!1)}function error(e){"string"==typeof e?(lastError=Date.now(),nu("error").style.display="block",nu("error").innerText=e):Date.now()>lastError+API_WAIT&&(nu("error").style.display="none",nu("error").innerText="")}
function askForPassword(r){const o=prompt(r);if(o)return o;throw new Error("User cancelled or used blank password.")}function askForConfirmation(r){if(!confirm(r))throw new Error("User cancelled or declined confirmation.")}
function lock(e){e.preventDefault(),post({lock:askForPassword("Re-enter password to lock")},!0)}function save(e){e.preventDefault(),post({save:askForPassword("Re-enter password to save")}).then(e=>{200==e.code&&error("Cache was successfully saved")})}
async function send(e){const s=e.target;"Enter"==e.key&&s.value&&(await post({"send msg":{uname:document.cookie.replace(/(?:(?:^|.*;\s*)uname\s*\=\s*([^;]*).*$)|^.*$/,"$1"),msg:s.value}}).then(e=>{400!=e.code&&reloadMsgs()}),s.value="")}
/*! MIT Licnse for nu available at -> https://github.com/dosisod/nu */
function nu(e,n,t,o){if(!n)return document.getElementById(e);let r=document.createElement(e);for(const e in n)r[e]=n[e];const c=r;function d(e){e instanceof HTMLElement?r=e.appendChild(r).parentNode:"string"==typeof e&&(r=document.getElementById(e).appendChild(r).parentNode)}return t&&(Array.isArray(t)?t.forEach((function(e){d(e)})):d(t)),o?c:r}
const setting={button:function(e){const o=e.innerText.toLowerCase()||e.id;"change password"==o?post({"change pwd":{old:askForPassword("Enter old password"),new:askForPassword("Enter new password")}}):"generate new key"==o?(askForConfirmation("Are you sure? Generating new key will make your friends unable to talk to you until your new public key is sent out"),post({"new key":askForPassword("Enter password to confirm")},!0)):"devmode"==o?post({devmode:e.className.includes("-unchecked")}).then(()=>{window.location.reload(!0)}):"nuke cache"==o?(askForConfirmation("Are you sure you want to delete cache?"),post({nuke:askForPassword("Enter password to confirm")},!0)):"fresh js"==o?post({"fresh js":isChecked(e)}).then(()=>{window.location.reload(!0)}):"fresh css"==o&&post({"fresh css":isChecked(e)}).then(()=>{window.location.reload(!0)})},dropdown:function(e){const o=e.attributes["data-type"].value.toLowerCase();"expiration timer"==o?post({"expiration timer":e.value}):"msg deletion"==o?post({"msg policy":e.value}):"theme"==o&&post({theme:e.value}).then(()=>{window.location.reload(!0)})}};function isChecked(e){return e.className.includes("-unchecked")}
var tray=nu("tray"),friends=[];async function checkFriends(){friends.length||(friends=(friends=await post({friends:""})).msg)}function realname(e){for(const n of friends)if(n.id==e)return n.name}function uname(e){for(const n of friends)if(n.name==e)return n.id}async function reloadMsgs(){const e=document.cookie.replace(/(?:(?:^|.*;\s*)uname\s*\=\s*([^;]*).*$)|^.*$/,"$1"),n=await postOrPreload({allfor:e});if(0==n.length)return;const a=n.msgs,r=n.id;0!=a.length?(replaceTemplate(newCard(n.hash,realname(e),"",!0,!1),reloadButton(reloadMsgs),a,e=>createMsg(e,r)),nu("reload").scrollIntoView()):replaceTemplate(newCard(n.hash,realname(e),"",!0,!1).outerHTML+blank("Say hi to "+realname(e)+"!"),reloadButton(reloadMsgs))}function createMsg(e,n){var a=nu("span",{className:e.sending?"x-sending":"x-receiving",innerText:"x",onclick:()=>{post({status:""}).then(a=>{if(0==a.msg["msg policy"])askForConfirmation("Are you sure you want to delete this message?");else if(1==a.msg["msg policy"])var r=askForPassword("Enter Password");else 2!=a.msg["msg policy"]&&error("Invalid Request");post({"delete msg":{id:n,index:e.index,pwd:r||""}}),reloadMsgs()})}},nu("li",{className:"item"}));return nu("span",{className:"msg",innerText:e.msg},[nu("div",{className:"holder block "+(e.sending?"sending":"receiving")}),a]),a}async function reloadIndex(){const e=await postOrPreload({recent:""});0!=e.length?replaceTemplate(void 0,reloadButton(reloadIndex),e,e=>newCard(e.hash,realname(e.id),e.msgs[e.msgs.length-1].msg,!0,!0,!0)):replaceTemplate(blank("Add a friend to start talking!"),reloadButton(reloadIndex))}async function postOrPreload(e){if(await checkFriends(),preload){const e=preload;return preload=!1,e}return(await post(e)).msg}async function replaceTemplate(e,n,a,r){tray.innerHTML='<div class="rightbar"><a class="rightitem name point" href="/add">ADD FRIEND</a><br><a class="rightitem name point" href="/account">ACCOUNT</a><br><span class="rightitem name point" onclick="save(event)">SAVE</span></div>',"string"==typeof e?tray.innerHTML+=e:e&&tray.appendChild(e),a&&a.forEach((e,n)=>{e.index=n,tray.appendChild(r(e))}),"string"==typeof n?tray.innerHTML+=n:n&&tray.appendChild(n)}function newCard(e,n,a,r=!1,t=!1,s=!1){var i=nu("ol",{});i.appendChild(nu("li",{className:"name title hide",innerText:n})),i.appendChild(nu("li",{className:"msg hide",innerText:a}));var o=nu("div",{className:s?"holder point":"holder"});t&&(o.onclick=()=>{window.location.href="/@"+uname(n)}),o.appendChild(makeProfilePic(e,n)),o.appendChild(document.createTextNode("\n")),o.appendChild(i);var l=nu("li",{className:"item"});if(l.appendChild(o),r)return l;tray.appendChild(l)}function reloadButton(e){return nu("span",{className:"center name point",id:"reload",innerText:"RELOAD",onclick:()=>e()})}function makeProfilePic(e,n){const a=nu("div",{className:"profile-pic-img",innerText:n[0]}),r=e.slice(0,6);return a.style.background="#"+e.slice(0,6),a.style.color=parseInt(r,16)>8388607.5?"#000":"#fff",a}function blank(e){return`<div class="holder nopoint blank"><span class="title center">${e}</span></div>`}
function url(t){history.replaceState({},"","/"+t)}
