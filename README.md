# 中良工業 TLC 介紹：一層一層

中良工業（Tiong Liong Industrial, TLC）的 30 秒介紹影片與互動介紹網頁。

| 檔案 | 說明 |
|---|---|
| `中良工業_30s.mp4` | 30 秒影片，1920×1080、30fps、含配樂（約 21MB） |
| `中良工業_30s_封面.jpg` | 影片封面，可當 LinkedIn 縮圖 |
| `中良工業_互動介紹.html` | 互動網頁，需與 mp4 放在同一資料夾；字型從 Google Fonts 載入 |
| `TLC_logo_向量版.svg` | 從 377px 原圖重建的向量 Logo（淺色底） |
| `TLC_logo_向量版_深色底用.svg` | 同上，文字改白色，深色底使用 |

## 影片段落

| 時間 | 內容 |
|---|---|
| 0:00 | 開場：一雙登山靴、一個背包、一副手套，答案藏在同一層材料裡 |
| 0:04 | 品牌：Logo 拼合，永續・創新・性能 |
| 0:08 | 核心工藝：織造、染整、機能處理與塗佈、貼合 |
| 0:14 | 複合材料：Coprime®、CORDURA®、ARIAPRENE®、3M™ Thinsulate™、生質防水膜；泡棉回彈 |
| 0:20 | 4 國布局與 ESG（Higg FEM、ZDHC、GHG、GRS） |
| 0:26 | 結語：一層一層，成為品牌最堅實的後盾 |

## 互動網頁區塊

3D 物理布料首頁、章節式影片播放器、捲動驅動的工藝流程、可旋轉拆解的 3D 材料疊層、ARIAPRENE® 泡棉物理實驗室（按壓／衝擊／循環／淋水，閉孔對開孔）、亞洲據點地圖、ESG 與 Pasont 循環案例。

## 對外使用前請確認

- 印尼標示為「布局中」，尚非生產據點。
- 越南只標到國家層級；中國標示福清、中山兩廠。
- Logo 為向量重建版，正式使用建議換成設計公司原始檔。
- 配樂為程式合成，正式投放前請先試聽。
- Pasont 案例已取得對方同意，但相關 LinkedIn 文章尚未發布。
- 泡棉實驗室的數值為示意模擬，非實驗量測。

## 重新產出（`build/`）

需要 Python 3（numpy、Pillow、playwright）、Node.js、ffmpeg。

```bash
cd build
npm install                 # d3-geo、topojson-client、world-atlas（地圖點陣用）
python gen_logo.py          # 產生 logo_parts.json 與向量 Logo
node mapdots.js             # 產生 mapdots.json
python build_film.py        # film.src.html → film.html
python music.py             # 合成 music.wav
python render.py            # 以 60fps 擷取 1800 格到 frames/
```

合成影片（60fps 擷取，兩格混合成帶動態模糊的 30fps）：

```bash
ffmpeg -framerate 60 -i frames/f%05d.png -i music.wav -filter_complex "[0:v]tmix=frames=2:weights='1 1',fps=30,format=yuv420p[v]" -map "[v]" -map 1:a -c:v libx264 -preset slow -crf 17 -movflags +faststart -c:a aac -b:a 192k -shortest ../中良工業_30s.mp4
```

互動網頁：改 `site.src.html` 後執行 `python build_site.py`（腳本內的 Pasont 照片與輸出路徑為本機絕對路徑）。

預覽影片某一秒：用瀏覽器開 `build/film.html?t=12`；不帶參數則循環播放。
