# AeroPath 氣道分割整理

`AeroPath` 是本研究用來產生 airway segmentation 的主要工具資料夾之一。它包含 AeroPath 專案程式、Gradio/Docker 執行方式、批次輸出、OBJ 3D model 與 NIfTI airway segmentation。此資料夾可支撐論文中的 airway segmentation 方法、related work，以及 WA% / airway-lung ratio 的資料來源說明。

## 資料夾定位

可支撐論文：

- 第二章：airway segmentation related work。
- 第三章：airway segmentation 工具與流程。
- 第五章：airway mask 格式限制與 future improvement。

## 整體內容

掃描到的主要資料型態：

- `.nii.gz`：CT input、airway prediction、lung annotation。
- `.obj`：airway 3D model。
- `.py`：Gradio GUI、batch processing、best segmentation 選擇。
- `.md` / `.txt`：README、license、output report。
- `.yml` / `.sh` / Docker 相關檔：環境與執行方式。

主要資料夾：

| 資料夾 | 內容 |
|---|---|
| `data` | 放入要跑 AeroPath 的 CT NIfTI |
| `batch_results` | 批次處理輸出，含 airway NIfTI 與 OBJ |
| `output` | 不同 autosave 批次與 best-per-patient 結果 |
| `demo` | Gradio demo 與處理程式 |
| `predict` | 推論相關程式或入口 |
| `shell` | 執行腳本 |

## AeroPath 原始用途

AeroPath 是氣道分割資料集/模型工具，目標是從胸部 CT 自動產生 airway tree segmentation。README 提到可透過：

- Gradio app。
- Docker。
- Hugging Face Space。
- Zenodo/Hugging Face 資料。

使用上可把它定位為 airway segmentation backend，而不是 COPD classifier 本身。

## 本研究中的實際用途

在本研究中，AeroPath 用來：

1. 將 CT NIfTI 輸入 airway segmentation model。
2. 輸出 airway segmentation NIfTI 或 airway OBJ 3D model。
3. 供 `COPDAnalyzer` 計算 airway-related biomarkers。

airway-related biomarkers 包含：

- WA%
- airway-lung ratio
- 可能的 airway volume

## `data` 資料夾

`AeroPath/data` 放了大量醫院 CT NIfTI，作為批次處理輸入。這些包含 normal 與 abnormal hospital CT，不是 AeroPath 原始公開 27 cases 的乾淨資料結構，而是本研究拿來跑 airway segmentation 的 input pool。

## `batch_results`

`batch_results` 有 `study_0001` 到 `study_0033` 類型的輸出。每個 case 通常包含：

- `*_airway_seg.nii.gz`
- `*.obj`

這代表 AeroPath 有成功輸出 airway mask 與 3D airway model。可用於：

- 檢查 airway tree 是否合理。
- 後續轉入 `COPDClassification`。
- 生成 airway 3D figure。

## `output`

`output` 中有多個批次：

- `batch_results_20251214_135626_autosave`
- `batch_results_20251215_061508_autosave`
- `best_per_patient`

autosave 表示批次處理過程中每處理成功一筆會保存結果，避免長時間運算中斷後全部遺失。

`best_per_patient` 是從多個輸出中挑選每位病人最佳 airway segmentation 的結果，與 `select_best_segmentation.py` 相關。

## `select_best_segmentation.py`

此腳本用於從多個 airway output 中挑選最佳結果。主要邏輯：

1. 依 patient ID 分組。patient ID 通常取檔名前綴。
2. 排除品質較差或不合適的 series，例如 COR、SAG、HRCT COR、HRCT_、Snapshot。
3. 以 OBJ 檔案大小作為 airway tree 完整度 proxy。
4. 排除 OBJ 小於 500 KB 的結果，因為可能 airway tree 不完整。
5. 在同一 patient 內選擇最大且有效的 OBJ/NIfTI 組合。
6. 產生 `selection_report.txt`。

可寫入論文或補充方法：

> For patients with multiple airway predictions, the output with the largest valid airway model size was selected after excluding non-axial or reformatted series.

要注意：檔案大小只是 proxy，不等於真正 segmentation accuracy。正式論文最好說成 heuristic selection。

## Gradio demo 流程

`demo/src/gui.py` 內有單檔與批次處理：

### 單檔處理

流程概念：

1. 接收 CT NIfTI。
2. 呼叫 `run_model` 產生 prediction。
3. 呼叫 `nifti_to_obj` 將 prediction 轉成 OBJ。
4. 載入 CT 與 prediction，供 2D/3D 顯示。

### 批次處理

功能：

- 支援多個檔案批次輸入。
- 每個 CT 約需數分鐘，註解中有約 8 分鐘/CT 的估計。
- 每處理成功一筆自動保存 ZIP。
- 產生 batch report。
- 輸出命名可變成 `{file_name}_airway_seg.nii.gz` 與 `.obj`。

這對研究流程很實用，因為 airway segmentation 比較耗時，中斷風險高。

## 與 COPDClassification 的連接問題

`COPDClassification/unified_pipeline.py` 會嘗試尋找：

```text
../airway/{base_name}_airway_seg.nii.gz
```

但目前主資料夾中看到很多 airway 結果是 `.obj`。因此有幾個可能狀況：

1. 有 NIfTI airway mask：可直接計算 airway feature。
2. 只有 OBJ：可視覺化 airway tree，但不一定能直接計算 voxel-based WA%。
3. 沒有 airway：程式 fallback 到 segmentation label 7 或跳過部分 airway feature。

論文中應說明 airway segmentation 的可用性與限制，避免過度宣稱所有個案都有精準 airway wall/lumen mask。

## 論文可寫方法段落

可寫成：

> Airway segmentation was performed using AeroPath. Input CT volumes were processed through the AeroPath inference pipeline, which generated airway masks and 3D airway surface models. For cases with multiple candidate outputs, a heuristic selection procedure excluded reformatted or low-quality series and selected the output with the largest valid airway model. The resulting airway information was used to derive airway-related quantitative features when voxel masks were available.

## 可放的圖

可考慮放：

- airway OBJ 3D rendering。
- CT slice + airway overlay。
- best segmentation selection flowchart。

目前圖檔多為 OBJ/NIfTI，若要放論文需要另外截圖或用 3D Slicer 產生 PNG。

## 限制

1. AeroPath output 格式混合 NIfTI 與 OBJ。
2. OBJ 不能直接取代 voxel mask 進行體積計算。
3. 以檔案大小挑選最佳 segmentation 是 heuristic。
4. 沒有人工 airway annotation 作為 quantitative validation。
5. 小氣道 wall/lumen 分割未必可靠。

## 後續建議

1. 統一 airway output 成 NIfTI mask。
2. 補一份 table：每例是否有 airway NIfTI、是否只有 OBJ、是否 fallback。
3. 對 FN 個案檢查 airway segmentation 是否失敗。
4. 若要強化 WA%，可以考慮 SlicerVMTK 或人工中心線量測。

