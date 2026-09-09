const $ = (s) => document.querySelector(s);
const usernameInput = $('#username');
const grid = $('#projects-grid');
const metrics = $('#metrics');
const status = $('#sync-status');
const card = $('#developer-card');
const embed = $('#embed');

const esc = (value='') => String(value).replace(/[&<>\"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#39;'}[c]));

async function github(path){
  const response = await fetch(`https://api.github.com${path}`, {headers:{Accept:'application/vnd.github+json'}});
  if(!response.ok) throw new Error(`GitHub API ${response.status}`);
  return response.json();
}

function metric(value,label){return `<div class="metric"><b>${esc(value)}</b><span>${esc(label)}</span></div>`}
function renderMetrics(user,repos){
  const languages = new Set(repos.flatMap(r => r.language ? [r.language] : [])).size;
  metrics.innerHTML = metric(user.public_repos,'Public repositories') + metric(user.followers,'Followers') + metric(user.following,'Following') + metric(languages,'Languages represented');
}
function renderProjects(repos){
  const featured = repos.filter(r=>!r.fork).sort((a,b)=>new Date(b.pushed_at)-new Date(a.pushed_at)).slice(0,12);
  grid.innerHTML = featured.map(r=>`<article class="project"><span class="eyebrow">${esc(r.language||'PROJECT')}</span><h3>${esc(r.name)}</h3><p>${esc(r.description||'Open-source engineering project.')}</p><div>${(r.topics||[]).slice(0,4).map(t=>`<span class="tag">${esc(t)}</span>`).join('')}</div><p><a href="${esc(r.html_url)}" target="_blank" rel="noopener noreferrer">View repository ↗</a></p></article>`).join('');
  if(!featured.length) grid.innerHTML='<p>No public repositories found.</p>';
}
function renderCard(user){
  const site = `https://github.com/${user.login}`;
  card.innerHTML = `<div><div class="eyebrow">SAYANOX · VERIFIED PUBLIC PROFILE</div><div class="name">${esc(user.name||user.login)}</div><div class="handle">@${esc(user.login)}</div><p>${esc(user.bio||'Open-source developer')}</p></div><div class="card-footer"><span>${esc(user.public_repos)} repositories</span><span>github.com/${esc(user.login)}</span></div>`;
  embed.textContent = `[![SAYANOX Developer](${location.origin}${location.pathname.replace(/[^/]*$/,'')}card.svg?user=${encodeURIComponent(user.login)})](${site})`;
}
async function load(username){
  const clean=username.trim();
  if(!/^[a-zA-Z0-9-]{1,39}$/.test(clean)){status.textContent='Invalid GitHub username';return;}
  status.textContent='Syncing GitHub…';
  try{
    const [user,repos] = await Promise.all([github(`/users/${encodeURIComponent(clean)}`), github(`/users/${encodeURIComponent(clean)}/repos?per_page=100&sort=updated`)]);
    renderMetrics(user,repos); renderProjects(repos); renderCard(user); status.textContent=`Synced @${user.login}`;
  }catch(error){status.textContent='GitHub sync failed';grid.innerHTML=`<p>Unable to load this public profile right now. ${esc(error.message)}</p>`;}
}
$('#generate').addEventListener('click',()=>load(usernameInput.value));
usernameInput.addEventListener('keydown',e=>{if(e.key==='Enter')load(usernameInput.value)});
$('#copy').addEventListener('click',async()=>{if(!embed.textContent)return;await navigator.clipboard.writeText(embed.textContent);$('#copy').textContent='Copied ✓';setTimeout(()=>$('#copy').textContent='Copy embed',1400)});
load('sayan9168');
