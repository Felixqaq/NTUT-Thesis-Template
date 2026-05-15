# NiiToLungLabel 肺部分割整理

`NiiToLungLabel` 是肺部 segmentation 流程的輔助資料夾，核心概念是透過 3D Slicer 開啟 MONAI Auto3DSeg server，讓 Python 腳本呼叫 server 產生 lung/lobe label。主實驗中實際 segmentation 結果已放在 `COPDClassification/NormalDataset/inference_output` 與 `COPDClassification/AbnormalDataset/inference_output`。

## 資料夾定位

可支撐論文第三章：

- 自動肺部分割流程。
- 3D Slicer / MONAI Auto3DSeg 作為 segmentation backend。
- 分割後 label map 作為 COPD quantitative biomarker 的基礎。

## 主要檔案

| 檔案/資料夾 | 用途 |
|---|---|
| `README.md` | 說明先開啟 3D Slicer MONAI Auto3DSeg server |
| `3DSlicerSeg.py` | 呼叫 3D Slicer server 進行 segmentation |
| `QC_report.py` | segmentation QC 報告腳本 |
| `lungs-v2.0.1.zip` | lung segmentation 相關模型或套件 |
| `data/inference_output/QC_Report` | QC 報告輸出位置，目前沒有看到正式結果 |

## 操作流程

README 的重點是：

1. 先開啟 3D Slicer。
2. 啟動 MONAI Auto3DSeg server。
3. 再用 Python 腳本送入 NIfTI 影像。
4. server 回傳或產生 segmentation label。

這個流程在主實驗中被 `COPDClassification/copd_segmentation.py` 與 `unified_pipeline.py` 吸收，形成比較完整的 pipeline。

## 與 COPDClassification 的關係

`NiiToLungLabel` 可以視為 segmentation 原型，正式結果在：

- `COPDClassification/NormalDataset/inference_output/seg_*.nii.gz`
- `COPDClassification/AbnormalDataset/inference_output/seg_*.nii.gz`

這些 segmentation label 被用來計算：

- total lung volume
- lobar volume
- lobar emphysema percentage
- vessel volume
- trachea/airway related volume
- PA diameter estimate

## Label map 在主實驗的重要性

COPD 定量特徵高度依賴 segmentation label。若 label 錯誤，會影響：

- 肺部 mask 範圍。
- -950 HU emphysema percentage。
- 肺葉別 emphysema。
- vessel density。
- SVV%。
- airway-lung ratio。

因此論文中需要說明 segmentation 是整個系統的第一個關鍵步驟。

## QC_report.py 的用途

`QC_report.py` 可用來做 segmentation quality control，例如：

- 檢查 segmentation 是否存在。
- 檢查輸出 label 是否為空。
- 統計每個 label 的 voxel count。
- 建立 QC report。

目前 `data/inference_output/QC_Report` 沒看到完整主結果，因此正式論文可以說本研究有基本輸出檢查，但若要更嚴謹，建議補上：

- 每例 lung volume 是否合理。
- label 1-5 是否都有合理體積。
- segmentation overlay screenshot。
- 人工抽樣檢查。

## 論文可寫方法段落

可寫成：

> 本研究使用 3D Slicer 中的 MONAI Auto3DSeg 模組進行胸部 CT 自動分割。輸入影像為 HU-preserved NIfTI volume，系統透過 Python client 將影像送至 Slicer inference server，輸出多類別 label map。後續定量分析使用 label 1-5 建立肺葉與總肺 mask，並使用血管與氣管相關 label 計算 vascular and airway biomarkers。

## 限制

1. 此資料夾本身沒有保存完整 54 例 QC 結果。
2. 分割模型是外部工具，需要在論文中說明版本與操作方式。
3. 若 3D Slicer server 參數不同，可能產生不同 segmentation。
4. segmentation accuracy 沒有正式和人工標註比較，因此應列為限制。

## 後續建議

1. 將 `QC_report.py` 套到 54 例 segmentation。
2. 產生一份 table：patient、label count、lung volume、是否通過 QC。
3. 抽樣產生 CT/segmentation overlay 圖，放入論文第三章或附錄。

