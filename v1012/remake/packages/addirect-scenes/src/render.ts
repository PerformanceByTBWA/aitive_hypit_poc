// render.ts — 장면별 HTML · CSS · 프레임 함수(htmlVisual). 좌표는 1920×1080 기준, within 크기에 맞춰 비율 조정.
// 장면 안 시각(프레임)은 원본 TIMELINE(05_판단기록)의 사건 시각을 장면 시작 기준으로 옮긴 값.
import { sealVisualTrack } from "@hypit/composition";
import type { VisualElement } from "@hypit/composition";
import { htmlVisual } from "@hypit/html-program";
import type { BlobRef } from "@hypit/hypit/protocol";
import type { FontArtifactRef } from "@hypit/media";
import type { Timeline } from "@hypit/timeline";
import type { SpatialFrame } from "@hypit/spatial";
import type { TemporalWindow } from "@hypit/temporal";

export const SCENES = ["bug", "title", "now", "select", "upload", "ttal", "cards", "promo", "band", "end"] as const;
export type SceneOptions = { id: string; scene: typeof SCENES[number]; stackOrder: number; copy: string[] };
type Fonts = { main: readonly FontArtifactRef[]; heavy: readonly FontArtifactRef[]; hand: readonly FontArtifactRef[] };
type Built = { html: string; css: string; setup?: string; data?: Record<string, unknown>; children: VisualElement[] };

const HELP = `const C=x=>Math.max(0,Math.min(1,x)),E=t=>t*t*(3-2*t),L=(a,b,t)=>a+(b-a)*t;`;

export function renderScene(timeline: Timeline, within: SpatialFrame, window: TemporalWindow, fonts: Fonts,
  options: SceneOptions, images: readonly BlobRef[]) {
  if (window.start.timelineId !== timeline.id) throw new Error("Scene window must belong to its Timeline.");
  let order = 0;
  const children: VisualElement[] = [];
  const copy = (i: number) => {
    const v = options.copy[i];
    if (v === undefined) throw new Error(`Scene ${options.id} (${options.scene}) needs copy item ${i + 1}.`);
    return v;
  };
  const text = (id: string, value: string, face: readonly FontArtifactRef[], size: number, color: string) => {
    children.push({ id, parent: "scene", kind: "text", order: ++order, text: value, fonts: face,
      style: [{ name: "font-size", value: `${size}px` }, { name: "color", value: color },
        { name: "white-space", value: "nowrap" }, { name: "line-height", value: "1.12" }] } as VisualElement);
    return `{{${id}}}`;
  };
  const img = (id: string, i: number) => {
    const artifact = images[i];
    if (artifact === undefined) throw new Error(`Scene ${options.id} (${options.scene}) needs image-${i + 1}.`);
    children.push({ id, parent: "scene", kind: "image", order: ++order, artifact,
      style: [{ name: "position", value: "absolute" }, { name: "left", value: 0 }, { name: "top", value: 0 },
        { name: "width", value: "100%" }, { name: "height", value: "100%" }, { name: "object-fit", value: "cover" }] } as VisualElement);
    return `{{${id}}}`;
  };
  const F = fonts;
  const cursor = `<svg class="cur" viewBox="0 0 40 52" width="40" height="52"><path d="M3 3 L3 43 L13 33 L21 50 L28 47 L20 30 L35 30 Z" fill="#6b3cf5" stroke="#fff" stroke-width="3" stroke-linejoin="round"/></svg>`;
  let b: Built;
  switch (options.scene) {
    case "bug":
      b = { html: `<div class="bug">${text("bug-k", copy(0), F.heavy, 30, "#5b2ee6")}${text("bug-e", copy(1), F.heavy, 17, "#5b2ee6")}</div>`,
        css: `.bug{position:absolute;left:30px;top:22px;display:flex;align-items:baseline;gap:6px}`, children };
      break;
    case "title":
      b = { html: `<div class="row"><div class="hand">${text("t-hand", copy(0), F.hand, 150, "#ffffff")}</div><div class="brand">${text("t-brand", copy(1), F.heavy, 64, "#ffffff")}</div></div>`,
        css: `.row{position:absolute;left:0;right:0;top:420px;display:flex;justify-content:center;align-items:center;gap:30px;filter:drop-shadow(0 3px 8px rgba(0,0,0,.35))}
          .hand{clip-path:inset(0 100% 0 0)} .brand{opacity:0}`,
        setup: `${HELP}const h=root.querySelector('.hand'),br=root.querySelector('.brand');
          return f=>{const p=E(C(f/15)),q=E(C((f-15)/6));h.style.clipPath='inset(0 '+((1-p)*100)+'% 0 0)';
          br.style.opacity=String(q);br.style.transform='translateX('+(-14*(1-q))+'px)';};`, children };
      break;
    case "now":
      b = { html: `<div class="now">${text("now-t", copy(0), F.main, 46, "#ffffff")}</div>`,
        css: `.now{position:absolute;left:250px;top:485px;opacity:0;filter:drop-shadow(0 2px 6px rgba(0,0,0,.25))}`,
        setup: `${HELP}const n=root.querySelector('.now');return f=>{const p=E(C(f/5));n.style.opacity=String(p);n.style.filter='blur('+((1-p)*6)+'px) drop-shadow(0 2px 6px rgba(0,0,0,.25))';};`, children };
      break;
    case "select":
      b = { html: `<div class="box"><i class="h a"></i><i class="h b"></i><i class="h c"></i><i class="h d"></i></div>
          <div class="ai"><div class="big">${text("ai-big", copy(0), F.heavy, 300, "#ffffff")}</div><div class="gen">${text("ai-gen", copy(1), F.heavy, 84, "#ffffff")}</div></div>${cursor}`,
        css: `.box{position:absolute;left:80px;top:150px;border:2px dashed rgba(255,255,255,.95)}
          .h{position:absolute;width:10px;height:10px;background:#fff;border:1px solid #bbb} .a{left:-6px;top:-6px}.b{right:-6px;top:-6px}.c{left:-6px;bottom:-6px}.d{right:-6px;bottom:-6px}
          .ai{position:absolute;left:110px;top:150px;opacity:0;transform-origin:20% 50%}
          .big *{background:linear-gradient(100deg,#f25fd8 0%,#9a5cff 50%,#2fb6ff 100%);-webkit-background-clip:text;background-clip:text;color:transparent !important}
          .gen{margin-top:-30px;padding-left:12px;filter:drop-shadow(0 2px 6px rgba(0,0,0,.3))}
          .cur{position:absolute;left:0;top:0}`,
        setup: `${HELP}const bx=root.querySelector('.box'),ai=root.querySelector('.ai'),cu=root.querySelector('.cur');
          return f=>{const g=E(C((f-1)/18)),w=520*g,h=440*g;bx.style.width=w+'px';bx.style.height=h+'px';
          bx.style.opacity=String(1-C((f-22)/4));cu.style.transform='translate('+(80+w-4)+'px,'+(150+h-4)+'px)';cu.style.opacity=String(1-C((f-20)/4));
          const a=E(C((f-19)/4));ai.style.opacity=String(a);ai.style.transform='scale('+L(.85,1,a)+')';};`, children };
      break;
    case "upload":
      b = { html: `<div class="bg"></div><div class="lab"><i class="ic"></i>${text("u-lab", copy(0), F.main, 20, "#55536a")}</div>
          <div class="panel"><svg class="pic" viewBox="0 0 24 24" width="30" height="30"><rect x="3" y="4" width="18" height="16" rx="3" fill="none" stroke="#6b3cf5" stroke-width="2"/><circle cx="9" cy="10" r="2" fill="#6b3cf5"/><path d="M5 18 L11 12 L15 16 L17 14 L20 17" fill="none" stroke="#6b3cf5" stroke-width="2"/></svg>
          <div class="u1">${text("u-1", copy(1), F.main, 30, "#222230")}</div><div class="u2">${text("u-2", copy(2), F.main, 17, "#9a98a8")}</div></div>
          <div class="card c2">${img("u-img2", 1)}</div><div class="card c1">${img("u-img1", 0)}</div>${cursor}
          <div class="ttal">${text("u-ttal", copy(3), F.heavy, 330, "#c8b4ff")}</div>`,
        css: `.bg{position:absolute;inset:0;background:#fff}
          .lab{position:absolute;left:535px;top:352px;display:flex;align-items:center;gap:10px}.ic{display:block;width:18px;height:18px;border-radius:4px;background:#6b3cf5}
          .panel{position:absolute;left:520px;top:392px;width:880px;height:200px;border-radius:18px;border:2px solid #e7e4f0;background:#fafafc;box-sizing:border-box}
          .pic{position:absolute;left:425px;top:26px}.u1{position:absolute;left:0;right:0;top:72px;display:flex;justify-content:center}.u2{position:absolute;left:0;right:0;top:128px;display:flex;justify-content:center}
          .card{position:absolute;left:0;top:0;width:250px;height:250px;border-radius:16px;overflow:hidden;background:#fff;box-shadow:0 18px 40px rgba(40,20,90,.22)}
          .c2{width:200px;height:200px}
          .cur{position:absolute;left:0;top:0}
          .ttal{position:absolute;left:30px;top:300px;opacity:0;transform-origin:30% 60%}`,
        setup: `${HELP}const p=root.querySelector('.panel'),c1=root.querySelector('.c1'),c2=root.querySelector('.c2'),cu=root.querySelector('.cur'),tt=root.querySelector('.ttal');
          return f=>{const m=E(C((f-8)/14)),x=L(1460,835,m),y=L(820,330,m),d=E(C((f-25)/7));
          c1.style.transform='translate('+x+'px,'+y+'px) rotate('+L(8,-4,m)+'deg) scale('+L(1,.55,d)+')';c1.style.opacity=String((f<8?0:1)*(1-d));
          c2.style.transform='translate('+(x+150)+'px,'+(y+70)+'px) rotate('+L(14,6,m)+'deg) scale('+L(1,.55,d)+')';c2.style.opacity=String((f<8?0:1)*(1-d));
          cu.style.transform='translate('+(x+200)+'px,'+(y+215)+'px)';cu.style.opacity=String(f<8?0:1-C((f-30)/4));
          const k=E(C((f-24)/6));p.style.background='rgb('+L(250,241,k)+','+L(250,236,k)+','+L(252,255,k)+')';p.style.borderColor='rgb('+L(231,185,k)+','+L(228,163,k)+','+L(240,255,k)+')';
          const t=C((f-36)/4);tt.style.opacity=String(t>0?1:0);tt.style.transform='scale('+L(1.18,1,E(t))+')';};`, children };
      break;
    case "ttal":
      b = { html: `<div class="l">${text("tt-l", copy(0), F.heavy, 330, "#c8b4ff")}</div><div class="r">${text("tt-r", copy(1), F.heavy, 330, "#9a78ff")}</div>`,
        css: `.l{position:absolute;left:30px;top:300px;opacity:.92}.r{position:absolute;left:1440px;top:300px;opacity:.9}`,
        setup: `${HELP}const r=root.querySelector('.r');return f=>{const p=E(C(f/6));r.style.transform='translateX('+((1-p)*240)+'px)';r.style.filter='blur('+((1-p)*14)+'px)';};`, children };
      break;
    case "cards": {
      const tab = (id: string, label: string) => `<div class="tab"><i></i>${text(id, label, F.main, 18, "#ffffff")}</div>`;
      const row = (n: number, li: number, vi: number) => `<div class="kv"><div class="k">${text(`c0-k${n}`, copy(li), F.main, 16, "#8a84a3")}</div><div class="v">${text(`c0-v${n}`, copy(vi), F.main, 22, "#222230")}</div></div>`;
      const sb = (n: number) => `<div class="sb"><div class="th">${img(`c1-img${n}`, n)}</div><div class="no">${text(`c1-n${n}`, String(n + 1), F.heavy, 24, "#6b3cf5")}</div><div class="sbt">${text(`c1-t${n}`, copy(10 + n), F.main, 19, "#2b2938")}</div></div>`;
      b = { html: `<div class="bg"></div><div class="deck">
          <div class="card k0">${tab("c0-tab", copy(0))}<div class="body"><div class="col">${row(0, 1, 2)}${row(1, 3, 4)}${row(2, 5, 6)}${row(3, 7, 8)}</div><div class="pt">${img("c0-prod", 3)}</div></div></div>
          <div class="card k1">${tab("c1-tab", copy(9))}<div class="body sbs">${sb(0)}${sb(1)}${sb(2)}</div></div>
          <div class="card k2">${tab("c2-tab", copy(13))}<div class="hero">${img("c2-img", 0)}</div><div class="lines"><i></i><i></i><i></i><i></i><i></i></div></div>
          <div class="card k3">${tab("c3-tab", copy(14))}<div class="hero wide">${img("c3-img", 2)}<div class="sel"></div></div></div></div>`,
        css: `.bg{position:absolute;inset:0;background:radial-gradient(circle at 50% 45%,#ffffff 0%,#f6f3ff 70%,#efe9ff 100%)}
          .deck{position:absolute;inset:0}
          .card{position:absolute;left:0;top:0;width:900px;height:540px;border-radius:24px;background:#fff;border:1px solid #ece8f7;box-shadow:0 24px 60px rgba(60,30,140,.16);overflow:hidden;opacity:0}
          .tab{position:absolute;left:28px;top:22px;display:flex;align-items:center;gap:8px;padding:6px 16px;border-radius:999px;background:#6b3cf5}.tab i{display:block;width:8px;height:8px;border-radius:50%;background:#fff}
          .body{position:absolute;left:48px;right:40px;top:86px;bottom:28px;display:flex;gap:32px}
          .col{flex:1;min-width:0;display:flex;flex-direction:column;gap:18px}.kv{display:flex;flex-direction:column;gap:4px}
          .pt{position:relative;flex:none;width:240px;height:240px;border-radius:16px;overflow:hidden;border:1px solid #eee}
          .sbs{flex-direction:column;gap:14px}.sb{position:relative;display:flex;align-items:center;gap:18px;height:118px}
          .th{position:relative;width:210px;height:118px;border-radius:10px;overflow:hidden;flex:none}.no{width:30px}
          .hero{position:absolute;left:40px;top:84px;width:600px;height:338px;border-radius:14px;overflow:hidden}
          .hero.wide{width:820px;height:420px}
          .lines{position:absolute;left:670px;top:96px;width:190px}.lines i{display:block;height:12px;margin:0 0 22px;border-radius:6px;background:#ece9f5}
          .sel{position:absolute;left:38.5%;top:60%;width:13%;height:34%;border:2px dashed #fff;box-shadow:0 0 0 1px rgba(107,60,245,.6)}`,
        data: { enter: [5, 17, 36, 65], push: 86 },
        setup: `${HELP}const cs=[...root.querySelectorAll('.card')],deck=root.querySelector('.deck'),sel=root.querySelector('.sel');
          return f=>{cs.forEach((c,k)=>{const e=data.enter[k];if(f<e){c.style.opacity='0';return;}
            const p=E(C((f-e)/8));let d=0;for(let j=k+1;j<cs.length;j++)d+=E(C((f-data.enter[j])/8));
            const x=420+d*70-(1-p)*160,y=230+d*45-(1-p)*100,s=(1-d*.03)*L(.96,1,p);
            c.style.opacity=String(p*Math.max(0,1-d*.2));c.style.zIndex=String(10+k);c.style.filter='blur('+((1-p)*10)+'px)';
            c.style.transform='translate('+x+'px,'+y+'px) scale('+s+')';});
            sel.style.opacity=String(C((f-70)/4));
            const z=E(C((f-data.push)/4));deck.style.transformOrigin='960px 520px';deck.style.transform='scale('+L(1,1.9,z)+')';deck.style.filter='blur('+(z*8)+'px)';};`, children };
      break;
    }
    case "promo":
      b = { html: `<div class="bgi">${img("p-bg", 0)}</div><div class="sm">${text("p-sm", copy(0), F.main, 34, "#ffffff")}</div>
          <div class="mu o">${text("p-mu-o", copy(1), F.heavy, 230, "#ffffff")}</div><div class="mu fill">${text("p-mu-f", copy(1), F.heavy, 230, "#ffffff")}</div>`,
        css: `.bgi{position:absolute;inset:0;overflow:hidden;transform-origin:65% 45%}
          .sm{position:absolute;left:100px;top:120px;clip-path:inset(0 100% 0 0);filter:drop-shadow(0 2px 5px rgba(0,0,0,.35))}
          .mu{position:absolute;left:90px;top:170px}.o *{color:transparent !important;-webkit-text-stroke:3px rgba(255,255,255,.95)}.fill{opacity:0;filter:drop-shadow(0 3px 8px rgba(0,0,0,.25))}`,
        data: { n: Array.from(copy(0)).length, typeFrom: 5, typeTo: 38, fill: 53 },
        setup: `${HELP}const bg=root.querySelector('.bgi'),sm=root.querySelector('.sm'),fi=root.querySelector('.fill');
          return f=>{bg.style.transform='scale('+L(1,1.04,C(f/70))+')';
          const shown=Math.floor(C((f-data.typeFrom)/(data.typeTo-data.typeFrom))*data.n+.0001);sm.style.clipPath='inset(0 '+(100-shown/data.n*100)+'% 0 0)';
          fi.style.opacity=String(E(C((f-data.fill)/3)));};`, children };
      break;
    case "band": {
      const conf = Array.from({ length: 24 }, (_, i) => ({ x: 1230 + ((i * 97) % 560), y: 640 + ((i * 53) % 250), c: ["#ff6fb5", "#ffc93c", "#5ad8ff", "#8f6bff", "#4ce0a0"][i % 5], d: (i * 3) % 14, r: (i * 37) % 360 }));
      b = { html: `<div class="fade"></div><div class="txt"><div>${text("bd-0", copy(0), F.heavy, 30, "#16151c")}</div><div>${text("bd-1", copy(1), F.heavy, 68, "#16151c")}</div>
          <div class="ln">${text("bd-2", copy(2), F.heavy, 68, "#5b2ee6")}${text("bd-3", copy(3), F.heavy, 68, "#16151c")}</div></div>
          <div class="won">${text("bd-4", copy(4), F.heavy, 250, "#ffffff")}</div><div class="conf">${conf.map(() => "<i></i>").join("")}</div>`,
        css: `.fade{position:absolute;left:0;right:0;top:600px;bottom:0;background:linear-gradient(to bottom,rgba(255,255,255,0) 0%,rgba(255,255,255,.88) 32%,#f3efff 68%,#e4dbff 100%)}
          .txt{position:absolute;left:70px;top:752px;display:flex;flex-direction:column;gap:2px}.ln{display:flex;gap:14px}
          .won{position:absolute;left:1330px;top:670px;transform:skewX(-10deg);filter:drop-shadow(0 10px 18px rgba(60,20,180,.35))}
          .won *{background:linear-gradient(160deg,#a58bff 0%,#6a45ff 45%,#3417c9 100%);-webkit-background-clip:text;background-clip:text;color:transparent !important;-webkit-text-stroke:4px #ffffff}
          .conf i{position:absolute;display:block;width:16px;height:9px;border-radius:2px;opacity:0}`,
        data: { conf, from: 46 },
        setup: `${HELP}const is=[...root.querySelectorAll('.conf i')];is.forEach((e,i)=>{const c=data.conf[i];e.style.background=c.c;});
          return f=>{is.forEach((e,i)=>{const c=data.conf[i],t=f-data.from-c.d;if(t<0){e.style.opacity='0';return;}
            const p=E(C(t/6));e.style.opacity=String(p);e.style.transform='translate('+c.x+'px,'+(c.y+Math.sin((t+c.d)/7)*6)+'px) rotate('+(c.r+t*4)+'deg) scale('+L(.3,1,p)+')';});};`, children };
      break;
    }
    case "end":
      b = { html: `<div class="bg"></div><div class="logo"><div class="ae">${text("e-ae", copy(0), F.heavy, 140, "#ffffff")}</div><div class="rest">${text("e-rest", copy(1), F.heavy, 140, "#ffffff")}</div><div class="en">${text("e-en", copy(2), F.heavy, 64, "#ffffff")}</div></div>
          <div class="sub">${text("e-sub", copy(3), F.main, 28, "#ffffff")}</div>`,
        css: `.bg{position:absolute;inset:0;background:linear-gradient(135deg,#5326e6 0%,#6a3cf7 60%,#7a52ff 100%)}
          .logo{position:absolute;left:0;right:0;top:200px;display:flex;justify-content:center;align-items:baseline}
          .ae{transform-origin:50% 60%}.rest{clip-path:inset(0 100% 0 0)}.en{margin-left:14px;transform:skewX(-10deg);opacity:0}
          .sub{position:absolute;left:0;right:0;top:385px;display:flex;justify-content:center;opacity:0}`,
        setup: `${HELP}const ae=root.querySelector('.ae'),re=root.querySelector('.rest'),en=root.querySelector('.en'),sb=root.querySelector('.sub');
          return f=>{const a=E(C(f/5));ae.style.transform='translate('+((1-a)*160)+'px,'+((1-a)*220)+'px) scale('+L(7,1,a)+')';
          ae.style.filter='drop-shadow(0 0 '+((1-a)*40+4)+'px rgba(255,255,255,'+L(.95,.35,a)+'))';ae.style.opacity=String(C(f/2+.4));
          const r=C((f-13)/9),j=(r>0&&r<1)?((f%2)*6-3):0;re.style.clipPath='inset(0 '+((1-r)*100)+'% 0 0)';re.style.transform='translateX('+j+'px)';
          const n=E(C((f-26)/10));en.style.opacity=String(n);en.style.transform='skewX(-10deg) translateY('+((1-n)*16)+'px)';
          sb.style.opacity=String(E(C((f-6)/6)));};`, children };
      break;
    default:
      throw new Error(`Unknown scene ${String(options.scene)}`);
  }
  const scale = within.widthPx / 1920;
  const program = htmlVisual({ html: `<div class="stage">${b.html}</div>`,
    css: `:scope{overflow:hidden}.stage{position:absolute;left:0;top:0;width:1920px;height:1080px;transform-origin:0 0;transform:scale(${scale})}${b.css}`,
    ...(b.setup ? { setup: b.setup } : {}), ...(b.data ? { data: b.data as never } : {}) });
  return sealVisualTrack({ id: options.id, timelineId: timeline.id, visualIr: "hypit.visual-ir@1",
    presents: [{ id: options.id, order: 0, z: options.stackOrder, span: window.span,
      elements: [{ id: "scene", kind: "program", order: 0, program,
        style: [{ name: "position", value: "absolute" }, { name: "left", value: `${within.xPx}px` },
          { name: "top", value: `${within.yPx}px` }, { name: "width", value: `${within.widthPx}px` },
          { name: "height", value: `${within.heightPx}px` }] }, ...b.children] }] });
}
