# CTEmphysemaScore Visual Score 備案整理

`CTEmphysemaScore` 是一個 slice-wise emphysema visual score prediction 的備案專案。它的目標不是直接做 normal/COPD classification，而是對 CT 切片或左右肺預測 emphysema visual score。此資料夾目前缺少正式 pretrained weights 與完整標籤，因此不建議作為主論文結果，但很適合寫入 related work、future work 或 severity scoring 延伸方向。

## 資料夾定位

可支撐論文：

- 第二章：visual emphysema score 與 CT-based severity assessment。
- 第五章：未來可加入 visual score regression 或 severity staging。

## 主要內容

主要資料夾位於 `CTEmphysemaScore/eval_scan`：

| 檔案/資料夾 | 用途 |
|---|---|
| `README.md` | 使用說明 |
| `MODELS.md` | 模型權重狀態與訓練說明 |
| `eval_scan.py` | 對單一 scan 做 visual score inference |
| `eval_scan_config.yml` | 推論設定 |
| `train_example.py` | minimal training example |
| `src/datasets` | dataset 讀取 |
| `src/transforms` | CT window、crop、mask、tensor transform |
| `src/models` | ResNet 等模型 |
| `data/E797258.nii.gz` | 範例 CT |

## eval_scan_config.yml

重要設定：

```yaml
model_path: models/ResNet18/best_model_1_1.pt
model: ResNet18
batch_size: 64
num_workers: 8
save_dir: results
verbose: true
device: cuda:0
slice_spacing: 5
```

模型設定：

```yaml
input_channels: 3
num_classes: 1
```

代表模型是 regression style，輸出一個 visual score。

## CT transform

設定中包含：

- `WindowCT`
  - window center：-650
  - window width：800
  - output range：0-1
- `CropObject`
  - output shape：512 x 512
- `ApplyMask`
- `ToTorchTensor`

Segmentation/mask 相關設定：

- threshold：-200
- median kernel：3
- cleaning ball radius：[3, 3]
- compression factor：0.25
- erosion：5 次，radius 1
- dilation：3 次，radius 3

此流程會先把 CT 做 lung-related preprocessing，再抽 slice 輸入 ResNet。

## MODELS.md 重點

此資料夾沒有完整正式 pretrained model weights。`MODELS.md` 說明可能選項：

1. 下載正式權重。
2. 使用 CSV 標籤訓練模型。
3. 使用 dummy weights 做功能測試。

訓練資料 CSV 需要欄位類似：

```text
ct_fn,single_lung_mask_fn,10score
```

這表示模型需要 visual emphysema score 標籤。目前本研究主資料沒有看到完整 visual score 標註，因此不能把此模型結果當作正式 COPD classification 結果。

## train_example.py

`train_example.py` 示範：

- 建立 `ResNet18(num_classes=1, input_channels=3)`。
- 使用 `NiiChunkDataset`。
- 使用 regression trainer。
- Optimizer：Adam，learning rate 1e-4。
- 儲存模型到 `models/ResNet18/best_model_1_1.pt`。

可作為未來訓練 emphysema visual score model 的起點。

## 與主研究的關係

目前主論文結果不應使用 CTEmphysemaScore 作為已完成實驗，原因：

- 缺少正式權重。
- 缺少 54 例完整 visual score label。
- 只看到 `E797258.nii.gz` 範例資料。
- 它輸出 visual score，不是直接 normal/COPD classifier。

可用定位：

- 未來 severity quantification。
- 與 PFT/GOLD severity label 結合。
- 作為 radiologist visual score 的自動化替代。

## 可寫入論文的 future work

可寫成：

> Future work may incorporate slice-wise emphysema visual score prediction. The CTEmphysemaScore pipeline provides a ResNet18-based regression framework that estimates emphysema scores from preprocessed CT slices. With radiologist visual score annotations or validated pretrained weights, this approach could complement the current quantitative HU-threshold features and support COPD severity staging.

## 限制

1. 目前不是主分類實驗的一部分。
2. 模型權重不完整或未確認。
3. 需要 visual score labels。
4. 與 GOLD severity 的關係需另外驗證。
5. 只可作備案，不可寫成正式結果。

## 後續建議

1. 若能取得 radiologist emphysema visual score，建立訓練 CSV。
2. 用 54 例 CT 產生 left/right lung score。
3. 分析 visual score 與 LAV950、PFT FEV1%、COPD label 的相關性。
4. 將 visual score 加入 12 維 feature，測試是否改善 FN。

