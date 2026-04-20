# Scene Patterns — Padrões de Cenas para Vídeos Publicitários

## Estrutura Padrão (10s, 3-4 cenas)

### Padrão A: Problema → Solução (4 cenas)
| # | Duração | Conteúdo | Animação entrada |
|---|---------|----------|-----------------|
| 1 | 2s | Logo + tagline | zoom in + glow |
| 2 | 3s | Problema/dor (3 items) | slide from left |
| 3 | 3s | Solução/features (4-6 cards) | pop in sequencial |
| 4 | 2s | Logo + CTA (site/contato) | fade + scale |

### Padrão B: Direto (3 cenas)
| # | Duração | Conteúdo | Animação entrada |
|---|---------|----------|-----------------|
| 1 | 3s | Headline impactante + logo | flash + reveal |
| 2 | 4s | Features em grid | card pop sequencial |
| 3 | 3s | CTA forte | scale + glow border |

### Padrão C: Números (4 cenas)
| # | Duração | Conteúdo | Animação entrada |
|---|---------|----------|-----------------|
| 1 | 2s | Logo intro | line grow + logo fade |
| 2 | 3s | Headline + subtítulo | fade up |
| 3 | 3s | 3-4 estatísticas (números animados) | scale in + counter |
| 4 | 2s | Logo + site | zoom + glow |

## Efeitos de Background

### Partículas (sempre usar)
```javascript
// 60-80 partículas, tamanho 2-5px, com halos
// Conexões entre partículas próximas (<200px)
// Oscilação de opacidade com sin()
```

### Estrelas Cadentes (opcional)
```javascript
// 4-6 estrelas, spawn aleatório a cada 2-4s
// Rastro com gradiente, 3px largura
// Ângulo ~0.3-0.6 rad
```

### Ondas de Pulso (opcional)
```javascript
// Círculos expandindo do centro a cada 2s
// Raio: 0 → 800px, opacidade: 0.2 → 0
```

### Scanline (sempre usar)
```css
/* Linha horizontal percorrendo a tela verticalmente, 6s ciclo */
background: linear-gradient(90deg, transparent, rgba(182,255,0,0.1), transparent);
animation: scan 6s linear infinite;
```

## Transições entre Cenas

### Flicker (obrigatório)
```javascript
// Flash verde rápido na mudança de cena
// 3 estágios: 0ms (verde), 80ms (transparente), 120ms (verde fraco), 200ms (fim)
```

### Fade (padrão)
```javascript
// opacity 0→1 em 0.6s ease-out
el.style.opacity = '1';
el.style.transition = 'opacity 0.6s ease-out';
```

### Zoom In (impacto)
```javascript
// scale(1.5) → scale(1) em 0.8s
el.style.animation = 'none'; void el.offsetWidth;
el.style.animation = 'fadeInScale 0.8s cubic-bezier(0.16,1,0.3,1) forwards';
```

### Slide from Left (listas)
```javascript
// translateX(-80px) → 0 em 0.6s
el.style.animation = 'slideFromLeft 0.6s cubic-bezier(0.16,1,0.3,1) forwards';
```

## Animações CSS Reference

```css
@keyframes fadeIn { from{opacity:0;transform:translateY(40px)} to{opacity:1;transform:translateY(0)} }
@keyframes fadeInScale { from{opacity:0;transform:scale(0.7)} to{opacity:1;transform:scale(1)} }
@keyframes slideFromLeft { from{opacity:0;transform:translateX(-80px)} to{opacity:1;transform:translateX(0)} }
@keyframes popIn { from{opacity:0;transform:scale(0.8) translateY(30px)} to{opacity:1;transform:scale(1) translateY(0)} }
@keyframes lineGrow { from{width:0} to{width:400px} }
@keyframes glowPulse { 0%,100%{filter:drop-shadow(0 0 80px rgba(R,G,B,0.3))} 50%{filter:drop-shadow(0 0 120px rgba(R,G,B,0.5))} }
```

## Regras de Tipografia

- **Headlines**: 3.5-4rem, font-weight 800-900
- **Subtítulos**: 2-2.5rem, font-weight 300
- **Body**: 1.2-1.8rem, font-weight 400
- **CTA URL**: 3-3.5rem, font-weight 800
- **Letter-spacing**: 0.2-0.4em para taglines uppercase
- **Fonte**: Inter (Google Fonts via `<link>`)

## Paleta de Cores Padrão

Sempre pedir ao usuário. Se não informar, usar:
- **Background**: #050608 (quase preto)
- **Primary**: cor da marca (hex)
- **Text**: #FFFFFF
- **Muted**: rgba(255,255,255,0.5)
- **Accent glow**: primary color com opacidade reduzida
