# Video Creator — Skill para Criação de Vídeos Publicitários HTML→MP4

Gera vídeos publicitários curtos (10s) a partir de HTML/CSS/JS animado, gravando com Playwright (gravação nativa Chromium) e exportando com FFmpeg em MP4.

## Quando Usar
- "Cria um vídeo de 10s sobre [produto/marca]"
- "Gera um comercial em MP4"
- "Faz um vídeo publicitário pra [cliente]"
- Triggers: vídeo, comercial, publicidade, MP4, promotional video, ad

## Fluxo Completo

### 1. Briefing — Perguntar ao Usuário

**SEMPRE fazer essas perguntas antes de criar o HTML.** Se o usuário já respondeu alguma no pedido, não repetir.

#### Perguntas Obrigatórias (fazer se não informado):

1. **Marca/produto** — "Qual a marca/produto? Tem tagline?"
2. **Objetivo** — "Qual o objetivo do vídeo? (ex: divulgar produto, apresentar empresa, promoção, branding)"
3. **Mensagem principal** — "Qual a mensagem principal que precisa aparecer?"
4. **Orientação** — "Portrait (vertical/LED) ou landscape (horizontal)?"
5. **Cores** — "Quais as cores da marca? (hex, ex: #B6FF00)"

#### Perguntas Opcionais (fazer se fizer sentido):

6. **Público-alvo** — "Quem vai ver esse vídeo?"
7. **CTA** — "Qual a chamada pra ação? (ex: acesse o site, entre em contato, baixe o app)"
8. **Logo** — "Tem logo em SVG ou PNG que quer usar?"
9. **Referência visual** — "Tem algum estilo ou referência visual?"
10. **Duração** — "10 segundos tá bom ou precisa de outro tamanho?"

#### Template de pergunta rápida:

> Pra criar o vídeo preciso saber:
> 1. Marca/produto e tagline
> 2. Mensagem principal
> 3. Portrait ou landscape?
> 4. Cor principal da marca (hex)
> 5. Chamada pra ação (CTA)

Se o usuário pediu urgência ou já deu todas as infos, pular direto pra criação.

### 2. Gerar HTML Animado
- Criar arquivo HTML com cenas que avançam via `setVideoFrame(n)`
- **Duração total**: 10 segundos
- **Estrutura típica**: 3-4 cenas (intro → problema/solução → CTA)
- **Efeitos**: partículas, transições suaves, flicker entre cenas
- **Sem áudio**, sem clock, sem "loading"
- **Fontes**: usar `<link>` do Google Fonts (NUNCA `@import`)
- **JavaScript**: vanilla JS puro, sem frameworks
- **Elementos grandes** (para visibilidade em LED)

#### ⚠️ REGRAS DE ANIMAÇÃO (OBRIGATÓRIO)

1. **Frame-based via `setVideoFrame(n)`** — O HTML NÃO pode auto-iniciar animações. Deve definir:

```javascript
// Estado inicial (visível mas parado)
renderFrame(0);

// Chamado pelo gravador para cada frame
window.setVideoFrame = function(n) {
  renderFrame(Math.min(n, totalFrames - 1));
};

// Fallback: startVideo para animação contínua (screensavers)
window.startVideo = function() {
  var cur = 0;
  function loop() {
    if (cur >= totalFrames) return;
    renderFrame(cur);
    cur++;
    setTimeout(loop, 1000 / fps);
  }
  loop();
};
```

2. **Sem `Date.now()` ou `setTimeout`** para timing de animação — tudo baseado no número do frame
3. **Espalhar animações pela duração completa da cena** — não terminar tudo nos primeiros frames
4. **Canvas para efeitos** — partículas, linhas, orbs, etc.
5. **`el.style.animation` inline** para transições (mais confiável que class toggle)

#### Dimensões
| Orientação | Width | Height |
|-----------|-------|--------|
| portrait  | 1080  | 1920   |
| landscape | 1920  | 1080   |

### 3. Converter HTML → MP4 (um comando)

```bash
python3 scripts/html2mp4.py input.html output.mp4 --duration 10 --fps 30 --orientation portrait
```

**O que o script faz:**
1. Abre Chromium headless via Playwright com `record_video_dir` (gravação nativa)
2. Carrega o HTML e espera 500ms (fonts, layout)
3. Avança frames em **tempo real** via `setVideoFrame(n)` — 1 frame por 1/30s
4. Chromium grava viewport nativamente em WebM (~10s para 10s)
5. FFmpeg re-encode para H.264 MP4 com specs exatas (~2s)
6. **Total: ~12s para um vídeo de 10s**

**Argumentos:**
| Flag | Default | Descrição |
|------|---------|-----------|
| `--duration` | 10 | Duração em segundos |
| `--fps` | 30 | FPS do vídeo |
| `--orientation` | portrait | `portrait` ou `landscape` |
| `--crf` | 18 | Qualidade H.264 (18 = visualmente lossless) |

**Specs do MP4 final:**
- Codec: H.264 (libx264)
- Pixel format: yuv420p (8-bit, máxima compatibilidade)
- FPS: 30
- Preset: medium
- Sem áudio
- faststart habilitado

### 4. Entrega
- Salvar MP4 em `media/outbound/` do workspace
- Enviar como MEDIA: attachment

## Pipeline: Método Antigo (fallback)

Se a gravação nativa falhar, usar o método frame-by-frame:

```bash
# 1. Capturar frames
python3 scripts/record_video.py \
  --input video.html --output /tmp/frames/ \
  --duration 10 --fps 30 --orientation portrait

# 2. Encodar
ffmpeg -y -framerate 30 -i /tmp/frames/frame_%04d.png \
  -c:v libx264 -preset medium -crf 18 \
  -pix_fmt yuv420p -movflags +faststart output.mp4

# 3. Limpar
rm -rf /tmp/frames/
```

**⚠️ Lento:** ~70-130s para 10s de vídeo (captura frame-by-frame)

## Arquivos da Skill

```
skills/video-creator/
├── SKILL.md                  # Este arquivo
├── scripts/
│   ├── html2mp4.py           # Pipeline rápido (nativo, ~12s)
│   └── record_video.py       # Fallback frame-by-frame (~120s)
├── templates/                # (futuro) Templates HTML base
└── references/
    └── scene-patterns.md     # Padrões de cenas e animações
```

## Regras Importantes

1. **NUNCA usar `@import` para fonts** — bloqueia renderização. Usar `<link>`.
2. **Frame-based (`setVideoFrame`)** — animações respondem ao frame number, nunca a `Date.now()`/`setTimeout`
3. **HTML não auto-inicia** — espera `setVideoFrame()` do gravador
4. **Visibility + Opacity** para mostrar/esconder cenas, não `display:none`
5. **Sem áudio** nos vídeos
6. **Logo em SVG inline** quando possível (melhor qualidade)
7. **Cores sempre em hex** (#B6FF00), não nomes
8. **Cada vídeo é único** — não reutilizar templates sem customização
9. **Duração padrão**: 10 segundos
10. **Sem loop** no vídeo — cenas preenchem a duração exata

## Dependências

- **Playwright**: v1.58+ (Chromium headless com `record_video_dir`)
- **FFmpeg**: v6.1+ (com libx264)
- **Python 3.12+**
- **Google Fonts**: via CDN

## Troubleshooting

| Problema | Solução |
|----------|---------|
| HTML estático/sem animação | Verificar `setVideoFrame()` está definida e renderFrame() funciona |
| Animação rápida demais | Trocar `Date.now()` por `setVideoFrame(n)` — frame-based |
| Animação lenta demais | Espalhar animações pela duração completa da cena |
| Fontes não carregam | Trocar `@import` por `<link>`, adicionar wait de 500ms |
| Vídeo preto/sem conteúdo | HTML está esperando signal — verificar `setVideoFrame`/`startVideo` |
| Chrome crash | Adicionar `--disable-gpu --no-sandbox --disable-dev-shm-usage` |
| WebM corrompido | Fechar context antes de acessar video.path() |
| MP4 sem playback | Verificar `-pix_fmt yuv420p` e `-movflags +faststart` |
