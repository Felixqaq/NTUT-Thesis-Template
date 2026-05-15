# DicomToNii 資料轉換與 PFT 整理

`DicomToNii` 是整個 COPD 研究的資料前處理核心。它負責把醫院原始 DICOM series 轉成 NIfTI/HU 影像，整理 hospital normal/abnormal dataset，也包含 PFT 圖片轉換、GOLD 分組、影像 protocol 異質性分析與資料組成實驗。

## 資料夾定位

此資料夾可支撐論文：

- 第三章資料前處理：DICOM 讀取、series 選擇、HU 轉換、NIfTI 產生。
- 第三章資料來源：normal 與 COPD 病人資料清單。
- 第四章實驗設定：protocol heterogeneity、kernel/thickness 分布。
- 附錄或補充實驗：PFT/GOLD 分級、protocol robustness。

## 主要資料夾

| 資料夾 | 內容 |
|---|---|
| `醫院dataset` | 33 位 abnormal/COPD 病人的原始 DICOM |
| `醫院NormalDataset20260116` | 21 位 normal 病人的原始 DICOM |
| `醫院NormalDataset20260421` | 12 位新增 normal 病人的原始 DICOM |
| `醫院dataset_nii_hu` | 33 位 abnormal/COPD 轉換後 NIfTI |
| `醫院NormalDataset20260116_nii_hu` | 21 位 normal 轉換後 NIfTI |
| `醫院NormalDataset20260421_nii_hu` | 12 位新增 normal 轉換後 NIfTI |
| `src/convert` | DICOM to NIfTI/HU 轉換程式 |
| `src/pft` | PFT 圖片處理、分組與分析程式 |
| `pft_images_all` | 54 例 PFT JPG 與 `pft.json` |
| `pft_jpg_output` | PFT 圖片輸出與 angle 分析 |
| `heterogeneity_analysis` | CT protocol 異質性分析 |
| `experiment_data` | protocol/subset robustness 實驗資料 |
| `experiment_results` | robustness 實驗圖表 |

## 醫院 abnormal/COPD 原始資料

`醫院dataset` 有 33 位病人：

`1261736`, `1687031`, `1800944`, `2588424`, `2991621`, `3647457`, `4372708`, `4710629`, `4796667`, `5127217`, `5630846`, `6887256`, `8009284`, `8126939`, `8404129`, `8704416`, `9075311`, `9529629`, `A613117`, `A762364`, `B213449`, `C041635`, `C435832`, `C543831`, `C586742`, `C905524`, `D132855`, `D550510`, `E353272`, `E558113`, `E647833`, `E771850`, `E797258`

轉換後輸出在 `醫院dataset_nii_hu`，共 33 個 NIfTI。這 33 例對應 `COPDClassification/AbnormalDataset/data`。

## 醫院 normal 原始資料

`醫院NormalDataset20260116` 有 21 位病人：

`1596038`, `1746380`, `2094528`, `2221276`, `2500824`, `2860903`, `3097765`, `3635301`, `4204917`, `4302294`, `5046455`, `5390303`, `6212308`, `6312603`, `6858508`, `7871759`, `8244460`, `8332556`, `A754735`, `C081146`, `E717248`

轉換後輸出在 `醫院NormalDataset20260116_nii_hu`，共 21 個 NIfTI。這 21 例對應 `COPDClassification/NormalDataset/data`。

## 20260421 新增 normal

`醫院NormalDataset20260421` 有 12 位病人：

`0781915`, `1604378`, `1663485`, `1814107`, `2256243`, `2291134`, `4205212`, `4230847`, `4996166`, `5925853`, `6757504`, `A267542`

轉換後輸出在 `醫院NormalDataset20260421_nii_hu`，共 12 個 NIfTI。這批目前適合當：

- 後續外部測試集。
- normal class 擴充資料。
- 檢驗模型對新資料批次的 generalization。

若要寫進正式結果，需要重新跑 segmentation、參數計算與模型評估，不能直接引用 54 例實驗結果。

## DICOM 轉換程式

主要程式位於 `src/convert`。

### `batch.py`

負責批次轉換所有 patient folder。核心功能：

- `_find_dicom_folder`：尋找病人資料夾內的 DICOM series。
- `_is_excluded_series`：排除不適合的 series。
- `_filter_eligible_series`：篩出可用 CT series。
- `_select_best_series`：挑選最適合 lung analysis 的 series。
- `_protocol_tag`：從 DICOM metadata 或 filename 推估 protocol。
- `_build_output_path`：建立輸出 NIfTI 檔名。
- `_convert_series`：實際執行單一 series 轉換。
- `process_patient_folder`：處理單一病人。
- `batch_convert_all_patients`：批次處理整批資料。

CLI 可依 dataset、output、group、all-series 等參數執行。論文中可以描述為「自動選擇最適合肺部分析之 axial chest CT series」。

### `dicom_reader.py`

負責 DICOM series 讀取與 NIfTI 建立：

- `group_dicom_by_series`：依 SeriesInstanceUID 或相關資訊分組。
- `read_dicom_series`：讀取 DICOM slices。
- `_build_affine`：使用 ImageOrientationPatient、ImagePositionPatient 與 pixel spacing 建立 affine。
- `create_nifti_from_dicom`：建立 NIfTI volume。

可寫進方法：

- 使用 DICOM `RescaleSlope` 與 `RescaleIntercept` 轉換成 HU。
- 依 `ImagePositionPatient` 排序 slices。
- 使用 `ImageOrientationPatient` 建立空間方向。
- 保留 voxel spacing 供後續體積計算。

### `series_filter.py`

主要功能：

- `is_target_series`：判斷 series 是否是目標 chest/lung axial CT。

用途是避免選到 scout、coronal/sagittal reformat、snapshot、非肺窗或不適合分析的 series。

### `protocol_split.py`

負責依 protocol 將 NIfTI 分組：

- `_parse_protocol_from_filename`
- `_classify_kernel`
- `_classify_thickness`
- `split_by_protocol`

可用於分析 lung kernel、soft kernel、thin slice、medium slice、thick slice 對模型表現的影響。

## HU 轉換重點

目前轉檔流程支援：

- JPEG Lossless DICOM decompression。
- `RescaleSlope` / `RescaleIntercept` 轉 HU。
- Siemens Extended CT Scale clamp 到合理 CT HU range。
- 依 DICOM spatial metadata 建立 affine。
- 保留 NIfTI spacing。

這是論文方法中很重要的一段，因為 emphysema threshold 依賴 HU 值。如果 HU 轉換錯誤，-950 HU 的 LAA 計算會完全失真。

## PFT 圖片與 GOLD 分組

`pft_images_all` 有 54 張 JPG 與 `pft.json`。`pft.json` 使用 post-bronchodilator FEV1 percent predicted 進行分組。

### GOLD 1

共 24 筆：

- Abnormal 3 例：`C041635` 87、`C543831` 80、`E797258` 93
- Normal 21 例：所有 20260116 normal 病人，FEV1 predicted 約 83 到 114

### GOLD 2

共 11 筆：

`4372708` 51、`4710629` 73、`4796667` 61、`5127217` 72、`8126939` 61、`9075311` 62、`9529629` 65、`A613117` 66、`A762364` 58、`D132855` 62、`D550510` 60

### GOLD 3

共 13 筆：

`1687031` 36、`1800944` 32、`3647457` 42、`5630846` 44、`6887256` 36、`8009284` 31、`8404129` 39、`8704416` 34、`C435832` 44、`C586742` 33、`C905524` 41、`E647833` 44、`E771850` 48

### GOLD 4

共 6 筆：

`1261736` 26、`2588424` 27、`2991621` 27、`B213449` 19、`E353272` 20、`E558113` 25

重要警語：這個分組目前主要根據 FEV1 % predicted。正式 GOLD COPD staging 通常需要 post-bronchodilator FEV1/FVC < 0.7 作為 COPD airflow limitation 條件。因此論文中應寫成「PFT-derived severity candidate」或「依 FEV1 predicted 初步分組」，不要把 normal 的 GOLD 1 直接說成 COPD GOLD 1。

## PFT 圖片處理程式

`src/pft` 包含：

| 程式 | 用途 |
|---|---|
| `extract_pft_dicom_to_jpg.py` | 從 DICOM 擷取 PFT 圖轉 JPG |
| `dicom_to_jpg.py` | DICOM image to JPG |
| `crop_pft_charts.py` | 裁切 PFT chart |
| `crop_blue_curves.py` | 擷取藍色曲線區域 |
| `create_patient_angle_mapping.py` | 建立 patient 與 curve angle mapping |
| `classify_pft_by_gold.py` | 根據 PFT 指標分類 GOLD |
| `classify_patients.py` | 病人分類 |
| `classify_by_group_and_angle.py` | group 與 angle 分析 |
| `find_optimal_split.py` | 找最佳切分點 |

`pft_jpg_output/patient_angle_classification_by_group.json` 記錄：

| Group | Mean angle | Median | Min | Max |
|---|---:|---:|---:|---:|
| Abnormal 33 | 141.0 | 142 | 105 | 177 |
| Normal 21 | 170.71 | 173 | 140 | 179 |

此 angle 可能是 PFT 圖曲線幾何特徵，不是 CT 解剖角度。若寫入論文，應列為 exploratory PFT image analysis，不應和 CT biomarker 混淆。

`pft_jpg_output/醫院NormalDataset20260421/20260421pft.json` 記錄 12 位新增 normal 的 PFT，皆可初步歸為 GOLD 1 / normal-like FEV1 predicted。

## CT protocol 異質性分析

`heterogeneity_analysis/heterogeneity_index.json` 記錄 54 例主資料的 CT acquisition 差異。

### Manufacturer

| Manufacturer | 數量 |
|---|---:|
| SIEMENS | 31 |
| Siemens Healthineers | 23 |

### Scanner model

| Model | 數量 |
|---|---:|
| SOMATOM Definition AS+ | 27 |
| SOMATOM go.Top | 24 |
| Definition Flash | 2 |
| Sensation 16 | 1 |

### Convolution kernel

| Kernel | 數量 |
|---|---:|
| Br60f | 21 |
| B60f | 17 |
| I70f | 8 |
| Br40f | 3 |
| B30f | 2 |
| I50f | 2 |
| B31f | 1 |

### Slice thickness

| Thickness | 數量 |
|---|---:|
| 3.0 mm | 46 |
| 1.0 mm | 5 |
| 5.0 mm | 3 |

### KVP

| KVP | 數量 |
|---|---:|
| 120 | 26 |
| 100 | 16 |
| 110 | 10 |
| 80 | 1 |
| 130 | 1 |

### Kernel type

| Type | 數量 |
|---|---:|
| Lung | 46 |
| Soft | 6 |
| Unknown | 2 |

### Thickness category

| Type | 數量 |
|---|---:|
| Medium | 46 |
| Thin | 5 |
| Thick | 3 |

可用於論文討論：雖然資料多數為 lung kernel、3.0 mm，但仍存在 soft kernel 與 5.0 mm thick slice，可能影響 emphysema threshold、vessel extraction 與模型 FN。

## Patient grouping

`patient_grouping.json` 顯示：

- Lung kernel：46 例
- Soft kernel：6 例
- Unknown：2 例
- Medium thickness：46 例
- Thin：5 例
- Thick：3 例
- `Lung_Medium`：46 例
- `Soft_Thin`：3 例
- `Soft_Thick`：3 例
- `Unknown_Thin`：2 例

Soft kernel 病人包含：

`5127217`, `5630846`, `8404129`, `9075311`, `8244460`, `8332556`

Unknown kernel 病人包含：

`2094528`, `7871759`

這與主模型 FN 有交集：`5630846` 與 `8404129` 都是 FN 且屬 soft/thick 類型，可作為討論點。

## 異質性圖表

`heterogeneity_analysis` 可用圖表：

- `dataset_parameter_comparison.png`
- `kernel_distribution.png`
- `kernel_type_distribution.png`
- `manufacturer_distribution.png`
- `parameter_combination_heatmap.png`
- `slice_thickness_distribution.png`
- `thickness_category_distribution.png`
- `heterogeneity_report.html`

建議放在第四章「資料異質性分析」或「實驗設定」。

## Protocol robustness 實驗

`experiment_data/experiment_summary.json`：

| Experiment | COPD | Normal |
|---|---:|---:|
| `E1_lung_only` | 32 | 19 |
| `E2_soft_only` | 35 | 24 |
| `E5_mixed_all` | 71 | 46 |

注意：`experiment_data` 中有些檔案是 0 byte placeholder，不可直接當作有效 NIfTI 結果引用。若要正式寫入論文，需要重新確認資料可讀性並重跑實驗。

`experiment_results` 圖表：

- `auc_comparison.png`
- `dataset_composition.png`
- `fold_auc_comparison.png`
- `multi_metric_comparison.png`

目前比較適合作為研究歷程或附錄，不如 `COPDClassification/models/training_20260206_132335` 可靠。

## 論文可寫的方法段落

可以整理成：

1. 收集醫院 chest CT DICOM series。
2. 以自動化腳本依 patient folder 讀取 DICOM metadata。
3. 排除 scout、coronal/sagittal reformat、snapshot 與非目標 chest CT series。
4. 依 SeriesInstanceUID 分組，選擇最適合肺部分析之 axial lung window series。
5. 依 DICOM RescaleSlope 與 RescaleIntercept 將 pixel value 轉換為 HU。
6. 依 ImagePositionPatient 排序 slices，並以 ImageOrientationPatient 建立 NIfTI affine。
7. 輸出 `.nii.gz` 供 segmentation 與 quantitative analysis。
8. 另以 DICOM metadata 統計 scanner manufacturer、kernel、slice thickness、KVP 等 protocol variation。

## 限制與待補

1. PFT/GOLD 分級仍需確認 FEV1/FVC。
2. 20260421 的 12 例新增 normal 尚未整合進主模型結果。
3. Protocol robustness 實驗資料需重檢 0 byte placeholder。
4. 異質性分析可以和 FN 個案交叉分析，這會讓第四章更有說服力。
5. 若要做 GOLD severity classification，需要把 PFT label 正式整合到 `COPDClassification`。

