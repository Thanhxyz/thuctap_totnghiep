import streamlit as st

st.set_page_config(
    page_title="Thiệp Chúc Mừng Năm Mới 2026",
    layout="wide"
)

SENDER = "Hoàng Ích Thanh"

html = f"""
<!DOCTYPE html>
<html lang="vi">
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
    background: radial-gradient(circle at top, #0a1a3a, #02040c);
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

/* CARD */
.card {{
    position: absolute;
    inset: 4%;
    border-radius: 26px;
    border: 2px solid rgba(160,220,255,0.85);
    box-shadow:
        0 0 70px rgba(120,200,255,0.8),
        inset 0 0 40px rgba(120,200,255,0.25);
    z-index: 1;
    backdrop-filter: blur(4px);
}}

/* TEXT */
.text-zone {{
    position: relative;
    z-index: 3;
    padding-top: 7vh;
    padding-bottom: 5vh;
    text-align: center;
}}

.title {{
    font-size: clamp(22px, 7vw, 36px);
    letter-spacing: 4px;
    font-weight: 800;
    background: linear-gradient(
        90deg,
        #ffffff,
        #7ee7ff,
        #9f8bff,
        #4dfcff,
        #ffffff
    );
    background-size: 500%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 4s linear infinite;
    filter: drop-shadow(0 0 26px rgba(140,220,255,1));
}}

@keyframes shine {{
    from {{ background-position: 0%; }}
    to {{ background-position: 500%; }}
}}

.subtitle {{
    margin-top: 1.5vh;
    font-size: clamp(14px, 4vw, 18px);
    color: #cfefff;
    text-shadow: 0 0 18px #7ee7ff;
}}

.content {{
    margin-top: 4vh;
    font-size: clamp(14.5px, 4vw, 18px);
    padding: 0 8vw;
    line-height: 1.85;
    color: #eaf7ff;
    text-shadow:
        0 0 14px rgba(120,200,255,0.8),
        0 0 28px rgba(100,180,255,0.5);
}}

.highlight {{
    color: #7ee7ff;
    font-weight: 600;
}}

.highlight.big {{
    font-size: 1.1em;
    display: block;
    margin: 1.2vh 0;
}}

.signature {{
    margin-top: 5vh;
    font-size: clamp(14px, 3.8vw, 16px);
    color: #d6f4ff;
    font-style: italic;
}}

.footer {{
    margin-top: 2.5vh;
    font-size: 14px;
    color: #9fe8ff;
}}

.year {{
    font-weight: 700;
    letter-spacing: 2px;
}}
</style>
</head>

<body>

<canvas id="fw"></canvas>

<div class="card"></div>

<div class="text-zone">
    <div class="title">CHÚC MỪNG NĂM MỚI 2026</div>
    <div class="subtitle">HAPPY NEW YEAR</div>

    <div class="content">
        Nhân dịp năm mới, kính chúc <span class="highlight">Quý anh/chị</span>
        <span class="highlight big">
            Sức khỏe dồi dào – An khang thịnh vượng<br>
            Thành công bền vững
        </span>
        Công việc suôn sẻ, <span class="highlight">đầu tư hiệu quả</span>,<br>
        <span class="highlight">giao dịch thuận lợi – chốt nhà liên tục</span>,<br>
        <span class="highlight">tài lộc viên mãn, phát triển dài lâu</span>.
    </div>

    <div class="signature">
        Trân trọng,<br>
        — <b>{SENDER}</b>
    </div>

    <div class="footer">
        🎆 <span class="year">Happy New Year 2026</span> 🎆
    </div>
</div>

<script>
// ===== FIREWORKS REALISTIC CENTER =====
const canvas = document.getElementById("fw");
const ctx = canvas.getContext("2d");

function resize() {{
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}}
resize();
window.addEventListener("resize", resize);

const colors = [
    "#ff4d4d", "#ffb703", "#fff44f",
    "#4dff88", "#4de1ff", "#3a86ff",
    "#9d4edd", "#ff4fd8", "#ffffff"
];

class Rocket {{
    constructor() {{
        this.x = canvas.width * (0.3 + Math.random() * 0.4);
        this.y = canvas.height + 20;
        this.targetY = canvas.height * (0.28 + Math.random() * 0.18);
        this.vy = -(9 + Math.random() * 3);
        this.exploded = false;
        this.color = colors[Math.floor(Math.random() * colors.length)];
    }}

    update() {{
        this.y += this.vy;
        if (this.y <= this.targetY && !this.exploded) {{
            this.exploded = true;
            explode(this.x, this.y, this.color);
        }}
    }}

    draw() {{
        ctx.fillStyle = this.color;
        ctx.fillRect(this.x, this.y, 2.5, 12);
    }}
}}

class Particle {{
    constructor(x, y, angle, speed, color) {{
        this.x = x;
        this.y = y;
        this.vx = Math.cos(angle) * speed;
        this.vy = Math.sin(angle) * speed;
        this.life = 110;
        this.color = color;
        this.size = Math.random() * 2.2 + 1.6;
    }}

    update() {{
        this.x += this.vx;
        this.y += this.vy;
        this.vy += 0.045;
        this.life--;
    }}

    draw() {{
        ctx.globalAlpha = this.life / 110;
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.shadowBlur = 20;
        ctx.shadowColor = this.color;
        ctx.fillStyle = this.color;
        ctx.fill();
        ctx.shadowBlur = 0;
        ctx.globalAlpha = 1;
    }}
}}

let rockets = [];
let particles = [];

function explode(x, y, baseColor) {{
    const count = 180;
    for (let i = 0; i < count; i++) {{
        const angle = (Math.PI * 2 / count) * i;
        const speed = 3.5 + Math.random() * 2;
        particles.push(
            new Particle(
                x,
                y,
                angle,
                speed,
                Math.random() > 0.55
                    ? colors[Math.floor(Math.random() * colors.length)]
                    : baseColor
            )
        );
    }}
}}

function loop() {{
    ctx.fillStyle = "rgba(0,0,0,0.25)";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    if (Math.random() < 0.06) rockets.push(new Rocket());

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

st.components.v1.html(html, height=900)
