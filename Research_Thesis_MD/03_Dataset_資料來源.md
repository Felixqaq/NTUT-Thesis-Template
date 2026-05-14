# Dataset 資料來源總整理

`Dataset` 是研究資料總倉庫，包含醫院 COPD/normal 原始資料、公開資料集、AeroPath 測試資料、MosMed、LUNA16、EMORY 與其他非主線資料。論文中不能把整個 `Dataset` 都說成主實驗資料；主實驗應明確限定在醫院 54 例 CT。

## 整體內容

掃描到的主要副檔名與資料型態：

| 型態 | 意義 |
|---|---|
| 無副檔名 DICOM | 醫院原始 CT slices，數量最多 |
| `.nii` / `.nii.gz` | NIfTI 影像或 segmentation |
| `.mhd` / `.raw` | LUNA16 或其他醫學影像格式 |
| `.csv` / `.parquet` | MosMed 或 metadata |
| `.md` / `.txt` | 資料說明、報告或整理 |
| `.zip` | 原始壓縮包或模型/資料包 |
| `.pdf` | 資料說明或文獻 |

`Dataset` 中 DICOM 切片超過兩萬檔，不適合逐檔列入論文。論文應以病人、series 與轉換後 volume 為統計單位。

## 主要資料夾

| 資料夾 | 內容 | 與主論文關係 |
|---|---|---|
| `醫院dataset` | 33 位 COPD/abnormal 原始 DICOM | 主實驗 abnormal 來源 |
| `醫院NormalDataset20260116` | 21 位 normal 原始 DICOM | 主實驗 normal 來源 |
| `醫院NormalDataset20260421` | 12 位新增 normal 原始 DICOM | 後續測試/擴充 |
| `AeroPath` | AeroPath airway dataset 或轉存資料 | 氣道分割工具測試/相關工作 |
| `MosMed` | MosMed CT 資料與報告 | 早期 normal/外部資料參考 |
| `Luna16` | LUNA16 lung nodule 資料 | 非 COPD 主線，可作肺部 CT 背景資料 |
| `EMORY` | 外部 CT 資料 | 非主結果 |
| `PericardialEffusion_USB` | 心包膜積液相關資料 | 與 COPD 主線無直接關係 |

## 主論文資料集

正式主實驗資料應寫為：

- Abnormal/COPD：33 例醫院 chest CT。
- Normal：21 例醫院 chest CT。
- Total：54 例。

這 54 例在 `DicomToNii` 完成 DICOM to NIfTI/HU 轉換，並複製/整理到 `COPDClassification` 進行 segmentation、特徵計算與分類。

## 醫院 COPD/abnormal dataset

`醫院dataset` 包含 33 位病人。這些資料是主模型 COPD/abnormal class 的來源。

對應資料流：

1. `Dataset/醫院dataset`：原始 DICOM。
2. `DicomToNii/醫院dataset_nii_hu`：轉換後 NIfTI/HU。
3. `COPDClassification/AbnormalDataset/data`：主分類實驗輸入。
4. `COPDClassification/AbnormalDataset/inference_output`：segmentation label。
5. `COPDClassification/AbnormalDataset/param`：影像定量 JSON。

## 醫院 normal dataset

`醫院NormalDataset20260116` 包含 21 位 normal。這些資料是主模型 normal class 的來源。

對應資料流：

1. `Dataset/醫院NormalDataset20260116`：原始 DICOM。
2. `DicomToNii/醫院NormalDataset20260116_nii_hu`：轉換後 NIfTI/HU。
3. `COPDClassification/NormalDataset/data`：主分類實驗輸入。
4. `COPDClassification/NormalDataset/inference_output`：segmentation label。
5. `COPDClassification/NormalDataset/param`：影像定量 JSON。

## 20260421 新 normal dataset

`醫院NormalDataset20260421` 包含 12 位 normal。這批資料目前還不是主 54 例結果的一部分。

建議用途：

- 外部 validation。
- 測試模型是否會把新增 normal 誤判成 COPD。
- 增加 normal class 後重訓模型。
- 分析不同批次資料對 feature distribution 的影響。

若未重跑 segmentation 與 classification，不建議把這 12 例混入已完成的 accuracy/AUC 敘述。

## AeroPath dataset

`Dataset/AeroPath` 包含 AeroPath 相關 NIfTI。AeroPath 原始公開資料設計是 CT、airway annotation、lung annotation。此資料可用於：

- 氣道分割模型測試。
- 說明 airway segmentation 來源。
- 比較 airway segmentation tool。

但目前主 COPD classification 的 54 例不是直接來自 AeroPath public cohort，因此論文中應把 AeroPath 定位為工具與輔助資料，不是主病人 cohort。

## MosMed

`MosMed` 包含大量 `.nii.gz`、`.csv`、`.parquet` 與報告檔。早期研究可能使用 MosMed CT-0 作 normal 對照。現在主實驗已改為醫院 normal 21 例，因此 MosMed 不建議再作正式主結果。

可寫入：

- 早期資料探索。
- 外部資料參考。
- 不納入最終 54 例模型。

## LUNA16

`Luna16` 主要是 lung nodule CT dataset，常見格式為 `.mhd` / `.raw`。它不是 COPD-specific dataset。

可用定位：

- CT preprocessing 或 lung CT image handling 參考。
- 不納入 COPD classification 主結果。

## EMORY

`EMORY` 是外部資料來源之一。從目前主流程看，尚未整合到 `COPDClassification` 的 54 例主實驗。

可用定位：

- 潛在 external validation。
- 未完成整合。

## PericardialEffusion_USB

`PericardialEffusion_USB` 與心包膜積液相關，和 COPD classification 主題無直接關係。論文中不建議提到，除非只是說明研究資料倉庫包含其他專案資料，已排除不用。

## 論文資料來源寫法

建議寫成：

> 本研究使用來自院內胸部 CT 之 54 例資料，其中 COPD/abnormal 33 例、normal 21 例。原始資料為 DICOM 格式，經自動化轉換流程產生 HU-preserved NIfTI volume。其他公開資料集與外部資料僅作前期方法測試或工具參考，未納入最終模型訓練與評估。

## 需要避免的寫法

不要寫：

- 「本研究使用 Dataset 資料夾全部資料」。
- 「MosMed、LUNA16、AeroPath 都納入主模型訓練」。
- 「PericardialEffusion_USB 是 COPD 資料」。

應寫：

- 主結果基於醫院 54 例。
- 其他資料用於測試、備案、前期探索或未來工作。

## 後續建議

1. 若時間允許，把 12 例 20260421 normal 跑完整 pipeline，作 external normal validation。
2. 建立一個正式 cohort table：patient ID、label、kernel、thickness、scanner、PFT FEV1%、是否納入 training。
3. 將 `Dataset` 中與 COPD 無關資料移到 archive 或在論文中完全不提，避免審查時混淆。

