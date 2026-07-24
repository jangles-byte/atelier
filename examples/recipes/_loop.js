/* cycle([[msOffset, fn], ...], periodMs) — autoplay so every demo records itself */
function cycle(steps, period){
  function run(){ steps.forEach(([t,fn])=>setTimeout(fn,t)); setTimeout(run, period); }
  run();
}
const $ = s => document.querySelector(s);
const $$ = s => [...document.querySelectorAll(s)];
