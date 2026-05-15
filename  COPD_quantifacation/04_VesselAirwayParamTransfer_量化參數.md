# VesselAirwayParamTransfer 量化參數整理

`VesselAirwayParamTransfer` 是 COPD 影像定量參數計算的原型資料夾。`COPDClassification` 內也有一份同類程式，主分類實驗實際引用的是 `COPDClassification/VesselAirwayParamTransfer/copd_analyzer.py`。本資料夾適合用來整理公式、參數定義與論文方法。

## 資料夾定位

可支撐論文第三章：

- CT quantitative biomarkers 定義。
- 肺葉體積與肺氣腫比例。
- 血管參數：SVV%、vessel density、PA diameter。
- 氣道參數：WA%、airway-lung ratio。
- 可解釋 feature extraction pipeline。

## 主要檔案

| 檔案 | 用途 |
|---|---|
| `copd_analyzer.py` | 核心 COPD 參數計算程式 |
| `analyze_data.py` | 批次分析入口 |
| `README.md` | 使用方式與資料夾結構 |
| `參數計算說明.md` | 公式與參數說明 |
| `data/seg` | segmentation 輸入位置，目前內容很少或空 |
| `data/airway` | airway segmentation 輸入位置，目前內容很少或空 |
| `data/param` | 參數輸出位置，目前本資料夾未放主結果 |
| `data/report` | 報告輸出位置，目前未放主結果 |

正式 54 例結果主要在 `COPDClassification/NormalDataset/param` 與 `COPDClassification/AbnormalDataset/param`。

## 核心程式架構

`copd_analyzer.py` 主要包含：

- `COPDAnalyzer`：讀取 CT、segmentation、airway，計算各項 biomarker。
- `DirectoryManager`：管理 data、seg、airway、param、report 等路徑。
- `BatchProcessor`：批次處理多個病人。

輸入：

- 原始 CT NIfTI。
- segmentation label NIfTI。
- airway segmentation NIfTI 或相關 airway 結果。

輸出：

- 每位病人的 `*_metrics.json`。
- 可能搭配 summary/report。

## Voxel volume 與體積計算

基本公式：

```text
voxel_volume_mm3 = spacing_x * spacing_y * spacing_z
structure_volume_mm3 = voxel_count * voxel_volume_mm3
structure_volume_ml = structure_volume_mm3 / 1000
```

此公式用於：

- 各肺葉體積。
- 總肺體積。
- 血管體積。
- 氣管/氣道體積。
- 肺氣腫低衰減區體積。

論文中應強調所有體積皆依 NIfTI header spacing 計算，而不是單純 voxel count。

## Label mapping

主分類實驗使用的 label 定義：

| Label | 結構 |
|---:|---|
| 1 | Left superior lobe |
| 2 | Left inferior lobe |
| 3 | Right superior lobe |
| 4 | Right middle lobe |
| 5 | Right inferior lobe |
| 6 | Blood vessel |
| 7 | Trachea |
| 8 | Pulmonary venous system |
| 9 | Pulmonary artery |

總肺 mask 通常由 label 1 到 5 組成。血管與 airway 相關 label 另外計算。

## Emphysema percentage

主實驗使用 emphysema threshold：

```text
emphysema_voxel = lung_voxel and CT_HU < -950
emphysema_percent = emphysema_voxel_count / lung_voxel_count * 100
```

肺葉別 emphysema：

```text
lobar_emphysema_percent = emphysema_voxel_in_lobe / lobe_voxel_count * 100
```

輸出包含：

- total emphysema percent。
- left superior/inferior lobe emphysema。
- right superior/middle/inferior lobe emphysema。

可寫入論文：使用 -950 HU 低衰減區作為 emphysema burden 的 CT biomarker。

## WA% 氣道壁比例

文件定義：

```text
WA% = wall_volume / total_airway_volume * 100
```

理想輸入 airway label：

- Label 1：lumen。
- Label 2：wall。

若有完整 airway wall segmentation：

```text
lumen_volume = count(lumen) * voxel_volume
wall_volume = count(wall) * voxel_volume
total_airway_volume = lumen_volume + wall_volume
WA% = wall_volume / total_airway_volume * 100
```

若沒有 wall/lumen 分離，程式可能使用 airway mask erosion 估計 lumen：

```text
lumen = binary_erosion(airway_mask, iterations=2)
wall = airway_mask - lumen
```

限制：

- 主資料中 AeroPath 很多是 OBJ，未必有完整 airway NIfTI。
- 若只用 label 7 trachea fallback，WA% 不一定代表完整 bronchial wall。
- 論文中要保守描述為 airway-derived feature，而不是過度宣稱精準小氣道壁厚量測。

## PA diameter

目前可穩定使用的是 pulmonary artery diameter estimate。

文件公式概念是用 pulmonary artery volume 推估等效球體直徑：

```text
radius = (3 * V / (4 * pi))^(1/3)
diameter = 2 * radius
```

此方法不是臨床標準手動畫線 PA diameter，而是 segmentation-based equivalent diameter。論文中應清楚說明是 automatic estimate。

## PA:A ratio

`PA_A_Ratio` 在目前 JSON 中多為 `null`，原因：

- 沒有可靠 aorta segmentation。
- 也沒有固定人工量測 PA 與 Aorta diameter 的流程結果。

因此正式論文不要把 PA:A ratio 寫成完成參數。可以寫：

- 本研究目前計算 PA diameter。
- PA:A ratio 需要主動脈 segmentation 或 3D Slicer 人工量測，列為未來工作。

## SVV%

Small Vessel Volume percentage 用於表示小血管負荷。

`參數計算說明.md` 的概念：

1. 從 vessel mask 取得血管區域。
2. 使用 distance transform 估計每個 vessel voxel 到邊界距離。
3. 用半徑 threshold 判斷小血管。
4. 計算 small vessel volume。

程式/文件中出現的 threshold：

- 小血管直徑 < 5 mm。
- 半徑 threshold < 2.5 mm。
- 另一份 AirwayQuan spec 使用 area < 5 mm² 換算半徑 `sqrt(5/pi)`。

目前主分類 JSON 內 `SVV%` 定義更接近：

```text
SVV% = small_vessel_volume / total_lung_volume * 100
```

AirwayQuan TODO 中則寫成：

```text
SVV% = small_vessel_volume / total_vessel_volume * 100
```

這是需要統一的地方。主論文若引用 `COPDClassification` 結果，應以主 JSON 與主程式定義為準，不要混用 AirwayQuan TODO。

## Vessel density

概念公式：

```text
Vessel_Density% = total_vessel_volume / total_lung_volume * 100
```

文件中可能把 label 6、8、9 都視為血管相關結構。實際主程式需要以 `copd_analyzer.py` 當前實作為準。論文中可以保守寫成：

> vessel density was computed as the ratio between segmented vascular volume and total lung volume.

若要更精準，寫論文前應確認程式是否只用 label 6，或同時包含 pulmonary artery/vein labels。

## Airway-Lung Ratio

概念公式：

```text
Airway_Lung_Ratio% = airway_volume / total_lung_volume * 100
```

airway volume 來源可能是：

- airway segmentation mask。
- trachea label 7 fallback。
- WA% 計算中的 total airway volume。

此參數代表 airway burden / airway segmentation volume 相對於肺部體積的比例。

## 主模型使用的 12 維特徵

`COPDClassification` 從本類參數抽取 12 維 feature：

| 類別 | 特徵 |
|---|---|
| Emphysema | total emphysema、五個 lobe emphysema |
| Vascular | SVV%、vessel density、PA diameter |
| Airway | WA%、airway-lung ratio |
| Lung morphology | total lung volume |

這些特徵的好處是可解釋，適合小樣本研究。

## 可寫入論文的方法段落

可描述為：

1. 讀取 CT volume 與 segmentation label map。
2. 由 NIfTI spacing 計算每個 voxel 的實際體積。
3. 根據 label 1 到 5 建立 lung mask 與 lobar masks。
4. 在 lung mask 內以 -950 HU threshold 計算 emphysema percentage。
5. 根據 vessel label 與 distance transform 估計 small vessel volume。
6. 根據 airway mask 或 trachea label 計算 airway volume 與 airway wall percentage。
7. 從 pulmonary artery label 估計 PA diameter。
8. 將所有參數輸出成 JSON，作為 classifier 的 tabular input。

## 目前限制

1. `VesselAirwayParamTransfer/data` 內目前不是主結果所在位置。
2. PA:A ratio 尚未完成。
3. Airway segmentation 格式不完全一致，OBJ 與 NIfTI 混用會影響 WA%。
4. SVV% 定義在不同草稿中有分母差異，需要在正式論文統一。
5. Vessel label 是否包含 label 8/9 需以最終程式確認。

## 論文建議

正式寫法建議：

- 把 `COPDClassification` 的 `*_metrics.json` 當正式結果來源。
- 把本資料夾當公式與程式原型來源。
- 在方法章明確列出每個 feature 的公式、輸入 label、單位與限制。
- 在限制章說明 airway wall 與 PA:A ratio 還需要更精準 segmentation 或人工校正。

