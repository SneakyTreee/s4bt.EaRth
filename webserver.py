import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path


RES_FILE = Path(__file__).with_name("res.json")


HTML_TEMPLATE = r"""
<!DOCTYPE html>
<html lang="en">

<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>EaRth Plant Monitor</title>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

<style>

:root{
    --accent: #4ddcff;
    --accent-2: #0066ff;
    --warn: #ff9800;
    --danger: #ff5252;
    --good: #6bff9e;
    --card-bg: rgba(255,255,255,.06);
    --card-border: rgba(255,255,255,.14);
}

*{
    margin:0;
    padding:0;
    box-sizing:border-box;
}

html,body{
    height:100%;
}

body{
    font-family:'Poppins', 'Segoe UI', sans-serif;
    min-height:100vh;
    padding:32px 20px 60px;
    color:#eef2f5;
    overflow-x:hidden;
    position:relative;
    background:#0a1a20;
}

/* ===== animated ambient background ===== */
.bg-glow{
    position:fixed;
    inset:0;
    z-index:-2;
    background:
        radial-gradient(circle at 20% 20%, rgba(77,220,255,.18), transparent 45%),
        radial-gradient(circle at 80% 15%, rgba(107,255,158,.12), transparent 40%),
        radial-gradient(circle at 50% 90%, rgba(0,102,255,.20), transparent 50%),
        linear-gradient(160deg, #0f2a33, #081418 75%);
    background-size:200% 200%, 200% 200%, 200% 200%, 100% 100%;
    animation: driftGlow 22s ease-in-out infinite;
}

@keyframes driftGlow{
    0%{background-position:0% 0%, 100% 0%, 50% 100%, 0 0;}
    50%{background-position:30% 40%, 60% 30%, 40% 60%, 0 0;}
    100%{background-position:0% 0%, 100% 0%, 50% 100%, 0 0;}
}

.leaf-field{
    position:fixed;
    inset:0;
    z-index:-1;
    overflow:hidden;
    pointer-events:none;
}

.leaf{
    position:absolute;
    bottom:-10%;
    font-size:1.4rem;
    opacity:.18;
    animation: floatUp linear infinite;
}

@keyframes floatUp{
    0%{ transform:translateY(0) rotate(0deg); opacity:0; }
    10%{ opacity:.25; }
    90%{ opacity:.2; }
    100%{ transform:translateY(-115vh) rotate(340deg); opacity:0; }
}

.container{
    max-width:920px;
    margin:auto;
    position:relative;
}

header{
    text-align:center;
    margin-bottom:28px;
    animation: dropIn .7s cubic-bezier(.2,.9,.3,1.2);
}

h1{
    font-size:2.4rem;
    font-weight:800;
    letter-spacing:-.5px;
    background:linear-gradient(90deg,#ffffff, var(--accent) 60%, var(--good));
    -webkit-background-clip:text;
    background-clip:text;
    color:transparent;
    text-shadow:0 10px 30px rgba(0,0,0,.35);
}

.subtitle{
    margin-top:8px;
    opacity:.65;
    font-size:.82rem;
    letter-spacing:2px;
    display:flex;
    align-items:center;
    justify-content:center;
    gap:8px;
    text-transform:uppercase;
}

.live-dot{
    position:relative;
    width:10px;
    height:10px;
    border-radius:50%;
    background:var(--good);
    box-shadow:0 0 0 0 rgba(107,255,158,.6);
    animation: pulseRing 1.8s infinite;
}

@keyframes pulseRing{
    0%{ box-shadow:0 0 0 0 rgba(107,255,158,.55); }
    70%{ box-shadow:0 0 0 10px rgba(107,255,158,0); }
    100%{ box-shadow:0 0 0 0 rgba(107,255,158,0); }
}

@keyframes dropIn{
    from{ opacity:0; transform:translateY(-16px); }
    to{ opacity:1; transform:translateY(0); }
}

/* ===== main card ===== */
.card{
    background:var(--card-bg);
    backdrop-filter:blur(22px) saturate(140%);
    -webkit-backdrop-filter:blur(22px) saturate(140%);
    border-radius:28px;
    padding:36px clamp(18px,4vw,44px) 40px;
    border:1px solid var(--card-border);
    box-shadow:0 25px 70px rgba(0,0,0,.45), inset 0 1px 0 rgba(255,255,255,.06);
    position:relative;
    overflow:hidden;
    animation: riseIn .8s cubic-bezier(.2,.85,.3,1.1);
}

@keyframes riseIn{
    from{ opacity:0; transform:translateY(24px) scale(.98); }
    to{ opacity:1; transform:translateY(0) scale(1); }
}

.card::before{
    content:"";
    position:absolute;
    top:-60%;
    left:-20%;
    width:140%;
    height:220%;
    background:conic-gradient(from 0deg, transparent 0 300deg, rgba(255,255,255,.05) 340deg, transparent 360deg);
    animation: sheen 8s linear infinite;
    pointer-events:none;
}

@keyframes sheen{
    to{ transform:rotate(360deg); }
}

.plant-head{
    text-align:center;
    margin-bottom:6px;
    position:relative;
    z-index:1;
}

.status-icon{
    font-size:3.6rem;
    display:inline-block;
    transition:transform .4s ease, filter .4s ease;
    filter:drop-shadow(0 6px 14px rgba(0,0,0,.4));
}

.status-icon.bump{
    animation: bump .5s ease;
}

@keyframes bump{
    0%,100%{ transform:scale(1); }
    40%{ transform:scale(1.18) rotate(-4deg); }
    70%{ transform:scale(.95) rotate(3deg); }
}

.plant-name{
    font-size:1.7rem;
    font-weight:700;
    margin-top:6px;
}

.device-id{
    opacity:.5;
    font-size:.8rem;
    font-family:'JetBrains Mono', monospace;
    margin-top:2px;
}

.status-text{
    text-align:center;
    font-size:1.05rem;
    margin-top:14px;
    min-height:1.4em;
    font-weight:500;
    transition:opacity .3s ease;
}

/* ===== water circle ===== */
.water-container{
    display:flex;
    justify-content:center;
    margin:38px 0 28px;
    position:relative;
    z-index:1;
}

.water-circle{
    width:230px;
    height:230px;
    border-radius:50%;
    position:relative;
    overflow:hidden;
    background:rgba(255,255,255,.06);
    border:3px solid rgba(255,255,255,.4);
    box-shadow:
        0 0 45px rgba(77,220,255,.35),
        inset 0 0 30px rgba(0,0,0,.25),
        inset 0 12px 24px rgba(255,255,255,.15),
        inset 0 -12px 20px rgba(0,0,0,.2);
    transition: box-shadow .6s ease, border-color .6s ease;
}

.glass-shine{
    position:absolute;
    top:-30%;
    left:-60%;
    width:55%;
    height:160%;
    background:linear-gradient(120deg, transparent 30%, rgba(255,255,255,.4) 50%, transparent 68%);
    transform:rotate(18deg);
    opacity:.4;
    z-index:4;
    pointer-events:none;
    animation: shineSweep 6.5s ease-in-out infinite;
}

@keyframes shineSweep{
    0%,100%{ left:-60%; opacity:.2; }
    50%{ left:85%; opacity:.55; }
}

.water-fill{
    position:absolute;
    bottom:0;
    width:100%;
    height:50%;
    background:linear-gradient(#4ddcff,#0066ff);
    transition: height 1.1s cubic-bezier(.4,1.4,.4,1), background 1s ease;
}

.wave{
    position:absolute;
    top:-22px;
    left:-50%;
    width:200%;
    height:44px;
    background:rgba(255,255,255,.32);
    border-radius:45%;
    animation: wave 5s linear infinite;
}

.wave:nth-child(2){
    animation-duration:7s;
    animation-direction:reverse;
    opacity:.45;
    top:-16px;
}

@keyframes wave{
    from{ transform:translateX(0) rotate(0deg); }
    to{ transform:translateX(-50%) rotate(360deg); }
}

.bubble{
    position:absolute;
    bottom:0;
    width:6px;
    height:6px;
    border-radius:50%;
    background:rgba(255,255,255,.55);
    animation: rise 3.4s ease-in infinite;
}

@keyframes rise{
    0%{ transform:translateY(0) scale(1); opacity:0; }
    15%{ opacity:.8; }
    100%{ transform:translateY(-190px) scale(.4); opacity:0; }
}

/* ===== overflow splash fx (inactive unless .overflow) ===== */
.ripple{
    position:absolute;
    top:50%;
    left:50%;
    width:10px;
    height:10px;
    border:2px solid rgba(255,255,255,.65);
    border-radius:50%;
    transform:translate(-50%,-50%);
    opacity:0;
    z-index:4;
    pointer-events:none;
}

.splash-drop{
    position:absolute;
    top:50%;
    left:50%;
    font-size:1.15rem;
    opacity:0;
    z-index:4;
    pointer-events:none;
}

.splash-drop::before{
    content:"💧";
}

/* ===== dry desert fx (inactive unless .dry) ===== */
.dust{
    position:absolute;
    bottom:8px;
    width:4px;
    height:4px;
    border-radius:50%;
    background:rgba(214,176,128,.8);
    opacity:0;
    z-index:3;
    pointer-events:none;
}

.heat-shimmer{
    position:absolute;
    left:6%;
    right:6%;
    top:14px;
    height:24px;
    background:linear-gradient(180deg, rgba(255,205,130,.28), transparent);
    filter:blur(3px);
    opacity:0;
    z-index:3;
    pointer-events:none;
}

.tumbleweed{
    position:absolute;
    bottom:10px;
    left:-40px;
    width:30px;
    height:30px;
    opacity:0;
    z-index:6;
    pointer-events:none;
}

.tumbleweed span{
    position:absolute;
    inset:0;
    border:2px solid rgba(196,148,92,.85);
    border-radius:50%;
}

.tumbleweed span:nth-child(1){ transform:rotate(15deg) scaleX(.55); }
.tumbleweed span:nth-child(2){ transform:rotate(75deg) scaleY(.55); }
.tumbleweed span:nth-child(3){ transform:rotate(-35deg) scale(.75); }

.water-text{
    position:absolute;
    inset:0;
    display:flex;
    flex-direction:column;
    justify-content:center;
    align-items:center;
    z-index:5;
    text-shadow:0 3px 12px rgba(0,0,0,.6);
    pointer-events:none;
}

.water-percent{
    font-size:2.7rem;
    font-weight:800;
    font-variant-numeric:tabular-nums;
}

.water-label{
    opacity:.75;
    font-size:.85rem;
    letter-spacing:1px;
    text-transform:uppercase;
    margin-top:2px;
}

.water-circle.overflow{
    animation: shake .35s infinite;
    border-color:#00d0ff;
    box-shadow:0 0 55px #00ccff, 0 0 110px rgba(0,119,255,.6);
}

.water-circle.overflow .water-fill{
    animation: overflowWave .9s infinite;
}

.water-circle.overflow::after{
    content:"💦";
    position:absolute;
    top:-42px;
    left:50%;
    transform:translateX(-50%);
    font-size:2.6rem;
    animation: splash 1s infinite;
    z-index:6;
}

@keyframes splash{
    0%{ opacity:0; transform:translate(-50%,0) scale(.5); }
    50%{ opacity:1; }
    100%{ opacity:0; transform:translate(-50%,-55px) scale(1.2); }
}

@keyframes overflowWave{
    50%{ transform:translateY(-10px); }
}

@keyframes shake{
    25%{ transform:translateX(4px); }
    75%{ transform:translateX(-4px); }
}

.water-circle.overflow .ripple{
    animation: rippleOut 1.5s ease-out infinite;
}

.water-circle.overflow .ripple.ripple2{
    animation-delay:.75s;
}

@keyframes rippleOut{
    0%{ width:14px; height:14px; opacity:.75; border-width:3px; }
    100%{ width:230px; height:230px; opacity:0; border-width:1px; }
}

.water-circle.overflow .splash-drop{
    animation: dropletFly 1.2s ease-out infinite;
}

@keyframes dropletFly{
    0%{ transform:translate(-50%,-50%) scale(.3) rotate(0deg); opacity:0; }
    12%{ opacity:1; }
    100%{
        transform:translate(calc(-50% + var(--dx)), calc(-50% + var(--dy))) scale(1) rotate(50deg);
        opacity:0;
    }
}

/* ===== glass shattering under too much water ===== */
.crack{
    position:absolute;
    height:2px;
    background:linear-gradient(90deg, transparent, rgba(255,255,255,.9), transparent);
    opacity:0;
    z-index:6;
    pointer-events:none;
    transform-origin:center;
}

.crack1{ top:35%; left:6%;  width:55%; transform:rotate(24deg); }
.crack2{ top:55%; left:38%; width:58%; transform:rotate(-18deg); }
.crack3{ top:18%; left:32%; width:38%; transform:rotate(70deg); }
.crack4{ top:68%; left:12%; width:46%; transform:rotate(-42deg); }

.shard{
    position:absolute;
    width:32px;
    height:32px;
    background:linear-gradient(135deg, rgba(255,255,255,.6), rgba(120,205,255,.3));
    clip-path:polygon(50% 0%, 100% 100%, 0% 100%);
    opacity:0;
    z-index:7;
    pointer-events:none;
    box-shadow:0 2px 6px rgba(0,60,100,.3);
}

.s1{ top:28%; left:18%; }
.s2{ top:20%; left:54%; width:24px; height:24px; }
.s3{ top:48%; left:68%; transform:rotate(45deg); }
.s4{ top:58%; left:14%; width:20px; height:20px; transform:rotate(-25deg); }
.s5{ top:38%; left:42%; width:28px; height:28px; transform:rotate(95deg); }

.gush{
    position:absolute;
    width:6px;
    height:32px;
    border-radius:4px;
    background:linear-gradient(#cdf4ff,#2f9dff);
    opacity:0;
    z-index:6;
    filter:blur(.4px);
    pointer-events:none;
}

.g1{ top:36%; left:10%; }
.g2{ top:58%; left:76%; }
.g3{ top:20%; left:58%; }

.water-circle.overflow .crack{
    animation: crackFlash 1.8s ease-in-out infinite;
}
.water-circle.overflow .crack2{ animation-delay:.15s; }
.water-circle.overflow .crack3{ animation-delay:.3s; }
.water-circle.overflow .crack4{ animation-delay:.45s; }

@keyframes crackFlash{
    0%{ opacity:0; }
    8%{ opacity:1; }
    40%{ opacity:.75; }
    70%{ opacity:.9; }
    100%{ opacity:0; }
}

.water-circle.overflow .shard{
    animation: shardFall 1.8s cubic-bezier(.5,0,.9,.4) infinite;
}
.water-circle.overflow .s2{ animation-delay:.2s; }
.water-circle.overflow .s3{ animation-delay:.4s; }
.water-circle.overflow .s4{ animation-delay:.6s; }
.water-circle.overflow .s5{ animation-delay:.8s; }

@keyframes shardFall{
    0%{ opacity:0; transform:translateY(0) rotate(0deg) scale(1); }
    10%{ opacity:1; }
    100%{ opacity:0; transform:translateY(160px) rotate(220deg) scale(.6); }
}

.water-circle.overflow .gush{
    animation: gushOut 1.1s ease-in infinite;
}
.water-circle.overflow .g2{ animation-delay:.3s; }
.water-circle.overflow .g3{ animation-delay:.6s; }

@keyframes gushOut{
    0%{ opacity:0; transform:translate(0,0) rotate(0deg) scaleY(.4); }
    15%{ opacity:1; }
    100%{ opacity:0; transform:translate(60px,90px) rotate(70deg) scaleY(1.3); }
}

.water-circle.dry{
    border-color:#ff8c42;
    box-shadow:0 0 55px rgba(255,102,0,.55);
    animation: dryPulse 2.2s infinite;
}

.water-circle.dry .water-fill{
    height:14% !important;
    background:linear-gradient(#c9822f,#5a2c05) !important;
    position:absolute;
}

.water-circle.dry .water-fill::before{
    content:"";
    position:absolute;
    inset:0;
    background:
        repeating-linear-gradient(112deg, transparent 0 13px, rgba(0,0,0,.28) 13px 14.5px),
        repeating-linear-gradient(20deg, transparent 0 17px, rgba(0,0,0,.22) 17px 18.5px);
    mix-blend-mode:multiply;
}

.water-circle.dry::before{
    content:"🌵";
    position:absolute;
    bottom:6px;
    left:50%;
    transform:translateX(-50%);
    font-size:1.6rem;
    opacity:.5;
    z-index:4;
}

@keyframes dryPulse{
    50%{ box-shadow:0 0 85px rgba(255,60,0,.7); }
}

.water-circle.dry .tumbleweed{
    opacity:.9;
    animation: rollAcross 4.2s linear infinite;
}

@keyframes rollAcross{
    0%{ left:-40px; bottom:10px; transform:rotate(0deg); }
    16%{ bottom:34px; }
    33%{ left:90px; bottom:10px; transform:rotate(360deg); }
    49%{ bottom:30px; }
    66%{ left:190px; bottom:10px; transform:rotate(680deg); }
    82%{ bottom:26px; }
    100%{ left:280px; bottom:10px; transform:rotate(1000deg); }
}

.water-circle.dry .heat-shimmer{
    opacity:.65;
    animation: shimmerWave 2.4s ease-in-out infinite;
}

@keyframes shimmerWave{
    0%,100%{ transform:translateX(-4px) scaleY(1); }
    50%{ transform:translateX(4px) scaleY(1.35); }
}

.water-circle.dry .dust{
    animation: driftDust 3.2s ease-in-out infinite;
}

@keyframes driftDust{
    0%{ opacity:0; transform:translate(0,0) scale(1); }
    20%{ opacity:.75; }
    100%{ opacity:0; transform:translate(38px,-16px) scale(.6); }
}

.sand-pile{
    position:absolute;
    left:0;
    right:0;
    bottom:0;
    height:0;
    background:
        radial-gradient(circle at 20% 30%, rgba(0,0,0,.14) 0 2px, transparent 3px),
        radial-gradient(circle at 62% 62%, rgba(0,0,0,.1) 0 2px, transparent 3px),
        radial-gradient(circle at 80% 22%, rgba(0,0,0,.1) 0 2px, transparent 3px),
        linear-gradient(#e6bd80,#a97a42);
    background-size:18px 18px, 22px 22px, 16px 16px, 100% 100%;
    clip-path:polygon(0% 100%, 8% 58%, 22% 74%, 38% 52%, 55% 78%, 70% 56%, 88% 80%, 100% 60%, 100% 100%);
    opacity:0;
    transition:height .9s ease, opacity .5s ease;
    z-index:2;
    pointer-events:none;
}

.water-circle.dry .sand-pile{
    height:36%;
    opacity:1;
}

.sand-grain{
    position:absolute;
    top:-6%;
    width:3px;
    height:3px;
    border-radius:50%;
    background:rgba(214,176,120,.9);
    opacity:0;
    z-index:2;
    pointer-events:none;
}

.water-circle.dry .sand-grain{
    animation: sandFall 2.6s linear infinite;
}

@keyframes sandFall{
    0%{ opacity:0; transform:translateY(0); }
    10%{ opacity:.85; }
    85%{ opacity:.55; }
    100%{ opacity:0; transform:translateY(190px); }
}

.dust-puff{
    position:absolute;
    bottom:8px;
    width:12px;
    height:12px;
    border-radius:50%;
    background:radial-gradient(circle, rgba(216,178,128,.65), transparent 70%);
    opacity:0;
    z-index:5;
    pointer-events:none;
}

.water-circle.dry .dust-puff{
    animation: puffOut 4.2s ease-out infinite;
}

.water-circle.dry .puff2{ animation-delay:1.4s; }
.water-circle.dry .puff3{ animation-delay:2.8s; }

@keyframes puffOut{
    0%,45%{ opacity:0; transform:scale(.3); }
    50%{ opacity:.7; transform:scale(1); }
    70%{ opacity:0; transform:scale(1.9); }
    100%{ opacity:0; }
}

/* ===== sparkline ===== */
.sparkline-wrap{
    text-align:center;
    margin:-6px 0 24px;
    opacity:.85;
    position:relative;
    z-index:1;
}

.sparkline-label{
    font-size:.7rem;
    letter-spacing:1.5px;
    text-transform:uppercase;
    opacity:.5;
    margin-bottom:6px;
}

canvas#sparkline{
    max-width:100%;
}

/* ===== metrics grid ===== */
.grid{
    display:grid;
    grid-template-columns:repeat(auto-fit,minmax(140px,1fr));
    gap:14px;
    position:relative;
    z-index:1;
}

.metric{
    background:rgba(255,255,255,.05);
    padding:18px 14px;
    border-radius:18px;
    text-align:center;
    border:1px solid rgba(255,255,255,.08);
    transition: transform .3s ease, background .3s ease, border-color .3s ease;
    opacity:0;
    transform:translateY(14px);
    animation: metricIn .6s ease forwards;
}

.metric:nth-child(1){ animation-delay:.05s; }
.metric:nth-child(2){ animation-delay:.1s; }
.metric:nth-child(3){ animation-delay:.15s; }
.metric:nth-child(4){ animation-delay:.2s; }
.metric:nth-child(5){ animation-delay:.25s; }
.metric:nth-child(6){ animation-delay:.3s; }

@keyframes metricIn{
    to{ opacity:1; transform:translateY(0); }
}

.metric:hover{
    transform:translateY(-4px);
    background:rgba(255,255,255,.09);
    border-color:rgba(255,255,255,.18);
}

.metric-icon{
    font-size:1.3rem;
    margin-bottom:4px;
    opacity:.8;
}

.metric-label{
    opacity:.6;
    font-size:.72rem;
    letter-spacing:1.2px;
    text-transform:uppercase;
}

.metric-value{
    font-size:1.4rem;
    font-weight:700;
    margin-top:4px;
    font-variant-numeric:tabular-nums;
    transition:color .4s ease;
}

.metric-value.warn{ color:var(--warn); }
.metric-value.danger{ color:var(--danger); }
.metric-value.good{ color:var(--good); }

.metric-unit{
    opacity:.55;
    font-size:.85rem;
}

.last-updated{
    text-align:center;
    opacity:.55;
    margin-top:26px;
    font-size:.8rem;
    font-family:'JetBrains Mono', monospace;
    position:relative;
    z-index:1;
}

@media (max-width:480px){
    h1{ font-size:1.85rem; }
    .water-circle{ width:190px; height:190px; }
    .water-percent{ font-size:2.1rem; }
}

</style>
</head>

<body>

<div class="bg-glow"></div>
<div class="leaf-field" id="leafField"></div>

<div class="container">

    <header>
        <h1>🌱 EaRth Plant Monitor</h1>
        <div class="subtitle"><span class="live-dot"></span> Live Sensor Dashboard</div>
    </header>

    <div class="card">

        <div class="plant-head">
            <div id="statusIcon" class="status-icon">🌱</div>
            <div id="plantName" class="plant-name">Loading...</div>
            <div id="deviceId" class="device-id">--</div>
        </div>

        <div id="statusText" class="status-text">Waiting for sensor data...</div>

        <div class="water-container">
            <div id="waterCircle" class="water-circle">
                <div id="waterFill" class="water-fill">
                    <div class="wave"></div>
                    <div class="wave"></div>
                    <div class="bubble" style="left:30%; animation-delay:0s;"></div>
                    <div class="bubble" style="left:55%; animation-delay:1.1s;"></div>
                    <div class="bubble" style="left:70%; animation-delay:2.2s;"></div>
                </div>

                <div class="sand-pile"></div>

                <div class="glass-shine"></div>

                <div class="ripple"></div>
                <div class="ripple ripple2"></div>

                <div class="crack crack1"></div>
                <div class="crack crack2"></div>
                <div class="crack crack3"></div>
                <div class="crack crack4"></div>

                <div class="shard s1"></div>
                <div class="shard s2"></div>
                <div class="shard s3"></div>
                <div class="shard s4"></div>
                <div class="shard s5"></div>

                <div class="gush g1"></div>
                <div class="gush g2"></div>
                <div class="gush g3"></div>

                <div class="splash-drop" style="--dx:-72px; --dy:-100px; animation-delay:0s;"></div>
                <div class="splash-drop" style="--dx:-26px; --dy:-135px; animation-delay:.2s;"></div>
                <div class="splash-drop" style="--dx:28px; --dy:-135px; animation-delay:.4s;"></div>
                <div class="splash-drop" style="--dx:74px; --dy:-100px; animation-delay:.6s;"></div>

                <div class="heat-shimmer"></div>
                <div class="dust" style="left:18%; animation-delay:0s;"></div>
                <div class="dust" style="left:42%; animation-delay:1s;"></div>
                <div class="dust" style="left:64%; animation-delay:2s;"></div>
                <div class="dust" style="left:82%; animation-delay:1.5s;"></div>

                <div class="sand-grain" style="left:14%; animation-delay:0s;"></div>
                <div class="sand-grain" style="left:36%; animation-delay:.7s;"></div>
                <div class="sand-grain" style="left:58%; animation-delay:1.4s;"></div>
                <div class="sand-grain" style="left:78%; animation-delay:2.1s;"></div>

                <div class="dust-puff" style="left:20%;"></div>
                <div class="dust-puff puff2" style="left:50%;"></div>
                <div class="dust-puff puff3" style="left:80%;"></div>

                <div class="tumbleweed"><span></span><span></span><span></span></div>

                <div class="water-text">
                    <div id="waterPercent" class="water-percent">--%</div>
                    <div class="water-label">Soil Moisture</div>
                </div>
            </div>
        </div>

        <div class="sparkline-wrap">
            <div class="sparkline-label">Moisture trend</div>
            <canvas id="sparkline" width="400" height="60"></canvas>
        </div>

        <div class="grid">
            <div class="metric">
                <div class="metric-icon">💧</div>
                <div class="metric-label">Moisture</div>
                <div id="soilValue" class="metric-value">--</div>
                <div class="metric-unit">%</div>
            </div>

            <div class="metric">
                <div class="metric-icon">📟</div>
                <div class="metric-label">Raw Sensor</div>
                <div id="rawValue" class="metric-value">--</div>
            </div>

            <div class="metric">
                <div class="metric-icon">🌡️</div>
                <div class="metric-label">Temperature</div>
                <div id="tempValue" class="metric-value">--</div>
                <div class="metric-unit">°C</div>
            </div>

            <div class="metric">
                <div class="metric-icon">💨</div>
                <div class="metric-label">Humidity</div>
                <div id="humidValue" class="metric-value">--</div>
                <div class="metric-unit">%</div>
            </div>

            <div class="metric">
                <div class="metric-icon">🔋</div>
                <div class="metric-label">Battery</div>
                <div id="battValue" class="metric-value">--</div>
                <div class="metric-unit">V</div>
            </div>

            <div class="metric">
                <div class="metric-icon">📅</div>
                <div class="metric-label">Last Watered</div>
                <div id="lastWatered" class="metric-value">--</div>
            </div>
        </div>

        <div id="lastUpdated" class="last-updated">--</div>

    </div>
</div>

<script>

let lastState = "";
let lastUpdateTime = null;
const history = [];
const HISTORY_MAX = 30;

/* floating leaves in background */
(function spawnLeaves(){
    const field = document.getElementById("leafField");
    const symbols = ["🍃","🌿","🍂"];
    for(let i=0;i<14;i++){
        const leaf = document.createElement("div");
        leaf.className = "leaf";
        leaf.textContent = symbols[Math.floor(Math.random()*symbols.length)];
        leaf.style.left = Math.random()*100 + "%";
        leaf.style.animationDuration = (14 + Math.random()*16) + "s";
        leaf.style.animationDelay = (Math.random()*16) + "s";
        leaf.style.fontSize = (1 + Math.random()*1.2) + "rem";
        field.appendChild(leaf);
    }
})();

/* animate a number counting from current text to target */
function animateNumber(el, target, decimals){
    const start = parseFloat(el.textContent) || 0;
    const end = parseFloat(target);
    if(isNaN(end)){ el.textContent = target; return; }
    const duration = 600;
    const startTime = performance.now();

    function step(now){
        const progress = Math.min((now - startTime) / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        const value = start + (end - start) * eased;
        el.textContent = decimals ? value.toFixed(decimals) : Math.round(value);
        if(progress < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
}

function setMetricClass(el, value, lowWarn, lowDanger, highWarn, highDanger){
    el.classList.remove("warn","danger","good");
    if(highDanger !== null && value >= highDanger) el.classList.add("danger");
    else if(lowDanger !== null && value <= lowDanger) el.classList.add("danger");
    else if(highWarn !== null && value >= highWarn) el.classList.add("warn");
    else if(lowWarn !== null && value <= lowWarn) el.classList.add("warn");
    else el.classList.add("good");
}

function drawSparkline(){
    const canvas = document.getElementById("sparkline");
    const ctx = canvas.getContext("2d");
    const w = canvas.width, h = canvas.height;
    ctx.clearRect(0,0,w,h);

    if(history.length < 2) return;

    const max = 100, min = 0;
    const stepX = w / (HISTORY_MAX - 1);
    const offset = HISTORY_MAX - history.length;

    ctx.beginPath();
    history.forEach((val, i) => {
        const x = (offset + i) * stepX;
        const y = h - ((val - min) / (max - min)) * (h - 8) - 4;
        if(i === 0) ctx.moveTo(x, y);
        else ctx.lineTo(x, y);
    });

    const gradient = ctx.createLinearGradient(0,0,w,0);
    gradient.addColorStop(0, "rgba(77,220,255,.9)");
    gradient.addColorStop(1, "rgba(107,255,158,.9)");
    ctx.strokeStyle = gradient;
    ctx.lineWidth = 2.5;
    ctx.lineJoin = "round";
    ctx.lineCap = "round";
    ctx.stroke();

    ctx.lineTo((offset + history.length - 1) * stepX, h);
    ctx.lineTo(offset * stepX, h);
    ctx.closePath();
    ctx.fillStyle = "rgba(77,220,255,.08)";
    ctx.fill();
}

async function loadData(){
    try{
        const response = await fetch("/api/data?t=" + Date.now(), { cache:"no-store" });
        const data = await response.json();
        const state = JSON.stringify(data);

        if(state !== lastState){
            lastState = state;
            updateDashboard(data);
        }

        lastUpdateTime = new Date();
        document.querySelector(".live-dot").style.background = "var(--good)";

    } catch(error){
        console.error(error);
        document.querySelector(".live-dot").style.background = "var(--danger)";
        document.getElementById("statusText").textContent = "❌ Connection lost";
    }
}

function updateDashboard(data){

    document.getElementById("plantName").textContent =
        data.plant_name || data.device_id || "Unknown Plant";

    document.getElementById("deviceId").textContent =
        "Device: " + (data.device_id || "--");

    const moisture = Number(data.soil_moisture ?? data.soil_percent ?? 0);
    const raw = Number(data.soil_moisture_raw ?? data.soil_raw ?? 0);

    animateNumber(document.getElementById("soilValue"), moisture, 0);
    animateNumber(document.getElementById("rawValue"), raw, 0);
    animateNumber(document.getElementById("waterPercent"), moisture, 0);
    // re-append % since animateNumber overwrites textContent
    setTimeout(() => {
        document.getElementById("waterPercent").textContent = Math.round(moisture) + "%";
    }, 620);

    history.push(moisture);
    if(history.length > HISTORY_MAX) history.shift();
    drawSparkline();

    const circle = document.getElementById("waterCircle");
    const fill = document.getElementById("waterFill");
    const icon = document.getElementById("statusIcon");
    const wasOverflow = circle.classList.contains("overflow");
    const wasDry = circle.classList.contains("dry");

    circle.classList.remove("overflow", "dry");

    let newIcon = "🌱";
    let statusMsg = data.text || "🌱 Plant healthy";

    if(moisture >= 90 && raw >= 1700){
        circle.classList.add("overflow");
        statusMsg = "🌊 Too much water! Plant is drowning";
        newIcon = "🌊";
        fill.style.height = "100%";

    } else if(moisture <= 20 && raw <= 600){
        circle.classList.add("dry");
        statusMsg = "🏜️ Plant is extremely dry";
        newIcon = "🥀";
        fill.style.height = "15%";

    } else {
        fill.style.height = moisture + "%";
        fill.style.background = "linear-gradient(#4ddcff,#0066ff)";
    }

    if(icon.textContent !== newIcon){
        icon.textContent = newIcon;
        icon.classList.remove("bump");
        void icon.offsetWidth;
        icon.classList.add("bump");
    }

    const statusEl = document.getElementById("statusText");
    if(statusEl.textContent !== statusMsg){
        statusEl.style.opacity = 0;
        setTimeout(() => {
            statusEl.textContent = statusMsg;
            statusEl.style.opacity = 1;
        }, 200);
    }

    const temp = Number(data.temperature ?? NaN);
    const tempEl = document.getElementById("tempValue");
    if(!isNaN(temp)){
        animateNumber(tempEl, temp, 1);
        setMetricClass(tempEl, temp, 10, 5, 32, 38);
    } else { tempEl.textContent = "--"; }

    const humid = Number(data.humidity ?? NaN);
    const humidEl = document.getElementById("humidValue");
    if(!isNaN(humid)){
        animateNumber(humidEl, humid, 0);
        setMetricClass(humidEl, humid, 25, 15, 80, 90);
    } else { humidEl.textContent = "--"; }

    const batt = Number(data.battery ?? NaN);
    const battEl = document.getElementById("battValue");
    if(!isNaN(batt)){
        animateNumber(battEl, batt, 2);
        setMetricClass(battEl, batt, 3.5, 3.2, null, null);
    } else { battEl.textContent = "--"; }

    document.getElementById("lastWatered").textContent =
        data.last_watered ? data.last_watered.split(" ")[0] : "--";
}

function tickClock(){
    const el = document.getElementById("lastUpdated");
    if(!lastUpdateTime){ el.textContent = "--"; return; }
    const secs = Math.floor((Date.now() - lastUpdateTime.getTime()) / 1000);
    const label = secs < 2 ? "just now" : secs + "s ago";
    el.textContent = "🟢 Live update: " + label;
}

loadData();
setInterval(loadData, 1000);
setInterval(tickClock, 1000);

</script>

</body>
</html>
"""


class PlantHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        pass

    def do_GET(self):

        if self.path == "/" or self.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode("utf-8"))

        elif self.path.startswith("/api/data"):
            try:
                if RES_FILE.exists():
                    with open(RES_FILE, "r", encoding="utf-8") as file:
                        data = json.load(file)
                else:
                    data = {"error": "res.json missing"}

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.send_header("Cache-Control", "no-store")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

            except Exception as e:
                self.send_response(500)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

        else:
            self.send_response(404)
            self.end_headers()


def run(port=8080):
    server = HTTPServer(("0.0.0.0", port), PlantHandler)
    print(f"🌱 EaRth Plant Monitor running: http://localhost:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.shutdown()


if __name__ == "__main__":
    run()