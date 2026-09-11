(() => {
  const root=document.querySelector('[data-voice-status]');
  if(!root)return;
  function render(){
  const data=window.SCRIPTA_VOICE_MIGRATION_STATUS;
  if(!data){root.textContent='Migration status has not been generated yet.';return;}
  const queryBefore=root.querySelector('[data-status-search]')?.value||'';
  const focusSearch=document.activeElement===root.querySelector('[data-status-search]');
  const openTitles=new Set([...root.querySelectorAll('details[open]')].map(details=>details.closest('article').dataset.statusBook));
  const labels={'qwen-complete':'Current script published with Qwen','rendering':'Voice generation in progress','pending-piper':'Previous Piper recording','needs-render':'Voice generation pending','needs-rerender':'Qwen recording needs updating','untracked':'Project missing'};
  const reviews={reviewed:'Script independently reviewed','independent-review-pending':'Draft rewritten · independent review pending','rewrite-pending':'Editorial rewrite pending'};
  const order=['qwen-complete','rendering','needs-rerender','pending-piper','needs-render','untracked'];
  const escape=value=>String(value??'').replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  const duration=ms=>`${Math.floor(ms/60000)}:${String(Math.round(ms/1000)%60).padStart(2,'0')}`;
  const link=(url,label)=>`<a href="${escape(url)}" target="_blank" rel="noopener noreferrer">${escape(label)}</a>`;
  const planText=value=>typeof value==='string'?value:Array.isArray(value)?value.map(planText).join(' '):value&&typeof value==='object'?Object.entries(value).map(([key,text])=>`${key}: ${planText(text)}`).join(' '):'';
  const article=entry=>{
    const review=entry.editorialReview;
    const stages=entry.stages||{};
    const failed=Object.values(stages).some(stage=>['failed','interrupted'].includes(stage.status));
    const done=stages.animation?.status==='done'&&stages.voice?.status==='done';
    const checking=entry.status==='qwen-complete'||['built','reviewing'].includes(stages.animation?.status)||stages.voice?.status==='generated';
    const state=entry.active?'active':failed?'failed':done?'done':checking?'review':'pending';
    const stateLabel={active:'În lucru',failed:'Necesită atenție',done:'Gata',review:'De verificat',pending:'De făcut'}[state];
    const currentSteps=Object.entries(stages).filter(([,stage])=>['running','reviewing','rewriting'].includes(stage.status)).map(([name])=>({text:'text',animation:'animație',voice:'voce'}[name]||name));
    const remaining=entry.status==='qwen-complete'
      ? 'Current wording and audio are present in the published film; listening and visual review are separate checks.'
      : `${entry.editorialStatus==='reviewed'?'':'Finish the script review. '}Adapt the artwork to the selected scenes, generate changed narration, measure and retime, then rebuild and inspect the film in all three themes.`;
    return `<article data-status-book="${escape(entry.title.toLowerCase())}" data-work-state="${state}">
      <div><h3>${link(entry.bookPage,entry.title)} <span class="status-indicator status-indicator-${state}"><span aria-hidden="true">${entry.active?'●':done?'✓':failed?'!':'○'}</span> ${stateLabel}${entry.active&&currentSteps.length?` · ${escape(currentSteps.join(' + '))}`:''}</span></h3>
        <p class="status-stages">Text: ${escape(entry.stages?.text?.status||entry.editorialStatus)} · Animation: ${escape(entry.stages?.animation?.status||'pending')} · Voice: ${escape(entry.stages?.voice?.status||'pending')}</p>
        <p>${escape(reviews[entry.editorialStatus]||'Review pending')} · ${entry.scriptWords||0} words · target 1–2 min, maximum 2 min</p>
        <p>Published film: ${escape(entry.publishedVoice||entry.voice||'Unknown voice')} · ${duration(entry.durationMs||0)}.</p>
        <p>Planned voice: ${escape(entry.plannedVoice||'Local Qwen; casting pending')}.</p>
      </div>
      <div class="status-actions">${link(entry.bookPage,'Book')}${entry.animationPage?link(entry.animationPage,'Published animation'):''}</div>
      <details${openTitles.has(entry.title.toLowerCase())?' open':''}><summary>Spoken script and film plan</summary>
        ${review?.hook?`<p class="status-hook"><strong>Opening hook:</strong> ${escape(review.hook)}</p>`:''}
        ${review?.distinctiveContribution?`<p><strong>Distinctive idea:</strong> ${escape(planText(review.distinctiveContribution))}</p>`:''}
        <h4>Exact narration</h4>
        ${(entry.script||[]).map(scene=>{
          const plan=entry.visualPlan?.scenes?.find(item=>item.sceneId===scene.id);
          return `<section class="status-scene"><h5>${escape(scene.title)}</h5>
            ${plan?`<p><strong>On screen:</strong> ${escape(planText(plan.composition))}</p>`:''}
            <ol>${scene.lines.map((line,index)=>{
              const intent=review?.independentReview?.sentenceIntentions?.find(item=>item.sceneId===scene.id&&item.line===index+1);
              const cue=plan?.cues?.find(item=>item.line===index+1);
              return `<li><p class="status-spoken">${escape(line)}</p><dl class="status-direction">
                <div><dt>Purpose</dt><dd>${escape(planText(intent?.purpose)||'Final review pending')}</dd></div>
                <div><dt>Viewer response</dt><dd>${escape(planText(intent?.viewerResponse)||'Final review pending')}</dd></div>
                <div><dt>Voice</dt><dd>${escape(scene.emotions?.[index]||'Pending')} · intensity ${Math.round((scene.intensities?.[index]||0)*100)}% · pause ${((scene.pausesMs?.[index]||0)/1000).toFixed(1)} s</dd></div>
                <div><dt>Exact TTS direction</dt><dd>${escape(scene.voiceDirections?.[index]||'Pending')}</dd></div>
                <div><dt>Visual cue</dt><dd>${escape(planText(cue?.visualAction)||'Detailed visual plan pending')}</dd></div>
              </dl></li>`;
            }).join('')}</ol>
            ${plan?`<p><strong>Keep:</strong> ${escape(planText(plan.keep)||'None')}<br><strong>Remove:</strong> ${escape(planText(plan.remove)||'None')}<br><strong>Add or change:</strong> ${escape(planText(plan.addOrChange)||'None')}</p>`:''}
          </section>`;
        }).join('')}
        <h4>Visual plan — proposed</h4>
        <p>${escape(planText(review?.visualPlan)||'Book-specific visual revision plan pending.')}</p>
        <p>${entry.presentationPlan?.scenes||0} selected scenes, ${entry.presentationPlan?.beats||0} narration sentences. Final duration will come from the measured audio.</p>
        ${entry.visualPlan?.checks?`<p><strong>Checks before completion:</strong> ${escape(planText(entry.visualPlan.checks))}</p>`:''}
        <h4>Remaining production work</h4><p>${escape(remaining)}</p>
      </details>
    </article>`;
  };
  const c=data.editorialCounts||{};
  const active=data.entries.filter(entry=>entry.active);
  root.innerHTML=`<p class="status-updated">Updated ${new Date(data.updatedAt).toLocaleString()} · refreshes every minute · ${escape(data.scope)}</p>
    <p class="status-gate">${data.conversionGate==='plans-reviewed'?'All scripts and visual plans are ready. Voice and film production are tracked separately below.':`Planning in progress: ${data.visualPlans||0} of ${data.entries.length} visual plans ready. Voice conversion waits until every script and visual plan is ready.`}</p>
    <div class="status-counts"><div><strong>${active.length}</strong><span>În lucru acum</span></div><div><strong>${data.entries.length}</strong><span>Cărți în total</span></div><div><strong>${c.reviewed||0}</strong><span>Texte revizuite</span></div><div data-production-count="animations"><strong>${data.productionCounts?.animations||0}</strong><span>Animații realizate</span><small>Vizual verificat</small></div><div data-production-count="voices"><strong>${data.productionCounts?.voices||0}</strong><span>Voci generate</span><small>Textul curent înregistrat</small></div><div data-production-count="published"><strong>${data.productionCounts?.published??data.counts?.['qwen-complete']??0}</strong><span>Filme noi publicate</span><small>Voce și animație împachetate</small></div></div>
    <label class="status-search">Find a book<input type="search" placeholder="Search titles" data-status-search></label>
    ${active.length?`<section class="status-group status-active"><h2>În lucru acum <small>${active.length}</small></h2><div class="status-list">${active.map(article).join('')}</div></section>`:'<p class="status-idle">Nicio carte nu este procesată în acest moment.</p>'}
    ${order.map(key=>{const entries=data.entries.filter(entry=>entry.status===key&&!entry.active);return entries.length?`<section class="status-group"><h2>${labels[key]} <small>${entries.length}</small></h2><div class="status-list">${entries.map(article).join('')}</div></section>`:'';}).join('')}`;
  root.querySelector('[data-status-search]').addEventListener('input',event=>{
    const query=event.target.value.toLowerCase().trim();
    root.querySelectorAll('[data-status-book]').forEach(article=>{article.hidden=!article.dataset.statusBook.includes(query);});
    root.querySelectorAll('.status-group').forEach(group=>{group.hidden=![...group.querySelectorAll('article')].some(article=>!article.hidden);});
  });
  const search=root.querySelector('[data-status-search]');search.value=queryBefore;search.dispatchEvent(new Event('input'));
  if(focusSearch)search.focus({preventScroll:true});
  }
  render();
  let refreshing=false;
  const refresh=()=>{
    if(refreshing)return;
    refreshing=true;
    const script=document.createElement('script');
    script.src=`assets/voice-migration-status.js?t=${Date.now()}`;
    script.onload=()=>{refreshing=false;script.remove();render();};
    script.onerror=()=>{refreshing=false;script.remove();};
    document.head.append(script);
  };
  setInterval(refresh,60000);
  document.addEventListener('visibilitychange',()=>{if(!document.hidden)refresh();});
})();
