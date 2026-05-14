# EmphysemaSeg 肺氣腫分割整理

`EmphysemaSeg` 是肺葉分割與 emphysema quantification 的備案工具。它可以從 chest CT `.nii.gz` 產生 lobe segmentation、emphysema mask、LAV threshold 統計與 PNG 視覺化。主實驗目前仍使用 `COPDClassification` 內的 -950 HU emphysema 計算，但 `EmphysemaSeg` 可作為方法比較或補充分析。

## 資料夾定位

可支撐論文：

- 第二章：肺氣腫 CT quantification 方法。
- 第三章：備用 lobe/emphysema segmentation 方法。
- 第四章：若補跑結果，可作 emphysema feature 對照。
- 第五章：未來整合更完整 emphysema pattern analysis。

## 主要資料夾

| 資料夾/檔案 | 內容 |
|---|---|
| `backup` | 大量醫院 CT NIfTI 備份，約 88 個 |
| `data` | 輸入 NIfTI 位置，少量檔案 |
| `seg` | segmentation output，包含 lobe 與 emphysema NIfTI |
| `clip` | axial/coronal/sagittal PNG 視覺化 |
| `EmphysemaSeg` | Python package |
| `config.YAML` | inference/quantification 設定 |
| `0911_TS_best_model.pth` | segmentation model weight |
| `Start.txt` | 執行提示 |
| `README.md` | 使用說明、限制與效能描述 |

## README 重點

工具目標：

- automatic lobe segmentation。
- emphysema quantification。
- 輸出 lobe label maps。
- 以 HU threshold 計算 low attenuation volume。
- 產生視覺化。

適用 CT 條件：

- chest CT。
- voxel dimension 約 0.5-1 mm x 0.5-1 mm x 0.5-1.25 mm。
- emphysema quantification 對 soft kernel 較可靠。

效能描述：

- runtime 約 1 分 20 秒。
- RAM < 12 GB。
- VRAM 約 6.5 GB。
- 以 512 x 512 x 400 volume 為參考。

重要限制：

- emphysema 對 reconstruction kernel 很敏感。
- hard kernel 可能造成 emphysema 估計偏差。
- 本研究主資料多數為 lung kernel，使用此工具的 emphysema 結果要特別小心。

## config.YAML

設定重點：

```yaml
data_dir: ./data/nifti
seg_dir: ./seg
clip_dir: ./clip
model_path: ./0911_TS_best_model.pth
pix_dim: [1, 1, 1]
window: [-1024, 600]
num_workers: 2
```

代表流程會：

1. 從 `data/nifti` 讀取 CT。
2. resample 到 1 mm spacing。
3. 使用 window -1024 到 600。
4. 輸出 segmentation 到 `seg`。
5. 輸出 clipping visualization 到 `clip`。

`Start.txt` 提示：

```bash
EmphysemaSeg --config config.YAML --emp
```

## seg 輸出

`seg` 中可看到多個配對：

- `*_lobe.nii.gz`
- `*_emphysema.nii.gz`

表示每個 CT 可能產生：

- 肺葉分割 label。
- emphysema mask。

掃描結果顯示約有 176 個 NIfTI，符合 88 例 x 2 種輸出。

## clip 視覺化

`clip` 中有約 129 張 PNG，通常是 axial/coronal/sagittal 視覺化結果。

用途：

- 快速 QC segmentation。
- 論文示意圖。
- 比較 lobe 與 emphysema mask。

注意：

- 部分 PNG 檔可能很小，需人工確認是否為空圖或失敗截圖。
- 正式放論文前應挑清楚且有代表性的圖。

## quantification.py

`EmphysemaSeg/quantification.py` 提供更完整的 emphysema quantification。

### Lobe label

此工具的 lobe label：

| Label | Lobe |
|---:|---|
| 1 | RUL |
| 2 | RML |
| 3 | RLL |
| 4 | LUL |
| 5 | LLL |

重要：這和 `COPDAnalyzer` 的 label 定義不同。若混用，肺葉名稱會錯。

### Threshold

支援多個 LAV threshold：

| 指標 | Threshold |
|---|---:|
| LAV950 | HU < -950 |
| LAV910 | HU < -910 |
| LAV856 | HU < -856 |

### 輸出指標

可計算：

- lobar volume。
- emphysema volume。
- LAV%。
- total lung volume。
- lung density statistics。
- mean HU。
- standard deviation。
- 15th percentile。
- 85th percentile。
- min/max HU。
- upper/lower LAV ratio。
- emphysema distribution pattern。

Pattern 可能包含：

- Upper_Lobe_Predominant
- Lower_Lobe_Predominant
- Homogeneous

也可輸出：

- CSV。
- Excel。
- Markdown report。

## 與主實驗的關係

主分類模型目前使用 `COPDClassification` 的 fixed -950 HU feature，並沒有明確使用 `EmphysemaSeg` 的 quantification CSV/Excel 作為 12 維 feature input。

因此論文建議：

- 主結果：引用 `COPDClassification` 的 emphysema feature。
- 補充/未來：`EmphysemaSeg` 可提供多 threshold LAV 與 emphysema distribution pattern。

## 可寫入論文的方法比較

可寫成：

> In addition to the main label-map based emphysema quantification, an EmphysemaSeg pipeline was explored for lobe segmentation and emphysema mask generation. The tool supports LAV950, LAV910, and LAV856 thresholds and can report lobar emphysema distribution. However, because emphysema estimation is sensitive to reconstruction kernel and because the main classification experiment was already based on the unified COPDAnalyzer features, EmphysemaSeg was treated as a supplementary analysis tool.

## 限制

1. Label definition differs from the main COPDAnalyzer.
2. Hard/lung kernel may affect emphysema threshold reliability.
3. Not integrated into the final 12-feature classifier.
4. Some visualization PNGs need QC.
5. Need to verify whether every `seg` output corresponds exactly to the main 54 cases.

## 後續建議

1. 將 main 54 cases 對應到 EmphysemaSeg output。
2. 比較 `COPDAnalyzer` LAV950 與 `EmphysemaSeg` LAV950。
3. 將 upper/lower predominance 作為新 feature 測試是否改善 FN。
4. 對 soft/thick slice FN 個案檢查 EmphysemaSeg 是否更可靠。

