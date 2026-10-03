# 中良工業 TLC：一層一層 · Tiong Liong Industrial: Layer by Layer

**線上看 / Live:** https://sugimotofang-spec.github.io/tlc-intro/ （中文 `?lang=zh` · English `?lang=en`）

中良工業（Tiong Liong Industrial, TLC）的 30 秒介紹影片與互動介紹網頁，中英雙語。
A 30-second brand film and an interactive site for Tiong Liong Industrial (TLC), in Traditional Chinese and English.

| 檔案 File | 說明 Description |
|---|---|
| `index.html` | 互動網頁，右上角切換「中 / EN」，預設依瀏覽器語言 · Interactive site with a 中 / EN toggle (defaults to browser language) |
| `media/tlc-intro-30s-zh.mp4` | 中文版影片 1080p 30fps · Chinese film |
| `media/tlc-intro-30s-en.mp4` | 英文版影片 1080p 30fps · English film |
| `media/poster-*.jpg` | 影片封面 · Video posters |
| `logo/tlc-logo.svg` · `logo/tlc-logo-dark.svg` | 向量 Logo（淺色底／深色底）· Vector logo for light / dark backgrounds |

## 影片段落 · Film chapters

| 時間 | 中文 | English |
|---|---|---|
| 0:00 | 開場：答案藏在同一層材料裡 | Hook: the layer inside them |
| 0:04 | 品牌：永續・創新・性能 | Brand: Sustainability · Innovation · Performance |
| 0:08 | 四道核心工藝：織造、染整、機能處理與塗佈、貼合 | Four core techniques |
| 0:14 | 工程化複合材料與泡棉回彈 | The Engineered Package · one physics question |
| 0:20 | 4 國布局與 ESG | Four countries, one governance standard |
| 0:26 | 結語 | Layer by layer |

## 互動網頁 · Interactive site

3D 物理布料首頁 · 章節式影片播放器 · 捲動驅動的工藝流程 · 可旋轉拆解的 3D 材料疊層 · ARIAPRENE® 泡棉物理實驗室（按壓／衝擊／循環／淋水，閉孔對開孔）· 亞洲據點地圖 · ESG 與 Pasont 循環案例。

Verlet-cloth hero · chaptered video player · scroll-scrubbed process line · rotatable 3D layer explorer · ARIAPRENE® foam lab (press / impact / cycle / rain, closed- vs open-cell) · Asia footprint map · ESG and the Pasont circular story.

泡棉實驗室為示意模擬，數值非實驗量測；材料疊構為示意，實際組合依產品規格而定。
The foam lab is an illustrative simulation, not test data; the stack-up is illustrative and actual constructions vary by specification.

## 重新產出 · Rebuild（`build/`）

需要 Python 3（numpy、Pillow、playwright）、Node.js、ffmpeg。

```bash
cd build
npm install                 # d3-geo, topojson-client, world-atlas
python gen_logo.py          # logo_parts.json + vector logo
node mapdots.js             # mapdots.json
python build_film.py        # film.src.html → film.html
python music.py             # music.wav
python render.py            # 中文影格 → frames/   （加 --en 輸出英文 → frames_en/）
```

合成影片（60fps 擷取，兩格混合成帶動態模糊的 30fps）：

```bash
ffmpeg -framerate 60 -i frames/f%05d.png -i music.wav -filter_complex "[0:v]tmix=frames=2:weights='1 1',fps=30,format=yuv420p[v]" -map "[v]" -map 1:a -c:v libx264 -preset slow -crf 17 -movflags +faststart -c:a aac -b:a 192k -shortest ../media/tlc-intro-30s-zh.mp4
```

互動網頁：修改 `site.src.html` 後執行 `python build_site.py` 產生 `index.html`。
預覽影片某一秒：開 `build/film.html?t=12`（英文 `?t=12&lang=en`）。
