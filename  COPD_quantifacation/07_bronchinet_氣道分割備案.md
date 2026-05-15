# bronchinet 氣道分割備案整理

`bronchinet` 是一套 airway segmentation framework，主要基於 3D CNN / U-Net 類模型進行 chest CT airway tree segmentation。它在本研究中比較適合作為備案工具、related work 或 future comparison，不是目前主分類結果的核心來源。

## 資料夾定位

可支撐論文：

- 第二章：airway segmentation related work。
- 第五章：future work，將 AeroPath 與 bronchinet 比較。
- 方法備案：若 AeroPath airway mask 不完整，可改用 bronchinet 重跑。

## 主要內容

掃描到的研究檔案包含：

- Python 程式約 89 個。
- NIfTI 測試影像約 10 個。
- shell script。
- 預訓練 model 檔。
- README 與設定檔。

主要資料夾：

| 資料夾 | 內容 |
|---|---|
| `Images` | 測試 CT NIfTI，如 `periDown_0001_0000.nii.gz` 到 `periDown_0010_0000.nii.gz` |
| `models` | 預訓練模型與 config |
| `src` | bronchinet 主程式 |
| `scripts` | shell script |
| `tests` | 測試 |

## 模型與設定

`models` 中可見：

- `model_trained_torch.pt`
- `model_trained_keras.hdf5`
- `configparams.txt`
- `run_model_trained.sh`

表示此資料夾包含可推論的 PyTorch/Keras 模型。若要實際用於本研究，需要確認：

- 輸入 spacing / intensity normalization。
- output airway mask label。
- 是否支援本研究 CT protocol。
- GPU/環境是否可跑。

## src 程式架構

`src` 可分為幾類：

### Data preparation

相關程式：

- `prepare_data.py`
- `compute_boundingbox_images.py`
- 其他 preprocessing scripts

用途：

- 建立工作資料夾。
- 準備 CT images、airway labels、lung masks。
- 可能計算 bounding box 或 crop region。

### Experiment scripts

相關程式：

- `distribute_data.py`
- `train_model.py`
- `predict_model.py`

用途：

- 分割 train/validation/test。
- 訓練模型。
- 使用模型預測 airway probability map。

### Evaluation and post-processing

相關程式：

- `postprocess_predictions.py`
- `process_predicted_airway_tree.py`
- `compute_result_metrics.py`
- `compute_result_metrics_diffthres.py`

用途：

- 對 prediction 做 threshold。
- 取 connected component。
- skeleton/thinning。
- 計算 airway tree metrics。
- 比較不同 threshold。

### Utility scripts

用途：

- 影像轉換。
- plotting。
- morphology operation。
- airway tree processing。

## README 中的典型流程

資料結構通常需要：

```text
Images/
Airways/
Lungs/
CoarseAirways/
```

其中 `Airways` 是 airway annotation，`Lungs` 是 lung mask，`CoarseAirways` 是可選輸入。

工作資料夾通常包含：

```text
BaseData -> data directory
Code -> bronchinet code
```

典型命令：

```bash
python prepare_data.py --datadir=<path_data_dir>
python distribute_data.py --basedir=<path_work_dir>
python train_model.py --basedir=<path_work_dir> --modelsdir=<path_output_models>
python predict_model.py <path_trained_model> <path_output_work_probmaps> --basedir=<path_work_dir> --in_config_file=<path_config_file>
```

後續還要 postprocess prediction、process airway tree、計算 metrics。

## 與主研究的關係

目前主分類實驗沒有證據顯示 bronchinet 的輸出已被整合進 54 例 `COPDClassification/param`。因此論文不能說主結果使用 bronchinet。

建議定位：

- AeroPath 的 alternative。
- 相關研究中的 airway segmentation model。
- future work：比較 AeroPath vs bronchinet 對 WA%、airway-lung ratio 與分類結果的影響。

## 可寫入論文的 related work

可描述為：

> bronchinet is a deep learning framework for airway tree segmentation from chest CT. It provides preprocessing, model training, prediction, post-processing, and airway-tree metric computation modules. In this study, it was considered as an alternative airway segmentation approach, while the main pipeline used the available AeroPath-derived airway outputs.

## 限制

1. 目前只看到測試 NIfTI 與預訓練模型，未看到 54 例 COPD 資料完整 bronchinet 結果。
2. 需要 airway annotation 才能正式訓練或評估。
3. 需要建立符合 bronchinet 要求的資料結構。
4. 若輸出 probability map，還需 threshold 與 post-processing 才能進入定量計算。

## 後續建議

1. 取 5-10 例與 AeroPath 交叉比較 airway output。
2. 建立 airway mask volume、branch count、tree length 等 QC 指標。
3. 若 bronchinet 輸出更穩定，可替代 AeroPath 的 OBJ-only 問題。

