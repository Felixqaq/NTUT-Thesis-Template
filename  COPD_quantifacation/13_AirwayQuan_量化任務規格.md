# AirwayQuan 量化任務規格整理

`AirwayQuan` 目前不是完整實作資料夾，而是一份 airway/vessel quantification 的任務規格草案。它定義了 PA:A ratio、SVV%、WA% 等量化流程，和 `VesselAirwayParamTransfer` / `COPDClassification` 的實際程式有部分重疊，也有一些定義差異。

## 資料夾定位

可支撐論文：

- 方法設計背景。
- future work：更標準化 airway/vessel quantification。
- 補充說明：哪些參數目前是 fully automatic，哪些需要 human-in-loop。

## 主要檔案

| 檔案 | 用途 |
|---|---|
| `TODO.md` | airway/vessel quantification 工作規格 |
| `研究整理.md` | 先前簡要整理 |

此資料夾大量 `.conda` 檔案屬於環境，不是研究結果。

## TODO.md 定義的輸入

規格中的輸入包含：

- `original_ct.nii.gz`
- `airway_label.nii.gz`
  - label 1：lumen
  - label 2：wall
- `vessel_mask.nii.gz`
  - label 1：vessel

這和目前 `COPDClassification` 的 label map 不完全相同。主實驗 segmentation label 是多類肺葉/血管/氣管 label，不一定有 airway lumen/wall 分離。

## TODO.md 定義的輸出

規格中的輸出包含：

- `pa_a_ratio.json`
- `vessel_metrics.json`
- `airway_metrics.csv`

目前主實驗正式輸出是 `*_metrics.json`，包含多個 COPD feature，但 `pa_a_ratio.json` 與 `airway_metrics.csv` 這類標準化輸出尚未完整建立。

## PA:A ratio 規格

TODO.md 中 PA:A ratio 偏向 human-in-loop：

1. 在 3D Slicer 中打開 CT。
2. 在 pulmonary artery bifurcation axial slice 量測 main PA diameter。
3. 同層或標準位置量測 ascending aorta diameter。
4. 計算：

```text
PA:A ratio = PA diameter / Aorta diameter
```

這是比目前 `COPDAnalyzer` 中 PA diameter estimate 更接近臨床標準的流程。

目前狀態：

- 主實驗已有 PA diameter estimate。
- 主實驗沒有可靠 Aorta diameter。
- 因此 `PA_A_Ratio` 多為 `null`。

論文中應寫：

- PA diameter 為自動估計參數。
- PA:A ratio 是未來可加入的 human-in-loop 或 aorta segmentation 參數。

## SVV% 規格

TODO.md 中 SVV% workflow：

1. 使用 SimpleITK 讀入 vessel mask。
2. 取得 voxel spacing。
3. 計算 voxel volume。
4. 計算 total vessel volume。
5. 使用 `distance_transform_edt(mask, sampling=spacing)`。
6. 用 area threshold 5 mm² 換算半徑：

```text
radius_threshold = sqrt(5 / pi)
```

7. 定義 small vessel mask：

```text
small_vessel = distance > 0 and distance < radius_threshold
```

8. 計算：

```text
SVV% = small_vessel_volume / total_vessel_volume * 100
```

重要差異：

- AirwayQuan 規格的分母是 total vessel volume。
- `COPDClassification` 主 JSON 中的 SVV% 更接近 small vessel volume / total lung volume。

正式論文必須統一定義。若引用主模型 12 特徵，應使用 `COPDClassification` 程式與 JSON 的定義。

## WA% 規格

TODO.md 中 WA% 偏向 tool-based workflow：

1. 使用 3D Slicer。
2. 使用 SlicerVMTK。
3. 建立 Lumen 與 Wall segments。
4. Extract Centerline。
5. Cross-Sectional Analysis。
6. 匯出 `airway_metrics.csv`。
7. 計算：

```text
Total_Area = Lumen_Area + Wall_Area
WA_Percentage = Wall_Area / Total_Area * 100
```

此流程比目前自動化 airway fallback 更標準，但需要：

- lumen/wall segmentation。
- centerline extraction。
- 可能的人為校正。

主研究目前未看到完整 `airway_metrics.csv` 批次結果，因此不能宣稱已完成 SlicerVMTK WA%。

## 與 VesselAirwayParamTransfer 的關係

| 參數 | AirwayQuan TODO | COPDAnalyzer 現況 |
|---|---|---|
| PA diameter | human-in-loop PA/Aorta measurement | segmentation-based PA diameter estimate |
| PA:A ratio | 目標輸出 | 多為 null |
| SVV% | small vessel / total vessel | 主 JSON 更接近 small vessel / lung volume |
| WA% | SlicerVMTK lumen/wall cross-section | airway mask erosion 或 fallback |
| output | 多個專用 JSON/CSV | 單一 `*_metrics.json` |

## 論文可寫位置

適合放在：

- 方法章限制說明：部分 airway/vessel 指標目前採自動估計。
- 未來工作：導入 SlicerVMTK 中心線與 PA:A ratio 人工/半自動量測。
- 附錄：列出未來 airway quantification workflow。

## 不建議的寫法

不要寫：

- 「本研究已完成 PA:A ratio」。
- 「所有 WA% 都由 SlicerVMTK cross-sectional analysis 得到」。
- 「SVV% 定義完全一致」。

建議寫：

- 「PA:A ratio was not included in the final classifier due to the lack of aorta measurements.」
- 「Airway wall percentage was estimated from available airway masks or fallback labels.」
- 「Future work will standardize vessel and airway metrics using centerline-based analysis.」

## 後續建議

1. 決定 SVV% 最終分母：total lung volume 或 total vessel volume。
2. 若要保留 PA:A ratio，建立 3D Slicer 人工量測 protocol。
3. 對 54 例產生 `airway_metrics.csv`。
4. 把 AirwayQuan 規格轉成可執行 pipeline，避免只停留在 TODO。

