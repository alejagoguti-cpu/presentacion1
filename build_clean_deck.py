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

# Classification of slide types: 'network' (full width real research network), 'map' (live leaflet satellite), 'case' (slide visual + matrix)
SLIDE_TYPES = {
    # Network slides (Real research network is the hero - NO fake duplicate)
    7: "network", 13: "network", 25: "network", 31: "network", 33: "network",
    34: "network", 36: "network", 37: "network", 47: "network", 53: "network",
    61: "network", 62: "network",

    # Live Satellite Map slides
    1: "map", 2: "map", 3: "map", 4: "map", 5: "map", 6: "map", 8: "map", 9: "map",
    10: "map", 11: "map", 12: "map", 16: "map", 21: "map", 22: "map", 24: "map",
    28: "map", 29: "map", 30: "map", 35: "map", 38: "map", 39: "map", 40: "map",
    41: "map", 44: "map", 48: "map", 49: "map", 56: "map", 57: "map", 58: "map",

    # Comparative / Matrix / Case slides
    14: "case", 15: "case", 17: "case", 18: "case", 19: "case", 20: "case", 23: "case",
    26: "case", 27: "case", 32: "case", 42: "case", 43: "case", 45: "case", 46: "case",
    50: "case", 51: "case", 52: "case", 54: "case", 55: "case", 59: "case", 60: "case"
}

# Geo coordinates dataset
GEO_DATA = {
    1: {"lat": 22.4200, "lng": 114.1200, "zoom": 11, "name": "Delta del Río Perla (Hong Kong & Shenzhen)", "poly": [[22.25, 113.85], [22.58, 113.85], [22.58, 114.40], [22.25, 114.40]]},
    2: {"lat": 22.3193, "lng": 114.1694, "zoom": 12, "name": "Hong Kong (Victoria Harbour & Kowloon)", "poly": [[22.26, 114.12], [22.35, 114.12], [22.35, 114.24], [22.26, 114.24]]},
    3: {"lat": 22.3193, "lng": 114.1694, "zoom": 10, "name": "China → Cantón → Hong Kong", "poly": [[22.15, 113.70], [22.60, 113.70], [22.60, 114.45], [22.15, 114.45]]},
    4: {"lat": 22.2855, "lng": 114.1577, "zoom": 14, "name": "Central & Puerto Histórico de Victoria", "poly": [[22.275, 114.145], [22.295, 114.145], [22.295, 114.175], [22.275, 114.175]]},
    5: {"lat": 22.2930, "lng": 114.1720, "zoom": 14, "name": "Victoria Harbour & Skyline Kowloon", "poly": [[22.280, 114.155], [22.305, 114.155], [22.305, 114.190], [22.280, 114.190]]},
    6: {"lat": 22.3193, "lng": 114.1694, "zoom": 13, "name": "Topología Urbana & Densidad de Hong Kong", "poly": [[22.290, 114.140], [22.340, 114.140], [22.340, 114.200], [22.290, 114.200]]},
    7: {"lat": 22.3800, "lng": 114.1800, "zoom": 12, "name": "Hong Kong: Parques Rurales & Red de Gobernanza", "poly": [[22.350, 114.100], [22.420, 114.100], [22.420, 114.240], [22.350, 114.240]]},
    8: {"lat": 22.5431, "lng": 114.0579, "zoom": 12, "name": "Shenzhen (Centro Metropolitano)", "poly": [[22.510, 113.900], [22.580, 113.900], [22.580, 114.150], [22.510, 114.150]]},
    9: {"lat": 22.5431, "lng": 114.0579, "zoom": 12, "name": "Zona Económica Especial de Shenzhen (1980)", "poly": [[22.500, 113.880], [22.570, 113.880], [22.570, 114.180], [22.500, 114.180]]},
    10: {"lat": 22.5400, "lng": 114.0500, "zoom": 13, "name": "Transformación Rural a Metrópolis (Shenzhen)", "poly": [[22.520, 114.020], [22.560, 114.020], [22.560, 114.080], [22.520, 114.080]]},
    11: {"lat": 22.5362, "lng": 114.0545, "zoom": 15, "name": "Futian CBD & Rascacielos Ping An", "poly": [[22.528, 114.045], [22.545, 114.045], [22.545, 114.065], [22.528, 114.065]]},
    12: {"lat": 22.5362, "lng": 114.0545, "zoom": 15, "name": "Núcleo Corporativo & Bolsa ChiNext (Futian)", "poly": [[22.528, 114.045], [22.545, 114.045], [22.545, 114.065], [22.528, 114.065]]},
    13: {"lat": 22.5408, "lng": 113.9497, "zoom": 13, "name": "Nanshan Hi-Tech District & Clústeres Tecnológicos", "poly": [[22.520, 113.920], [22.560, 113.920], [22.560, 113.970], [22.520, 113.970]]},
    14: {"lat": 22.4500, "lng": 114.0800, "zoom": 11, "name": "Frontera y Sutura Hong Kong - Shenzhen", "poly": [[22.400, 113.980], [22.550, 113.980], [22.550, 114.200], [22.400, 114.200]]},
    15: {"lat": 22.4200, "lng": 114.1000, "zoom": 11, "name": "Comparación de Modelos: Common Law vs. Estado-Corporativo", "poly": [[22.300, 113.950], [22.560, 113.950], [22.560, 114.250], [22.300, 114.250]]},
    16: {"lat": 22.3900, "lng": 114.1400, "zoom": 12, "name": "Parques Rurales de Hong Kong (40% Protegido)", "poly": [[22.360, 114.110], [22.420, 114.110], [22.420, 114.180], [22.360, 114.180]]},
    17: {"lat": 22.3280, "lng": 114.1620, "zoom": 16, "name": "Sham Shui Po & Viviendas Subdivididas (Cage Homes)", "poly": [[22.322, 114.156], [22.334, 114.156], [22.334, 114.168], [22.322, 114.168]]},
    18: {"lat": 22.2800, "lng": 114.1588, "zoom": 15, "name": "Central District: Sistema de Arrendamiento Leasehold", "poly": [[22.274, 114.152], [22.286, 114.152], [22.286, 114.165], [22.274, 114.165]]},
    19: {"lat": 22.2920, "lng": 114.2050, "zoom": 14, "name": "Sede ICAC & Estabilidad Institucional", "poly": [[22.285, 114.195], [22.298, 114.195], [22.298, 114.215], [22.285, 114.215]]},
    20: {"lat": 22.4280, "lng": 114.2120, "zoom": 15, "name": "Hong Kong Science Park (Pak Shek Kok)", "poly": [[22.422, 114.205], [22.435, 114.205], [22.435, 114.220], [22.422, 114.220]]},
    21: {"lat": 22.2855, "lng": 114.1577, "zoom": 14, "name": "Bolsa HKEX & Distrito Financiero Admiralty", "poly": [[22.278, 114.150], [22.290, 114.150], [22.290, 114.168], [22.278, 114.168]]},
    22: {"lat": 22.4862, "lng": 114.0378, "zoom": 14, "name": "Reserva Natural de Mai Po & Sitio Ramsar", "poly": [[22.475, 114.025], [22.498, 114.025], [22.498, 114.050], [22.475, 114.050]]},
    23: {"lat": 22.3193, "lng": 114.1694, "zoom": 13, "name": "Kowloon & Hong Kong Island: Demografía & Fiscalidad", "poly": [[22.290, 114.140], [22.340, 114.140], [22.340, 114.200], [22.290, 114.200]]},
    24: {"lat": 22.2988, "lng": 113.9877, "zoom": 13, "name": "Proyecto Lantau Tomorrow Vision (Reclamación Marina)", "poly": [[22.270, 113.940], [22.320, 113.940], [22.320, 114.040], [22.270, 114.040]]},
    25: {"lat": 22.4280, "lng": 114.2120, "zoom": 15, "name": "Ecosistema I+D: Parque Científico HKSTP", "poly": [[22.422, 114.205], [22.435, 114.205], [22.435, 114.220], [22.422, 114.220]]},
    26: {"lat": 22.5408, "lng": 113.9497, "zoom": 14, "name": "Nanshan: Intensidad de I+D (6.46% del PIB)", "poly": [[22.525, 113.930], [22.555, 113.930], [22.555, 113.965], [22.525, 113.965]]},
    27: {"lat": 22.5408, "lng": 113.9497, "zoom": 13, "name": "Shenzhen: 20 Clústeres Industriales Estratégicos", "poly": [[22.510, 113.900], [22.570, 113.900], [22.570, 113.980], [22.510, 113.980]]},
    28: {"lat": 22.5484, "lng": 114.0863, "zoom": 16, "name": "Distrito Electrónico de Huaqiangbei", "poly": [[22.543, 114.080], [22.554, 114.080], [22.554, 114.093], [22.543, 114.093]]},
    29: {"lat": 22.5328, "lng": 113.9355, "zoom": 15, "name": "Sedes Corporativas: Tencent, DJI, Huawei & BYD", "poly": [[22.525, 113.925], [22.540, 113.925], [22.540, 113.945], [22.525, 113.945]]},
    30: {"lat": 22.5362, "lng": 114.0545, "zoom": 15, "name": "Bolsa de Valores ChiNext (Futian)", "poly": [[22.530, 114.048], [22.542, 114.048], [22.542, 114.060], [22.530, 114.060]]},
    31: {"lat": 22.5385, "lng": 113.9685, "zoom": 16, "name": "Aldeas Urbanas (Baishizhou & Gangxia)", "poly": [[22.532, 113.960], [22.545, 113.960], [22.545, 113.977], [22.532, 113.977]]},
    32: {"lat": 22.5500, "lng": 114.0200, "zoom": 13, "name": "Shenzhen: Población Flotante & Régimen Hukou", "poly": [[22.520, 113.980], [22.580, 113.980], [22.580, 114.060], [22.520, 114.060]]},
    33: {"lat": 22.5431, "lng": 114.0579, "zoom": 14, "name": "Reforma del Suelo Urbano de 2013 (Shenzhen)", "poly": [[22.530, 114.040], [22.555, 114.040], [22.555, 114.075], [22.530, 114.075]]},
    34: {"lat": 22.5431, "lng": 114.0579, "zoom": 14, "name": "Gobernanza Estatal-Corporativa & SASAC", "poly": [[22.530, 114.040], [22.555, 114.040], [22.555, 114.075], [22.530, 114.075]]},
    35: {"lat": 22.5200, "lng": 114.0300, "zoom": 14, "name": "Programa Sponge City (Ciudad Esponja Futian)", "poly": [[22.505, 114.010], [22.535, 114.010], [22.535, 114.050], [22.505, 114.050]]},
    36: {"lat": 22.5238, "lng": 114.0135, "zoom": 15, "name": "Reserva Natural de Manglares de Futian", "poly": [[22.518, 114.005], [22.530, 114.005], [22.530, 114.025], [22.518, 114.025]]},
    37: {"lat": 22.5100, "lng": 113.9500, "zoom": 13, "name": "Litoral de la Bahía de Shenzhen & Riesgo Costero", "poly": [[22.485, 113.920], [22.535, 113.920], [22.535, 113.980], [22.485, 113.980]]},
    38: {"lat": 22.5312, "lng": 113.8967, "zoom": 14, "name": "Zona de Cooperación Qianhai (ZEE Especial)", "poly": [[22.515, 113.880], [22.545, 113.880], [22.545, 113.915], [22.515, 113.915]]},
    39: {"lat": 22.5158, "lng": 114.0754, "zoom": 15, "name": "Lok Ma Chau Loop (Parque HSITP Transfronterizo)", "poly": [[22.508, 114.065], [22.522, 114.065], [22.522, 114.085], [22.508, 114.085]]},
    40: {"lat": 22.7500, "lng": 114.2000, "zoom": 11, "name": "Sistema de Trasvase Dongjiang (83 km Acueducto)", "poly": [[22.650, 114.100], [22.850, 114.100], [22.850, 114.300], [22.650, 114.300]]},
    41: {"lat": 22.5980, "lng": 114.5427, "zoom": 14, "name": "Central Nuclear de Daya Bay (Península de Dapeng)", "poly": [[22.585, 114.530], [22.610, 114.530], [22.610, 114.555], [22.585, 114.555]]},
    42: {"lat": 22.5180, "lng": 114.0700, "zoom": 13, "name": "Conexión de Metro y Puntos de Control Transfronterizos", "poly": [[22.505, 114.050], [22.530, 114.050], [22.530, 114.090], [22.505, 114.090]]},
    43: {"lat": 22.5158, "lng": 114.0754, "zoom": 14, "name": "Blueprint de Innovación y Tecnología 2022", "poly": [[22.505, 114.060], [22.525, 114.060], [22.525, 114.090], [22.505, 114.090]]},
    44: {"lat": 22.3500, "lng": 113.8500, "zoom": 9, "name": "Área de la Gran Bahía (Guangdong-Hong Kong-Macao)", "poly": [[21.800, 113.200], [23.100, 113.200], [23.100, 114.600], [21.800, 114.600]]},
    45: {"lat": 22.8000, "lng": 114.3000, "zoom": 10, "name": "Estrés Hídrico y Cuenca del Río Dongjiang (2021)", "poly": [[22.600, 114.000], [23.000, 114.000], [23.000, 114.500], [22.600, 114.500]]},
    46: {"lat": 22.4500, "lng": 114.0500, "zoom": 11, "name": "Simbiosis Territorial: Hong Kong - Shenzhen", "poly": [[22.350, 113.950], [22.550, 113.950], [22.550, 114.150], [22.350, 114.150]]},
    47: {"lat": 22.4500, "lng": 114.0500, "zoom": 11, "name": "Red Territorial Integrada de la Gran Bahía", "poly": [[22.350, 113.950], [22.550, 113.950], [22.550, 114.150], [22.350, 114.150]]},
    48: {"lat": 37.6675, "lng": 32.8283, "zoom": 16, "name": "Çatalhöyük (Konya, Turquía) — Malla Celular 7500 a.C.", "poly": [[37.663, 32.823], [37.672, 32.823], [37.672, 32.834], [37.663, 32.834]]},
    49: {"lat": 37.6675, "lng": 32.8283, "zoom": 17, "name": "Çatalhöyük: Cero Calles & Circulación por Techos", "poly": [[37.665, 32.825], [37.670, 32.825], [37.670, 32.832], [37.665, 32.832]]},
    50: {"lat": 37.6675, "lng": 32.8283, "zoom": 16, "name": "Çatalhöyük: Autoorganización Horizontal P2P", "poly": [[37.663, 32.823], [37.672, 32.823], [37.672, 32.834], [37.663, 32.834]]},
    51: {"lat": 37.6675, "lng": 32.8283, "zoom": 16, "name": "Çatalhöyük: Ausencia de Monumentos & Palacios", "poly": [[37.663, 32.823], [37.672, 32.823], [37.672, 32.834], [37.663, 32.834]]},
    52: {"lat": 37.6675, "lng": 32.8283, "zoom": 17, "name": "Çatalhöyük: Estructura Doméstica Continua", "poly": [[37.665, 32.825], [37.670, 32.825], [37.670, 32.832], [37.665, 32.832]]},
    53: {"lat": 37.6675, "lng": 32.8283, "zoom": 16, "name": "Çatalhöyük: Topología Sin Jerarquía Espacial", "poly": [[37.663, 32.823], [37.672, 32.823], [37.672, 32.834], [37.663, 32.834]]},
    54: {"lat": 37.6675, "lng": 32.8283, "zoom": 16, "name": "Çatalhöyük: Resiliencia Arqueológica", "poly": [[37.663, 32.823], [37.672, 32.823], [37.672, 32.834], [37.663, 32.834]]},
    55: {"lat": 37.6675, "lng": 32.8283, "zoom": 15, "name": "Lección de Çatalhöyük para la Metrópolis Contemporánea", "poly": [[37.660, 32.818], [37.675, 32.818], [37.675, 32.838], [37.660, 32.838]]},
    56: {"lat": 4.6293, "lng": -74.1578, "zoom": 16, "name": "Corabastos & Localidad de Kennedy (Bogotá)", "poly": [[4.623, -74.165], [4.636, -74.165], [4.636, -74.150], [4.623, -74.150]]},
    57: {"lat": 4.6338, "lng": -74.1652, "zoom": 16, "name": "Barrio Patio Bonito (Autogestión Comunitaria 1985)", "poly": [[4.628, -74.172], [4.640, -74.172], [4.640, -74.158], [4.628, -74.158]]},
    58: {"lat": 4.6293, "lng": -74.1578, "zoom": 15, "name": "Corabastos Regional (12.000 ton/día de Alimentos)", "poly": [[4.620, -74.168], [4.638, -74.168], [4.638, -74.148], [4.620, -74.148]]},
    59: {"lat": 4.6300, "lng": -74.1550, "zoom": 15, "name": "Concentración Silenciosa del Poder en Nodos Logísticos", "poly": [[4.622, -74.164], [4.638, -74.164], [4.638, -74.146], [4.622, -74.146]]},
    60: {"lat": 4.6293, "lng": -74.1578, "zoom": 16, "name": "La Pregunta Incorrecta: Síntomas vs. Concentración", "poly": [[4.623, -74.165], [4.636, -74.165], [4.636, -74.150], [4.623, -74.150]]},
    61: {"lat": 4.6310, "lng": -74.1600, "zoom": 15, "name": "La Pregunta Correcta: Interfaz Institucional con JAC & POT", "poly": [[4.622, -74.170], [4.640, -74.170], [4.640, -74.150], [4.622, -74.150]]},
    62: {"lat": 22.4200, "lng": 114.1000, "zoom": 10, "name": "Topología Global del Poder Urbano (Síntesis Final)", "poly": [[22.200, 113.800], [22.600, 113.800], [22.600, 114.400], [22.200, 114.400]]}
}

geo_json_str = json.dumps(GEO_DATA)
slide_types_str = json.dumps(SLIDE_TYPES)

clean_html = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Hong Kong & Shenzhen — Topologías de la Densidad y el Poder (Defensa de Maestría)</title>
  
  <!-- Tipografías de Alta Gama -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=DM+Mono:ital,wght@0,300;0,400;0,500;1,400&family=Playfair+Display:ital,wght@0,400;0,600;0,700;1,400;1,600&family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />

  <!-- API de Mapas Interactivos (Leaflet HD) -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

  <style>
    /* ==========================================================================
       ESTÉTICA EDITORIAL PURA (DISEÑO ADAPTATIVO: MAPA SATELITAL / RED REAL)
       ========================================================================== */
    :root {{
      --bg-dark: #080c16;
      --bg-card: #0f172a;
      
      --text-pure: #ffffff;
      --text-silver: #cbd5e1;
      --text-muted: #94a3b8;
      --text-faint: #64748b;
      
      --cat-eco: #f43f5e;
      --cat-urb: #0284c7;
      --cat-env: #10b981;
      --cat-soc: #f59e0b;
      --cat-gov: #8b5cf6;
      
      --accent-hk: #38bdf8;
      --accent-sz: #a78bfa;
      --accent-ct: #fbbf24;
      --accent-bg: #34d399;
      
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
    .arch-header {{
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 56px;
      padding: 0 2.5rem;
      background: rgba(8, 12, 22, 0.95);
      backdrop-filter: blur(14px);
      -webkit-backdrop-filter: blur(14px);
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      z-index: 1000;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}

    .header-left {{
      display: flex;
      align-items: center;
      gap: 1.5rem;
    }}

    .thesis-tag {{
      font-family: var(--font-mono);
      font-size: 0.72rem;
      letter-spacing: 0.14em;
      text-transform: uppercase;
      font-weight: 600;
      color: #ffffff;
      border: 1px solid rgba(255, 255, 255, 0.2);
      padding: 3px 8px;
      border-radius: 4px;
      background: rgba(255, 255, 255, 0.05);
    }}

    .authors-text {{
      font-family: var(--font-body);
      font-size: 0.84rem;
      font-weight: 500;
      color: var(--text-silver);
    }}

    .header-nav {{
      display: flex;
      align-items: center;
      gap: 0.8rem;
    }}

    .slide-select-dropdown {{
      font-family: var(--font-mono);
      font-size: 0.74rem;
      font-weight: 600;
      color: var(--accent-hk);
      background: rgba(56, 189, 248, 0.1);
      border: 1px solid rgba(56, 189, 248, 0.25);
      padding: 4px 12px;
      border-radius: 6px;
      cursor: pointer;
      outline: none;
      max-width: 380px;
    }}

    .slide-select-dropdown option {{
      background: #0d1424;
      color: #ffffff;
    }}

    .nav-arrow-btn {{
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: #ffffff;
      width: 30px;
      height: 30px;
      border-radius: 6px;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.15s ease;
      font-size: 0.85rem;
    }}

    .nav-arrow-btn:hover {{
      background: rgba(255, 255, 255, 0.2);
      border-color: var(--accent-hk);
      color: var(--accent-hk);
    }}

    .progress-bar-line {{
      position: fixed;
      top: 55px;
      left: 0;
      height: 2px;
      width: 0%;
      background: linear-gradient(90deg, #38bdf8, #818cf8, #34d399, #f59e0b);
      z-index: 1001;
      transition: width 0.3s ease-out;
    }}

    /* ==========================================================================
       ESCENARIO PRINCIPAL (100VH)
       ========================================================================== */
    .main-deck-stage {{
      width: 100vw;
      height: 100vh;
      padding: 72px 2.8vw 1.2rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      position: relative;
    }}

    /* Encabezado del Slide */
    .slide-header-strip {{
      margin-bottom: 0.6rem;
      animation: fadeInHead 0.35s ease;
    }}

    @keyframes fadeInHead {{
      from {{ opacity: 0; transform: translateY(-6px); }}
      to {{ opacity: 1; transform: translateY(0); }}
    }}

    .slide-meta-row {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-family: var(--font-mono);
      font-size: 0.72rem;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--text-silver);
      margin-bottom: 0.2rem;
    }}

    .slide-num-pill {{
      font-weight: 600;
      color: var(--accent-hk);
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }}

    .slide-title-text {{
      font-family: var(--font-serif);
      font-size: clamp(1.6rem, 2.3vw, 2.2rem);
      font-weight: 600;
      line-height: 1.15;
      color: #ffffff;
      margin-bottom: 0.2rem;
    }}

    .slide-sub-text {{
      font-family: var(--font-body);
      font-size: clamp(0.9rem, 1.1vw, 1.05rem);
      line-height: 1.4;
      color: var(--text-silver);
      font-weight: 300;
    }}

    /* ==========================================================================
       CONTENEDOR DE CONTENIDO (ADAPTATIVO SEGÚN TIPO DE SLIDE)
       ========================================================================== */
    .stage-content-container {{
      flex: 1;
      display: flex;
      min-height: 0;
      margin-bottom: 0.4rem;
      position: relative;
    }}

    /* MODO 1: RED SISTÉMICA COMPLETA HERO (SLIDE 7, 13, 25, 47, etc.) */
    .hero-network-frame {{
      width: 100%;
      height: 100%;
      background: #0f172a;
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 14px;
      overflow: hidden;
      display: none;
      flex-direction: column;
      box-shadow: 0 16px 40px -10px rgba(0, 0, 0, 0.5);
      position: relative;
    }}

    .hero-network-frame.active {{
      display: flex;
    }}

    .hero-network-img-box {{
      flex: 1;
      width: 100%;
      height: 100%;
      background: #0b0f19;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
      cursor: zoom-in;
      overflow: hidden;
      padding: 1rem;
    }}

    .hero-network-img {{
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
      transition: transform 0.3s ease;
    }}

    .hero-network-img-box:hover .hero-network-img {{
      transform: scale(1.02);
    }}

    /* MODO 2: GRID DÚO (MAPA SATELITAL VIVO O LÁMINA + PANEL ANALÍTICO) */
    .split-panels-grid {{
      width: 100%;
      height: 100%;
      display: grid;
      grid-template-columns: 1.15fr 1fr;
      gap: 1.4rem;
      min-height: 0;
    }}

    /* Frame del Mapa Satelital HD */
    .map-panel-frame {{
      background: #0f172a;
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 14px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      box-shadow: 0 16px 40px -10px rgba(0, 0, 0, 0.5);
      position: relative;
    }}

    .panel-top-bar {{
      padding: 0.55rem 1rem;
      background: rgba(15, 23, 42, 0.95);
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.6rem;
      z-index: 50;
    }}

    .panel-label {{
      font-family: var(--font-mono);
      font-size: 0.72rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--accent-hk);
      display: flex;
      align-items: center;
      gap: 0.45rem;
    }}

    .pulse-radar-dot {{
      width: 8px;
      height: 8px;
      background: var(--accent-hk);
      border-radius: 50%;
      box-shadow: 0 0 0 0 rgba(56, 189, 248, 0.7);
      animation: pulseRadar 1.8s infinite;
    }}

    @keyframes pulseRadar {{
      0% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(56, 189, 248, 0.7); }}
      70% {{ transform: scale(1); box-shadow: 0 0 0 8px rgba(56, 189, 248, 0); }}
      100% {{ transform: scale(0.95); box-shadow: 0 0 0 0 rgba(56, 189, 248, 0); }}
    }}

    .panel-mode-toggles {{
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }}

    .mode-btn {{
      font-family: var(--font-mono);
      font-size: 0.66rem;
      font-weight: 600;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      padding: 3px 8px;
      border-radius: 4px;
      background: rgba(255, 255, 255, 0.07);
      border: 1px solid rgba(255, 255, 255, 0.15);
      color: var(--text-silver);
      cursor: pointer;
      transition: all 0.15s ease;
    }}

    .mode-btn:hover {{
      background: rgba(255, 255, 255, 0.18);
      color: #ffffff;
      border-color: var(--accent-hk);
    }}

    .mode-btn.active {{
      background: var(--accent-hk);
      color: #0b0f19;
      border-color: var(--accent-hk);
    }}

    /* Mapa Leaflet */
    .leaflet-map-box {{
      flex: 1;
      width: 100%;
      height: 100%;
      min-height: 260px;
      background: #090d16;
      position: relative;
    }}

    #liveMap {{
      width: 100%;
      height: 100%;
      background: #090d16;
    }}

    .static-slide-box {{
      position: absolute;
      inset: 41px 0 0 0;
      background: #090d16;
      display: none;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      z-index: 40;
    }}

    .static-slide-box.active {{ display: flex; }}

    .static-slide-box img {{
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
      cursor: zoom-in;
    }}

    .geo-telemetry-badge {{
      position: absolute;
      bottom: 10px;
      left: 10px;
      background: rgba(11, 15, 25, 0.88);
      backdrop-filter: blur(8px);
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 6px;
      padding: 5px 10px;
      font-family: var(--font-mono);
      font-size: 0.68rem;
      color: var(--text-silver);
      z-index: 1000;
      pointer-events: none;
    }}

    .geo-telemetry-badge span {{
      color: var(--accent-hk);
      font-weight: 600;
    }}

    /* Panel Derecho: Matriz / Análisis Territorial */
    .analysis-panel-frame {{
      background: rgba(15, 23, 42, 0.85);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 14px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 16px 40px -10px rgba(0, 0, 0, 0.5);
      padding: 1.25rem 1.4rem;
    }}

    .analysis-card-title {{
      font-family: var(--font-mono);
      font-size: 0.76rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: var(--accent-hk);
      margin-bottom: 0.4rem;
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }}

    .analysis-body-content {{
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: center;
      gap: 1rem;
    }}

    .metrics-grid-2x2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 0.8rem;
    }}

    .metric-data-card {{
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid rgba(255, 255, 255, 0.09);
      border-radius: 8px;
      padding: 0.75rem 0.9rem;
    }}

    .metric-data-val {{
      font-family: var(--font-sans);
      font-size: 1.3rem;
      font-weight: 700;
      color: #ffffff;
      line-height: 1.1;
      margin-bottom: 2px;
    }}

    .metric-data-lbl {{
      font-family: var(--font-mono);
      font-size: 0.66rem;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: var(--text-muted);
    }}

    .quote-callout-box {{
      background: rgba(56, 189, 248, 0.06);
      border-left: 3px solid var(--accent-hk);
      padding: 0.8rem 1rem;
      border-radius: 0 8px 8px 0;
      font-family: var(--font-body);
      font-size: 0.84rem;
      line-height: 1.5;
      color: var(--text-silver);
      font-style: italic;
    }}

    /* ==========================================================================
       BARRA INFERIOR
       ========================================================================== */
    .footer-control-bar {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
      padding-top: 0.4rem;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      font-family: var(--font-mono);
      font-size: 0.72rem;
    }}

    .legend-chips-group {{
      display: flex;
      align-items: center;
      gap: 0.7rem;
    }}

    .legend-mini-chip {{
      font-size: 0.65rem;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: var(--text-silver);
      display: flex;
      align-items: center;
      gap: 5px;
    }}

    .legend-mini-chip .dot {{
      width: 6px;
      height: 6px;
      border-radius: 50%;
    }}

    .next-teaser-btn {{
      color: rgba(255, 255, 255, 0.6);
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-weight: 600;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      transition: all 0.15s ease;
    }}

    .next-teaser-btn:hover {{
      color: var(--accent-hk);
      transform: translateX(3px);
    }}

    .next-teaser-btn::after {{
      content: '→';
      font-size: 0.9rem;
    }}

    /* Modal Lightbox */
    .lightbox-modal {{
      position: fixed;
      inset: 0;
      background: rgba(8, 12, 22, 0.94);
      backdrop-filter: blur(12px);
      z-index: 2000;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 2rem;
    }}

    .lightbox-modal.active {{ display: flex; }}

    .lightbox-box {{
      position: relative;
      max-width: 92vw;
      max-height: 90vh;
      background: #0f172a;
      border: 1px solid rgba(255, 255, 255, 0.2);
      border-radius: 12px;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }}

    .lightbox-header {{
      padding: 0.65rem 1.2rem;
      background: #1e293b;
      display: flex;
      align-items: center;
      justify-content: space-between;
      font-family: var(--font-mono);
      font-size: 0.78rem;
    }}

    .lightbox-box img {{
      max-width: 100%;
      max-height: calc(88vh - 50px);
      object-fit: contain;
    }}

    .lightbox-close {{
      background: transparent;
      border: none;
      color: #ffffff;
      font-size: 1.2rem;
      cursor: pointer;
    }}
  </style>
</head>
<body>

  <!-- Barra de Progreso Superior -->
  <div class="progress-bar-line" id="progressBar"></div>

  <!-- Cabecera Superior -->
  <header class="arch-header">
    <div class="header-left">
      <span class="thesis-tag">DEFENSA DE MAESTRÍA</span>
      <span class="authors-text">Hong Kong & Shenzhen: Topologías del Poder</span>
    </div>
    <div class="header-nav">
      <span style="font-family: var(--font-mono); font-size: 0.72rem; color: var(--text-silver);">Ir a:</span>
      <select id="slideSelector" class="slide-select-dropdown" onchange="jumpToSlide(parseInt(this.value))"></select>
      <button class="nav-arrow-btn" onclick="prevSlide()" title="Anterior (←)">←</button>
      <button class="nav-arrow-btn" onclick="nextSlide()" title="Siguiente (→)">→</button>
    </div>
  </header>

  <!-- Escenario Principal -->
  <main class="main-deck-stage">
    
    <!-- Encabezado del Slide Actual -->
    <div class="slide-header-strip">
      <div class="slide-meta-row">
        <div class="slide-num-pill" id="slidePill">
          <span>●</span> SLIDE 01
        </div>
        <div id="slideCategory">01. INTRODUCCIÓN</div>
      </div>
      <h1 class="slide-title-text" id="slideTitle">Hong Kong & Shenzhen</h1>
      <p class="slide-sub-text" id="slideSubtitle">¿Qué modelo de ciudad es mejor: el de Hong Kong o el de Shenzhen?</p>
    </div>

    <!-- Contenedor Dinámico Adaptativo -->
    <div class="stage-content-container">
      
      <!-- MODO 1: RED SISTÉMICA COMPLETA DE INVESTIGACIÓN (SLIDE 7, 13, 25, 47, etc.) -->
      <div class="hero-network-frame" id="heroNetworkFrame">
        <div class="panel-top-bar">
          <div class="panel-label">
            <span class="pulse-radar-dot"></span>
            <span id="heroNetworkLabel">RED SISTÉMICA COMPLETA (5 DIMENSIONES)</span>
          </div>
          <div class="panel-mode-toggles">
            <button class="mode-btn active" onclick="openLightbox()">🔍 Inspeccionar en Alta Resolución</button>
          </div>
        </div>
        <div class="hero-network-img-box" onclick="openLightbox()">
          <img id="heroNetworkImg" class="hero-network-img" src="slides/slide_7.png" alt="Red Sistémica Completa" />
        </div>
      </div>

      <!-- MODO 2: GRID DÚO (MAPA SATELITAL VIVO O LÁMINA + MATRIZ ANALÍTICA) -->
      <div class="split-panels-grid" id="splitPanelsGrid">
        
        <!-- Panel Izquierdo: Mapa Satelital HD API / Lámina -->
        <div class="map-panel-frame">
          <div class="panel-top-bar">
            <div class="panel-label">
              <span class="pulse-radar-dot"></span>
              <span id="mapPanelTitle">🛰️ Satélite Vivo (Leaflet HD)</span>
            </div>
            <div class="panel-mode-toggles">
              <button class="mode-btn active" id="btnSatellite" onclick="setMapLayer('satellite')">🛰️ Satélite HD</button>
              <button class="mode-btn" id="btnDark" onclick="setMapLayer('dark')">🌑 Blueprint</button>
              <button class="mode-btn" id="btnSlideImg" onclick="toggleSlideImg()">🖼️ Lámina</button>
              <button class="mode-btn" onclick="recenterMap()" title="Centrar cámara">🎯 Foco</button>
              <button class="mode-btn" onclick="openLightbox()" title="Ampliar">🔍</button>
            </div>
          </div>

          <!-- Mapa Leaflet -->
          <div class="leaflet-map-box">
            <div id="liveMap"></div>
            <div class="geo-telemetry-badge" id="geoBadge">
              Coordenadas: <span id="geoCoords">22.4200° N, 114.1200° E</span> • Foco: <span id="geoTarget">Delta del Río Perla</span>
            </div>
          </div>

          <!-- Lámina Estática Alternativa -->
          <div class="static-slide-box" id="staticSlideBox" onclick="openLightbox()">
            <img id="staticSlideImg" src="slides/slide_1.png" alt="Lámina Arquitectónica" />
          </div>
        </div>

        <!-- Panel Derecho: Matriz / Análisis Territorial -->
        <div class="analysis-panel-frame" id="analysisPanelFrame">
          <div>
            <div class="analysis-card-title">✦ ANÁLISIS ESTRUCTURAL & GOBERNANZA</div>
            <div style="font-family: var(--font-body); font-size: 0.88rem; color: var(--text-silver); line-height: 1.45;" id="analysisSummary">
              Síntesis del modelo urbano, concentración de decisión y balance socioecológico.
            </div>
          </div>

          <div class="analysis-body-content">
            <div class="metrics-grid-2x2" id="metricsGrid">
              <div class="metric-data-card">
                <div class="metric-data-val" id="m1Val">7.5 M</div>
                <div class="metric-data-lbl" id="m1Lbl">Población</div>
              </div>
              <div class="metric-data-card">
                <div class="metric-data-val" id="m2Val">2,755</div>
                <div class="metric-data-lbl" id="m2Lbl">Densidad (Hab/km²)</div>
              </div>
              <div class="metric-data-card">
                <div class="metric-data-val" id="m3Val">90%</div>
                <div class="metric-data-lbl" id="m3Lbl">Transporte Público</div>
              </div>
              <div class="metric-data-card">
                <div class="metric-data-val" id="m4Val">40%</div>
                <div class="metric-data-lbl" id="m4Lbl">Suelo Protegido</div>
              </div>
            </div>

            <div class="quote-callout-box" id="quoteCallout">
              «Pensar la densidad no es contar rascacielos; es comprender la capacidad viva de una sociedad para negociar su propio destino en el espacio.»
            </div>
          </div>

          <div style="font-family: var(--font-mono); font-size: 0.68rem; color: var(--text-faint); display: flex; align-items: center; justify-content: space-between;">
            <span id="footerCapLabel">Investigación de Maestría</span>
            <span>Alejandra Gómez • Ana Casas • Juan Trujillo</span>
          </div>
        </div>

      </div>

    </div>

    <!-- Barra Inferior de Navegación & Leyenda -->
    <div class="footer-control-bar">
      <div class="legend-chips-group">
        <span style="color: var(--text-faint); margin-right: 2px;">Dimensiones:</span>
        <span class="legend-mini-chip"><span class="dot" style="background: var(--cat-eco);"></span> Economía</span>
        <span class="legend-mini-chip"><span class="dot" style="background: var(--cat-urb);"></span> Urbanismo</span>
        <span class="legend-mini-chip"><span class="dot" style="background: var(--cat-env);"></span> Ambiente</span>
        <span class="legend-mini-chip"><span class="dot" style="background: var(--cat-soc);"></span> Sociedad</span>
        <span class="legend-mini-chip"><span class="dot" style="background: var(--cat-gov);"></span> Gobernanza</span>
      </div>

      <div class="next-teaser-btn" id="nextTeaserBtn" onclick="nextSlide()">
        Siguiente: <span>HONG KONG</span>
      </div>
    </div>

  </main>

  <!-- Modal Lightbox -->
  <div class="lightbox-modal" id="lightboxModal" onclick="closeLightbox()">
    <div class="lightbox-box" onclick="event.stopPropagation()">
      <div class="lightbox-header">
        <span id="lightboxTitle">Lámina Visual</span>
        <button class="lightbox-close" onclick="closeLightbox()">✕</button>
      </div>
      <img id="lightboxImg" src="" alt="Lámina Ampliada" />
    </div>
  </div>

  <script>
    // ==========================================================================
    // 1. DATASETS
    // ==========================================================================
{sections_js}

    const GEO_DATA = {geo_json_str};
    const SLIDE_TYPES = {slide_types_str};

    // ==========================================================================
    // 2. INICIALIZACIÓN DEL MAPA SATELITAL LEAFLET HD
    // ==========================================================================
    let map = null;
    let satelliteLayer = null;
    let darkLayer = null;
    let currentGeoPolygon = null;
    let currentRadarMarker = null;

    function initLeafletMap() {{
      map = L.map('liveMap', {{
        center: [22.42, 114.12],
        zoom: 11,
        zoomControl: false,
        attributionControl: false
      }});

      L.control.zoom({{ position: 'topright' }}).addTo(map);

      satelliteLayer = L.tileLayer('https://mt1.google.com/vt/lyrs=y&x={{x}}&y={{y}}&z={{z}}', {{
        maxZoom: 20,
        subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
      }}).addTo(map);

      darkLayer = L.tileLayer('https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
        maxZoom: 20,
        subdomains: 'abcd'
      }});
    }}

    function setMapLayer(mode) {{
      document.getElementById('staticSlideBox').classList.remove('active');
      document.getElementById('btnSlideImg').classList.remove('active');
      document.getElementById('btnSatellite').classList.remove('active');
      document.getElementById('btnDark').classList.remove('active');

      if (mode === 'satellite') {{
        if (map.hasLayer(darkLayer)) map.removeLayer(darkLayer);
        if (!map.hasLayer(satelliteLayer)) satelliteLayer.addTo(map);
        document.getElementById('btnSatellite').classList.add('active');
        document.getElementById('mapPanelTitle').textContent = '🛰️ Satélite Vivo (Leaflet HD)';
      }} else if (mode === 'dark') {{
        if (map.hasLayer(satelliteLayer)) map.removeLayer(satelliteLayer);
        if (!map.hasLayer(darkLayer)) darkLayer.addTo(map);
        document.getElementById('btnDark').classList.add('active');
        document.getElementById('mapPanelTitle').textContent = '🌑 Blueprint Arquitectónico';
      }}
      setTimeout(() => map && map.invalidateSize(), 100);
    }}

    function toggleSlideImg() {{
      const box = document.getElementById('staticSlideBox');
      const isVisible = box.classList.contains('active');
      if (isVisible) {{
        box.classList.remove('active');
        document.getElementById('btnSlideImg').classList.remove('active');
        document.getElementById('btnSatellite').classList.add('active');
      }} else {{
        box.classList.add('active');
        document.getElementById('btnSlideImg').classList.add('active');
        document.getElementById('btnSatellite').classList.remove('active');
        document.getElementById('btnDark').classList.remove('active');
      }}
    }}

    function updateMapForSlide(slideNum) {{
      const geo = GEO_DATA[slideNum] || GEO_DATA[1];
      document.getElementById('geoCoords').textContent = `${{geo.lat.toFixed(4)}}° N, ${{geo.lng.toFixed(4)}}° E`;
      document.getElementById('geoTarget').textContent = geo.name;

      if (map) {{
        map.flyTo([geo.lat, geo.lng], geo.zoom, {{
          duration: 1.4,
          easeLinearity: 0.25
        }});

        if (currentGeoPolygon) map.removeLayer(currentGeoPolygon);
        if (currentRadarMarker) map.removeLayer(currentRadarMarker);

        if (geo.poly) {{
          currentGeoPolygon = L.polygon(geo.poly, {{
            color: '#38bdf8',
            weight: 2,
            opacity: 0.85,
            fillColor: '#38bdf8',
            fillOpacity: 0.12,
            dashArray: '4, 4'
          }}).addTo(map);
        }}

        const pulseIcon = L.divIcon({{
          className: 'pulse-icon-container',
          html: `<div style="width: 14px; height: 14px; background: #38bdf8; border-radius: 50%; border: 2px solid #ffffff; box-shadow: 0 0 12px #38bdf8;"></div>`,
          iconSize: [14, 14],
          iconAnchor: [7, 7]
        }});

        currentRadarMarker = L.marker([geo.lat, geo.lng], {{ icon: pulseIcon }}).addTo(map);
      }}
    }}

    function recenterMap() {{
      const geo = GEO_DATA[currentSlideNum] || GEO_DATA[1];
      if (map && geo) {{
        map.flyTo([geo.lat, geo.lng], geo.zoom, {{ duration: 1.0 }});
      }}
    }}

    // ==========================================================================
    // 3. NAVEGACIÓN Y RENDERIZADO DINÁMICO
    // ==========================================================================
    let currentSlideNum = 1;

    const slideSelector = document.getElementById('slideSelector');
    const progressBar = document.getElementById('progressBar');
    const slidePill = document.getElementById('slidePill');
    const slideCategory = document.getElementById('slideCategory');
    const slideTitle = document.getElementById('slideTitle');
    const slideSubtitle = document.getElementById('slideSubtitle');
    const staticSlideImg = document.getElementById('staticSlideImg');
    const heroNetworkFrame = document.getElementById('heroNetworkFrame');
    const heroNetworkImg = document.getElementById('heroNetworkImg');
    const heroNetworkLabel = document.getElementById('heroNetworkLabel');
    const splitPanelsGrid = document.getElementById('splitPanelsGrid');
    const nextTeaserBtn = document.getElementById('nextTeaserBtn');

    // Métricas
    const m1Val = document.getElementById('m1Val'), m1Lbl = document.getElementById('m1Lbl');
    const m2Val = document.getElementById('m2Val'), m2Lbl = document.getElementById('m2Lbl');
    const m3Val = document.getElementById('m3Val'), m3Lbl = document.getElementById('m3Lbl');
    const m4Val = document.getElementById('m4Val'), m4Lbl = document.getElementById('m4Lbl');
    const quoteCallout = document.getElementById('quoteCallout');
    const analysisSummary = document.getElementById('analysisSummary');

    function initSelector() {{
      let html = '';
      SECTIONS.forEach(s => {{
        html += `<option value="${{s.num}}">Slide ${{String(s.num).padStart(2, '0')}}: ${{s.title}}</option>`;
      }});
      slideSelector.innerHTML = html;
    }}
    initSelector();

    function updateMetrics(num, sec) {{
      if (num <= 15) {{
        m1Val.textContent = "7.5 M"; m1Lbl.textContent = "Población HK";
        m2Val.textContent = "17.6 M"; m2Lbl.textContent = "Población SZ";
        m3Val.textContent = "90%"; m3Lbl.textContent = "Transp. Público HK";
        m4Val.textContent = "6.46%"; m4Lbl.textContent = "I+D Shenzhen (% PIB)";
        analysisSummary.textContent = "Dilema de dos modelos metropolitanos: la densidad insular financiera bajo Common Law frente al dinamismo experimental manufacturero y tecnológico.";
        quoteCallout.textContent = "«¿Qué modelo de ciudad es mejor: el de Hong Kong o el de Shenzhen? Dos respuestas territoriales a la gobernanza de la densidad.»";
      }} else if (num <= 25) {{
        m1Val.textContent = "40%"; m1Lbl.textContent = "Parques Rurales Protegidos";
        m2Val.textContent = "0.54"; m2Lbl.textContent = "Coeficiente Gini";
        m3Val.textContent = "220k"; m3Lbl.textContent = "Subdivided Cage Homes";
        m4Val.textContent = "80%"; m4Lbl.textContent = "Dependencia Agua Dongjiang";
        analysisSummary.textContent = "Hong Kong: Estructura de suelo leasehold (1997), alta concentración vertical y tensión distributiva entre reservas fiscales e infravivienda.";
        quoteCallout.textContent = "«La hiperdensidad vertical coexiste con un 40% de suelo verde intocable por ley estatutaria colonial.»";
      }} else if (num <= 37) {{
        m1Val.textContent = "6.46%"; m1Lbl.textContent = "Gasto I+D (% PIB)";
        m2Val.textContent = "90%"; m2Lbl.textContent = "I+D Financiado por Empresas";
        m3Val.textContent = "20"; m3Lbl.textContent = "Clústeres Estratégicos";
        m4Val.textContent = "90%"; m4Lbl.textContent = "Hardware Global (Huaqiangbei)";
        analysisSummary.textContent = "Shenzhen: Del modelo Shanzhai a la innovación propia de frontera. Régimen dual de suelo, comités vecinales y aldeas urbanas como Baishizhou.";
        quoteCallout.textContent = "«El modelo estatal-corporativo moviliza capital en ChiNext y articula aldeas urbanas como amortiguador social.»";
      }} else if (num <= 47) {{
        m1Val.textContent = "87 ha"; m1Lbl.textContent = "Lok Ma Chau Loop (HSITP)";
        m2Val.textContent = "83 km"; m2Lbl.textContent = "Acueducto Dongjiang";
        m3Val.textContent = "1994"; m3Lbl.textContent = "Central Nuclear Daya Bay";
        m4Val.textContent = "2021"; m4Lbl.textContent = "Plan Qianhai ZEE";
        analysisSummary.textContent = "Zonas de Sutura: Las infraestructuras críticas compartidas revelan una simbiosis socioecológica irreversible por encima de las fronteras políticas.";
        quoteCallout.textContent = "«La centralización de infraestructuras para ganar eficiencia económica también concentra el riesgo regional.»";
      }} else if (num <= 55) {{
        m1Val.textContent = "7500 a.C."; m1Lbl.textContent = "Antigüedad Malla Neolítica";
        m2Val.textContent = "10.000"; m2Lbl.textContent = "Habitantes";
        m3Val.textContent = "0"; m3Lbl.textContent = "Calles / Palacios";
        m4Val.textContent = "P2P"; m4Lbl.textContent = "Acceso por Techos";
        analysisSummary.textContent = "Çatalhöyük: La primera gran densidad humana demostró que una comunidad masiva puede autoorganizarse sin clases dominantes ni jerarquía espacial.";
        quoteCallout.textContent = "«La densidad celular continua: habitar sin monumentos de poder, donde cada cubierta es el espacio público compartido.»";
      }} else {{
        m1Val.textContent = "12.000"; m1Lbl.textContent = "ton/día Alimentos";
        m2Val.textContent = "6.500"; m2Lbl.textContent = "Locales Comerciales";
        m3Val.textContent = "1985"; m3Lbl.textContent = "Fundación Patio Bonito";
        m4Val.textContent = "Art. 566"; m4Lbl.textContent = "POT Actuaciones Estratégicas";
        analysisSummary.textContent = "Bogotá (Kennedy, Patio Bonito y Corabastos): La concentración silenciosa de capacidad decisoria y la urgencia de interfaces vinculantes con las JAC.";
        quoteCallout.textContent = "«La pregunta no es qué está mal en Corabastos, sino en qué otros nodos territoriales ya ocurrió esa misma concentración silenciosa.»";
      }}
    }}

    function renderSlide(num) {{
      currentSlideNum = num;
      const sec = SECTIONS.find(s => s.num === num) || SECTIONS[0];
      const idx = SECTIONS.indexOf(sec);
      const slideType = SLIDE_TYPES[num] || "map";

      // Progreso y selector
      const progress = ((num) / SECTIONS.length) * 100;
      progressBar.style.width = `${{progress}}%`;
      slideSelector.value = num;

      // Textos
      slidePill.innerHTML = `<span>●</span> SLIDE ${{String(num).padStart(2, '0')}}`;
      slideCategory.textContent = sec.category;
      slideTitle.textContent = sec.title;
      slideSubtitle.textContent = sec.subtitle;
      staticSlideImg.src = `slides/slide_${{num}}.png`;

      // ADAPTACIÓN DE VISTA SEGÚN TIPO DE SLIDE
      if (slideType === "network") {{
        // Slide de Red Completa -> Mostrar solo la red real de investigación en toda la pantalla
        heroNetworkFrame.classList.add('active');
        splitPanelsGrid.style.display = 'none';
        heroNetworkImg.src = `slides/slide_${{num}}.png`;
        heroNetworkLabel.textContent = sec.title.toUpperCase();
      }} else {{
        // Slide de Mapa o Caso -> Mostrar Grid Dúo (Mapa Satelital / Lámina + Matriz Analítica)
        heroNetworkFrame.classList.remove('active');
        splitPanelsGrid.style.display = 'grid';

        if (slideType === "case") {{
          // Activar lámina directamente
          document.getElementById('staticSlideBox').classList.add('active');
          document.getElementById('btnSlideImg').classList.add('active');
          document.getElementById('btnSatellite').classList.remove('active');
          document.getElementById('btnDark').classList.remove('active');
        }} else {{
          // Activar mapa satelital vivo
          document.getElementById('staticSlideBox').classList.remove('active');
          document.getElementById('btnSlideImg').classList.remove('active');
          document.getElementById('btnSatellite').classList.add('active');
          document.getElementById('btnDark').classList.remove('active');
          updateMapForSlide(num);
        }}
      }}

      // Actualizar Métricas
      updateMetrics(num, sec);

      // Teaser Siguiente
      const nextSec = SECTIONS[idx + 1];
      if (nextSec) {{
        nextTeaserBtn.innerHTML = `Siguiente: <span>${{nextSec.title.toUpperCase()}}</span>`;
        nextTeaserBtn.style.display = 'flex';
      }} else {{
        nextTeaserBtn.innerHTML = `<span>FIN DE LA PRESENTACIÓN</span>`;
      }}
    }}

    function jumpToSlide(num) {{
      if (num >= 1 && num <= 62) renderSlide(num);
    }}

    function prevSlide() {{
      if (currentSlideNum > 1) jumpToSlide(currentSlideNum - 1);
    }}

    function nextSlide() {{
      if (currentSlideNum < 62) jumpToSlide(currentSlideNum + 1);
    }}

    function openLightbox() {{
      document.getElementById('lightboxTitle').textContent = `Slide ${{currentSlideNum}}: ${{SECTIONS[currentSlideNum-1].title}}`;
      document.getElementById('lightboxImg').src = `slides/slide_${{currentSlideNum}}.png`;
      document.getElementById('lightboxModal').classList.add('active');
    }}

    function closeLightbox() {{
      document.getElementById('lightboxModal').classList.remove('active');
    }}

    // Teclado
    document.addEventListener('keydown', (e) => {{
      if (document.getElementById('lightboxModal').classList.contains('active')) {{
        if (e.key === 'Escape') closeLightbox();
      }} else {{
        if (e.key === 'ArrowRight' || e.key === 'PageDown' || e.key === ' ') {{
          e.preventDefault();
          nextSlide();
        }} else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {{
          e.preventDefault();
          prevSlide();
        }}
      }}
    }});

    window.addEventListener('DOMContentLoaded', () => {{
      initLeafletMap();
      renderSlide(1);
    }});
  </script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(clean_html)

print("Successfully deployed intelligent adaptive layout: Full research network for network slides, Leaflet Maps API for map slides!")
