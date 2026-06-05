# TAP-CT Late Fusion Architecture for GOLD 2026 Classification

## 1. Overall Architecture

本模型採用 **late fusion** 架構，將兩種 patient-level representation 串接後進行 GOLD 2026 五分類：

1. **3D CT branch**
   - Trainable Hybrid Mamba-Attention encoder
   - 從 3D CT volume 擷取 352-dimensional image feature

2. **TAP-CT branch**
   - Frozen TAP-CT-B 3D model
   - 使用預先擷取的 patient-level TAP-CT embedding
   - 原始 embedding 為 2304-d，經 projection 壓縮為 128-d

3. **Late fusion classifier**
   - 將 CT feature 與 TAP-CT feature concatenate
   - Fusion vector = 352 + 128 = 480-d
   - 經 MLP classifier 輸出 5 個 GOLD 2026 logits

---

## 2. Model Configuration

| Item | Value |
|---|---:|
| Model name | `hybrid_mamba_tapct_fusion` |
| Task | GOLD 2026 five-class classification |
| CT input channels | 1 |
| CT input size | `1 x 112 x 136 x 112` |
| Base channels | 32 |
| Mamba blocks per stage | 3 |
| Attention layers | 1 |
| Attention heads | 8 |
| Attention MLP ratio | 2.0 |
| Attention dropout | 0.1 |
| TAP-CT embedding dim | 2304 |
| TAP-CT projection dim | 128 |
| Fusion dropout | 0.1 |
| Classifier hidden dim | 256 |
| Classifier dropout | 0.3 |
| Output classes | 5 |

---

## 3. Parameter Count Summary

> Note: TAP-CT-B itself is frozen and used as a precomputed feature extractor.  
> The parameter count below refers to the trainable late-fusion model after TAP-CT embeddings are loaded.

| Component | Trainable Parameters |
|---|---:|
| Full late-fusion model | 1,484,709 |
| CT image encoder | 1,028,384 |
| TAP-CT embedding projection branch | 299,648 |
| Fusion classifier head | 156,677 |

---

## 4. CT Branch: Hybrid Mamba-Attention Encoder

### 4.1 CT Input

| Layer | Operation | Output Shape |
|---|---|---|
| Input | 3D CT volume | `B x 1 x 112 x 136 x 112` |

---

### 4.2 Stem Layer

| Component | Detail |
|---|---|
| Conv3D | `in_channels=1`, `out_channels=32`, `kernel_size=7`, `stride=4`, `padding=3`, `bias=False` |
| Normalization | GroupNorm, `num_groups=8`, `num_channels=32` |
| Activation | GELU |
| Output shape | `B x 32 x 28 x 34 x 28` |
| Parameters | 11,040 |

---

### 4.3 Stage 1

| Component | Detail |
|---|---|
| Input shape | `B x 32 x 28 x 34 x 28` |
| Downsample conv | Conv3D `32 -> 32`, `kernel_size=3`, `stride=1`, `padding=1`, `bias=False` |
| Normalization | GroupNorm, `num_groups=8`, `num_channels=32` |
| Activation | GELU |
| Mamba blocks | 3 Residual Mamba Blocks |
| Output shape | `B x 32 x 28 x 34 x 28` |
| Stage parameters | 59,392 |

#### Stage 1 Parameter Breakdown

| Sub-layer | Parameters |
|---|---:|
| Initial Conv3D + GroupNorm + GELU | 27,712 |
| Residual Mamba Block 1 | 10,560 |
| Residual Mamba Block 2 | 10,560 |
| Residual Mamba Block 3 | 10,560 |

---

### 4.4 Stage 2

| Component | Detail |
|---|---|
| Input shape | `B x 32 x 28 x 34 x 28` |
| Downsample conv | Conv3D `32 -> 64`, `kernel_size=3`, `stride=2`, `padding=1`, `bias=False` |
| Normalization | GroupNorm, `num_groups=8`, `num_channels=64` |
| Activation | GELU |
| Mamba blocks | 3 Residual Mamba Blocks |
| Output shape | `B x 64 x 14 x 17 x 14` |
| Stage parameters | 169,472 |

#### Stage 2 Parameter Breakdown

| Sub-layer | Parameters |
|---|---:|
| Initial Conv3D + GroupNorm + GELU | 55,424 |
| Residual Mamba Block 1 | 38,016 |
| Residual Mamba Block 2 | 38,016 |
| Residual Mamba Block 3 | 38,016 |

---

### 4.5 Stage 3

| Component | Detail |
|---|---|
| Input shape | `B x 64 x 14 x 17 x 14` |
| Downsample conv | Conv3D `64 -> 128`, `kernel_size=3`, `stride=2`, `padding=1`, `bias=False` |
| Normalization | GroupNorm, `num_groups=8`, `num_channels=128` |
| Activation | GELU |
| Mamba blocks | 3 Residual Mamba Blocks |
| Output shape | `B x 128 x 7 x 9 x 7` |
| Stage parameters | 652,288 |

#### Stage 3 Parameter Breakdown

| Sub-layer | Parameters |
|---|---:|
| Initial Conv3D + GroupNorm + GELU | 221,440 |
| Residual Mamba Block 1 | 143,616 |
| Residual Mamba Block 2 | 143,616 |
| Residual Mamba Block 3 | 143,616 |

---

## 5. Residual Mamba Block Details

Each Residual Mamba Block follows:

```text
Input feature map
  -> GroupNorm
  -> 1x1x1 Conv3D projection
  -> reshape 3D feature map into token sequence
  -> Mamba sequence mixer
  -> reshape tokens back to 3D feature map
  -> GroupNorm
  -> 1x1x1 Conv3D projection
  -> residual addition
  -> GELU