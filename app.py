import streamlit as st
import base64

st.set_page_config(
    page_title="Thiệp Năm Mới 2026 ❤️",
    layout="wide"
)

NAME = "NGUYỄN THỊ KIM"

def img_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img1 = img_base64("img1.png")
img2 = img_base64("img2.png")
img3 = img_base64("img3.png")

html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
html, body {{
    width: 100%;
    height: 100%;
    margin: 0;
}}

body {{
    background: radial-gradient(circle at top, #1b0033, #050010);
    overflow: hidden;
    font-family: 'Segoe UI', sans-serif;
}}

canvas {{
    position: fixed;
    inset: 0;
    width: 100vw;
    height: 100vh;
    z-index: 0;
}}

/* ===== CARD ===== */
.card {{
    position: absolute;
    inset: 3%;
    border-radius: 26px;
    border: 2px solid rgba(255,200,230,0.9);
    box-shadow:
        0 0 80px rgba(255,180,240,0.6),
        inset 0 0 30px rgba(255,180,240,0.3);
    z-index: 1;
}}

/* ===== TEXT ===== */
.text-zone {{
    position: relative;
    z-index: 4;
    padding-top: 6vh;
    text-align: center;
}}

.title {{
    font-size: clamp(22px, 6vw, 40px);
    letter-spacing: 4px;
    color: #ffd6f0;
    text-shadow: 0 0 25px #ff9ad5;
}}

.name {{
    margin-top: 2vh;
    font-size: clamp(34px, 9vw, 64px);
    font-weight: 900;
    background: linear-gradient(90deg,#fff,#ff9ad5,#ffd1f0,#b388ff,#7ee7ff,#fff);
    background-size: 600%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 3.5s linear infinite;
    filter: drop-shadow(0 0 30px rgba(255,220,255,1));
}}

@keyframes shine {{
    from {{ background-position: 0%; }}
    to   {{ background-position: 600%; }}
}}

.wish {{
    margin-top: 2vh;
    font-size: clamp(16px, 4.5vw, 24px);
    padding: 0 8vw;
    color: #fff0f8;
    text-shadow: 0 0 18px #ff9ad5;
}}

/* ===== PHOTOS (BAY GẦN LỜI CHÚC) ===== */
.photo {{
    position: absolute;
    width: 30vw;
    max-width: 140px;
    aspect-ratio: 1/1;
    border-radius: 22px;
    object-fit: cover;
    box-shadow:
        0 0 35px rgba(255,220,255,1),
        0 0 70px rgba(255,170,255,0.9);
    animation:
        angelFloat 8s ease-in-out infinite,
        glowPulse 3s ease-in-out infinite;
    z-index: 2;
}}

.p1 {{ left: 6%;  bottom: -38%; animation-delay: 0s; }}
.p2 {{ left: 35%; bottom: -42%; animation-delay: 2s; }}
.p3 {{ left: 64%; bottom: -38%; animation-delay: 4s; }}

@keyframes angelFloat {{
    0%   {{ transform: translateY(0) scale(1); }}
    60%  {{ transform: translateY(-32vh) scale(1.05); }}
    100% {{ transform: translateY(-38vh) scale(1.1); }}
}}

@keyframes glowPulse {{
    0%,100% {{
        box-shadow:
            0 0 35px rgba(255,220,255,1),
            0 0 70px rgba(255,170,255,0.9);
    }}
    50% {{
        box-shadow:
            0 0 60px rgba(255,255,255,1),
            0 0 120px rgba(255,200,255,1);
    }}
}}

/* ===== HEART ===== */
.heart {{
    position: absolute;
    width: 14px;
    height: 14px;
    background: #ff5fa2;
    transform: rotate(45deg);
    animation: floatUp 7s linear infinite;
    z-index: 1;
}}

.heart::before,
.heart::after {{
    content: "";
    position: absolute;
    width: 14px;
    height: 14px;
    background: #ff5fa2;
    border-radius: 50%;
}}

.heart::before {{ top: -7px; left: 0; }}
.heart::after  {{ left: -7px; top: 0; }}

@keyframes floatUp {{
    from {{ transform: translateY(0) rotate(45deg); opacity: 0; }}
    10%  {{ opacity: 1; }}
    to   {{ transform: translateY(-100vh) rotate(45deg); opacity: 0; }}
}}
</style>
</head>

<body>

<canvas id="fw"></canvas>

<div class="card"></div>

<div class="text-zone">
    <div class="title">HAPPY NEW YEAR 2026</div>
    <div class="name">{NAME}</div>
    <div class="wish">
        Chúc em một năm mới rực rỡ như pháo hoa,<br>
        hạnh phúc ngập tràn và nhiều niềm vui ❤️
    </div>
</div>

<img class="photo p1" src="data:image/png;base64,{img1}">
<img class="photo p2" src="data:image/png;base64,{img2}">
<img class="photo p3" src="data:image/png;base64,{img3}">

<script>
// Hearts
for (let i = 0; i < 30; i++) {{
    const h = document.createElement("div");
    h.className = "heart";
    h.style.left = Math.random() * 100 + "%";
    h.style.bottom = "-40px";
    h.style.animationDelay = Math.random() * 7 + "s";
    document.body.appendChild(h);
}}

// Fireworks
const canvas = document.getElementById("fw");
const ctx = canvas.getContext("2d");

function resize() {{
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}}
resize();
window.onresize = resize;

const colors = ["#ff004c","#ff9f00","#ffee00","#33ff57","#00ffd5","#00aaff","#7a5cff","#ff6fff","#ffffff"];

class Rocket {{
    constructor() {{
        this.x = Math.random() * canvas.width;
        this.y = canvas.height;
        this.vy = -(8 + Math.random() * 4);
        this.exploded = false;
    }}
    update() {{
        this.y += this.vy;
        this.vy += 0.05;
        if (this.vy >= 0 && !this.exploded) {{
            this.exploded = true;
            explode(this.x, this.y);
        }}
    }}
    draw() {{
        ctx.fillStyle = "#fff";
        ctx.fillRect(this.x, this.y, 2, 10);
    }}
}}

class Particle {{
    constructor(x, y, color) {{
        const a = Math.random() * Math.PI * 2;
        const s = Math.random() * 4 + 2;
        this.x = x;
        this.y = y;
        this.vx = Math.cos(a) * s;
        this.vy = Math.sin(a) * s;
        this.life = 80;
        this.color = color;
    }}
    update() {{
        this.x += this.vx;
        this.y += this.vy;
        this.vy += 0.04;
        this.life--;
    }}
    draw() {{
        ctx.globalAlpha = this.life / 80;
        ctx.beginPath();
        ctx.arc(this.x, this.y, 2.5, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.fill();
        ctx.globalAlpha = 1;
    }}
}}

let rockets = [];
let particles = [];

function explode(x, y) {{
    for (let i = 0; i < 120; i++) {{
        particles.push(new Particle(x, y, colors[Math.floor(Math.random()*colors.length)]));
    }}
}}

function loop() {{
    ctx.fillStyle = "rgba(0,0,0,0.25)";
    ctx.fillRect(0,0,canvas.width,canvas.height);

    if (Math.random() < 0.08) rockets.push(new Rocket());
    rockets.forEach(r => {{ r.update(); r.draw(); }});
    rockets = rockets.filter(r => !r.exploded);

    particles.forEach(p => {{ p.update(); p.draw(); }});
    particles = particles.filter(p => p.life > 0);

    requestAnimationFrame(loop);
}}
loop();
</script>

</body>
</html>
"""

st.components.v1.html(html, height=950)
