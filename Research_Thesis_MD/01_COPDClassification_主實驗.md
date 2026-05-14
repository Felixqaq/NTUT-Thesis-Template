# COPDClassification 主實驗詳細整理

`COPDClassification` 是目前整個研究中最完整、最適合寫成論文主軸的資料夾。它不是單純放模型或資料，而是一個從胸部 CT 影像到 COPD 自動分類的完整實驗流程：輸入 DICOM 轉換後的 NIfTI/HU 影像，透過肺部結構分割產生 label map，再從 CT 與 segmentation 中計算可解釋的 COPD 定量特徵，最後使用 PyTorch 神經網路模型進行 normal 與 COPD/abnormal 的二元分類。

本文件目標是把 `COPDClassification` 內的資料、程式、實驗流程、名詞、原理、公式、結果與限制全部整理成論文可用素材。可以優先用在論文第三章「研究方法」與第四章「實驗結果」。

## 研究核心問題

本研究要回答的問題是：

> 能否使用胸部 CT 影像自動萃取 COPD 相關定量特徵，並透過神經網路模型區分 normal 與 COPD/abnormal 個案？

換成論文語氣可以寫成：

> 本研究建立一套基於胸部電腦斷層影像之 COPD 自動分類流程，透過自動肺部結構分割與影像定量特徵萃取，將肺氣腫、血管、氣道與肺部形態資訊轉換為可解釋特徵，並以神經網路模型進行 COPD 與 normal 之二元分類。

## 主實驗結論摘要

主實驗資料集共有 54 例：

| 類別 | 例數 | 資料位置 |
|---|---:|---|
| Normal | 21 | `NormalDataset/data` |
| COPD/Abnormal | 33 | `AbnormalDataset/data` |
| Total | 54 | `COPDClassification` |

建議作為正式論文主結果的訓練資料夾：

```text
COPDClassification/models/training_20260206_132335
```

主要結果：

| 指標 | 數值 |
|---|---:|
| Accuracy | 0.9259 |
| Precision | 1.0000 |
| Recall / Sensitivity | 0.8788 |
| F1-score | 0.9355 |
| AUC | 0.9784 |
| Specificity | 1.0000 |

混淆矩陣：

| 真實類別 | 預測 Normal | 預測 COPD |
|---|---:|---:|
| Normal | 21 | 0 |
| COPD | 4 | 29 |

結果重點：

- 模型對 normal 的辨識非常穩定，沒有 false positive。
- 模型主要錯誤來自 COPD 被判為 normal，也就是 false negative。
- AUC 0.9784 表示模型對兩類樣本的排序能力很好。
- 目前是 binary classification，不是 GOLD severity staging。

## 名詞解釋

### COPD

COPD 是 Chronic Obstructive Pulmonary Disease，中文常稱慢性阻塞性肺病。它通常與長期氣道阻塞、肺氣腫、慢性支氣管炎、肺部血管與氣道結構改變有關。臨床診斷常依肺功能檢查，例如 FEV1/FVC 與 FEV1 predicted percentage；影像上則常觀察肺氣腫、低衰減區與肺血管改變。

本研究中的 COPD/abnormal class 是影像與臨床資料整理後的 abnormal 組，模型任務是將其與 normal 組分開。

### Normal

Normal 指本研究中作為對照組的胸部 CT 個案。這些個案來自醫院 normal dataset，作為模型學習「非 COPD/非 abnormal」影像特徵的對照。

### Abnormal

Abnormal 在本專案中大致對應 COPD 或疑似 COPD 相關異常個案。檔案與資料夾名稱使用 `AbnormalDataset`，論文中可寫成 COPD/abnormal cohort，但要注意目前模型是二元分類，並非直接預測 GOLD 1-4。

### CT

CT 是 Computed Tomography，電腦斷層影像。胸部 CT 可提供肺實質、氣道、血管與肺葉結構資訊。本研究使用胸部 CT 作為唯一影像輸入。

### DICOM

DICOM 是臨床醫學影像常用格式。醫院原始 CT 通常是一系列 DICOM slices，每張 slice 包含影像 pixel 與 metadata，例如 spacing、slice thickness、RescaleSlope、RescaleIntercept、scanner manufacturer、kernel 等。

本研究的原始醫院資料在 `DicomToNii` 與 `Dataset` 中，經轉換後才進入 `COPDClassification`。

### NIfTI

NIfTI 是神經影像與醫學影像分析常用的 3D volume 格式，副檔名常為 `.nii` 或 `.nii.gz`。本研究將 DICOM series 轉成 NIfTI，讓後續 segmentation、特徵計算與模型流程更容易處理。

### HU

HU 是 Hounsfield Unit，CT 影像強度單位。常見參考：

| 組織/物質 | 大約 HU |
|---|---:|
| 空氣 | -1000 |
| 正常肺部 | 約 -900 到 -500 |
| 水 | 0 |
| 軟組織 | 約 30 到 80 |
| 骨頭 | 大於 300 |

肺氣腫定量通常依賴 HU threshold。例如本研究使用 HU < -950 作為 emphysema low attenuation area 的主要門檻。

### Voxel

Voxel 是 3D 影像中的體素，相當於 2D pixel 的 3D 版本。每個 voxel 有一個 CT intensity，也就是 HU 值。體積計算需要知道 voxel spacing。

### Spacing

Spacing 是 voxel 在 x、y、z 三個方向上的實際物理尺寸，單位通常是 mm。例如 spacing = 0.7 mm x 0.7 mm x 3.0 mm。若只數 voxel 數量而不乘 spacing，體積會錯誤。

基本體積公式：

```text
voxel_volume_mm3 = spacing_x * spacing_y * spacing_z
structure_volume_mm3 = voxel_count * voxel_volume_mm3
structure_volume_ml = structure_volume_mm3 / 1000
```

### Segmentation

Segmentation 是把影像中的不同解剖結構分割出來的過程。本研究需要分割肺葉、血管、氣管或其他肺部結構，才能在特定區域內計算 COPD 定量特徵。

### Label map

Label map 是 segmentation 的輸出影像。它和原始 CT 一樣是 3D volume，但每個 voxel 的值不是 HU，而是類別編號。例如 label 1 代表某個肺葉，label 6 代表血管。

### Lung mask

Lung mask 是肺部區域的二元遮罩。通常由多個肺葉 label 合併得到。在本研究中，label 1 到 5 可組成總肺 mask。

### Lobe

Lobe 是肺葉。本研究 segmentation 將肺部分成左上/左下、右上/右中/右下等肺葉，用於計算肺葉別 emphysema percentage。

### Airway

Airway 是氣道，包含氣管與支氣管系統。COPD 會造成氣道壁增厚、氣道狹窄等改變。本研究中 airway feature 包含 WA% 與 airway-lung ratio，但目前 airway segmentation 有 OBJ 與 NIfTI 混用限制。

### Vessel

Vessel 是血管。本研究使用血管 label 計算 vessel density 與 small vessel volume percentage。COPD 可能導致肺血管床改變，因此血管相關特徵是 COPD 影像 biomarker 的一部分。

### Trachea

Trachea 是氣管。在本研究 label map 中 label 7 為 trachea。當完整 airway segmentation 不足時，部分 airway feature 可能使用 trachea 或 airway fallback。

### Emphysema

Emphysema 是肺氣腫，通常指肺泡壁破壞、肺泡空間擴大，CT 上常呈現低衰減區。影像定量常以低於某個 HU threshold 的肺部 voxel 比例表示。

### LAA / LAV950

LAA 是 Low Attenuation Area，低衰減區。LAV950 是 Low Attenuation Volume below -950 HU。本研究主要使用：

```text
emphysema_voxel = lung_voxel and CT_HU < -950
```

因此 Total Emphysema Percent 可理解為肺部中 HU < -950 的比例。

### Biomarker

Biomarker 是生物標記。影像 biomarker 指從影像中萃取、可反映疾病狀態的數值。本研究的 biomarker 包含 emphysema percentage、SVV%、WA%、vessel density、PA diameter 等。

### PA diameter

PA 是 Pulmonary Artery，肺動脈。本研究從 segmentation label 估計 pulmonary artery diameter。注意這是自動估計值，不是臨床標準手動畫線量測。

### PA:A ratio

PA:A ratio 是 pulmonary artery diameter 與 aorta diameter 的比例。這在 COPD 或肺高壓相關研究中常被使用。但本研究目前沒有可靠 aorta segmentation，因此 `PA_A_Ratio` 多為 `null`，不應寫成正式完成指標。

### SVV%

SVV% 是 Small Vessel Volume percentage，小血管體積比例。概念是估計肺部中小血管佔比。COPD 可能伴隨小血管床減少或血管結構改變，因此 SVV% 是血管型 biomarker。

### WA%

WA% 是 Wall Area percentage，氣道壁面積或體積比例。概念上：

```text
WA% = airway_wall / total_airway * 100
```

若有完整 airway lumen/wall segmentation，WA% 可代表氣道壁增厚程度。本研究目前有 airway segmentation 格式限制，因此 WA% 應保守解釋。

### Vessel Density

Vessel Density 是血管密度，通常定義為血管體積除以總肺體積：

```text
Vessel_Density% = total_vessel_volume / total_lung_volume * 100
```

### Airway-Lung Ratio

Airway-Lung Ratio 是氣道體積相對於總肺體積的比例：

```text
Airway_Lung_Ratio% = airway_volume / total_lung_volume * 100
```

### MLP

MLP 是 Multi-Layer Perceptron，多層感知器。它是一種用於 tabular data 的神經網路。因為本研究輸入是 12 個數值特徵，而不是直接輸入 3D CT，所以使用 MLP 比使用大型 3D CNN 更合理。

### StandardScaler

StandardScaler 是特徵標準化方法：

```text
z = (x - mean) / standard_deviation
```

因為 12 個特徵單位不同，例如 percent、ml、mm，若不標準化，尺度較大的特徵可能主導模型訓練。

### Stratified K-Fold

Stratified K-Fold 是分層交叉驗證。它會把資料分成 K 份，同時盡量保持每一份中 normal 與 COPD 的比例接近整體資料。這對小樣本分類很重要。

### Confusion Matrix

Confusion matrix 是分類結果表。二元分類有四種結果：

| 名稱 | 意義 |
|---|---|
| TP | COPD 被正確預測為 COPD |
| TN | Normal 被正確預測為 normal |
| FP | Normal 被錯誤預測為 COPD |
| FN | COPD 被錯誤預測為 normal |

本研究最主要錯誤是 FN。

### Accuracy

Accuracy 是整體正確率：

```text
Accuracy = (TP + TN) / (TP + TN + FP + FN)
```

### Precision

Precision 表示模型預測為 COPD 的樣本中，有多少是真的 COPD：

```text
Precision = TP / (TP + FP)
```

本研究 precision = 1.0000，因為沒有 false positive。

### Recall / Sensitivity

Recall 也稱 sensitivity，表示所有 COPD 中有多少被抓出來：

```text
Recall = TP / (TP + FN)
```

本研究 recall = 0.8788，因為 33 個 COPD 中有 4 個被漏判。

### Specificity

Specificity 表示所有 normal 中有多少被正確判為 normal：

```text
Specificity = TN / (TN + FP)
```

本研究 specificity = 1.0000。

### F1-score

F1-score 是 precision 與 recall 的 harmonic mean：

```text
F1 = 2 * Precision * Recall / (Precision + Recall)
```

### ROC 與 AUC

ROC curve 描述不同分類 threshold 下 sensitivity 與 false positive rate 的關係。AUC 是 ROC 曲線下面積，越接近 1 代表模型排序能力越好。本研究 AUC = 0.9784。

## 資料夾與檔案功能

| 檔案/資料夾 | 用途 |
|---|---|
| `unified_pipeline.py` | 端到端 COPD 分析流程，整合 segmentation、參數計算、分類與報告 |
| `copd_segmentation.py` | 呼叫 3D Slicer / MONAI Auto3DSeg server 進行肺部結構分割 |
| `copd_classifier.py` | PyTorch MLP 分類模型與 5-fold training/evaluation |
| `train_copd_model.py` | 訓練 COPD classifier |
| `predict_copd.py` | 使用已訓練模型進行推論 |
| `adaptive_emphysema.py` | 肺氣腫 threshold 與 adaptive threshold 實驗 |
| `generate_viz.py` | 產生結果視覺化圖 |
| `NormalDataset` | 21 例 normal CT、segmentation、參數與圖表 |
| `AbnormalDataset` | 33 例 COPD/abnormal CT、segmentation、參數與圖表 |
| `TestDataset` | 額外測試資料，含 hospital series 與 `study_0034` 到 `study_0044` |
| `models` | 訓練結果、fold model、scaler、ROC、混淆矩陣、錯誤分類分析 |
| `VesselAirwayParamTransfer` | 內嵌的 COPDAnalyzer 參數計算程式 |
| `NTUT-Thesis-Template` | 已開始撰寫的 COPD 論文章節草稿 |

## 主實驗資料

### NormalDataset

`NormalDataset/data` 有 21 個 NIfTI：

1. `1596038_Thorax Lung Br60 S2 3.00.nii.gz`
2. `1746380_Thorax Lung Br60 S2 3.00.nii.gz`
3. `2094528_LUNG AX 1_1 LW.nii.gz`
4. `2221276_LW AXI 3_3  B60f.nii.gz`
5. `2500824_LW AXI 3_3  I70f  2.nii.gz`
6. `2860903_LW AXI 3_3  I70f  2.nii.gz`
7. `3097765_Thorax CM Lung Br60 S3 3.00.nii.gz`
8. `3635301_Thorax Br60 S3 3.00.nii.gz`
9. `4204917_LW AXI 3_3  I70f  2.nii.gz`
10. `4302294_Thorax Lung Br60 S2 3.00.nii.gz`
11. `5046455_LW AXI 3_3  I70f  2.nii.gz`
12. `5390303_LW AXI 3_3  I70f  2.nii.gz`
13. `6212308_Thorax Lung Br60 S2 3.00.nii.gz`
14. `6312603_LW AXI 3_3  B60f.nii.gz`
15. `6858508_LW AXI 3_3  B60f.nii.gz`
16. `7871759_~LUNG AX 1_1 LW.nii.gz`
17. `8244460_Thorax 1_1 Br40 S3 1.00.nii.gz`
18. `8332556_Thorax 1_1 Br40 S3 1.00.nii.gz`
19. `A754735_LW AXI 3_3  B60f.nii.gz`
20. `C081146_LW AXI 3_3  I70f  2.nii.gz`
21. `E717248_Thorax Lung Br60 S2 3.00.nii.gz`

配套輸出：

- `NormalDataset/inference_output/seg_*.nii.gz`：肺部/肺葉/血管/氣管 label map。
- `NormalDataset/param/*_metrics.json`：COPD 定量特徵。
- `NormalDataset/airway/*.obj`：AeroPath airway 3D model。
- `NormalDataset/visualizations`：feature distribution、correlation heatmap、comparison bar 等圖。
- `NormalDataset/report`：目前未看到正式報告檔。

### AbnormalDataset

`AbnormalDataset/data` 有 33 個 NIfTI：

1. `1261736_LW AXI 3_3  B60f.nii.gz`
2. `1687031_Thorax Lung Br60 S2 3.00.nii.gz`
3. `1800944_Thorax Lung Br60 S2 3.00.nii.gz`
4. `2588424_LW AXI 3_3  B60f.nii.gz`
5. `2991621_LW  AXI 3.0  B60f.nii.gz`
6. `3647457_LW AXI 3_3  B60f.nii.gz`
7. `4372708_LW-insp.  AXI 3_3  B60f.nii.gz`
8. `4710629_LW  AXI 3.0  I70f  2.nii.gz`
9. `4796667_Thorax Lung Br60 S2 3.00.nii.gz`
10. `5127217_Thorax 1_1 Br40 S3 1.00.nii.gz`
11. `5630846_Aorta C+  5.0  B30f.nii.gz`
12. `6887256_Thorax Lung Br60 S2 3.00.nii.gz`
13. `8009284_Thorax Lung Br60 S2 3.00.nii.gz`
14. `8126939_LW AXI 3_3  B60f.nii.gz`
15. `8404129_Chest C-  5.0  B31f.nii.gz`
16. `8704416_Thorax Lung Br60 S3 3.00.nii.gz`
17. `9075311_Thorax  5.0  B30f.nii.gz`
18. `9529629_Thorax Lung Br60 S2 3.00.nii.gz`
19. `A613117_LW AXI 3_3  B60f.nii.gz`
20. `A762364_LW AXI 3_3  B60f.nii.gz`
21. `B213449_LW AXI 3_3  B60f.nii.gz`
22. `C041635_LW AXI 3_3  I70f  2.nii.gz`
23. `C435832_LW AXI 3_3  B60f.nii.gz`
24. `C543831_Thorax Lung Br60 S2 3.00.nii.gz`
25. `C586742_LW AXI 3_3  B60f.nii.gz`
26. `C905524_Thorax_No CM  3_3  Br60  S2  3.00.nii.gz`
27. `D132855_LW AXI 3_3  B60f.nii.gz`
28. `D550510_Thorax CM Lung Br60 S3 3.00.nii.gz`
29. `E353272_LW AXI 3_3  B60f.nii.gz`
30. `E558113_Thorax Lung Br60 S2 3.00.nii.gz`
31. `E647833_Thorax Lung Br60 S2 3.00.nii.gz`
32. `E771850_Thorax Lung Br60 S2 3.00.nii.gz`
33. `E797258_Thorax Lung Br60 S2 3.00.nii.gz`

配套輸出：

- `AbnormalDataset/inference_output/seg_*.nii.gz`
- `AbnormalDataset/param/*_metrics.json`
- `AbnormalDataset/airway/*.obj`
- `AbnormalDataset/visualizations`
- `AbnormalDataset/report` 目前未看到正式報告檔。

## 實驗總流程

整個主實驗可以拆成八個階段。

### Stage 1：DICOM 轉 NIfTI/HU

雖然此階段主要在 `DicomToNii` 完成，但它是 `COPDClassification` 的輸入基礎。

流程：

1. 讀取醫院 DICOM series。
2. 選擇適合肺部分析的 chest CT axial series。
3. 使用 `RescaleSlope` 與 `RescaleIntercept` 將 pixel value 轉成 HU。
4. 根據 DICOM metadata 排序 slices。
5. 建立 3D NIfTI volume。
6. 將轉換後檔案放入 `NormalDataset/data` 或 `AbnormalDataset/data`。

原理：

- COPD emphysema feature 依賴 HU，因此 CT intensity 必須正確轉換。
- NIfTI 保留 spacing，後續才能計算真實體積。

論文可寫：

> Original DICOM CT series were converted into HU-preserved NIfTI volumes. Slice ordering, voxel spacing, and image orientation were derived from DICOM metadata to preserve the anatomical geometry for subsequent volumetric measurements.

### Stage 2：肺部結構自動分割

主要相關檔案：

- `copd_segmentation.py`
- `unified_pipeline.py`
- `NormalDataset/inference_output`
- `AbnormalDataset/inference_output`

流程：

1. 輸入 CT NIfTI。
2. 呼叫 3D Slicer / MONAI Auto3DSeg server。
3. server 對 CT 進行多類別 segmentation。
4. 輸出 `seg_*.nii.gz` label map。
5. 後續所有 biomarker 都依賴此 label map。

原理：

- segmentation 把肺部 CT 的解剖區域轉成數值 label。
- 每個 label 代表特定結構，模型不需要人工畫 ROI。
- 這讓整個流程可以半自動或全自動執行。

主實驗 label mapping：

| Label | 結構 | 用途 |
|---:|---|---|
| 1 | Left superior lobe | 左上肺葉體積、左上肺葉 emphysema |
| 2 | Left inferior lobe | 左下肺葉體積、左下肺葉 emphysema |
| 3 | Right superior lobe | 右上肺葉體積、右上肺葉 emphysema |
| 4 | Right middle lobe | 右中肺葉體積、右中肺葉 emphysema |
| 5 | Right inferior lobe | 右下肺葉體積、右下肺葉 emphysema |
| 6 | Blood vessel | vessel volume、vessel density、SVV% |
| 7 | Trachea | airway/trachea fallback |
| 8 | Pulmonary venous system | 血管相關結構 |
| 9 | Pulmonary artery | PA diameter |

注意：

- `EmphysemaSeg` 的 label 順序不同，不可混用。
- 若 label map 品質不好，所有後續 feature 都會受影響。

### Stage 3：Airway segmentation

主要相關工具：

- AeroPath
- `NormalDataset/airway`
- `AbnormalDataset/airway`
- `unified_pipeline.py` 中的 airway search/API logic

流程：

1. 對 CT 執行 AeroPath airway segmentation。
2. 輸出 airway NIfTI 或 OBJ 3D model。
3. pipeline 嘗試尋找 airway NIfTI：

```text
../airway/{base_name}_airway_seg.nii.gz
```

4. 若找不到 airway NIfTI，部分 airway feature 可能 fallback。

原理：

- COPD 常與氣道壁增厚、氣道狹窄相關。
- 若能取得 airway lumen/wall mask，可計算 WA%。
- 若只有 OBJ，適合視覺化但不一定適合 voxel-based feature extraction。

限制：

- 主資料中大量 airway 結果是 `.obj`。
- OBJ 不能直接提供每個 voxel 的 label。
- WA% 在目前實驗中需要保守解釋。

論文可寫：

> Airway segmentation was incorporated when voxel-based airway masks were available. For cases with only surface model outputs, airway-related measurements were treated cautiously or estimated through fallback labels.

### Stage 4：COPD 定量特徵計算

主要相關檔案：

- `VesselAirwayParamTransfer/copd_analyzer.py`
- `NormalDataset/param/*_metrics.json`
- `AbnormalDataset/param/*_metrics.json`

輸入：

- CT NIfTI。
- segmentation label map。
- airway segmentation 或 fallback label。

輸出：

- 每例一個 `*_metrics.json`。

核心原理：

1. 使用 label 1-5 建立肺部與肺葉 mask。
2. 使用 HU threshold 計算 emphysema。
3. 使用 label 6/8/9 等血管 label 計算 vessel feature。
4. 使用 airway mask 或 trachea label 計算 airway feature。
5. 以 spacing 將 voxel count 轉換成體積。

### Stage 5：建立 12 維特徵向量

從每個 JSON 中抽出 12 個 feature：

| 編號 | Feature | 類別 | 單位/意義 |
|---:|---|---|---|
| 1 | `Total_Emphysema_Percent` | 肺氣腫 | 全肺 HU < -950 比例 |
| 2 | `Left_Superior_Lobe_Emphysema` | 肺氣腫 | 左上肺葉肺氣腫比例 |
| 3 | `Left_Inferior_Lobe_Emphysema` | 肺氣腫 | 左下肺葉肺氣腫比例 |
| 4 | `Right_Superior_Lobe_Emphysema` | 肺氣腫 | 右上肺葉肺氣腫比例 |
| 5 | `Right_Middle_Lobe_Emphysema` | 肺氣腫 | 右中肺葉肺氣腫比例 |
| 6 | `Right_Inferior_Lobe_Emphysema` | 肺氣腫 | 右下肺葉肺氣腫比例 |
| 7 | `SVV_Percent` | 血管 | 小血管體積比例 |
| 8 | `WA_Percent` | 氣道 | 氣道壁比例 |
| 9 | `Vessel_Density_Percent` | 血管 | 血管體積/總肺體積 |
| 10 | `Airway_Lung_Ratio_Percent` | 氣道 | 氣道體積/總肺體積 |
| 11 | `Total_Lung_Volume_ml` | 肺形態 | 總肺體積 |
| 12 | `PA_Diameter_mm` | 血管 | 肺動脈直徑估計 |

特徵設計原理：

- 肺氣腫特徵反映肺實質破壞。
- 血管特徵反映肺血管床變化。
- 氣道特徵反映 airway remodeling。
- 肺體積反映 hyperinflation 或整體肺部形態。
- PA diameter 反映肺血管或肺高壓相關變化的可能性。

### Stage 6：特徵標準化

使用 `StandardScaler` 對 12 個 feature 做標準化。

原理：

不同 feature 尺度差異很大：

- Emphysema 是百分比。
- Total lung volume 是 ml。
- PA diameter 是 mm。
- Vessel density 是百分比。

若不標準化，數值較大的 feature 可能在神經網路訓練中造成不合理權重。

標準化公式：

```text
z = (x - mean) / standard_deviation
```

注意：

- 每個 fold 的 scaler 只能用 training data fit。
- validation data 只能 transform，不能一起 fit。
- 這樣才不會 data leakage。

### Stage 7：MLP 模型訓練

主要檔案：

- `copd_classifier.py`
- `train_copd_model.py`

模型架構：

| 層級 | 功能 |
|---|---|
| Input | 12 維 feature |
| Dense 64 | 學習 feature interaction |
| BatchNorm | 穩定訓練 |
| ReLU | 非線性轉換 |
| Dropout | 降低過擬合 |
| Dense 32 | 中層表示 |
| BatchNorm + ReLU + Dropout | 正規化與非線性 |
| Dense 16 | 壓縮到較小 representation |
| Output 2 | normal / COPD logits |

訓練設定：

- Loss：CrossEntropyLoss。
- Optimizer：Adam。
- Scheduler：ReduceLROnPlateau。
- Validation：Stratified 5-fold cross validation。
- Early stopping：避免過擬合。

為什麼不用 3D CNN：

- 樣本數只有 54 例，直接訓練 3D CNN 很容易過擬合。
- 3D CNN 需要更多 GPU 記憶體與更多資料。
- 本研究的 12 個特徵有臨床與影像解釋性。
- MLP 對 tabular feature 比較合適。

### Stage 8：五折交叉驗證與評估

使用 Stratified 5-fold cross validation。

流程：

1. 將 54 例分成 5 folds。
2. 每次用 4 folds 訓練、1 fold 驗證。
3. 每個 fold 都重新 fit StandardScaler。
4. 每個 fold 都訓練一個模型。
5. 收集每 fold 的 prediction、probability、metric。
6. 合併得到 overall confusion matrix 與 ROC/AUC。

原理：

- 小樣本下如果只切一次 train/test，結果容易受切分影響。
- 5-fold 可讓每個樣本都有機會當 validation。
- stratified 可避免某個 fold 裡 normal 或 COPD 比例太偏。

## 定量特徵公式與原理

### Total lung volume

總肺 mask：

```text
lung_mask = label in {1, 2, 3, 4, 5}
```

總肺體積：

```text
total_lung_volume_mm3 = count(lung_mask) * voxel_volume_mm3
total_lung_volume_ml = total_lung_volume_mm3 / 1000
```

意義：

- COPD 可能造成 hyperinflation，使肺體積改變。
- 但肺體積會受吸氣程度、體型、掃描範圍影響。

### Total emphysema percent

公式：

```text
emphysema_mask = lung_mask and CT_HU < -950
Total_Emphysema_Percent = count(emphysema_mask) / count(lung_mask) * 100
```

原理：

- 肺氣腫區域在 CT 上密度較低。
- -950 HU 是常見 emphysema quantification threshold。

限制：

- reconstruction kernel 會影響 HU distribution。
- thick slice 會有 partial volume effect。
- 吸氣程度也會影響肺密度。

### Lobar emphysema percent

每個肺葉：

```text
lobe_mask = label == lobe_label
lobar_emphysema = lobe_mask and CT_HU < -950
lobar_percent = count(lobar_emphysema) / count(lobe_mask) * 100
```

意義：

- COPD/emphysema 分布可能不是均勻的。
- 上肺葉或下肺葉 predominance 可能反映不同 phenotype。

本研究將五個肺葉的 emphysema percent 都作為 feature。

### SVV%

概念：

```text
small_vessel_volume = volume of vessels below small-vessel threshold
SVV% = small_vessel_volume / reference_volume * 100
```

主程式中的 reference volume 建議以實際 JSON/程式為準，主分類特徵名稱為 `SVV_Percent`。

原理：

- COPD 可能造成小血管減少或血管床 remodeling。
- 小血管特徵提供 emphysema 以外的 vascular information。

注意：

- 不同文件對 SVV% 分母有差異，有的使用 total lung volume，有的使用 total vessel volume。
- 寫論文時要和最終程式定義一致。

### WA%

理想公式：

```text
WA% = wall_volume / (wall_volume + lumen_volume) * 100
```

原理：

- COPD 或慢性氣道疾病可能造成 airway wall thickening。
- WA% 越高可能表示氣道壁相對增厚。

本研究限制：

- 需要可靠 airway lumen/wall segmentation。
- 目前 AeroPath 輸出常為 OBJ。
- 若沒有 voxel airway mask，WA% 可能使用估計或 fallback。

### Vessel density

公式：

```text
Vessel_Density% = total_vessel_volume / total_lung_volume * 100
```

原理：

- 肺血管密度可反映血管床狀態。
- COPD 肺氣腫會造成肺泡壁與毛細血管床破壞，血管密度可能下降。

### Airway-lung ratio

公式：

```text
Airway_Lung_Ratio% = airway_volume / total_lung_volume * 100
```

原理：

- 將 airway volume 對肺體積正規化。
- 可降低個體肺大小差異影響。

### PA diameter

概念：

```text
PA_Diameter_mm = estimated diameter from pulmonary artery segmentation
```

若採等效球體估計，可概念化為：

```text
radius = (3 * V / (4 * pi))^(1/3)
diameter = 2 * radius
```

限制：

- 這不是標準 axial slice 手動量測。
- PA:A ratio 尚未完成。

## `*_metrics.json` 內容解釋

每個病人的 metrics JSON 大致包含：

| 欄位 | 意義 |
|---|---|
| `volumes` | 各 segmentation label 的 voxel count 與 volume |
| `total_lung_volume_mm3` | 總肺體積 |
| `total_vessel_volume` | 血管總體積 |
| `trachea_volume` | 氣管體積 |
| `WA%` | 氣道壁比例或估計值 |
| `PA_Diameter_mm` | 肺動脈直徑估計 |
| `PA_A_Ratio` | 肺動脈/主動脈比例，目前多為 null |
| `SVV%` | 小血管體積比例 |
| `emphysema` | 肺氣腫 threshold 與肺葉/總肺百分比 |
| `Vessel_Density%` | 血管密度 |
| `Airway_Lung_Ratio%` | 氣道肺體積比例 |

JSON 的角色：

- 是影像到 tabular feature 的中間結果。
- 可追蹤每個病人的 feature。
- 可用於錯誤分類分析。

## Adaptive emphysema 實驗

`adaptive_emphysema.py` 探索不同 emphysema threshold：

| 方法 | 說明 |
|---|---|
| Fixed threshold | 使用固定 HU threshold，例如 -950 |
| Percentile threshold | 根據個案 HU distribution 取百分位 |
| Adaptive threshold | 使用 mean - n * std |
| Multi-threshold | mild -950、moderate -960、severe -970 |
| Combined thresholds | 比較 -980 到 -930 多個 threshold |

目前主模型仍使用 fixed -950 HU，原因：

- 54 例 JSON 與模型訓練已對應此版本。
- -950 HU 是常見且容易解釋的 emphysema threshold。
- adaptive threshold 尚未形成完整主結果。

論文可以在限制或 future work 寫：

> Future work may evaluate adaptive emphysema thresholds to reduce protocol-dependent bias caused by reconstruction kernel and slice thickness.

## 模型訓練結果

`models` 中有三組主要訓練結果：

| Training folder | Overall Acc | Precision | Recall | F1 | AUC | Mean Acc | Mean AUC | 定位 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| `training_20260128_140828` | 0.8889 | 0.9355 | 0.8788 | 0.9063 | 0.9553 | 0.8909 | 0.9695 | 早期結果 |
| `training_20260130_182130` | 0.9259 | 1.0000 | 0.8788 | 0.9355 | 0.9784 | 0.9273 | 0.9657 | 改善後結果 |
| `training_20260206_132335` | 0.9259 | 1.0000 | 0.8788 | 0.9355 | 0.9784 | 0.9273 | 0.9657 | 建議正式結果 |

建議論文只把 `training_20260206_132335` 當正式主結果，其他兩組可作研究歷程或附錄。

## 20260206 五折結果

| Fold | Train | Val | Accuracy | Precision | Recall | F1 | AUC | FN | FP |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 43 | 11 | 0.9091 | 1.0000 | 0.8333 | 0.9091 | 0.9000 | 1 | 0 |
| 2 | 43 | 11 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0 | 0 |
| 3 | 43 | 11 | 0.8182 | 1.0000 | 0.7143 | 0.8333 | 0.9286 | 2 | 0 |
| 4 | 43 | 11 | 0.9091 | 1.0000 | 0.8571 | 0.9231 | 1.0000 | 1 | 0 |
| 5 | 44 | 10 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0 | 0 |

結果解讀：

- Fold 2 與 Fold 5 完全正確。
- Fold 3 表現最弱，主要問題是 COPD false negative。
- 所有 fold 都沒有 false positive。
- 模型的 precision 高於 recall，代表它預測 COPD 時很準，但仍會漏掉一些 COPD。

## 整體混淆矩陣

| 真實類別 | 預測 Normal | 預測 COPD |
|---|---:|---:|
| Normal | 21 | 0 |
| COPD | 4 | 29 |

由此可得：

```text
TP = 29
TN = 21
FP = 0
FN = 4
```

指標計算：

```text
Accuracy = (29 + 21) / 54 = 0.9259
Precision = 29 / (29 + 0) = 1.0000
Recall = 29 / (29 + 4) = 0.8788
Specificity = 21 / (21 + 0) = 1.0000
F1 = 2 * 1.0000 * 0.8788 / (1.0000 + 0.8788) = 0.9355
```

論文解讀：

> The classifier achieved perfect specificity and precision, indicating that normal cases were not falsely classified as COPD. The remaining errors were false negatives, suggesting that the model was conservative and may under-detect mild or protocol-variant COPD cases.

## 錯誤分類個案

`misclassified_samples.json` 記錄四個 false negative：

| 個案 | 真實類別 | 預測 | COPD probability | 錯誤類型 |
|---|---|---|---:|---|
| `4796667_Thorax Lung Br60 S2 3.00` | COPD | Normal | 0.1313 | False Negative |
| `5630846_Aorta C+  5.0  B30f` | COPD | Normal | 0.4609 | False Negative |
| `C543831_Thorax Lung Br60 S2 3.00` | COPD | Normal | 0.2978 | False Negative |
| `8404129_Chest C-  5.0  B31f` | COPD | Normal | 0.4885 | False Negative |

### FN 個案可能原因

1. COPD 影像特徵較 mild 或接近 normal。
2. 部分個案使用 soft kernel 或 thick slice，影響 HU-based emphysema。
3. segmentation 或 airway feature 可能不完整。
4. PFT abnormal 但 CT emphysema 不明顯，造成影像特徵不足。
5. 目前模型偏保守，threshold 0.5 下較不容易把邊界樣本判成 COPD。

### 個案解讀

`8404129` COPD probability = 0.4885，接近 0.5，代表它是邊界樣本。若改變 threshold，可能會被判為 COPD。

`5630846` 與 `8404129` 檔名顯示 5.0 mm 與 soft kernel 相關 protocol，與大多數 3.0 mm lung kernel 不同，這可能影響 emphysema 與 vessel feature。

## 圖表素材

正式結果圖建議使用：

`models/training_20260206_132335`：

- `kfold_confusion_matrix.png`
- `kfold_metrics_boxplot.png`
- `kfold_metrics_comparison.png`
- `kfold_roc_curve.png`

`models` root：

- `fn_samples_comparison.png`
- `fn_samples_radar.png`

`NormalDataset/visualizations` 與 `AbnormalDataset/visualizations`：

- `comparison_bar`
- `correlation_heatmap`
- `feature_distributions`
- `heatmap_all`
- `heatmap_emphysema`

論文章節配置：

| 圖 | 建議位置 |
|---|---|
| Pipeline flowchart | 第三章方法 |
| 12 feature table | 第三章方法 |
| Confusion matrix | 第四章結果 |
| ROC curve | 第四章結果 |
| Metrics comparison | 第四章結果 |
| FN radar/comparison | 第四章討論 |
| Feature distribution | 第四章討論 |

## `unified_pipeline.py` 實驗流程

`unified_pipeline.py` 是端到端整合流程。常見參數：

| 參數 | 功能 |
|---|---|
| `-i/--input` | 輸入 CT NIfTI |
| `-o/--output` | 輸出資料夾 |
| `--seg` | 指定既有 segmentation label |
| `--airway` | 指定既有 airway segmentation |
| `--batch` | 批次模式 |
| `--skip-seg` | 跳過 segmentation |
| `--no-predict` | 只算參數，不做分類 |
| `--viz-only` | 只產生視覺化 |
| `--model-path` | 指定 classifier model |
| `--scaler-path` | 指定 scaler |
| `--server` | 指定 3D Slicer server |
| `--device` | 指定 CPU/GPU |

可整理成 pipeline：

```text
Input CT NIfTI
    ↓
Segmentation label map
    ↓
Airway segmentation search or fallback
    ↓
COPDAnalyzer feature extraction
    ↓
Feature normalization
    ↓
COPDClassifier prediction
    ↓
Metrics JSON + probability + visualization/report
```

## 論文方法章可直接使用的描述

以下是一段可放入第三章的草稿：

> 本研究提出一套基於胸部 CT 影像之 COPD 自動分類流程。首先，將原始 DICOM 影像轉換為保留 HU 值與空間資訊之 NIfTI volume。接著，透過 3D Slicer 中的 MONAI Auto3DSeg inference server 產生肺部多類別 label map，包含左右肺葉、血管、氣管與肺動脈等結構。根據 segmentation label 與 CT HU 值，本研究計算全肺與肺葉別 emphysema percentage、小血管體積比例、氣道壁比例、血管密度、氣道肺體積比例、總肺體積與肺動脈直徑等 12 個定量特徵。所有特徵經 StandardScaler 標準化後輸入多層感知器分類模型，並以 stratified five-fold cross validation 評估 normal 與 COPD/abnormal 之分類效能。

## 論文結果章可直接使用的描述

以下是一段可放入第四章的草稿：

> 在 54 例胸部 CT 資料中，包含 21 例 normal 與 33 例 COPD/abnormal。本研究使用 stratified five-fold cross validation 評估分類模型。最佳正式模型結果顯示，整體 accuracy 為 0.9259，precision 為 1.0000，recall 為 0.8788，F1-score 為 0.9355，AUC 為 0.9784。混淆矩陣顯示所有 normal 個案皆被正確分類，specificity 達 1.0000；模型錯誤主要來自 4 例 COPD 個案被誤判為 normal。此結果表示模型對 normal 與 COPD 的區分具有良好能力，但仍需改善 mild 或 protocol-variant COPD 個案之偵測敏感度。

## 本實驗的科學原理

### 為什麼 CT 可以分類 COPD

COPD 不只影響肺功能，也會改變肺部結構：

- 肺氣腫造成肺實質低衰減區增加。
- 小血管可能因肺泡破壞與 vascular remodeling 而減少。
- 氣道壁可能增厚。
- 肺部可能 hyperinflation。
- 肺動脈形態可能與肺血管壓力或疾病狀態相關。

因此，CT 影像中的 HU distribution、segmentation volume 與解剖比例可以提供 COPD 相關資訊。

### 為什麼使用定量特徵而不是直接看整張 CT

本研究資料量較小，直接訓練 end-to-end 3D CNN 會有高過擬合風險。定量特徵方法有幾個優點：

1. 特徵可解釋。
2. 需要較少資料。
3. 可結合臨床已知 biomarker。
4. 模型較輕量。
5. 容易分析錯誤個案。

### 為什麼使用 -950 HU

肺氣腫在 CT 上呈現低密度。-950 HU 是常用於 inspiratory CT emphysema quantification 的 threshold，可作為 low attenuation area 的定量門檻。本研究使用此 threshold 是因為它簡單、可解釋，且與既有文獻常見做法相近。

### 為什麼需要分肺葉

只看 total emphysema 可能忽略分布型態。不同肺葉的 emphysema 分布可能反映不同 disease phenotype。因此本研究不只使用 total emphysema percent，也使用五個肺葉的 emphysema percent。

### 為什麼需要血管與氣道特徵

COPD 不只是 emphysema。不同病人可能以 airway disease、vascular change 或 emphysema 為主要表現。加入血管與氣道 feature 可以讓模型捕捉更多 phenotype。

## 實驗限制

1. 樣本數只有 54 例，仍屬小樣本研究。
2. 目前是 normal vs COPD/abnormal 二元分類，不是 GOLD 1-4 staging。
3. PFT/GOLD label 尚未完整整合進主模型。
4. CT protocol 有異質性，包含 kernel、slice thickness、scanner model 差異。
5. Airway segmentation 結果常為 OBJ，限制 WA% 的可靠性。
6. PA:A ratio 尚未完成，因缺少 aorta diameter。
7. Segmentation 尚未和人工標註做正式 Dice/accuracy 驗證。
8. External validation 尚未完成。
9. False negative 個案顯示模型對部分 mild 或 protocol-variant COPD sensitivity 仍需改善。

## 未來工作

1. 整合 20260421 的 12 例新增 normal 作為 external validation。
2. 將 PFT FEV1/FVC 與 FEV1 predicted 正式整合，建立 GOLD severity label。
3. 重新訓練多分類模型，從 binary classification 擴展到 severity staging。
4. 統一 airway segmentation 為 voxel mask，改善 WA%。
5. 加入 aorta segmentation 或人工量測，完成 PA:A ratio。
6. 比較 fixed -950 HU 與 adaptive emphysema threshold。
7. 對 segmentation 做人工抽樣 QC 或 Dice validation。
8. 使用 protocol subgroup 分析模型對 lung kernel、soft kernel、thin/thick slice 的穩定性。
9. 評估是否加入 nnMamba 或其他 3D model 作為 end-to-end comparison。

## 寫論文時的注意事項

1. 不要把本研究寫成完整 GOLD staging；目前主結果是 binary classification。
2. 不要說 PA:A ratio 已完成；目前主要是 PA diameter。
3. 不要過度宣稱 WA% 是精準 airway wall measurement，因 airway mask 格式有限。
4. 不要把舊 PDF 或 MosMed 早期結果混入正式 54 例結果。
5. 寫 AUC、accuracy、confusion matrix 時以 `training_20260206_132335` 為準。
6. 若提 PFT/GOLD，要說明目前是依 FEV1 predicted 初步分組，正式 COPD staging 還需 FEV1/FVC。
7. 若提 EmphysemaSeg，要注意它的 label order 與 `COPDAnalyzer` 不同。

## 可以直接放進摘要的版本

> 本研究建立一套胸部 CT 影像之 COPD 自動分類流程，結合自動肺部結構分割、影像定量特徵萃取與神經網路分類模型。研究資料包含 54 例胸部 CT，其中 normal 21 例、COPD/abnormal 33 例。系統首先由 CT 影像產生肺葉、血管與氣道相關 label map，接著計算全肺與肺葉別肺氣腫比例、小血管體積比例、氣道壁比例、血管密度、氣道肺體積比例、總肺體積與肺動脈直徑等 12 個定量特徵。分類模型採用多層感知器並以 stratified five-fold cross validation 評估。實驗結果達到 accuracy 0.9259、F1-score 0.9355 與 AUC 0.9784，顯示 CT 定量特徵對 COPD 自動分類具有潛力。

