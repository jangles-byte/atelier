/* shared generative toolkit — seeded prng, perlin, fbm, oklch LUTs */
const mulberry32 = a => () => { a |= 0; a = a + 0x6D2B79F5 | 0;
  let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
  return ((t ^ t >>> 14) >>> 0) / 4294967296; };

function makeNoise(rnd){                       // seeded permutation, so reloads match
  const p = new Uint8Array(512), t = Array.from({length:256},(_,i)=>i);
  for (let i=255;i>0;i--){ const j=(rnd()*(i+1))|0; [t[i],t[j]]=[t[j],t[i]]; }
  for (let i=0;i<512;i++) p[i]=t[i&255];
  const fade=x=>x*x*x*(x*(x*6-15)+10), lerp=(a,b,x)=>a+(b-a)*x;
  const grad=(h,x,y,z)=>{const g=h&15,u=g<8?x:y,v=g<4?y:(g===12||g===14?x:z);
    return ((g&1)===0?u:-u)+((g&2)===0?v:-v);};
  return function(x,y,z){
    const X=Math.floor(x)&255,Y=Math.floor(y)&255,Z=Math.floor(z)&255;
    x-=Math.floor(x); y-=Math.floor(y); z-=Math.floor(z);
    const u=fade(x),v=fade(y),w=fade(z);
    const A=p[X]+Y,AA=p[A]+Z,AB=p[A+1]+Z,B=p[X+1]+Y,BA=p[B]+Z,BB=p[B+1]+Z;
    return lerp(lerp(lerp(grad(p[AA],x,y,z),grad(p[BA],x-1,y,z),u),
                     lerp(grad(p[AB],x,y-1,z),grad(p[BB],x-1,y-1,z),u),v),
                lerp(lerp(grad(p[AA+1],x,y,z-1),grad(p[BA+1],x-1,y,z-1),u),
                     lerp(grad(p[AB+1],x,y-1,z-1),grad(p[BB+1],x-1,y-1,z-1),u),v),w);};
}
const fbm = (n,x,y,z,oct=2,lac=1.97,gain=0.5)=>{
  let a=1,f=1,s=0,norm=0;
  for(let i=0;i<oct;i++){ s+=a*n(x*f,y*f,z*f); norm+=a; a*=gain; f*=lac; }
  return s/norm;
};

/* OKLCH -> sRGB, and a 256-entry ramp LUT so per-pixel work stays cheap */
function oklch(L,C,H){
  const a=C*Math.cos(H*Math.PI/180), b=C*Math.sin(H*Math.PI/180);
  const l_=L+0.3963377774*a+0.2158037573*b, m_=L-0.1055613458*a-0.0638541728*b,
        s_=L-0.0894841775*a-1.2914855480*b;
  const l=l_**3,m=m_**3,s=s_**3;
  const r= 4.0767416621*l-3.3077115913*m+0.2309699292*s,
        g=-1.2684380046*l+2.6097574011*m-0.3413193965*s,
        bb=-0.0041960863*l-0.7034186147*m+1.7076147010*s;
  const e=v=>{v=Math.max(0,Math.min(1,v));
    return Math.round(255*(v>0.0031308?1.055*Math.pow(v,1/2.4)-0.055:12.92*v));};
  return [e(r),e(g),e(bb)];
}
/* stops: [[t, L, C, H], ...] with t 0..1 — chroma should rise with lightness */
function ramp(stops,n=256){
  const out=new Uint8Array(n*3);
  for(let i=0;i<n;i++){
    const t=i/(n-1);
    let a=stops[0],b=stops[stops.length-1];
    for(let k=0;k<stops.length-1;k++) if(t>=stops[k][0]&&t<=stops[k+1][0]){a=stops[k];b=stops[k+1];break;}
    const f=b[0]===a[0]?0:(t-a[0])/(b[0]-a[0]);
    const [r,g,bl]=oklch(a[1]+(b[1]-a[1])*f, a[2]+(b[2]-a[2])*f, a[3]+(b[3]-a[3])*f);
    out[i*3]=r; out[i*3+1]=g; out[i*3+2]=bl;
  }
  return out;
}
const clamp=(v,a,b)=>v<a?a:v>b?b:v;
