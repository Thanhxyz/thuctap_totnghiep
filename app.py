import streamlit as st
import base64

# ================== CONFIG ==================
st.set_page_config(
    page_title="Thiệp Năm Mới 2026 ❤️",
    layout="wide"
)

NAME = "NGUYỄN THỊ KIM"

# ================== LOAD IMAGE BASE64 ==================
def img_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img1 = img_base64("img1.png")
img2 = img_base64("img2.png")
img3 = img_base64("img3.png")

# ================== HTML ==================
html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
body {{
    margin: 0;
    background: radial-gradient(circle at top, #1b0033, #050010);
    overflow: hidden;
    font-family: 'Segoe UI', sans-serif;
}}

canvas {{
    position: absolute;
    inset: 0;
}}

.card {{
    position: absolute;
    inset: 4%;
    border-radius: 36px;
    border: 2px solid rgba(255,200,230,0.9);
    box-shadow:
        0 0 120px rgba(255,180,240,0.7),
        inset 0 0 40px rgba(255,180,240,0.3);
}}

.title {{
    position: absolute;
    top: 60px;
    width: 100%;
    text-align: center;
    font-size: 54px;
    letter-spacing: 8px;
    color: #ffd6f0;
    text-shadow: 0 0 40px #ff9ad5;
}}

.name {{
    position: absolute;
    top: 190px;
    width: 100%;
    text-align: center;
    font-size: 80px;
    font-weight: 900;
    background: linear-gradient(90deg,#fff,#ff9ad5,#ffd1f0,#b388ff,#7ee7ff,#fff);
    background-size: 600%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 3.5s linear infinite;
    filter: drop-shadow(0 0 60px rgba(255,220,255,1));
}}

@keyframes shine {{
    0% {{ background-position: 0%; }}
    100% {{ background-position: 600%; }}
}}

.wish {{
    position: absolute;
    top: 370px;
    width: 100%;
    text-align: center;
    font-size: 28px;
    color: #fff0f8;
    text-shadow: 0 0 25px #ff9ad5;
}}

/* ================= PHOTOS ================= */
.photo {{
    position: absolute;
    width: 190px;
    height: 190px;
    border-radius: 26px;
    object-fit: cover;

    /* Ánh sáng lóe rõ ràng */
    box-shadow:
        0 0 50px rgba(255,220,255,1),
        0 0 100px rgba(255,170,255,0.9),
        0 0 140px rgba(255,150,255,0.8);

    animation:
        angelFloat 8s ease-in-out infinite,
        glowPulse 3s ease-in-out infinite;
}}

.p1 {{ left: 12%; bottom: -240px; animation-delay: 0s; }}
.p2 {{ left: 42%; bottom: -260px; animation-delay: 2s; }}
.p3 {{ left: 72%; bottom: -240px; animation-delay: 4s; }}

@keyframes angelFloat {{
    0% {{ transform: translateY(0) scale(1); }}
    50% {{ transform: translateY(-380px) scale(1.05); }}
    100% {{ transform: translateY(-620px) scale(1.1); }}
}}

@keyframes glowPulse {{
    0%,100% {{
        box-shadow:
            0 0 50px rgba(255,220,255,1),
            0 0 100px rgba(255,170,255,0.9),
            0 0 140px rgba(255,150,255,0.8);
    }}
    50% {{
        box-shadow:
            0 0 90px rgba(255,255,255,1),
            0 0 180px rgba(255,200,255,1),
            0 0 240px rgba(255,180,255,0.9);
    }}
}}

/* ================= HEART FLOAT ================= */
.heart {{
    position: absolute;
    width: 18px;
    height: 18px;
    background: #ff5fa2;
    transform: rotate(45deg);
    animation: floatUp 7s linear infinite;
}}

.heart::before,
.heart::after {{
    content: "";
    position: absolute;
    width: 18px;
    height: 18px;
    background: #ff5fa2;
    border-radius: 50%;
}}

.heart::before {{ top: -9px; left: 0; }}
.heart::after {{ left: -9px; top: 0; }}

@keyframes floatUp {{
    0% {{ transform: translateY(0) rotate(45deg); opacity: 0; }}
    10% {{ opacity: 1; }}
    100% {{ transform: translateY(-900px) rotate(45deg); opacity: 0; }}
}}
</style>
</head>

<body>

<canvas id="fw"></canvas>

<div class="card"></div>
<div class="title">HAPPY NEW YEAR 2026</div>
<div class="name">{NAME}</div>

<div class="wish">
Chúc em một năm mới rực rỡ như pháo hoa,<br>
hạnh phúc ngập tràn và nhiều niềm vui ❤️
</div>

<img class="photo p1" src="data:image/png;base64,{img1}">
<img class="photo p2" src="data:image/png;base64,{img2}">
<img class="photo p3" src="data:image/png;base64,{img3}">

<script>
for (let i = 0; i < 45; i++) {{
    const h = document.createElement("div");
    h.className = "heart";
    h.style.left = Math.random() * 100 + "%";
    h.style.bottom = "-40px";
    h.style.animationDelay = Math.random() * 7 + "s";
    document.body.appendChild(h);
}}

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
        this.vy = -(9 + Math.random() * 5);
        this.exploded = false;
    }}
    update() {{
        this.y += this.vy;
        this.vy += 0.06;
        if (this.vy >= 0 && !this.exploded) {{
            this.exploded = true;
            explode(this.x, this.y);
        }}
    }}
    draw() {{
        ctx.fillStyle = "#fff";
        ctx.fillRect(this.x, this.y, 3, 14);
    }}
}}

class Particle {{
    constructor(x, y, color) {{
        const a = Math.random() * Math.PI * 2;
        const s = Math.random() * 5 + 2;
        this.x = x;
        this.y = y;
        this.vx = Math.cos(a) * s;
        this.vy = Math.sin(a) * s;
        this.life = 100;
        this.color = color;
    }}
    update() {{
        this.x += this.vx;
        this.y += this.vy;
        this.vy += 0.04;
        this.life--;
    }}
    draw() {{
        ctx.globalAlpha = this.life / 100;
        ctx.beginPath();
        ctx.arc(this.x, this.y, 3, 0, Math.PI * 2);
        ctx.fillStyle = this.color;
        ctx.fill();
        ctx.globalAlpha = 1;
    }}
}}

let rockets = [];
let particles = [];

function explode(x, y) {{
    for (let i = 0; i < 180; i++) {{
        particles.push(new Particle(x, y, colors[Math.floor(Math.random()*colors.length)]));
    }}
}}

function loop() {{
    ctx.fillStyle = "rgba(0,0,0,0.25)";
    ctx.fillRect(0,0,canvas.width,canvas.height);
    if (Math.random() < 0.12) rockets.push(new Rocket());
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
