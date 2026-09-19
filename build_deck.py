# -*- coding: utf-8 -*-
import os
import json

# Extract base SECTIONS data from index.html
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

start_idx = text.find('const SECTIONS = [')
end_idx = text.find('// ==========================================================================\n    // 2. RENDERIZADO DEL STREAM')
if end_idx == -1:
    end_idx = text.find('// 2. RENDERIZADO DEL STREAM')
sections_js = text[start_idx:end_idx].strip()

# Create Python script to assemble the exact UI matching the uploaded reference image
deck_html = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Hong Kong & Shenzhen — Topologías de la Densidad y el Poder (Defensa de Maestría)</title>
  
  <!-- Tipografías de Alta Gama -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=DM+Mono:ital,wght@0,300;0,400;0,500;1,400&family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />

  <style>
    /* ==========================================================================
       ESTÉTICA CINEMATOGRÁFICA & HUD DE VIDRIO (MAESTRÍA ARQUITECTÓNICA)
       ========================================================================== */
    :root {{
      --bg-dark: #080c16;
      --glass-bg: rgba(13, 20, 36, 0.72);
      --glass-border: rgba(255, 255, 255, 0.16);
      --glass-hover: rgba(255, 255, 255, 0.24);
      
      --text-pure: #ffffff;
      --text-silver: #cbd5e1;
      --text-muted: #94a3b8;
      --text-faint: #64748b;
      
      --cat-eco: #f43f5e;       /* Economía (Rojo/Rosa) */
      --cat-urb: #0284c7;       /* Urbanismo (Azul) */
      --cat-env: #10b981;       /* Medio Ambiente (Verde) */
      --cat-soc: #f59e0b;       /* Sociedad (Ámbar) */
      --cat-gov: #8b5cf6;       /* Gobernanza (Violeta) */
      
      --font-serif: "Playfair Display", Georgia, serif;
      --font-sans: "Space Grotesk", -apple-system, BlinkMacSystemFont, sans-serif;
      --font-body: "Inter", sans-serif;
      --font-mono: "DM Mono", monospace;
    }}

    *, *::before, *::after {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    html, body {{
      width: 100%;
      height: 100%;
      overflow: hidden;
      background-color: var(--bg-dark);
      color: var(--text-pure);
      font-family: var(--font-sans);
      -webkit-font-smoothing: antialiased;
    }}

    /* ==========================================================================
       CABECERA SUPERIOR
       ========================================================================== */
    .top-header {{
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 60px;
      padding: 0 2.5rem;
      background: linear-gradient(180deg, rgba(8, 12, 22, 0.95) 0%, rgba(8, 12, 22, 0.4) 80%, transparent 100%);
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
      z-index: 100;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid rgba(255, 255, 255, 0.07);
    }}

    .header-left {{
      display: flex;
      align-items: center;
      gap: 2rem;
    }}

    .master-tag {{
      font-family: var(--font-mono);
      font-size: 0.76rem;
      font-weight: 600;
      letter-spacing: 0.16em;
      text-transform: uppercase;
      color: #ffffff;
      position: relative;
      padding-bottom: 4px;
    }}

    .master-tag::after {{
      content: '';
      position: absolute;
      bottom: 0;
      left: 0;
      width: 100%;
      height: 2px;
      background: rgba(255, 255, 255, 0.6);
      border-radius: 2px;
    }}

    .authors-label {{
      font-family: var(--font-body);
      font-size: 0.84rem;
      font-weight: 500;
      color: var(--text-silver);
      letter-spacing: 0.02em;
    }}

    .header-right {{
      display: flex;
      align-items: center;
      gap: 0.8rem;
    }}

    .section-dropdown-box {{
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-family: var(--font-mono);
      font-size: 0.76rem;
      color: var(--text-silver);
    }}

    .slide-select {{
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: #ffffff;
      font-family: var(--font-sans);
      font-size: 0.8rem;
      font-weight: 500;
      padding: 6px 14px;
      border-radius: 20px;
      outline: none;
      cursor: pointer;
      backdrop-filter: blur(8px);
      transition: all 0.2s ease;
      max-width: 380px;
    }}

    .slide-select:hover {{
      background: rgba(255, 255, 255, 0.16);
      border-color: rgba(255, 255, 255, 0.4);
    }}

    .slide-select option {{
      background: #0d1424;
      color: #ffffff;
    }}

    .circle-nav-btn {{
      width: 34px;
      height: 34px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: #ffffff;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.2s ease;
      font-size: 0.9rem;
    }}

    .circle-nav-btn:hover {{
      background: rgba(255, 255, 255, 0.25);
      border-color: #ffffff;
      transform: scale(1.06);
    }}

    /* Barra de Progreso Lineal */
    .progress-line {{
      position: fixed;
      top: 59px;
      left: 0;
      height: 2px;
      width: 0%;
      background: linear-gradient(90deg, var(--cat-urb), var(--cat-gov), var(--cat-env), var(--cat-eco));
      z-index: 101;
      transition: width 0.3s ease;
    }}

    /* ==========================================================================
       ESCENARIO PRINCIPAL DEL SLIDE (FULL VIEWPORT)
       ========================================================================== */
    .viewport-stage {{
      position: relative;
      width: 100vw;
      height: 100vh;
      overflow: hidden;
      display: flex;
      align-items: center;
      padding: 75px 3.2vw 2.5vh;
    }}

    /* Fondo Fotográfico / Lámina Arquitectónica Dinámica */
    .backdrop-canvas {{
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      z-index: 1;
      overflow: hidden;
    }}

    .backdrop-img {{
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: center;
      opacity: 0;
      transform: scale(1.04);
      transition: opacity 0.5s ease, transform 0.8s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    .backdrop-img.active {{
      opacity: 1;
      transform: scale(1);
    }}

    /* Capa de Gradiente Arquitectónico */
    .backdrop-gradient-overlay {{
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      background: linear-gradient(
        90deg,
        rgba(8, 12, 22, 0.92) 0%,
        rgba(8, 12, 22, 0.82) 36%,
        rgba(8, 12, 22, 0.45) 58%,
        rgba(8, 12, 22, 0.25) 75%,
        rgba(8, 12, 22, 0.65) 100%
      );
      z-index: 2;
      pointer-events: none;
    }}

    /* ==========================================================================
       COLUMNA IZQUIERDA: NARRATIVA, PREGUNTA Y TARJETAS COMPARATIVAS
       ========================================================================== */
    .hero-narrative {{
      position: relative;
      z-index: 10;
      width: 54%;
      max-width: 780px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      padding-right: 2rem;
      animation: fadeInNarrative 0.5s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    @keyframes fadeInNarrative {{
      from {{ opacity: 0; transform: translateY(12px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    .slide-pill-badge {{
      font-family: var(--font-mono);
      font-size: 0.76rem;
      letter-spacing: 0.18em;
      text-transform: uppercase;
      font-weight: 600;
      color: var(--text-silver);
      display: flex;
      align-items: center;
      gap: 0.5rem;
      margin-bottom: 0.8rem;
    }}

    .slide-pill-badge::before {{
      content: '•';
      color: #38bdf8;
      font-size: 1.2rem;
    }}

    .main-slide-title {{
      font-family: var(--font-sans);
      font-size: clamp(2.4rem, 3.8vw, 3.8rem);
      font-weight: 700;
      line-height: 1.08;
      color: #ffffff;
      letter-spacing: -0.02em;
      margin-bottom: 0.8rem;
      text-shadow: 0 4px 24px rgba(0, 0, 0, 0.6);
    }}

    .main-slide-subtitle {{
      font-family: var(--font-body);
      font-size: clamp(1.05rem, 1.4vw, 1.35rem);
      font-weight: 300;
      line-height: 1.5;
      color: var(--text-silver);
      margin-bottom: 1.2rem;
      max-width: 680px;
      text-shadow: 0 2px 10px rgba(0, 0, 0, 0.7);
    }}

    .thesis-taglines-row {{
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
      padding-top: 0.8rem;
      margin-bottom: 1.6rem;
      position: relative;
    }}

    .thesis-taglines-row::before {{
      content: '';
      width: 120px;
      height: 1.5px;
      background: rgba(255, 255, 255, 0.4);
      margin-bottom: 0.6rem;
    }}

    .tagline-item {{
      font-family: var(--font-mono);
      font-size: 0.72rem;
      font-weight: 500;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: rgba(255, 255, 255, 0.65);
    }}

    /* Tarjetas Comparativas de Territorio / Métricas */
    .territorial-cards-row {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.2rem;
      margin-bottom: 1.4rem;
    }}

    .territory-card {{
      background: rgba(15, 23, 42, 0.68);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 12px;
      padding: 1rem 1.2rem;
      transition: all 0.2s ease;
    }}

    .territory-card:hover {{
      border-color: rgba(255, 255, 255, 0.3);
      transform: translateY(-2px);
    }}

    .card-top-head {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 0.2rem;
    }}

    .card-city-name {{
      font-family: var(--font-sans);
      font-size: 1.05rem;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      color: #ffffff;
    }}

    .card-subtags {{
      font-family: var(--font-mono);
      font-size: 0.64rem;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--text-muted);
      margin-bottom: 0.8rem;
    }}

    .explore-btn {{
      font-family: var(--font-mono);
      font-size: 0.66rem;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.18);
      color: #ffffff;
      padding: 3px 8px;
      border-radius: 4px;
      cursor: pointer;
      transition: all 0.15s ease;
      display: inline-block;
      margin-bottom: 0.7rem;
    }}

    .explore-btn:hover {{
      background: rgba(255, 255, 255, 0.2);
      border-color: #ffffff;
    }}

    .metrics-pills-row {{
      display: flex;
      align-items: center;
      gap: 0.8rem;
    }}

    .metric-pill {{
      display: flex;
      align-items: center;
      gap: 0.4rem;
      font-family: var(--font-sans);
      font-size: 0.76rem;
    }}

    .metric-pill .icon {{
      font-size: 0.85rem;
      opacity: 0.8;
    }}

    .metric-pill .val {{
      font-weight: 700;
      color: #ffffff;
    }}

    .metric-pill .lbl {{
      font-size: 0.68rem;
      color: var(--text-muted);
    }}

    .bottom-footnote {{
      font-family: var(--font-mono);
      font-size: 0.72rem;
      letter-spacing: 0.06em;
      color: var(--text-faint);
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }}

    /* ==========================================================================
       COLUMNA DERECHA: HUD DE VIDRIO 3D & CONSOLA TOPOLÓGICA
       ========================================================================== */
    .hud-console-wrap {{
      position: relative;
      z-index: 10;
      width: 46%;
      height: 100%;
      max-height: calc(100vh - 110px);
      display: flex;
      flex-direction: column;
    }}

    .glass-hud-card {{
      flex: 1;
      background: var(--glass-bg);
      backdrop-filter: blur(28px);
      -webkit-backdrop-filter: blur(28px);
      border: 1px solid var(--glass-border);
      border-radius: 20px;
      box-shadow: 0 25px 60px -10px rgba(0, 0, 0, 0.6), inset 0 1px 1px rgba(255, 255, 255, 0.15);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      position: relative;
    }}

    /* HUD Bar Superior */
    .hud-top-bar {{
      padding: 0.85rem 1.25rem;
      border-bottom: 1px solid rgba(255, 255, 255, 0.09);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.8rem;
    }}

    .hud-title-badge {{
      font-family: var(--font-mono);
      font-size: 0.74rem;
      font-weight: 600;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: #38bdf8;
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }}

    .hud-actions {{
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }}

    .hud-btn {{
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid rgba(255, 255, 255, 0.18);
      color: #ffffff;
      font-family: var(--font-mono);
      font-size: 0.68rem;
      font-weight: 600;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      padding: 4px 9px;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.15s ease;
      display: flex;
      align-items: center;
      gap: 0.3rem;
    }}

    .hud-btn:hover {{
      background: rgba(255, 255, 255, 0.18);
      border-color: #ffffff;
    }}

    .hud-btn.active {{
      background: #ffffff;
      color: #0c121e;
      border-color: #ffffff;
    }}

    /* Leyenda de Categorías en esquina superior */
    .category-legend-strip {{
      position: absolute;
      top: 52px;
      right: 14px;
      display: flex;
      flex-direction: column;
      gap: 4px;
      z-index: 15;
      pointer-events: none;
    }}

    .legend-item {{
      font-family: var(--font-mono);
      font-size: 0.6rem;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 5px;
      color: rgba(255, 255, 255, 0.75);
    }}

    .legend-item .dot {{
      width: 6px;
      height: 6px;
      border-radius: 50%;
    }}

    /* Lienzo 3D */
    .hud-canvas-container {{
      flex: 1;
      width: 100%;
      height: 100%;
      min-height: 280px;
      position: relative;
      cursor: grab;
      user-select: none;
    }}

    .hud-canvas-container:active {{ cursor: grabbing; }}

    .hud-canvas-container canvas {{
      width: 100%;
      height: 100%;
      display: block;
    }}

    /* Banner Informativo / Telemetría */
    .hud-info-strip {{
      margin: 0 1rem 0.6rem;
      padding: 0.6rem 0.9rem;
      background: rgba(15, 23, 42, 0.75);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 10px;
      font-family: var(--font-body);
      font-size: 0.75rem;
      line-height: 1.4;
      color: var(--text-silver);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.6rem;
      transition: all 0.2s ease;
    }}

    .hud-info-strip .info-icon {{
      font-size: 0.9rem;
      color: #38bdf8;
      flex-shrink: 0;
    }}

    .hud-info-text {{
      flex: 1;
    }}

    .hud-info-text strong {{
      color: #ffffff;
      font-family: var(--font-mono);
      text-transform: uppercase;
      letter-spacing: 0.06em;
      font-size: 0.74rem;
    }}

    /* Fila de Filtros de Categoría */
    .hud-category-filter-row {{
      padding: 0.6rem 1rem 0.9rem;
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 0.4rem;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
    }}

    .cat-tab-btn {{
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 8px;
      padding: 6px 4px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 2px;
      cursor: pointer;
      transition: all 0.2s ease;
      color: var(--text-silver);
    }}

    .cat-tab-btn:hover {{
      background: rgba(255, 255, 255, 0.15);
      border-color: rgba(255, 255, 255, 0.3);
      transform: translateY(-2px);
    }}

    .cat-tab-btn.active {{
      background: rgba(255, 255, 255, 0.22);
      border-color: #ffffff;
      color: #ffffff;
    }}

    .cat-tab-btn .cat-icon {{
      font-size: 0.85rem;
    }}

    .cat-tab-btn .cat-title {{
      font-family: var(--font-mono);
      font-size: 0.58rem;
      font-weight: 600;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }}

    /* Teaser Siguiente Diapositiva (Esquina Inferior Derecha) */
    .next-teaser-link {{
      position: fixed;
      bottom: 1.2rem;
      right: 2.8vw;
      font-family: var(--font-mono);
      font-size: 0.72rem;
      font-weight: 600;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: rgba(255, 255, 255, 0.5);
      display: flex;
      align-items: center;
      gap: 0.6rem;
      cursor: pointer;
      z-index: 50;
      transition: all 0.2s ease;
    }}

    .next-teaser-link:hover {{
      color: #ffffff;
      transform: translateX(4px);
    }}

    .next-teaser-link::after {{
      content: '──';
      color: rgba(255, 255, 255, 0.4);
    }}

    /* Atajos de Teclado flotantes en esquina */
    .keyboard-hint {{
      position: fixed;
      bottom: 1.2rem;
      left: 2.8vw;
      font-family: var(--font-mono);
      font-size: 0.68rem;
      color: rgba(255, 255, 255, 0.4);
      display: flex;
      align-items: center;
      gap: 0.4rem;
      z-index: 50;
    }}

    .kbd-key {{
      background: rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(255, 255, 255, 0.2);
      padding: 1px 5px;
      border-radius: 4px;
      color: #ffffff;
    }}
  </style>
</head>
<body>

  <!-- Barra de Progreso Superior -->
  <div class="progress-line" id="progressBar"></div>

  <!-- Cabecera Superior -->
  <header class="top-header">
    <div class="header-left">
      <div class="master-tag">INVESTIGACIÓN DE MAESTRÍA</div>
      <div class="authors-label">Alejandra Gómez • Ana Casas • Juan Trujillo</div>
    </div>
    <div class="header-right">
      <div class="section-dropdown-box">
        <span>Sección:</span>
        <select id="slideSelector" class="slide-select" onchange="jumpToSlide(parseInt(this.value))"></select>
      </div>
      <button class="circle-nav-btn" onclick="prevSlide()" title="Anterior (←)">←</button>
      <button class="circle-nav-btn" onclick="nextSlide()" title="Siguiente (→)">→</button>
    </div>
  </header>

  <!-- Escenario Principal del Slide -->
  <main class="viewport-stage" id="viewportStage">
    
    <!-- Fondo Visual con Imagen y Gradiente -->
    <div class="backdrop-canvas">
      <img id="bgImage" class="backdrop-img active" src="slides/slide_1.png" alt="Visual Arquitectónico" />
      <div class="backdrop-gradient-overlay"></div>
    </div>

    <!-- Columna Izquierda: Narrativa & Métricas -->
    <div class="hero-narrative" id="narrativeCol">
      <div class="slide-pill-badge" id="slideBadge">SLIDE 01</div>
      <h1 class="main-slide-title" id="slideTitle">Hong Kong & Shenzhen</h1>
      <p class="main-slide-subtitle" id="slideSubtitle">¿Qué modelo de ciudad es mejor: el de Hong Kong o el de Shenzhen?</p>

      <div class="thesis-taglines-row">
        <span class="tagline-item">DOS TERRITORIOS</span>
        <span class="tagline-item">UNA REGIÓN</span>
        <span class="tagline-item">UN FUTURO COMPARTIDO</span>
      </div>

      <!-- Tarjetas Territoriales Dinámicas -->
      <div class="territorial-cards-row" id="territorialCardsRow">
        <!-- Generado dinámicamente -->
      </div>

      <div class="bottom-footnote" id="bottomFootnote">
        ✦ Región del Gran Delta del Río Perla
      </div>
    </div>

    <!-- Columna Derecha: HUD de Vidrio & Consola 3D -->
    <div class="hud-console-wrap">
      <div class="glass-hud-card">
        
        <!-- HUD Header -->
        <div class="hud-top-bar">
          <div class="hud-title-badge" id="hudTitleBadge">✦ RED BIPOLAR: DILEMA TERRITORIAL</div>
          <div class="hud-actions">
            <button class="hud-btn" onclick="triggerPulse()">⚡ Pulso</button>
            <button class="hud-btn" id="orbitBtn" onclick="toggleOrbit()">🌀 Órbita</button>
            <button class="hud-btn" onclick="resetGraph()">⟲ Reset</button>
          </div>
        </div>

        <!-- Leyenda de Categorías -->
        <div class="category-legend-strip">
          <div class="legend-item"><span class="dot" style="background: var(--cat-eco);"></span> ECONOMÍA</div>
          <div class="legend-item"><span class="dot" style="background: var(--cat-urb);"></span> URBANISMO</div>
          <div class="legend-item"><span class="dot" style="background: var(--cat-env);"></span> MEDIO AMBIENTE</div>
          <div class="legend-item"><span class="dot" style="background: var(--cat-soc);"></span> SOCIEDAD</div>
          <div class="legend-item"><span class="dot" style="background: var(--cat-gov);"></span> GOBERNANZA</div>
        </div>

        <!-- Canvas 3D -->
        <div class="hud-canvas-container" id="canvasBox">
          <canvas id="stageCanvas"></canvas>
        </div>

        <!-- Banner Informativo / Telemetría -->
        <div class="hud-info-strip" id="infoStrip">
          <span class="info-icon">ⓘ</span>
          <div class="hud-info-text" id="infoText">
            Selecciona o arrastra un nodo para ver detalles, comparar indicadores y explorar relaciones en 3D.
          </div>
        </div>

        <!-- Fila de Filtros de Categoría -->
        <div class="hud-category-filter-row">
          <button class="cat-tab-btn" onclick="filterCategory('urbanismo', this)">
            <span class="cat-icon">🏙️</span>
            <span class="cat-title">URBANISMO</span>
          </button>
          <button class="cat-tab-btn" onclick="filterCategory('economia', this)">
            <span class="cat-icon">📊</span>
            <span class="cat-title">ECONOMÍA</span>
          </button>
          <button class="cat-tab-btn" onclick="filterCategory('ambiente', this)">
            <span class="cat-icon">🌿</span>
            <span class="cat-title">MEDIO AMB.</span>
          </button>
          <button class="cat-tab-btn" onclick="filterCategory('sociedad', this)">
            <span class="cat-icon">👥</span>
            <span class="cat-title">SOCIEDAD</span>
          </button>
          <button class="cat-tab-btn" onclick="filterCategory('gobernanza', this)">
            <span class="cat-icon">🛡️</span>
            <span class="cat-title">GOBERNANZA</span>
          </button>
        </div>

      </div>
    </div>

  </main>

  <!-- Teaser Siguiente Diapositiva -->
  <div class="next-teaser-link" id="nextTeaser" onclick="nextSlide()">
    MÁS ALLÁ DE LA COMPETENCIA
  </div>

  <!-- Atajos de Teclado -->
  <div class="keyboard-hint">
    <span>Navegar:</span>
    <span class="kbd-key">←</span>
    <span class="kbd-key">→</span>
    <span>o barra espaciadora</span>
  </div>

  <script>
    // ==========================================================================
    // 1. DATASET DE LAS 62 SECCIONES / DIAPOSITIVAS
    // ==========================================================================
{sections_js}

    // ==========================================================================
    // 2. CONTROL DEL ESTADO & RENDERIZADO DEL SLIDE ACTUAL
    // ==========================================================================
    let currentSlideNum = 1;
    let activeCategoryFilter = null;

    const bgImage = document.getElementById('bgImage');
    const slideBadge = document.getElementById('slideBadge');
    const slideTitle = document.getElementById('slideTitle');
    const slideSubtitle = document.getElementById('slideSubtitle');
    const territorialCardsRow = document.getElementById('territorialCardsRow');
    const bottomFootnote = document.getElementById('bottomFootnote');
    const hudTitleBadge = document.getElementById('hudTitleBadge');
    const slideSelector = document.getElementById('slideSelector');
    const progressBar = document.getElementById('progressBar');
    const nextTeaser = document.getElementById('nextTeaser');
    const infoText = document.getElementById('infoText');

    // Inicializar Opciones del Selector de Diapositivas
    function initSlideSelector() {{
      let optionsHtml = '';
      SECTIONS.forEach(s => {{
        optionsHtml += `<option value="${{s.num}}">Slide ${{String(s.num).padStart(2, '0')}}: ${{s.title}}</option>`;
      }});
      slideSelector.innerHTML = optionsHtml;
    }}
    initSlideSelector();

    // Generar Tarjetas Dinámicas de Contexto Territorial según el Slide
    function getTerritorialCardsHtml(sec) {{
      const num = sec.num;
      
      if (num <= 15) {{
        // Comparación Hong Kong vs Shenzhen
        return `
          <div class="territory-card">
            <div class="card-top-head">
              <span class="card-city-name" style="color: #38bdf8;">HONG KONG</span>
            </div>
            <div class="card-subtags">GLOBAL • CONSOLIDADA • DENSA</div>
            <div class="explore-btn" onclick="filterCategory('urbanismo')">EXPLORAR →</div>
            <div class="metrics-pills-row">
              <div class="metric-pill"><span class="icon">👥</span><div><div class="val">7.5 M</div><div class="lbl">Habitantes</div></div></div>
              <div class="metric-pill"><span class="icon">🏢</span><div><div class="val">2,755</div><div class="lbl">Hab/km²</div></div></div>
              <div class="metric-pill"><span class="icon">🚌</span><div><div class="val">90%</div><div class="lbl">Transp. público</div></div></div>
            </div>
          </div>

          <div class="territory-card">
            <div class="card-top-head">
              <span class="card-city-name" style="color: #a78bfa;">SHENZHEN</span>
            </div>
            <div class="card-subtags">INNOVACIÓN • CRECIMIENTO • FLEXIBILIDAD</div>
            <div class="explore-btn" onclick="filterCategory('economia')">EXPLORAR →</div>
            <div class="metrics-pills-row">
              <div class="metric-pill"><span class="icon">👥</span><div><div class="val">17.6 M</div><div class="lbl">Habitantes</div></div></div>
              <div class="metric-pill"><span class="icon">🏢</span><div><div class="val">6,600</div><div class="lbl">Hab/km²</div></div></div>
              <div class="metric-pill"><span class="icon">🚌</span><div><div class="val">70%</div><div class="lbl">Transp. público</div></div></div>
            </div>
          </div>
        `;
      }} else if (num <= 25) {{
        // Hong Kong en detalle
        return `
          <div class="territory-card">
            <div class="card-top-head">
              <span class="card-city-name" style="color: #38bdf8;">DENSIDAD & SUELO</span>
            </div>
            <div class="card-subtags">PARQUES RURALES VS. VERTICALIDAD</div>
            <div class="metrics-pills-row">
              <div class="metric-pill"><span class="icon">🌲</span><div><div class="val">40%</div><div class="lbl">Protegido</div></div></div>
              <div class="metric-pill"><span class="icon">⚖️</span><div><div class="val">0.54</div><div class="lbl">Gini</div></div></div>
              <div class="metric-pill"><span class="icon">📦</span><div><div class="val">220k</div><div class="lbl">Cage Homes</div></div></div>
            </div>
          </div>

          <div class="territory-card">
            <div class="card-top-head">
              <span class="card-city-name" style="color: #38bdf8;">GOBERNANZA HK</span>
            </div>
            <div class="card-subtags">COMMON LAW • LEASEHOLD (1997)</div>
            <div class="metrics-pills-row">
              <div class="metric-pill"><span class="icon">🛡️</span><div><div class="val">ICAC</div><div class="lbl">1974</div></div></div>
              <div class="metric-pill"><span class="icon">💧</span><div><div class="val">80%</div><div class="lbl">Dongjiang</div></div></div>
              <div class="metric-pill"><span class="icon">🎓</span><div><div class="val">TTPS</div><div class="lbl">Top Talent</div></div></div>
            </div>
          </div>
        `;
      }} else if (num <= 37) {{
        // Shenzhen en detalle
        return `
          <div class="territory-card">
            <div class="card-top-head">
              <span class="card-city-name" style="color: #a78bfa;">I+D & MANUFACTURA</span>
            </div>
            <div class="card-subtags">HUAQIANGBEI • CHINEXT • 20 CLÚSTERES</div>
            <div class="metrics-pills-row">
              <div class="metric-pill"><span class="icon">💡</span><div><div class="val">6.46%</div><div class="lbl">I+D (PIB)</div></div></div>
              <div class="metric-pill"><span class="icon">⚡</span><div><div class="val">90%</div><div class="lbl">I+D Privado</div></div></div>
              <div class="metric-pill"><span class="icon">📱</span><div><div class="val">90%</div><div class="lbl">Hardware Global</div></div></div>
            </div>
          </div>

          <div class="territory-card">
            <div class="card-top-head">
              <span class="card-city-name" style="color: #a78bfa;">TEJIDO SOCIAL SZ</span>
            </div>
            <div class="card-subtags">ALDEAS URBANAS • HUKOU • CIUDAD ESPONJA</div>
            <div class="metrics-pills-row">
              <div class="metric-pill"><span class="icon">🏘️</span><div><div class="val">Urban</div><div class="lbl">Villages</div></div></div>
              <div class="metric-pill"><span class="icon">🌊</span><div><div class="val">Sponge</div><div class="lbl">City</div></div></div>
              <div class="metric-pill"><span class="icon">🌿</span><div><div class="val">Futian</div><div class="lbl">Manglar</div></div></div>
            </div>
          </div>
        `;
      }} else if (num <= 47) {{
        // Zonas de Sutura & Sinergias
        return `
          <div class="territory-card">
            <div class="card-top-head">
              <span class="card-city-name" style="color: #34d399;">ZONAS DE SUTURA</span>
            </div>
            <div class="card-subtags">QIANHAI ZEE • LOK MA CHAU LOOP</div>
            <div class="metrics-pills-row">
              <div class="metric-pill"><span class="icon">🌉</span><div><div class="val">Qianhai</div><div class="lbl">Plan 2021</div></div></div>
              <div class="metric-pill"><span class="icon">🔬</span><div><div class="val">87 ha</div><div class="lbl">HSITP Loop</div></div></div>
              <div class="metric-pill"><span class="icon">🌐</span><div><div class="val">GBA</div><div class="lbl">Gran Bahía</div></div></div>
            </div>
          </div>

          <div class="territory-card">
            <div class="card-top-head">
              <span class="card-city-name" style="color: #34d399;">SISTEMA CIRCULATORIO</span>
            </div>
            <div class="card-subtags">DONGJIANG (83 KM) • DAYA BAY NUCLEAR</div>
            <div class="metrics-pills-row">
              <div class="metric-pill"><span class="icon">💧</span><div><div class="val">83 km</div><div class="lbl">Acueducto</div></div></div>
              <div class="metric-pill"><span class="icon">⚛️</span><div><div class="val">Daya Bay</div><div class="lbl">Energía</div></div></div>
              <div class="metric-pill"><span class="icon">⚠️</span><div><div class="val">2021</div><div class="lbl">Estrés Hídrico</div></div></div>
            </div>
          </div>
        `;
      }} else if (num <= 55) {{
        // Çatalhöyük
        return `
          <div class="territory-card">
            <div class="card-top-head">
              <span class="card-city-name" style="color: #fbbf24;">ÇATALHÖYÜK</span>
            </div>
            <div class="card-subtags">MALLA CELULAR PEER-TO-PEER (7500 A.C.)</div>
            <div class="metrics-pills-row">
              <div class="metric-pill"><span class="icon">🏺</span><div><div class="val">7500 a.C.</div><div class="lbl">Neolítico</div></div></div>
              <div class="metric-pill"><span class="icon">👥</span><div><div class="val">10.000</div><div class="lbl">Habitantes</div></div></div>
              <div class="metric-pill"><span class="icon">🚫</span><div><div class="val">Cero</div><div class="lbl">Calles</div></div></div>
            </div>
          </div>

          <div class="territory-card">
            <div class="card-top-head">
              <span class="card-city-name" style="color: #fbbf24;">TOPOLOGÍA SOCIAL</span>
            </div>
            <div class="card-subtags">ACCESO POR TECHOS • CERO JERARQUÍA</div>
            <div class="metrics-pills-row">
              <div class="metric-pill"><span class="icon">🪜</span><div><div class="val">Techos</div><div class="lbl">Circulación</div></div></div>
              <div class="metric-pill"><span class="icon">🏛️</span><div><div class="val">Cero</div><div class="lbl">Palacios</div></div></div>
              <div class="metric-pill"><span class="icon">🔗</span><div><div class="val">P2P</div><div class="lbl">Autoorganización</div></div></div>
            </div>
          </div>
        `;
      }} else {{
        // Bogotá / Patio Bonito / Corabastos
        return `
          <div class="territory-card">
            <div class="card-top-head">
              <span class="card-city-name" style="color: #34d399;">CORABASTOS (KENNEDY)</span>
            </div>
            <div class="card-subtags">CENTRO AGROALIMENTARIO REGIONAL</div>
            <div class="metrics-pills-row">
              <div class="metric-pill"><span class="icon">🚛</span><div><div class="val">12.000</div><div class="lbl">ton/día</div></div></div>
              <div class="metric-pill"><span class="icon">🏪</span><div><div class="val">6.500</div><div class="lbl">Locales</div></div></div>
              <div class="metric-pill"><span class="icon">🥬</span><div><div class="val">Sabana</div><div class="lbl">Cund./Boyacá</div></div></div>
            </div>
          </div>

          <div class="territory-card">
            <div class="card-top-head">
              <span class="card-city-name" style="color: #34d399;">INTERFAZ INSTITUCIONAL</span>
            </div>
            <div class="card-subtags">PATIO BONITO 1985 • POT ART. 566-568 • JAC</div>
            <div class="metrics-pills-row">
              <div class="metric-pill"><span class="icon">🏘️</span><div><div class="val">1985</div><div class="lbl">Patio Bonito</div></div></div>
              <div class="metric-pill"><span class="icon">📜</span><div><div class="val">POT</div><div class="lbl">Actuaciones Estrat.</div></div></div>
              <div class="metric-pill"><span class="icon">🤝</span><div><div class="val">JAC</div><div class="lbl">Interfaz Real</div></div></div>
            </div>
          </div>
        `;
      }}
    }}

    function renderSlide(num) {{
      currentSlideNum = num;
      const sec = SECTIONS.find(s => s.num === num) || SECTIONS[0];
      const idx = SECTIONS.indexOf(sec);

      // Actualizar Barra de Progreso
      const progress = ((num) / SECTIONS.length) * 100;
      progressBar.style.width = `${{progress}}%`;

      // Actualizar Selector
      slideSelector.value = num;

      // Actualizar Imagen de Fondo con Fade Suave
      bgImage.classList.remove('active');
      setTimeout(() => {{
        bgImage.src = `slides/slide_${{num}}.png`;
        bgImage.onload = () => bgImage.classList.add('active');
      }}, 100);

      // Actualizar Narrativa Izquierda
      slideBadge.textContent = `SLIDE ${{String(num).padStart(2, '0')}} • ${{sec.category}}`;
      slideTitle.textContent = sec.title;
      slideSubtitle.textContent = sec.subtitle;
      territorialCardsRow.innerHTML = getTerritorialCardsHtml(sec);
      bottomFootnote.textContent = `✦ ${{sec.category}} — Monografía Arquitectónica`;

      // Actualizar HUD
      hudTitleBadge.textContent = `✦ ${{sec.label}}`;
      infoText.innerHTML = `Selecciona o arrastra un nodo para ver detalles, comparar indicadores y explorar relaciones en 3D.`;

      // Actualizar Teaser Siguiente
      const nextSec = SECTIONS[idx + 1];
      if (nextSec) {{
        nextTeaser.textContent = `${{nextSec.title.toUpperCase()}}`;
        nextTeaser.style.display = 'flex';
      }} else {{
        nextTeaser.textContent = 'FIN DE LA PRESENTACIÓN';
      }}

      // Cargar Datos en el Motor 3D
      if (window.engine) {{
        window.engine.loadSection(idx);
      }}
    }}

    function jumpToSlide(num) {{
      if (num >= 1 && num <= 62) {{
        renderSlide(num);
      }}
    }}

    function nextSlide() {{
      if (currentSlideNum < 62) jumpToSlide(currentSlideNum + 1);
    }}

    function prevSlide() {{
      if (currentSlideNum > 1) jumpToSlide(currentSlideNum - 1);
    }}

    // ==========================================================================
    // 3. MOTOR TOPOLÓGICO 3D DE ALTO RENDIMIENTO CON NODOS BRILLANTES
    // ==========================================================================
    class StageEngine {{
      constructor() {{
        this.canvas = document.getElementById('stageCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.angleX = 0.25;
        this.angleY = 0.35;
        this.autoRotate = true;
        this.isDraggingBg = false;
        this.draggedNode = null;
        this.hoveredNode = null;
        this.pinnedNode = null;
        this.shockwaves = [];
        this.lastMouse = {{ x: 0, y: 0 }};
        this.currentIdx = 0;
        this.data = null;
        this.rgb = [2, 132, 199];

        this.initEvents();
        this.resize();
      }}

      loadSection(idx) {{
        this.currentIdx = idx;
        this.data = JSON.parse(JSON.stringify(SECTIONS[idx]));
        this.rgb = SECTIONS[idx].rgb;
        this.shockwaves = [];
        this.triggerPulse();
      }}

      resize() {{
        const box = this.canvas.parentElement;
        this.width = box.clientWidth || 500;
        this.height = box.clientHeight || 350;
        const dpr = Math.min(window.devicePixelRatio || 1, 2);
        this.canvas.width = Math.floor(this.width * dpr);
        this.canvas.height = Math.floor(this.height * dpr);
        this.ctx.setTransform(1, 0, 0, 1, 0, 0);
        this.ctx.scale(dpr, dpr);
      }}

      initEvents() {{
        window.addEventListener('resize', () => this.resize());

        this.canvas.addEventListener('mousedown', (e) => this.onMouseDown(e));
        window.addEventListener('mousemove', (e) => this.onMouseMove(e));
        window.addEventListener('mouseup', () => this.onMouseUp());
        this.canvas.addEventListener('click', (e) => this.onClick(e));
      }}

      project(p) {{
        const cosY = Math.cos(this.angleY), sinY = Math.sin(this.angleY);
        const x1 = p.x * cosY - p.z * sinY;
        const z1 = p.z * cosY + p.x * sinY;

        const cosX = Math.cos(this.angleX), sinX = Math.sin(this.angleX);
        const y2 = p.y * cosX - z1 * sinX;
        const z2 = z1 * cosX + p.y * sinX;

        const fov = 380;
        const scale = fov / (fov + z2);
        return {{
          x: this.width / 2 + x1 * scale,
          y: this.height / 2 + y2 * scale,
          scale: Math.max(0.2, scale),
          z2: z2
        }};
      }}

      getNodeUnderCursor(mx, my) {{
        if (!this.data) return null;
        let best = null;
        let minDist = 26;
        this.data.nodes.forEach(n => {{
          const proj = this.project(n);
          const dist = Math.hypot(proj.x - mx, proj.y - my);
          if (dist < n.r * proj.scale + 12 && dist < minDist) {{
            minDist = dist;
            best = n;
          }}
        }});
        return best;
      }}

      onMouseDown(e) {{
        const rect = this.canvas.getBoundingClientRect();
        const mx = e.clientX - rect.left;
        const my = e.clientY - rect.top;

        const targetNode = this.getNodeUnderCursor(mx, my);
        if (targetNode) {{
          this.draggedNode = targetNode;
        }} else {{
          this.isDraggingBg = true;
          this.lastMouse = {{ x: e.clientX, y: e.clientY }};
        }}
      }}

      onMouseMove(e) {{
        const rect = this.canvas.getBoundingClientRect();
        const mx = e.clientX - rect.left;
        const my = e.clientY - rect.top;

        if (this.draggedNode) {{
          const cosY = Math.cos(-this.angleY), sinY = Math.sin(-this.angleY);
          const dx = (mx - this.width / 2) * 1.5;
          const dy = (my - this.height / 2) * 1.5;
          this.draggedNode.x = dx * cosY - 0 * sinY;
          this.draggedNode.y = dy;
          this.draggedNode.z = 0 * cosY + dx * sinY;
          return;
        }}

        if (this.isDraggingBg) {{
          const dx = e.clientX - this.lastMouse.x;
          const dy = e.clientY - this.lastMouse.y;
          this.angleY += dx * 0.007;
          this.angleX -= dy * 0.007;
          this.lastMouse = {{ x: e.clientX, y: e.clientY }};
        }} else {{
          const node = this.getNodeUnderCursor(mx, my);
          this.hoveredNode = node;
          if (node) {{
            this.showNodeDetails(node);
          }}
        }}
      }}

      onMouseUp() {{
        this.isDraggingBg = false;
        this.draggedNode = null;
      }}

      onClick(e) {{
        const rect = this.canvas.getBoundingClientRect();
        const mx = e.clientX - rect.left;
        const my = e.clientY - rect.top;
        const node = this.getNodeUnderCursor(mx, my);

        if (node) {{
          this.pinnedNode = node;
          this.showNodeDetails(node);
          this.triggerPulse();
        }}
      }}

      showNodeDetails(node) {{
        infoText.innerHTML = `<strong>${{node.label}}</strong>: ${{node.desc}}`;
      }}

      triggerPulse() {{
        this.shockwaves.push({{ radius: 5, maxRadius: 280, alpha: 1 }});
      }}

      resetNodes() {{
        if (this.data) {{
          this.data = JSON.parse(JSON.stringify(SECTIONS[this.currentIdx]));
          this.shockwaves = [];
          this.triggerPulse();
        }}
      }}

      render() {{
        if (!this.data) return;

        if (this.autoRotate && !this.isDraggingBg && !this.draggedNode) {{
          this.angleY += 0.004;
        }}

        this.ctx.clearRect(0, 0, this.width, this.height);

        // Ondas de choque
        for (let i = this.shockwaves.length - 1; i >= 0; i--) {{
          const sw = this.shockwaves[i];
          sw.radius += 4;
          sw.alpha *= 0.95;

          this.ctx.beginPath();
          this.ctx.arc(this.width / 2, this.height / 2, sw.radius, 0, Math.PI * 2);
          this.ctx.strokeStyle = `rgba(${{this.rgb[0]}}, ${{this.rgb[1]}}, ${{this.rgb[2]}}, ${{sw.alpha * 0.6}})`;
          this.ctx.lineWidth = 1.8;
          this.ctx.stroke();

          if (sw.alpha < 0.02) this.shockwaves.splice(i, 1);
        }}

        // Aristas / Conexiones
        this.data.links.forEach(([i, j]) => {{
          const n1 = this.data.nodes[i];
          const n2 = this.data.nodes[j];
          if (!n1 || !n2) return;

          const p1 = this.project(n1);
          const p2 = this.project(n2);

          const isConnected = (this.hoveredNode && (this.hoveredNode.id === n1.id || this.hoveredNode.id === n2.id));

          this.ctx.beginPath();
          this.ctx.moveTo(p1.x, p1.y);
          this.ctx.lineTo(p2.x, p2.y);

          if (isConnected) {{
            this.ctx.strokeStyle = `rgba(${{this.rgb[0]}}, ${{this.rgb[1]}}, ${{this.rgb[2]}}, 0.9)`;
            this.ctx.lineWidth = 2.4;
          }} else {{
            this.ctx.strokeStyle = `rgba(${{this.rgb[0]}}, ${{this.rgb[1]}}, ${{this.rgb[2]}}, 0.28)`;
            this.ctx.lineWidth = 1.2;
          }}
          this.ctx.stroke();
        }});

        // Nodos con Glow y Gradiente Esférico
        const sorted = [...this.data.nodes].map(n => ({{ node: n, proj: this.project(n) }}))
          .sort((a, b) => a.proj.z2 - b.proj.z2);

        sorted.forEach(({{ node, proj }}) => {{
          const isHovered = this.hoveredNode && this.hoveredNode.id === node.id;
          const r = node.r * proj.scale * (isHovered ? 1.35 : 1);

          // Glow exterior
          this.ctx.beginPath();
          this.ctx.arc(proj.x, proj.y, r * 2.2, 0, Math.PI * 2);
          this.ctx.fillStyle = `rgba(${{this.rgb[0]}}, ${{this.rgb[1]}}, ${{this.rgb[2]}}, ${{isHovered ? 0.4 : 0.15}})`;
          this.ctx.fill();

          // Cuerpo de la esfera
          this.ctx.beginPath();
          this.ctx.arc(proj.x, proj.y, r, 0, Math.PI * 2);
          const grad = this.ctx.createRadialGradient(
            proj.x - r * 0.35, proj.y - r * 0.35, r * 0.1,
            proj.x, proj.y, r
          );
          grad.addColorStop(0, '#ffffff');
          grad.addColorStop(0.4, `rgb(${{this.rgb[0]}}, ${{this.rgb[1]}}, ${{this.rgb[2]}})`);
          grad.addColorStop(1, `rgba(${{this.rgb[0] * 0.4}}, ${{this.rgb[1] * 0.4}}, ${{this.rgb[2] * 0.4}}, 1)`);
          this.ctx.fillStyle = grad;
          this.ctx.fill();

          // Borde fino brillante
          this.ctx.strokeStyle = '#ffffff';
          this.ctx.lineWidth = isHovered ? 2 : 1;
          this.ctx.stroke();

          // Etiqueta del Nodo
          this.ctx.font = `600 ${{Math.max(10, Math.floor(12 * proj.scale))}}px "Space Grotesk", sans-serif`;
          this.ctx.fillStyle = isHovered ? '#ffffff' : 'rgba(255, 255, 255, 0.85)';
          this.ctx.textAlign = 'center';
          this.ctx.fillText(node.label, proj.x, proj.y + r + 14 * proj.scale);
        }});
      }}
    }}

    // Inicializar Motor Topológico al Cargar
    window.addEventListener('DOMContentLoaded', () => {{
      window.engine = new StageEngine();
      renderSlide(1);

      function loop() {{
        if (window.engine) window.engine.render();
        requestAnimationFrame(loop);
      }}
      loop();
    }});

    function triggerPulse() {{
      if (window.engine) window.engine.triggerPulse();
    }}

    function toggleOrbit() {{
      if (window.engine) {{
        window.engine.autoRotate = !window.engine.autoRotate;
        document.getElementById('orbitBtn').classList.toggle('active', window.engine.autoRotate);
      }}
    }}

    function resetGraph() {{
      if (window.engine) window.engine.resetNodes();
    }}

    function filterCategory(cat, btn) {{
      document.querySelectorAll('.cat-tab-btn').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');
      triggerPulse();
    }}

    // Navegación por Teclado
    document.addEventListener('keydown', (e) => {{
      if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') {{
        e.preventDefault();
        nextSlide();
      }} else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {{
        e.preventDefault();
        prevSlide();
      }} else if (e.key === 'Home') {{
        jumpToSlide(1);
      }} else if (e.key === 'End') {{
        jumpToSlide(62);
      }}
    }});
  </script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(deck_html)

print("Masterpiece slide deck index.html generated successfully!")
