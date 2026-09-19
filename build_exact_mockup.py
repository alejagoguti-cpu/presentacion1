# -*- coding: utf-8 -*-
import os
import json

# Extract base SECTIONS data
with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

start_idx = text.find('const SECTIONS = [')
end_idx = text.find('// ==========================================================================\n    // 2. INICIALIZACIÓN DEL MAPA')
if end_idx == -1:
    end_idx = text.find('// 2. INICIALIZACIÓN DEL MAPA')
if end_idx == -1:
    end_idx = text.find('const GEO_DATA = {')

sections_js = text[start_idx:end_idx].strip()

# Create master HTML template matching the exact uploaded reference mockup
mockup_html = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Hong Kong & Shenzhen — Topologías de la Densidad y el Poder (Defensa de Maestría)</title>
  
  <!-- Tipografías Editoriales Modernas -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=DM+Mono:ital,wght@0,300;0,400;0,500;1,400&family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet" />

  <style>
    /* ==========================================================================
       ESTÉTICA CINEMATOGRÁFICA EXACTA AL MOCKUP (HUD FROSTED GLASS + FLAT ICONS)
       ========================================================================== */
    :root {{
      --bg-dark: #080c16;
      --glass-hud: rgba(14, 22, 38, 0.72);
      --glass-border: rgba(255, 255, 255, 0.18);
      --glass-card-left: rgba(12, 18, 30, 0.65);
      
      --text-pure: #ffffff;
      --text-silver: #cbd5e1;
      --text-muted: #94a3b8;
      --text-faint: #64748b;
      
      --cat-eco: #e11d48;       /* Economía (Rojo) */
      --cat-urb: #0284c7;       /* Urbanismo (Azul) */
      --cat-env: #10b981;       /* Medio Ambiente (Verde) */
      --cat-soc: #f59e0b;       /* Sociedad (Ámbar) */
      --cat-gov: #8b5cf6;       /* Gobernanza (Violeta) */
      
      --font-serif: "Playfair Display", Georgia, serif;
      --font-sans: "Space Grotesk", -apple-system, BlinkMacSystemFont, sans-serif;
      --font-body: "Inter", -apple-system, sans-serif;
      --font-mono: "DM Mono", monospace;
    }}

    *, *::before, *::after {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    html, body {{
      width: 100vw;
      height: 100vh;
      overflow: hidden;
      background-color: var(--bg-dark);
      color: var(--text-pure);
      font-family: var(--font-sans);
      -webkit-font-smoothing: antialiased;
    }}

    /* ==========================================================================
       CABECERA SUPERIOR DISCRETA
       ========================================================================== */
    .top-header {{
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 56px;
      padding: 0 3.2vw;
      background: linear-gradient(180deg, rgba(8, 12, 22, 0.95) 0%, rgba(8, 12, 22, 0.4) 80%, transparent 100%);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      z-index: 100;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
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
      background: rgba(255, 255, 255, 0.8);
      border-radius: 2px;
    }}

    .authors-label {{
      font-family: var(--font-body);
      font-size: 0.84rem;
      font-weight: 500;
      color: var(--text-silver);
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
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: #ffffff;
      font-family: var(--font-sans);
      font-size: 0.8rem;
      font-weight: 500;
      padding: 5px 14px;
      border-radius: 20px;
      outline: none;
      cursor: pointer;
      backdrop-filter: blur(8px);
      transition: all 0.2s ease;
      max-width: 360px;
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
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: #ffffff;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.2s ease;
    }}

    .circle-nav-btn svg {{
      width: 14px;
      height: 14px;
      stroke: currentColor;
    }}

    .circle-nav-btn:hover {{
      background: rgba(255, 255, 255, 0.25);
      border-color: #ffffff;
      transform: scale(1.05);
    }}

    .progress-line {{
      position: fixed;
      top: 55px;
      left: 0;
      height: 2px;
      width: 0%;
      background: linear-gradient(90deg, #0284c7, #8b5cf6, #10b981, #f59e0b);
      z-index: 101;
      transition: width 0.3s ease;
    }}

    /* ==========================================================================
       ESCENARIO PRINCIPAL DEL SLIDE (100VH FULLSCREEN)
       ========================================================================== */
    .viewport-stage {{
      position: relative;
      width: 100vw;
      height: 100vh;
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 72px 3.2vw 2.5vh;
    }}

    /* Fondo Fotográfico / Panorámico */
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
      transform: scale(1.03);
      transition: opacity 0.5s ease, transform 0.8s cubic-bezier(0.16, 1, 0.3, 1);
    }}

    .backdrop-img.active {{
      opacity: 1;
      transform: scale(1);
    }}

    .backdrop-gradient-overlay {{
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      background: linear-gradient(
        90deg,
        rgba(8, 12, 22, 0.92) 0%,
        rgba(8, 12, 22, 0.84) 36%,
        rgba(8, 12, 22, 0.45) 58%,
        rgba(8, 12, 22, 0.2) 75%,
        rgba(8, 12, 22, 0.6) 100%
      );
      z-index: 2;
      pointer-events: none;
    }}

    /* ==========================================================================
       COLUMNA IZQUIERDA: HERO NARRATIVA & TARJETAS DE MÉTRICAS FLAT
       ========================================================================== */
    .hero-narrative {{
      position: relative;
      z-index: 10;
      width: 53%;
      max-width: 760px;
      display: flex;
      flex-direction: column;
      justify-content: center;
      padding-right: 1.5rem;
      animation: fadeInNarrative 0.45s ease;
    }}

    @keyframes fadeInNarrative {{
      from {{ opacity: 0; transform: translateY(10px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    .slide-pill-badge {{
      font-family: var(--font-mono);
      font-size: 0.74rem;
      letter-spacing: 0.16em;
      text-transform: uppercase;
      font-weight: 600;
      color: var(--text-silver);
      display: flex;
      align-items: center;
      gap: 0.5rem;
      margin-bottom: 0.6rem;
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
      text-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
    }}

    .main-slide-subtitle {{
      font-family: var(--font-body);
      font-size: clamp(1.05rem, 1.35vw, 1.35rem);
      font-weight: 300;
      line-height: 1.5;
      color: var(--text-silver);
      margin-bottom: 1.2rem;
      max-width: 660px;
      text-shadow: 0 2px 10px rgba(0, 0, 0, 0.7);
    }}

    .thesis-taglines-row {{
      display: flex;
      flex-direction: column;
      gap: 0.25rem;
      padding-top: 0.6rem;
      margin-bottom: 1.4rem;
      position: relative;
    }}

    .thesis-taglines-row::before {{
      content: '';
      width: 120px;
      height: 1.5px;
      background: rgba(255, 255, 255, 0.4);
      margin-bottom: 0.5rem;
    }}

    .tagline-item {{
      font-family: var(--font-mono);
      font-size: 0.7rem;
      font-weight: 500;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      color: rgba(255, 255, 255, 0.65);
    }}

    /* Tarjetas Territoriales de Métricas (Flat Icons) */
    .territorial-cards-row {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.1rem;
      margin-bottom: 1.2rem;
    }}

    .territory-card {{
      background: var(--glass-card-left);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 12px;
      padding: 0.95rem 1.1rem;
      transition: all 0.2s ease;
    }}

    .territory-card:hover {{
      border-color: rgba(255, 255, 255, 0.25);
      transform: translateY(-2px);
    }}

    .card-top-head {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 0.15rem;
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
      font-size: 0.62rem;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: var(--text-muted);
      margin-bottom: 0.7rem;
    }}

    .explore-btn {{
      font-family: var(--font-mono);
      font-size: 0.64rem;
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
      margin-bottom: 0.65rem;
    }}

    .explore-btn:hover {{
      background: rgba(255, 255, 255, 0.2);
      border-color: #ffffff;
    }}

    .metrics-pills-row {{
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }}

    .metric-pill {{
      display: flex;
      align-items: center;
      gap: 0.4rem;
      font-family: var(--font-sans);
      font-size: 0.74rem;
    }}

    .flat-svg-icon {{
      width: 18px;
      height: 18px;
      stroke: var(--text-silver);
      fill: none;
      stroke-width: 1.8;
      flex-shrink: 0;
      opacity: 0.9;
    }}

    .metric-pill .val {{
      font-weight: 700;
      color: #ffffff;
      line-height: 1.1;
    }}

    .metric-pill .lbl {{
      font-size: 0.64rem;
      color: var(--text-muted);
      white-space: nowrap;
    }}

    .bottom-footnote {{
      font-family: var(--font-mono);
      font-size: 0.7rem;
      letter-spacing: 0.06em;
      color: var(--text-faint);
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }}

    /* ==========================================================================
       COLUMNA DERECHA: HUD FROSTED GLASS CONSOLA & RED 3D
       ========================================================================== */
    .hud-console-wrap {{
      position: relative;
      z-index: 10;
      width: 44%;
      height: 100%;
      max-height: calc(100vh - 105px);
      display: flex;
      flex-direction: column;
    }}

    .glass-hud-card {{
      flex: 1;
      background: var(--glass-hud);
      backdrop-filter: blur(28px) saturate(180%);
      -webkit-backdrop-filter: blur(28px) saturate(180%);
      border: 1px solid var(--glass-border);
      border-radius: 20px;
      box-shadow: 0 30px 70px -10px rgba(0, 0, 0, 0.6), inset 0 1px 1px rgba(255, 255, 255, 0.2);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      position: relative;
    }}

    /* Barra Superior del HUD */
    .hud-top-bar {{
      padding: 0.8rem 1.2rem;
      border-bottom: 1px solid rgba(255, 255, 255, 0.09);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.8rem;
    }}

    .hud-title-badge {{
      font-family: var(--font-mono);
      font-size: 0.72rem;
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
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid rgba(255, 255, 255, 0.18);
      color: #ffffff;
      font-family: var(--font-mono);
      font-size: 0.66rem;
      font-weight: 600;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      padding: 4px 9px;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.15s ease;
      display: flex;
      align-items: center;
      gap: 0.35rem;
    }}

    .hud-btn svg {{
      width: 12px;
      height: 12px;
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

    /* Leyenda de Categorías en la esquina superior */
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
      font-size: 0.58rem;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 5px;
      color: rgba(255, 255, 255, 0.8);
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
      min-height: 270px;
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
      margin: 0 1rem 0.5rem;
      padding: 0.55rem 0.9rem;
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 10px;
      font-family: var(--font-body);
      font-size: 0.74rem;
      line-height: 1.4;
      color: var(--text-silver);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.6rem;
    }}

    .hud-info-strip .info-icon svg {{
      width: 15px;
      height: 15px;
      stroke: #38bdf8;
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

    /* Fila de Filtros de Categoría con Iconos Flat */
    .hud-category-filter-row {{
      padding: 0.55rem 1rem 0.85rem;
      display: grid;
      grid-template-columns: repeat(5, 1fr);
      gap: 0.4rem;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
    }}

    .cat-tab-btn {{
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 8px;
      padding: 6px 4px;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 3px;
      cursor: pointer;
      transition: all 0.2s ease;
      color: var(--text-silver);
    }}

    .cat-tab-btn svg {{
      width: 18px;
      height: 18px;
      stroke: currentColor;
      fill: none;
      stroke-width: 1.8;
      transition: all 0.2s ease;
    }}

    .cat-tab-btn:hover {{
      background: rgba(255, 255, 255, 0.15);
      border-color: rgba(255, 255, 255, 0.3);
      color: #ffffff;
      transform: translateY(-2px);
    }}

    .cat-tab-btn.active {{
      background: rgba(255, 255, 255, 0.22);
      border-color: #ffffff;
      color: #ffffff;
    }}

    .cat-tab-btn .cat-title {{
      font-family: var(--font-mono);
      font-size: 0.56rem;
      font-weight: 600;
      letter-spacing: 0.08em;
      text-transform: uppercase;
    }}

    /* Teaser Siguiente Diapositiva */
    .next-teaser-link {{
      position: fixed;
      bottom: 1.2rem;
      right: 3.2vw;
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

    .keyboard-hint {{
      position: fixed;
      bottom: 1.2rem;
      left: 3.2vw;
      font-family: var(--font-mono);
      font-size: 0.66rem;
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
      <button class="circle-nav-btn" onclick="prevSlide()" title="Anterior (←)">
        <svg viewBox="0 0 24 24" fill="none" stroke-width="2.5"><path d="M15 19l-7-7 7-7"/></svg>
      </button>
      <button class="circle-nav-btn" onclick="nextSlide()" title="Siguiente (→)">
        <svg viewBox="0 0 24 24" fill="none" stroke-width="2.5"><path d="M9 5l7 7-7 7"/></svg>
      </button>
    </div>
  </header>

  <!-- Escenario Principal del Slide -->
  <main class="viewport-stage">
    
    <!-- Fondo Visual Dinámico -->
    <div class="backdrop-canvas">
      <img id="bgImage" class="backdrop-img active" src="slides/slide_1.png" alt="Visual Arquitectónico" />
      <div class="backdrop-gradient-overlay"></div>
    </div>

    <!-- Columna Izquierda: Narrativa & Tarjetas Territoriales Flat -->
    <div class="hero-narrative" id="narrativeCol">
      <div class="slide-pill-badge" id="slideBadge">SLIDE 01</div>
      <h1 class="main-slide-title" id="slideTitle">Hong Kong & Shenzhen</h1>
      <p class="main-slide-subtitle" id="slideSubtitle">¿Qué modelo de ciudad es mejor: el de Hong Kong o el de Shenzhen?</p>

      <div class="thesis-taglines-row" id="taglinesRow">
        <span class="tagline-item">DOS TERRITORIOS</span>
        <span class="tagline-item">UNA REGIÓN</span>
        <span class="tagline-item">UN FUTURO COMPARTIDO</span>
      </div>

      <!-- Tarjetas Territoriales Dinámicas (Iconos Flat SVG) -->
      <div class="territorial-cards-row" id="territorialCardsRow">
        <!-- Generado dinámicamente -->
      </div>

      <div class="bottom-footnote" id="bottomFootnote">
        ✦ Región del Gran Delta del Río Perla
      </div>
    </div>

    <!-- Columna Derecha: HUD Frosted Glass & Red 3D -->
    <div class="hud-console-wrap">
      <div class="glass-hud-card">
        
        <!-- HUD Header -->
        <div class="hud-top-bar">
          <div class="hud-title-badge" id="hudTitleBadge">✦ RED BIPOLAR: DILEMA TERRITORIAL</div>
          <div class="hud-actions">
            <button class="hud-btn" onclick="triggerPulse()">
              <svg viewBox="0 0 24 24" fill="currentColor"><path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/></svg>
              Pulso
            </button>
            <button class="hud-btn" id="orbitBtn" onclick="toggleOrbit()">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(30 12 12)"/></svg>
              Órbita
            </button>
            <button class="hud-btn" onclick="resetGraph()">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>
              Reset
            </button>
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
          <div class="info-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>
          </div>
          <div class="hud-info-text" id="infoText">
            Selecciona o arrastra un nodo para ver detalles, comparar indicadores y explorar relaciones.
          </div>
        </div>

        <!-- Fila de Filtros de Categoría con Iconos Flat SVG -->
        <div class="hud-category-filter-row">
          <button class="cat-tab-btn" onclick="filterCategory('urbanismo', this)">
            <svg viewBox="0 0 24 24"><path d="M3 21h18"/><path d="M6 21V9a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v12"/><path d="M10 21V5a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v16"/><path d="M14 21v-8a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1v8"/></svg>
            <span class="cat-title">URBANISMO</span>
          </button>
          <button class="cat-tab-btn" onclick="filterCategory('economia', this)">
            <svg viewBox="0 0 24 24"><path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/></svg>
            <span class="cat-title">ECONOMÍA</span>
          </button>
          <button class="cat-tab-btn" onclick="filterCategory('ambiente', this)">
            <svg viewBox="0 0 24 24"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg>
            <span class="cat-title">MEDIO AMB.</span>
          </button>
          <button class="cat-tab-btn" onclick="filterCategory('sociedad', this)">
            <svg viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
            <span class="cat-title">SOCIEDAD</span>
          </button>
          <button class="cat-tab-btn" onclick="filterCategory('gobernanza', this)">
            <svg viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
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
    // 1. DATASET DE LAS 62 SECCIONES
    // ==========================================================================
{sections_js}

    // Flat SVG Icon definitions for dynamic injection
    const ICONS = {{
      users: `<svg class="flat-svg-icon" viewBox="0 0 24 24"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>`,
      building: `<svg class="flat-svg-icon" viewBox="0 0 24 24"><rect x="4" y="2" width="16" height="20" rx="2"/><line x1="8" y1="6" x2="8" y2="6.01"/><line x1="16" y1="6" x2="16" y2="6.01"/><line x1="8" y1="10" x2="8" y2="10.01"/><line x1="16" y1="10" x2="16" y2="10.01"/><line x1="8" y1="14" x2="8" y2="14.01"/><line x1="16" y1="14" x2="16" y2="14.01"/><line x1="8" y1="18" x2="8" y2="18.01"/><line x1="16" y1="18" x2="16" y2="18.01"/></svg>`,
      transit: `<svg class="flat-svg-icon" viewBox="0 0 24 24"><rect x="3" y="3" width="18" height="15" rx="3"/><circle cx="7" cy="15" r="1.5"/><circle cx="17" cy="15" r="1.5"/><path d="M3 9h18"/><path d="M7 18v2"/><path d="M17 18v2"/></svg>`,
      leaf: `<svg class="flat-svg-icon" viewBox="0 0 24 24"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg>`,
      growth: `<svg class="flat-svg-icon" viewBox="0 0 24 24"><path d="M3 3v18h18"/><path d="m19 9-5 5-4-4-3 3"/></svg>`,
      shield: `<svg class="flat-svg-icon" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>`,
      tech: `<svg class="flat-svg-icon" viewBox="0 0 24 24"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>`,
      water: `<svg class="flat-svg-icon" viewBox="0 0 24 24"><path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/></svg>`
    }};

    // ==========================================================================
    // 2. CONTROL DEL ESTADO & RENDERIZADO DEL SLIDE ACTUAL
    // ==========================================================================
    let currentSlideNum = 1;

    const bgImage = document.getElementById('bgImage');
    const slideBadge = document.getElementById('slideBadge');
    const slideTitle = document.getElementById('slideTitle');
    const slideSubtitle = document.getElementById('slideSubtitle');
    const taglinesRow = document.getElementById('taglinesRow');
    const territorialCardsRow = document.getElementById('territorialCardsRow');
    const bottomFootnote = document.getElementById('bottomFootnote');
    const hudTitleBadge = document.getElementById('hudTitleBadge');
    const slideSelector = document.getElementById('slideSelector');
    const progressBar = document.getElementById('progressBar');
    const nextTeaser = document.getElementById('nextTeaser');
    const infoText = document.getElementById('infoText');

    function initSlideSelector() {{
      let optionsHtml = '';
      SECTIONS.forEach(s => {{
        optionsHtml += `<option value="${{s.num}}">Slide ${{String(s.num).padStart(2, '0')}}: ${{s.title}}</option>`;
      }});
      slideSelector.innerHTML = optionsHtml;
    }}
    initSlideSelector();

    // Renderizar Tarjetas Territoriales de Métricas según el Capítulo
    function getTerritorialCardsHtml(sec) {{
      const num = sec.num;
      
      if (num <= 15) {{
        return `
          <div class="territory-card">
            <div class="card-top-head">
              <span class="card-city-name" style="color: #38bdf8;">HONG KONG</span>
            </div>
            <div class="card-subtags">GLOBAL • CONSOLIDADA • DENSA</div>
            <div class="explore-btn" onclick="filterCategory('urbanismo')">EXPLORAR →</div>
            <div class="metrics-pills-row">
              <div class="metric-pill">${{ICONS.users}}<div><div class="val">7.5 M</div><div class="lbl">Habitantes</div></div></div>
              <div class="metric-pill">${{ICONS.building}}<div><div class="val">2,755</div><div class="lbl">Hab/km²</div></div></div>
              <div class="metric-pill">${{ICONS.transit}}<div><div class="val">90%</div><div class="lbl">Transp. público</div></div></div>
            </div>
          </div>

          <div class="territory-card">
            <div class="card-top-head">
              <span class="card-city-name" style="color: #a78bfa;">SHENZHEN</span>
            </div>
            <div class="card-subtags">INNOVACIÓN • CRECIMIENTO • FLEXIBILIDAD</div>
            <div class="explore-btn" onclick="filterCategory('economia')">EXPLORAR →</div>
            <div class="metrics-pills-row">
              <div class="metric-pill">${{ICONS.users}}<div><div class="val">17.6 M</div><div class="lbl">Habitantes</div></div></div>
              <div class="metric-pill">${{ICONS.building}}<div><div class="val">6,600</div><div class="lbl">Hab/km²</div></div></div>
              <div class="metric-pill">${{ICONS.transit}}<div><div class="val">70%</div><div class="lbl">Transp. público</div></div></div>
            </div>
          </div>
        `;
      }} else if (num <= 25) {{
        return `
          <div class="territory-card">
            <div class="card-top-head">
              <span class="card-city-name" style="color: #38bdf8;">DENSIDAD & SUELO</span>
            </div>
            <div class="card-subtags">PARQUES RURALES VS. VERTICALIDAD</div>
            <div class="explore-btn" onclick="filterCategory('urbanismo')">VER DATOS →</div>
            <div class="metrics-pills-row">
              <div class="metric-pill">${{ICONS.leaf}}<div><div class="val">40%</div><div class="lbl">Protegido</div></div></div>
              <div class="metric-pill">${{ICONS.growth}}<div><div class="val">0.54</div><div class="lbl">Gini</div></div></div>
              <div class="metric-pill">${{ICONS.building}}<div><div class="val">220k</div><div class="lbl">Cage Homes</div></div></div>
            </div>
          </div>

          <div class="territory-card">
            <div class="card-top-head">
              <span class="card-city-name" style="color: #38bdf8;">GOBERNANZA HK</span>
            </div>
            <div class="card-subtags">COMMON LAW • LEASEHOLD (1997)</div>
            <div class="explore-btn" onclick="filterCategory('gobernanza')">FACTORES →</div>
            <div class="metrics-pills-row">
              <div class="metric-pill">${{ICONS.shield}}<div><div class="val">ICAC</div><div class="lbl">1974</div></div></div>
              <div class="metric-pill">${{ICONS.water}}<div><div class="val">80%</div><div class="lbl">Dongjiang</div></div></div>
              <div class="metric-pill">${{ICONS.tech}}<div><div class="val">TTPS</div><div class="lbl">Top Talent</div></div></div>
            </div>
          </div>
        `;
      }} else if (num <= 37) {{
        return `
          <div class="territory-card">
            <div class="card-top-head">
              <span class="card-city-name" style="color: #a78bfa;">I+D & MANUFACTURA</span>
            </div>
            <div class="card-subtags">HUAQIANGBEI • CHINEXT • 20 CLÚSTERES</div>
            <div class="explore-btn" onclick="filterCategory('economia')">EXPLORAR →</div>
            <div class="metrics-pills-row">
              <div class="metric-pill">${{ICONS.growth}}<div><div class="val">6.46%</div><div class="lbl">I+D (PIB)</div></div></div>
              <div class="metric-pill">${{ICONS.tech}}<div><div class="val">90%</div><div class="lbl">I+D Privado</div></div></div>
              <div class="metric-pill">${{ICONS.building}}<div><div class="val">90%</div><div class="lbl">Hardware Global</div></div></div>
            </div>
          </div>

          <div class="territory-card">
            <div class="card-top-head">
              <span class="card-city-name" style="color: #a78bfa;">TEJIDO SOCIAL SZ</span>
            </div>
            <div class="card-subtags">ALDEAS URBANAS • HUKOU • CIUDAD ESPONJA</div>
            <div class="explore-btn" onclick="filterCategory('sociedad')">FACTORES →</div>
            <div class="metrics-pills-row">
              <div class="metric-pill">${{ICONS.users}}<div><div class="val">Urban</div><div class="lbl">Villages</div></div></div>
              <div class="metric-pill">${{ICONS.leaf}}<div><div class="val">Sponge</div><div class="lbl">City</div></div></div>
              <div class="metric-pill">${{ICONS.water}}<div><div class="val">Futian</div><div class="lbl">Manglar</div></div></div>
            </div>
          </div>
        `;
      }} else if (num <= 47) {{
        return `
          <div class="territory-card">
            <div class="card-top-head">
              <span class="card-city-name" style="color: #34d399;">ZONAS DE SUTURA</span>
            </div>
            <div class="card-subtags">QIANHAI ZEE • LOK MA CHAU LOOP</div>
            <div class="explore-btn" onclick="filterCategory('urbanismo')">EXPLORAR →</div>
            <div class="metrics-pills-row">
              <div class="metric-pill">${{ICONS.building}}<div><div class="val">Qianhai</div><div class="lbl">Plan 2021</div></div></div>
              <div class="metric-pill">${{ICONS.tech}}<div><div class="val">87 ha</div><div class="lbl">HSITP Loop</div></div></div>
              <div class="metric-pill">${{ICONS.growth}}<div><div class="val">GBA</div><div class="lbl">Gran Bahía</div></div></div>
            </div>
          </div>

          <div class="territory-card">
            <div class="card-top-head">
              <span class="card-city-name" style="color: #34d399;">SISTEMA CIRCULATORIO</span>
            </div>
            <div class="card-subtags">DONGJIANG (83 KM) • DAYA BAY NUCLEAR</div>
            <div class="explore-btn" onclick="filterCategory('ambiente')">FACTORES →</div>
            <div class="metrics-pills-row">
              <div class="metric-pill">${{ICONS.water}}<div><div class="val">83 km</div><div class="lbl">Acueducto</div></div></div>
              <div class="metric-pill">${{ICONS.tech}}<div><div class="val">Daya Bay</div><div class="lbl">Energía</div></div></div>
              <div class="metric-pill">${{ICONS.leaf}}<div><div class="val">2021</div><div class="lbl">Estrés Hídrico</div></div></div>
            </div>
          </div>
        `;
      }} else if (num <= 55) {{
        return `
          <div class="territory-card">
            <div class="card-top-head">
              <span class="card-city-name" style="color: #fbbf24;">ÇATALHÖYÜK</span>
            </div>
            <div class="card-subtags">MALLA CELULAR PEER-TO-PEER (7500 A.C.)</div>
            <div class="explore-btn" onclick="filterCategory('urbanismo')">EXPLORAR →</div>
            <div class="metrics-pills-row">
              <div class="metric-pill">${{ICONS.building}}<div><div class="val">7500 a.C.</div><div class="lbl">Neolítico</div></div></div>
              <div class="metric-pill">${{ICONS.users}}<div><div class="val">10.000</div><div class="lbl">Habitantes</div></div></div>
              <div class="metric-pill">${{ICONS.transit}}<div><div class="val">Cero</div><div class="lbl">Calles</div></div></div>
            </div>
          </div>

          <div class="territory-card">
            <div class="card-top-head">
              <span class="card-city-name" style="color: #fbbf24;">TOPOLOGÍA SOCIAL</span>
            </div>
            <div class="card-subtags">ACCESO POR TECHOS • CERO JERARQUÍA</div>
            <div class="explore-btn" onclick="filterCategory('sociedad')">FACTORES →</div>
            <div class="metrics-pills-row">
              <div class="metric-pill">${{ICONS.leaf}}<div><div class="val">Techos</div><div class="lbl">Circulación</div></div></div>
              <div class="metric-pill">${{ICONS.shield}}<div><div class="val">Cero</div><div class="lbl">Palacios</div></div></div>
              <div class="metric-pill">${{ICONS.tech}}<div><div class="val">P2P</div><div class="lbl">Autoorganización</div></div></div>
            </div>
          </div>
        `;
      }} else {{
        return `
          <div class="territory-card">
            <div class="card-top-head">
              <span class="card-city-name" style="color: #34d399;">CORABASTOS (KENNEDY)</span>
            </div>
            <div class="card-subtags">CENTRO AGROALIMENTARIO REGIONAL</div>
            <div class="explore-btn" onclick="filterCategory('urbanismo')">EXPLORAR →</div>
            <div class="metrics-pills-row">
              <div class="metric-pill">${{ICONS.transit}}<div><div class="val">12.000</div><div class="lbl">ton/día</div></div></div>
              <div class="metric-pill">${{ICONS.building}}<div><div class="val">6.500</div><div class="lbl">Locales</div></div></div>
              <div class="metric-pill">${{ICONS.leaf}}<div><div class="val">Sabana</div><div class="lbl">Cund./Boyacá</div></div></div>
            </div>
          </div>

          <div class="territory-card">
            <div class="card-top-head">
              <span class="card-city-name" style="color: #34d399;">INTERFAZ INSTITUCIONAL</span>
            </div>
            <div class="card-subtags">PATIO BONITO 1985 • POT ART. 566-568 • JAC</div>
            <div class="explore-btn" onclick="filterCategory('gobernanza')">FACTORES →</div>
            <div class="metrics-pills-row">
              <div class="metric-pill">${{ICONS.users}}<div><div class="val">1985</div><div class="lbl">Patio Bonito</div></div></div>
              <div class="metric-pill">${{ICONS.shield}}<div><div class="val">POT</div><div class="lbl">Actuaciones Estrat.</div></div></div>
              <div class="metric-pill">${{ICONS.growth}}<div><div class="val">JAC</div><div class="lbl">Interfaz Real</div></div></div>
            </div>
          </div>
        `;
      }}
    }}

    function renderSlide(num) {{
      currentSlideNum = num;
      const sec = SECTIONS.find(s => s.num === num) || SECTIONS[0];
      const idx = SECTIONS.indexOf(sec);

      // Progreso
      const progress = ((num) / SECTIONS.length) * 100;
      progressBar.style.width = `${{progress}}%`;
      slideSelector.value = num;

      // Imagen de fondo con Fade Suave
      bgImage.classList.remove('active');
      setTimeout(() => {{
        bgImage.src = `slides/slide_${{num}}.png`;
        bgImage.onload = () => bgImage.classList.add('active');
      }}, 80);

      // Textos
      slideBadge.textContent = `SLIDE ${{String(num).padStart(2, '0')}} • ${{sec.category}}`;
      slideTitle.textContent = sec.title;
      slideSubtitle.textContent = sec.subtitle;
      territorialCardsRow.innerHTML = getTerritorialCardsHtml(sec);
      bottomFootnote.textContent = `✦ ${{sec.category}} — Monografía Arquitectónica`;

      // HUD Header & Info
      hudTitleBadge.textContent = `✦ ${{sec.label}}`;
      infoText.innerHTML = `Selecciona o arrastra un nodo para ver detalles, comparar indicadores y explorar relaciones.`;

      // Teaser Siguiente
      const nextSec = SECTIONS[idx + 1];
      if (nextSec) {{
        nextTeaser.textContent = `${{nextSec.title.toUpperCase()}}`;
        nextTeaser.style.display = 'flex';
      }} else {{
        nextTeaser.textContent = 'FIN DE LA PRESENTACIÓN';
      }}

      // Cargar en Motor 3D
      if (window.engine) {{
        window.engine.loadSection(idx);
      }}
    }}

    function jumpToSlide(num) {{
      if (num >= 1 && num <= 62) renderSlide(num);
    }}

    function nextSlide() {{
      if (currentSlideNum < 62) jumpToSlide(currentSlideNum + 1);
    }}

    function prevSlide() {{
      if (currentSlideNum > 1) jumpToSlide(currentSlideNum - 1);
    }}

    // ==========================================================================
    // 3. MOTOR TOPOLÓGICO 3D CON ESFERAS BRILLANTES E ICONOS FLAT
    // ==========================================================================
    class StageEngine {{
      constructor() {{
        this.canvas = document.getElementById('stageCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.angleX = 0.22;
        this.angleY = 0.35;
        this.autoRotate = true;
        this.isDraggingBg = false;
        this.draggedNode = null;
        this.hoveredNode = null;
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
        this.height = box.clientHeight || 340;
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
        let minDist = 28;
        this.data.nodes.forEach(n => {{
          const proj = this.project(n);
          const dist = Math.hypot(proj.x - mx, proj.y - my);
          if (dist < (n.r || 14) * proj.scale + 14 && dist < minDist) {{
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
            infoText.innerHTML = `<strong>${{node.label}}</strong>: ${{node.desc}}`;
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
          infoText.innerHTML = `<strong>${{node.label}}</strong>: ${{node.desc}}`;
          this.triggerPulse();
        }}
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

        // Ondas de choque pulsantes
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

        // Aristas / Conexiones elegantes
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
            this.ctx.strokeStyle = `rgba(${{this.rgb[0]}}, ${{this.rgb[1]}}, ${{this.rgb[2]}}, 0.95)`;
            this.ctx.lineWidth = 2.4;
          }} else {{
            this.ctx.strokeStyle = `rgba(${{this.rgb[0]}}, ${{this.rgb[1]}}, ${{this.rgb[2]}}, 0.28)`;
            this.ctx.lineWidth = 1.2;
          }}
          this.ctx.stroke();
        }});

        // Nodos con Glow y Avatares Esféricos
        const sorted = [...this.data.nodes].map(n => ({{ node: n, proj: this.project(n) }}))
          .sort((a, b) => a.proj.z2 - b.proj.z2);

        sorted.forEach(({{ node, proj }}) => {{
          const isHovered = this.hoveredNode && this.hoveredNode.id === node.id;
          const r = (node.r || 14) * proj.scale * (isHovered ? 1.35 : 1);

          // Glow exterior
          this.ctx.beginPath();
          this.ctx.arc(proj.x, proj.y, r * 2.2, 0, Math.PI * 2);
          this.ctx.fillStyle = `rgba(${{this.rgb[0]}}, ${{this.rgb[1]}}, ${{this.rgb[2]}}, ${{isHovered ? 0.45 : 0.18}})`;
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
          this.ctx.fillStyle = isHovered ? '#ffffff' : 'rgba(255, 255, 255, 0.9)';
          this.ctx.textAlign = 'center';
          this.ctx.fillText(node.label, proj.x, proj.y + r + 14 * proj.scale);

          // Badge de Acción / Tag ("VER FACTORES →")
          if (isHovered || proj.scale > 0.85) {{
            const tag = isHovered ? "EXPLORAR →" : "VER FACTORES →";
            this.ctx.font = `600 ${{Math.max(8, Math.floor(9 * proj.scale))}}px "DM Mono", monospace`;
            this.ctx.fillStyle = `rgba(${{this.rgb[0]}}, ${{this.rgb[1]}}, ${{this.rgb[2]}}, 0.9)`;
            this.ctx.fillText(tag, proj.x, proj.y + r + 26 * proj.scale);
          }}
        }});
      }}
    }}

    // Inicialización
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

    // Navegación con Teclado
    document.addEventListener('keydown', (e) => {{
      if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') {{
        e.preventDefault();
        nextSlide();
      }} else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {{
        e.preventDefault();
        prevSlide();
      }}
    }});
  </script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(mockup_html)

print("Masterpiece UI matching reference mockup exactly with flat SVG icons generated successfully!")
