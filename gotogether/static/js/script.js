document.addEventListener('DOMContentLoaded', function(){
  // clock 12-hour format with AM/PM
  function updateClock(){
    const el = document.getElementById('clock');
    if(!el) return;
    const now = new Date();
    let hh = now.getHours();
    const mm = String(now.getMinutes()).padStart(2,'0');
    const ss = String(now.getSeconds()).padStart(2,'0');
    const ampm = hh >= 12 ? 'PM' : 'AM';
    hh = hh % 12; hh = hh ? hh : 12;
    el.textContent = hh + ':' + mm + ':' + ss + ' ' + ampm;
  }
  setInterval(updateClock,1000);
  updateClock();

  // carousel
  function initCarousel(id){
    const c = document.getElementById(id);
    if(!c) return;
    const track = c.querySelector('.carousel-track');
    const slides = Array.from(track.querySelectorAll('.slide'));
    const prev = c.querySelector('.prev');
    const next = c.querySelector('.next');
    let index = 0; const gap = 14;
    function slideW(){ return slides[0] ? slides[0].offsetWidth + gap : 314; }
    let timer = null;
    function goTo(i){ if(slides.length===0) return; if(i<0) i = slides.length-1; if(i>=slides.length) i=0; index=i; track.scrollTo({left:index*slideW(), behavior:'smooth'}); }
    function start(){ timer = setInterval(()=> goTo(index+1),4000); }
    function stop(){ if(timer) clearInterval(timer); timer=null; }
    if(prev) prev.addEventListener('click', ()=>{ stop(); goTo(index-1); start(); });
    if(next) next.addEventListener('click', ()=>{ stop(); goTo(index+1); start(); });
    c.addEventListener('mouseover', stop); c.addEventListener('mouseout', start);
    window.addEventListener('resize', ()=> goTo(index));
    start();
  }
  initCarousel('carousel-passengers');
  initCarousel('carousel-drivers');

  const bubble = document.getElementById('bubble');
  document.querySelectorAll('.schedule').forEach(btn=>{
    btn.addEventListener('click', ()=>{
      const role = btn.dataset.role;
      const self_id = btn.dataset.self;
      const target_id = btn.dataset.target;
      fetch('/schedule_service', {
        method:'POST',
        headers: {'Content-Type':'application/x-www-form-urlencoded'},
        body: `role=${role}&self_id=${self_id}&target_id=${target_id}`
      }).then(r=>r.json()).then(resp=>{
        if(bubble){ try{ bubble.currentTime=0; bubble.play(); }catch(e){} }
        const n = document.getElementById('notifications');
        const el = document.createElement('div');
        el.className = 'notify';
        el.innerHTML = `<strong>${resp.message}</strong><div>ID: ${resp.servicio.id}</div><div>Hora: ${resp.servicio.time} · Precio: ${resp.servicio.price}</div>`;
        n.prepend(el);
      });
    });
  });

  // chat
  document.querySelectorAll('.chat').forEach(btn=>{
    btn.addEventListener('click', ()=>{
      const name = btn.dataset.name || 'Contacto';
      const msg = prompt('Enviar mensaje a ' + name + ':');
      if(!msg) return;
      fetch('/chat_simulate', {
        method:'POST',
        headers: {'Content-Type':'application/x-www-form-urlencoded'},
        body: `sender=Usuario&message=${encodeURIComponent(msg)}`
      }).then(r=>r.json()).then(resp=>{
        alert(resp.reply);
      });
    });
  });

  document.querySelectorAll('.complete').forEach(btn=>{
    btn.addEventListener('click', ()=>{
      const sid = btn.dataset.service;
      fetch('/complete_service', {
        method:'POST',
        headers: {'Content-Type':'application/x-www-form-urlencoded'},
        body: `service_id=${sid}`
      }).then(r=>r.json()).then(()=>{
        btn.closest('.trip-item').remove();
      });
    });
  });
});
