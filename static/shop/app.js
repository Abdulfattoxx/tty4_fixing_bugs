window.Telegram?.WebApp?.ready();
window.Telegram?.WebApp?.expand();

function applyTheme(params){
  const root=document.documentElement;
  root.style.setProperty('--bg',params.bg_color||'#fff');
  root.style.setProperty('--text',params.text_color||'#000');
  root.style.setProperty('--accent',params.button_color||'#ff4081');
}
applyTheme(window.Telegram?.WebApp?.themeParams||{});
window.Telegram?.WebApp?.onEvent('themeChanged',()=>applyTheme(window.Telegram.WebApp.themeParams));

function getCookie(name){
  const value=`; ${document.cookie}`;
  const parts=value.split(`; ${name}=`);
  if(parts.length===2) return parts.pop().split(';').shift();
}
async function apiFetch(url, options={}){
  options.headers=options.headers||{};
  options.headers['X-CSRFToken']=getCookie('csrftoken');
  options.credentials='same-origin';
  const res=await fetch(url, options);
  if(!res.ok) throw new Error('Request failed');
  return res.json();
}

function updateBadge(id,count){
  const el=document.getElementById(id);
  if(el) el.textContent=count>0?count:'';
}

async function toggleFav(btn){
  const pid=btn.dataset.productId;
  try{
    const data=await apiFetch('/api/favorites/toggle/',{method:'POST',body:new URLSearchParams({product_id:pid})});
    updateBadge('fav-badge',data.count);
  }catch(e){console.error(e);}
}

async function addToCart(btn){
  const slug=btn.dataset.slug;
  const qty=prompt('Qty','1');
  if(!qty) return;
  try{
    const data=await apiFetch('/api/cart/add/',{method:'POST',body:new URLSearchParams({slug:slug,qty:qty})});
    updateBadge('cart-badge',data.count);
  }catch(e){console.error(e);}
}

document.addEventListener('click',e=>{
  if(e.target.closest('.js-fav-toggle')){e.preventDefault();toggleFav(e.target.closest('.js-fav-toggle'));}
  if(e.target.closest('.js-add-to-cart')){e.preventDefault();addToCart(e.target.closest('.js-add-to-cart'));}
  if(e.target.classList.contains('js-qty-inc')||e.target.classList.contains('js-qty-dec')){
    e.preventDefault();
    const tr=e.target.closest('tr');
    const slug=e.target.dataset.slug;
    const qtyEl=tr.querySelector('.qty');
    let qty=parseInt(qtyEl.textContent,10);
    qty+=e.target.classList.contains('js-qty-inc')?1:-1;
    apiFetch('/api/cart/update/',{method:'POST',body:new URLSearchParams({slug:slug,qty:qty})}).then(data=>{
      qtyEl.textContent=qty;
      document.getElementById('cart-total').textContent=data.total;
      updateBadge('cart-badge',data.count);
    });
  }
  if(e.target.classList.contains('js-cart-remove')){
    e.preventDefault();
    const slug=e.target.dataset.slug;
    apiFetch('/api/cart/remove/',{method:'POST',body:new URLSearchParams({slug:slug})}).then(data=>{
      e.target.closest('tr').remove();
      updateBadge('cart-badge',data.count);
    });
  }
});

function debounce(fn,delay){let t;return function(...args){clearTimeout(t);t=setTimeout(()=>fn.apply(this,args),delay);};}
const searchInput=document.getElementById('search-input');
if(searchInput){
  searchInput.addEventListener('input',debounce(async function(){
    const q=this.value;
    const res=await fetch(`/search/?q=${encodeURIComponent(q)}`);
    const html=await res.text();
    const tmp=document.createElement('div');
    tmp.innerHTML=html;
    const grid=tmp.querySelector('#search-results');
    document.getElementById('search-results').innerHTML=grid?grid.innerHTML:'';
  },300));
}
