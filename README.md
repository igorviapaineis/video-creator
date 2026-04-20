# 🎬 Video Creator

Skill para criar vídeos publicitários curtos (10s) a partir de HTML/CSS/JS animado, exportando em MP4 via Playwright + FFmpeg.

## Como Funciona

1. **Briefing** — coleta infos da marca, mensagem, cores, orientação
2. **HTML Animado** — gera página com animações frame-based (`setVideoFrame`)
3. **Gravação Nativa** — Playwright grava viewport do Chromium em tempo real (~12s)
4. **Exporta MP4** — FFmpeg re-encode em H.264, specs exatas

## Pipeline Rápido

```bash
python3 scripts/html2mp4.py input.html output.mp4 --duration 10 --fps 30 --orientation portrait
```

**10s de vídeo em ~12s de processamento.**

## Specs do MP4

| Parâmetro | Valor |
|-----------|-------|
| Codec | H.264 (libx264) |
| Resolução | 1080x1920 (portrait) ou 1920x1080 (landscape) |
| FPS | 30 |
| Pixel format | yuv420p (8-bit) |
| Qualidade | CRF 18 (visualmente lossless) |
| Áudio | Sem áudio |

## Estrutura

```
video-creator/
├── SKILL.md                  # Documentação completa da skill
├── scripts/
│   ├── html2mp4.py           # Pipeline rápido (nativo, ~12s)
│   └── record_video.py       # Fallback frame-by-frame
└── references/
    └── scene-patterns.md     # Padrões de cenas e animações
```

## Dependências

- **Playwright** v1.58+ (com Chromium)
- **FFmpeg** v6.1+ (com libx264)
- **Python 3.12+**

## Instalação

```bash
# Clone
git clone https://github.com/igorviapaineis/video-creator.git

# Instale dependências
pip install playwright
playwright install chromium
sudo apt install ffmpeg
```

## Licença

MIT
