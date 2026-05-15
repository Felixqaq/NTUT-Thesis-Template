---
title: AI Meeting

---

AI Meeting
====
[TOC]

## 2025/08/19
:::info

- [x] 研究以及訓練張維俊學長的*自我監督式學習應用於醫療影像之研究*
- [ ] 跟學長交接設備以及Code
:::

### Result
Epoch 100
🏆 最佳 Mean Dice: 0.210911 (Epoch 100)
⏰ 總訓練時間: 0:58:12
📊 平均每個 Epoch: 34.9秒
![image](https://hackmd.io/_uploads/S1e1ZTbFex.png)
![image](https://hackmd.io/_uploads/Bk6tB6ZYll.png)

### [Gemini DeepSearch](https://gemini.google.com/app/664764f9799ebfbb?hl=zh-TW)

#### [Execel](https://docs.google.com/spreadsheets/d/17BVYxpkIIjeoIfsSktherlJNoSgU7GsBfSI0dnl47rg/edit?gid=1842215313#gid=1842215313)

DART: Disease-aware Image-Text Alignment and Self-correcting Re-alignment for Trustworthy Radiology Report Generation
生成可信賴且準確的放射學報告
https://cvpr.thecvf.com/virtual/2025/poster/32986


### To Do
寄信給尤老師拿醫院主任資料集
看SSL相關技術
看學長論文去跟現在結果做對比以及看學長CT相關論文技術



## 2025/09/16
:::info
- [x] 跟學長交接設備以及Code
- [x] 跟醫院主任聯絡
- [ ] 看醫生給的資料*2023台灣COPD指引*
- [x] 看[Quantitative CT imaging in chronic obstructive pulmonary disease](https://academic.oup.com/bjr/advance-article/doi/10.1093/bjr/tqaf105/8186037?login=true)
:::

### Result
Quantitative CT imaging in chronic obstructive pulmonary disease
[簡報](https://docs.google.com/presentation/d/1HDB0reRpp7qu4lPIEA8cM0LfHqm4lDAAsotAxQ_ncWA/edit?slide=id.g35e4e1de2cb_0_0#slide=id.g35e4e1de2cb_0_0)
### To Do


## 2025/09/23
:::info
- [x] 看醫生給的資料*2023台灣COPD指引*
:::

### Result
[筆記](https://hackmd.io/MS_egr15SWGwwHDQ7ONKpw?both)

### To Do
* 跟醫生取得小部分資料集跟確認研究主題
* 研究CT如何分辨COPD症狀

## 2025/09/30
:::info
- [ ] 取得小部分資料集
- [x] 確認研究主題
- [x] 研究CT如何分辨COPD症狀
- [x] 研究PFT
:::

### Result
一般COPD患者
![COPD患者](https://hackmd.io/_uploads/Hy39a9knlx.jpg)
預後較差的COPD患者
![特殊病人患者](https://hackmd.io/_uploads/Sklgia5yhex.jpg)
醫生手繪![S__38330451](https://hackmd.io/_uploads/Hkp_ki13gg.jpg)

Pre = 吸入支氣管擴張劑前的數值。
Post = 吸入支氣管擴張劑後的數值。
Ref = 參考值 (根據您的年齡、身高、性別等計算出的預期正常值)。
% Ref = 測量值佔參考值的百分比。
Meas = 測量值

> 每個不同的人都有不一樣的標準，所以%數的分母不同

#### 研究主題
因為這兩種病人在CT上難以看出差異，所以
醫生希望可以結合PFT針對者兩種患者去做判別(沒人做過)

資料及部分
醫生提供原始的肺部CT，還有PFT

其他主題可以再討論，也可以用單純的影像辨識。

[COPD Pocket Guide](https://goldcopd.org/wp-content/uploads/2024/11/Pocket-Guide-2025-v1.0-New-Format-15Nov2024_WMV.pdf)


### 肺功能測試 (PFT) 

#### 第一部分：肺量計測定 (Spirometry)


*   **FVC (Forced Vital Capacity / 用力肺活量)**: 深吸一口氣到最飽後，用最大力量、最快速度呼出的所有氣體總量。
    *   **代表意義**: 您的肺部一次能有效利用的最大容量。

*   **FEV1 (Forced Expiratory Volume in 1 second / 一秒用力呼氣容積)**: 在做 FVC 動作時，第一秒鐘內所呼出的氣體量。

*   **FEV1/FVC % (一秒率)**: FEV1 佔 FVC 的比例。

*   **FEF25-75% (Forced Expiratory Flow 25-75% / 中段用力呼氣流速)**: 在 FVC 呼氣過程中，從 25% 到 75% 這中間一段的平均氣流速度。
    *   **代表意義**: 反映中小氣道的功能。這個數值下降通常是早期氣道阻塞的敏感指標。

*   **PEF (Peak Expiratory Flow / 尖峰呼氣流速)**: 用力呼氣時，瞬間能達到的最快速度。
    *   **代表意義**: 反映大氣道的通暢程度和呼吸肌肉的力量。

*   **PIF (Peak Inspiratory Flow / 尖峰吸氣流速)**: 用力吸氣時，瞬間能達到的最快速度。
    *   **代表意義**: 用於評估上呼吸道（如喉嚨、氣管）是否有阻塞。

*   **VC (Vital Capacity / 肺活量)**: 深吸一口氣到最飽後，緩慢平穩地將氣體完全呼出的總量。有時會比 FVC 大。

#### 第二部分：肺容積 (Lung Volumes)
> 這部分測量的是您肺部各個「空間」的大小，評估肺的總容量以及是否有氣體滯留。可以想像成是測量油箱的「總容量」和「剩餘油量」。
---

*   **Vt (Tidal Volume / 潮氣容積)**: 您在平靜休息狀態下，每次正常呼吸所吸入或呼出的氣體量。

*   **TLC (Total Lung Capacity / 肺總量)**: 肺部所能容納的最大氣體總量（深吸到最飽時肺裡的全部空氣）。
    *   **代表意義**: 評估肺部是變大還是變小。在限制性肺病（如肺纖維化）中會減小；在肺氣腫中可能正常或增大。

*   **RV (Residual Volume / 肺餘容積)**: 當您用力把氣呼到最盡後，仍然殘留在肺裡的空氣量。
    *   **代表意義**: 這個數值如果異常增高，表示有**氣體滯留 (Air Trapping)**，舊的廢氣排不出去，常見於肺氣腫。

*   **FRC (Functional Residual Capacity / 功能肺餘量)**: 當您平靜地呼氣後，肺部自然剩餘的空氣量。

*   **ERV (Expiratory Reserve Volume / 呼氣儲備容積)**: 平靜呼氣後，您還能額外用力呼出去的最大氣體量。

*   **IC (Inspiratory Capacity / 吸氣容量)**: 平靜呼氣後，您還能用力吸進來的最大氣體量。

#### 第三部分：氣體擴散功能 (Diffusion)
> 這部分測量的是氧氣從肺泡進入血液的交換效率。可以想像成是檢查引擎進氣系統的「過濾網」效能好不好。

---

*   **DLCO (Diffusing capacity of the Lungs for Carbon Monoxide / 一氧化碳擴散量)**: 測量一氧化碳（一種示蹤氣體）穿過肺泡-微血管膜進入血液的速度。
    *   **代表意義**: 直接反映氣體交換功能。如果數值下降，表示肺泡壁被破壞（如肺氣腫）或增厚（如肺纖維化），導致氧氣難以進入血液。

*   **VA (Alveolar Volume / 肺泡容積)**: 進行 DLCO 測試時，實際參與氣體交換的肺泡總容積。

*   **DLCO/VA (或稱 KCO)**: 將 DLCO 校正肺泡容積後的值，代表單位肺容積的氣體交換效率。
    *   **代表意義**: 幫助區分 DLCO 下降的原因。例如，如果肺部切除了一半，DLCO 會下降，但 DLCO/VA 可能正常（因為剩下的肺是好的）。如果因為肺氣腫導致整個肺的效率變差，則 DLCO 和 DLCO/VA 都會下降。

*   **IVC (Inspiratory Vital Capacity / 吸氣肺活量)**: 從完全呼氣狀態下，深吸一口氣到最飽的總氣量。通常在 DLCO 測試中測量。

### To Do

### Problem
對於那些 PFT 很差但肉眼 CT 看似正常的病人，模型是否在我們沒注意到的地方發現了微小的病變模式？


## 2025/10/07
:::info
- [ ] 取得小部分資料集
- [x] 找尋現有CT肺部量化開源模型
:::

### Result

#### EmphysemaSegmentation

肺部與肺結核分割
https://github.com/JoHof/lungmask
肺氣腫分割
https://github.com/MASILab/EmphysemaSeg
利用PRM去做自監督學習:
異常檢測不需預先定義 COPD 的特徵或依賴 PRM 所使用的固定閾值
https://www.frontiersin.org/journals/medicine/articles/10.3389/fmed.2024.1360706/full

## 2025/10/14
:::info
- [ ] 取得小部分資料集
- [x] 研究現有CT肺部量化開源模型
:::

### Result

#### Python techical
https://theaisummer.com/medical-image-python/
#### 預處理
precision-medicine-toolbox
https://github.com/primakov/precision-medicine-toolbox?utm_source=chatgpt.com

#### Airway segmentation

https://github.com/antonioguj/bronchinet

AeroPath 
https://github.com/raidionics/AeroPath?tab=readme-ov-file
![image](https://hackmd.io/_uploads/HkU9tf5axg.png)

#### Lung and Vessel Segmentation and Volume Analysis
https://github.com/zaniarshokati/CT_Image_Segmentation
#### PFT
時序性肺功能圖判斷COPD未來風險([data](https://www.ukbiobank.ac.uk/))
Paper https://www.nature.com/articles/s41540-025-00489-y
Github https://github.com/yudaleng/COPD-Early-Prediction

## 2025/10/21
:::info
- [ ] 跟醫生取得資料集
- [x] 研究EmphysemaSeg
- [x] 研究bronchinet
:::

### Result
EmphysemaSeg
Paper
https://pubmed.ncbi.nlm.nih.gov/37469854/
PDF
https://pmc.ncbi.nlm.nih.gov/articles/PMC10353481/pdf/JMI-010-044002.pdf
![image](https://hackmd.io/_uploads/B122NDoale.png)

Airway Segementation
![image](https://hackmd.io/_uploads/SJd_3BQClg.png)




Dataset
LUNA16
https://luna16.grand-challenge.org/Download/
Others
https://zenodo.org/records/5797912
https://zenodo.org/records/6384747
https://zenodo.org/records/6406114
TotalSegmentator
https://zenodo.org/records/10047292


nn-U-Net

## 2025/10/28
:::info
- [x] 取得小部分資料集
- [x] 研究AeroPath論文
- [x] 實作EmphysemaSeg
:::

### Result
#### EmphysemaSeg
![periDown_0001_0000_axial](https://hackmd.io/_uploads/HkzCRoVRel.png)
#### AeroPath
[Paper](https://arxiv.org/abs/2311.01138)
[dataset](https://zenodo.org/records/10069289)
![image](https://hackmd.io/_uploads/B16H052Cle.png)
AG Unet
![image](https://hackmd.io/_uploads/H1cpJin0xl.png)



## 2025/11/4
:::info
- [x] 使用醫院資料集去實作EmphysemaSeg跟AeroPath
- [x] 把醫院檔案轉成.nii.gz
:::
![image](https://hackmd.io/_uploads/H1Aa3d2JZx.png)
![E647833_axial](https://hackmd.io/_uploads/Hkgp4th1-e.png)
![image](https://hackmd.io/_uploads/BkMDqYnk-e.png)
![image](https://hackmd.io/_uploads/Sy8v8q2Jbx.png)

### Result


## 2025/11/11
:::info
- [x] 使用MONAI的MONAI Auto3DSeg "lungs 2.0.1"切割氣道跟血管
:::

### Result
![image](https://hackmd.io/_uploads/ryNKyqn1Ze.png)

E797258
![image](https://hackmd.io/_uploads/r1WLkqhkWl.png)
![image](https://hackmd.io/_uploads/SJXv1chJZg.png)

1261736
LW AXI 3/3  B60f
![螢幕擷取畫面 2025-11-08 174102](https://hackmd.io/_uploads/SkXOg92JWl.jpg)
Chest C-  5.0  B40f
![image](https://hackmd.io/_uploads/SJVed9hJZg.png)


## 2025/11/18
:::info
- [x] 肺氣腫生成實際參數
- [x] 問醫生氣道跟血管如何算出重要的參數
:::

### Result
https://hackmd.io/@kc22zFlwRBKP6GihZ3SYWg/HkJITBxxbx

## 2025/11/25
:::info
- [x] 整理*Machine learning slice‑wise whole‑lung CT emphysema score correlates with airway obstruction*
- [x] 實作三個氣道、血管的指標
- [x] 把3D slicer Seg轉為python實作
:::

### Result
**Machine learning slice‑wise whole‑lung CT emphysema score correlates with airway obstruction**
這篇論文沒有公開權重但是有code
監督式學習
ResNet-18
醫生手標label
從四個嚴重程度分為一張每個slice都有分數 然後 分為10級 
使用FEV1/FVC去做參考依據 跟LAV950比較
概念
![image](https://hackmd.io/_uploads/HymCtN3gWe.png)
實際做法
![image](https://hackmd.io/_uploads/B1R_5N2l-g.png)

{%preview https://hackmd.io/@kc22zFlwRBKP6GihZ3SYWg/By5yhr2lWe %}
[Auto3Dseg Plugin權重](https://github.com/lassoan/SlicerMONAIAuto3DSeg/releases/tag/Models)


## 2025/12/02
:::info
- [x] 檢查DICOM轉NIfTI是否有被壓縮
- [x] 準備正常病人資料集
- [ ] 取得全部資料集的參數
- [ ] 實作分類網路(全連接input:18 output:2 需要正規化)
:::

### Result
1. 像素資料完整保留：
直接讀取 DICOM 的 pixel_array，沒有進行任何縮放或插值，建立 3D numpy 陣列時，使用原始的像素維度：[height, width, num_slices]

2.使用
https://www.kaggle.com/datasets/mathurinache/mosmeddata-chest-ct-scans-with-covid19

## 2025/12/09
:::info
- [x] 取得全部資料集的參數
- [x] 實作分類網路(全連接input:12 output:2)
:::

### Result
1. 使用3D Slicer Auto3DSeg切割
2. 從原始檔抓取肺氣腫區域(<-950HU)生成參數
3. ![image](https://hackmd.io/_uploads/BkR0v6CZbx.png)

## 2025/12/15
:::info
- [x] 使用AeroPath生成氣道標記檔
:::

### Result

## 2025/12/22
:::info
- [x] 5折交叉驗證測試
- [x] 加入AeroPath進行訓練
:::

## 2025/12/30
:::info
- [x] 跟醫生報告目前進度以及詢問正常病人資料集(兩個資料集中，模型可能不是抓到病徵而是CT照片的差異)
- [x] 研究3D模型框架
:::

### Result 
[nnMamba](https://github.com/lhaof/nnMamba)
<!-- ![image](https://hackmd.io/_uploads/B199rMbNWe.png) -->

[SegMamba](https://github.com/ge-xing/SegMamba)
<!-- ![image](https://hackmd.io/_uploads/ByCiSG-Nbx.png) -->

[MedMamba](https://github.com/YubiaoYue/MedMamba)
<!-- ![image](https://hackmd.io/_uploads/SyiKIMWVZx.png) -->
### To Do
跟醫生約時間報告

## 2026/1/7
:::info
- [x] 跟醫生約時間報告
- [x] 研究 and 實作 nnMamba
:::

### Result
**醫生希望可以從 CT 去推斷肺功能(PFT)的狀態**

[nnMamba](https://github.com/lhaof/nnMamba)


![image](https://hackmd.io/_uploads/B199rMbNWe.png)

### Annotation
醫院相關論文發表前要過IRB


## 2026/1/13
:::info
- [x] 研究CT to PFT
:::

### Result
#### Paper

[dbGaP(COPDGene)](https://dbgap.ncbi.nlm.nih.gov/beta/study/phs000179.v7.p2/#study)
教授才能申請

[點雲方式切割血管](https://github.com/multimodallearning/Lung250M-4B)

[Deep Learning–based Approach to Predict Pulmonary Function at Chest CT](https://pubs.rsna.org/doi/epdf/10.1148/radiol.221488)
*Apr 2023 Radiological Society of North America, RSNA*

使用 **I3D** 但是移除最後的 1×1×1 卷積層，取而代之的是Global Average Pooling和一個包含 500 個節點的 Fully Connected Layer 預測出的數值，結合受試者的年齡、身高、性別等參數，利用方程式計算出 FVC% 和 FEV1%

[Deep learning based CT images for lung function prediction in patients with chronic obstructive pulmonary disease](https://www.proquest.com/docview/3268450439?ccountid=14227&sourcetype=Scholarly%20Journals)
Oct 2025 BMC
結合 DenseNet 影像特徵與臨床數據（如年齡、性別）的多模態深度學習模型

[BeyondCT: A deep learning model for predicting pulmonary function from chest CT scans](https://arxiv.org/abs/2408.05645)
Aug 2024 Arxiv
結合 3D CNN（提取局部特徵） 與 Vision Transformer（捕捉全局依賴性） 並融入人口統計數據

#### Dataset 
[OSIC Pulmonary Fibrosis Progression](https://www.kaggle.com/competitions/osic-pulmonary-fibrosis-progression/data)

Paper
https://pubmed.ncbi.nlm.nih.gov/34736226/
https://pmc.ncbi.nlm.nih.gov/articles/PMC8596329/

#### To Do
整理論文結果
根據論文結果報告給醫生

## 2026/1/20
:::info
- [x] 整理論文結果
- [x] 根據論文結果報告給醫生
:::

### Result

#### 醫生想法
一樣分正常病人跟異常病人
希望可以偵測出阻塞的情況，讓病人能根據CT去決定要不要回來做肺功能檢查
醫生說之後可以加入比較輕微的阻塞病人，去區分嚴重性

> 阻塞特徵
> 肺動脈血管大小
> 氣道的大小
> 氣道發炎會導致到末端的進氣量變少，導致末端的血管收縮變小
> 如果肺動脈近末端的血管變小會導致近側端的血管變大
> 單靠肺功能檢查並沒辦法知道原因

>PFT(Saddle shape)
>流量-容積圖 (Flow-Volume Loop)」中，正常的吐氣曲線應該像三角形。如果圖形頂端變平，甚至中間凹下去呈現「雙峰」或「馬鞍狀」，這通常暗示有氣道阻塞。

|研究名稱|模型架構|資料規模|硬體|指標(FVC MAE)|臨床亮點|
|------------------------|------------------------|---------------|-----------------------|---------------------|-----------------------------|
| Park et al. (2023)| I3D CNN (膨脹卷積)| 16,148 |Tesla V100| 0.22 L (CCC 0.94)| 目前誤差最低；高風險群分類準確率 90.2%|
| BeyondCT (Geng et al.) | 3D CNN + ViT| 4,281| RTX 3060| 0.356 L (R² 0.77)   | COPD 識別敏感度高達 95%|
| Li et al. (2025)| DenseNet + MLP (多模態融合)| 2,408| 雙源螺旋 CT| 0.42 L (r 0.81)| 針對 COPD 患者；多模態融合了人口統計數據|
| Fibro-CoSANet| CNN + Self-Attention| 176| Tesla V100 / PyTorch  | RMSE 181.5 mL| 專注於預測 IPF 病程斜率 (LLLm -6.68) |
| Fibrosis-Net| Machine-driven CNN| 200| RTX 2080 Ti / TF| LLLm -6.8188| 極輕量化 (1.38M 參數)，推論僅需 0.053秒 |
#### Annotation
$r$： Pearson 相關係數 (Pearson correlation coefficient)。它是用來衡量「模型預測值」與「實際測量值」之間線性相關程度的指標。有時MAE (絕對誤差) 很低，但 $r$ 很低，代表模型只是在「猜平均值」。$r$ 很高代表模型真的學會了特徵的變化規律。

RMSE (Root Mean Square Error): 均方根誤差

$R^2$ (決定係數)： 回歸分析的標準指標，代表模型能解釋多少變異。

CCC（Lin’s Concordance Correlation Coefficient）: Lin's 一致性相關係數，CCC 同時考慮了數值的精確度（Precision）跟準確度（Accuracy，即觀測值是否偏離 45 度理想線）
公式:
![image](https://hackmd.io/_uploads/rybW_64SWx.png)
![image](https://hackmd.io/_uploads/SyY7uTErZl.png)



LLLm(Modified Laplace Log Likelihood score): 修改後的拉普拉斯對數似然得分，考量了預測的準確性（誤差 Δ）以及模型對該預測的確定性（信心值 $\sigma$），當影像很模糊或充滿雜訊時，模型會自動調高 $\sigma$ (不確定性) 來反映真實情況，數值越大越好 (越接近 0 越好)。

IPF:特發性肺纖維化 (Idiopathic Pulmonary Fibrosis)
### github
Fibrosis-Net
https://github.com/darwinai/FibrosisNet
Fibro-CoSANet
https://github.com/zabir-nabil/Fibro-CoSANet
Park et al. (2023)
https://github.com/mi2rl/PFT_prediction

## 2026/1/27
:::info
- [x] 換成醫院正常病人資料集跑參數分類模型
- [x] 跑nnMamba
:::

### Result
![kfold_confusion_matrix](https://hackmd.io/_uploads/Skcd1hHU-x.png)
![5_emphysema_analysis](https://hackmd.io/_uploads/rJCTkhr8-g.png)


## 2026/2/3
:::info
- [x] 跟醫生回報現在的進度，順便問資料集中的極端資料
- [x] nnMamba做資料增強 300張
- [x] literature survey
:::
### 進度
{%preview https://hackmd.io/iNXCrqQRQCS8Oc09Ue6PEw?view %}

### literature survey
| 年份 | 論文 / 作者 | 主要技術 / 模型 | 數據輸入 (Input) | 主要貢獻與差異點 (Key Contributions) |
| :---: | :--- | :--- | :--- | :--- |
| **2020** | **Humphries et al.** | CNN + LSTM | 25 張軸向 CT 切片 | **自動化 Fleischner 評分**<br>證明深度學習評分比人工視覺評分更能準確預測全因死亡率，將主觀的臨床評分轉化為客觀指標。 |
| **2021** | **Wu et al.** | Vision Transformer (ViT) | CT 影像切塊 (Patches) | **架構突破：首度引入 ViT**<br>應用於肺氣腫亞型分類（CLE, PLE, PSE）。證明在小數據集上透過預訓練微調，ViT 效能優於傳統 CNN。 |
| **2024** | **Zhang et al.** | RFEBNet (CNN) + FCNet | 雙相 CT (吸氣+呼氣) + 臨床文本 | **多模態融合 (影像+文本)**<br>證實「吸氣+呼氣」結合「臨床問卷」診斷效果優於單一模態。強調**呼氣 CT** 對捕捉氣體滯留 (Air Trapping) 的重要性。 |
| **2025** | **Qian et al.** | ResNet18 + Spatial Attention | 預處理後的肺實質 CT 堆疊 | **解決長尾問題 (Long-tail Problem)**<br>引入 Focal Loss 解決類別不平衡（重症樣本少），並透過空間注意力機制強化特徵，專注於 COPD **嚴重度分級**。 |
| **2025** | **Deng et al.** | MMDF-Net (多模態動態融合) | CT + 肺功能 + 環境數據 (PM2.5) | **環境數據整合**<br>首度納入環境暴露數據與基因資訊。使用對比學習對齊異質數據，能根據病患特徵（如吸菸與否）**動態調整**各模態權重。 |
| **2025** | **Zhang et al.** | Generative DL (G-PRM) | 單張 **吸氣** CT | **生成式 AI (Generative AI) 應用**<br>不需拍攝呼氣 CT，直接用 AI 生成呼氣影像來計算 PRM 指標。大幅降低輻射劑量，用於檢測**早期小呼吸道疾病 (fSAD)**。 |
| **2026** | **Yang et al.** | Systematic Review (Meta-Analysis) | 綜合分析 56 篇研究 | **現況總結與痛點分析**<br>指出 DL 在 COPD **二元診斷**（有病/沒病）準確度極高 (Sens 0.87)，但在 **GOLD 多級嚴重度分類** 上表現仍不穩定，準確度較低。 |

### nnMamba Result
![total_cm](https://hackmd.io/_uploads/HJCF3RALZe.png)

## 2026/2/10
:::info
- [x] research *Accuracy of Deep Learning in Diagnosing Chronic
Obstructive Pulmonary Disease: Systematic Review
and Meta-Analysis*
- [x] 檢查結果的錯誤案例是否屬於特殊案例
:::

### Result
![kfold_confusion_matrix](https://hackmd.io/_uploads/ry44QZQPbl.png)

#### FN
4796667_Thorax Lung Br60 S2 3.00
5630846_Aorta C+  5.0  B30f
C543831_Thorax Lung Br60 S2 3.00
8404129_Chest C-  5.0  B31f

![image](https://hackmd.io/_uploads/ry_a2xXDWl.png)
![image](https://hackmd.io/_uploads/SkJR2eXwWx.png)
![image](https://hackmd.io/_uploads/Sksg6x7v-l.png)
![image](https://hackmd.io/_uploads/SyZeTgmDZl.png)
![image](https://hackmd.io/_uploads/H1Ozpgmvbe.png)
![fn_samples_radar](https://hackmd.io/_uploads/rJnbGb7D-g.png)
![fn_samples_comparison](https://hackmd.io/_uploads/HJ3bfb7wWg.png)

### Proposed Directions
#### Proposal 1: Fine-Grained GOLD 1-2 Detection
* **目標：**  **GOLD vs. Healthy** 
* **預期貢獻：** 高於 **61.7%** GOLD 1準確率。(Survey中最高準確率)

#### Proposal 2: Robustness to Imaging Protocols
* **目標：** 利用多參數 DICOM，證明 `nnMamba` 在面對影像異質性時的穩定性。
* **實驗設計：**
    * **Training:** 不使用最高切片進行訓練，而是選擇單一參數或者是全部同時訓練。
* **預期貢獻：** 採用 Survey 中呼籲的「需要評估成像協議變異影響」，增強臨床落地可行性。

## 2026/3/3
:::info
- [x] 蒐集GOLD CT肺部資料集
:::

### Result

目前開源平台上 **不存在** 同時滿足「原始 3D CT 影像」、「具備 GOLD 分期標籤」且「完全免申請」的完美資料集。主因為高解析度 CT 結合肺功能數據具備極高病患隱私風險，皆受 IRB 嚴格監管。

### 開源資源
1. **有 GOLD 標籤，但「無」原始 CT 影像**
   * **資料型態：** CSV 表格數據、從 CT 萃取出的特徵矩陣。
   * **代表資料集：** * [Kaggle: COPD Student Dataset](https://www.kaggle.com/datasets/prakharrathi25/copd-student-dataset)
     * [Figshare: Automatic Emphysema Detection](https://figshare.com/articles/dataset/Dataset_features_extracted_from_chest_CT_images_accompanying_the_paper_Automatic_emphysema_detection_using_weakly_labeled_HRCT_lung_images/6373145)
   * **研究限制：** 無法進行端到端 (End-to-End) 的深度學習影像訓練。

2. **有原始 CT 影像，但「無」GOLD 分期**
   * **資料型態：** 原始 DICOM / NIfTI 影像。
   * **代表資料集：** * [TCIA: LIDC-IDRI](https://www.cancerimagingarchive.net/collection/lidc-idri/)
     * [Kaggle: Chest Diseases by Medical Imaging](https://www.kaggle.com/datasets/programmer3/chest-diseases-by-medical-imaging)
   * **研究限制：** 僅有「是否患有氣流障礙」或「肺結節位置」等標註，完全缺乏 FEV1 等肺功能指標或 GOLD 1-4 級分類。

### 需申請的標準醫學資料庫 (符合 CT 端到端訓練需求)

若後續欲結合與振興醫院的臨床專案，或必須直接將 3D CT 影像對應至精確的 GOLD 分級進行訓練，必須透過正式管道申請以下資料庫：

* **[NHLBI TOPMed (COPDGene)](https://www.ncbi.nlm.nih.gov/projects/gap/cgi-bin/study.cgi?study_id=phs000951.v5.p5)**
  * **規模：** > 10,000 例。
  * **內容：** 包含完整的吸氣/呼氣高解析 CT 原始影像，並嚴格標註 GOLD Stage 0-4 與 FEV1 等 200 多項生理指標。
  * **門檻：** 需提交詳細研究計畫，並取得機構 IRB 批准與 NIH 授權 (dbGaP 系統)。

* **[DIR-LAB COPDgene](https://med.emory.edu/departments/radiation-oncology/research-laboratories/deformable-image-registration/downloads-and-reference-data/copdgene.html)**
  * **規模：** 僅 10 例成對 CT 影像。
  * **內容：** 附有專家手動標註的解剖特徵點，主要用於評估影像配準 (DIR) 演算法。
  * **門檻：** 填寫表單獲取解鎖密碼即可下載。

<!-- ## Robustness to Imaging Protocols
:::info
- [x] 多參數 DICOM，選擇lung跟soft參數進行對比
:::
### Result 
![auc_comparison](https://hackmd.io/_uploads/SkRM2ZjvZg.png)
![dataset_composition](https://hackmd.io/_uploads/HyZQ3ZjD-l.png)
![fold_auc_comparison](https://hackmd.io/_uploads/Hy7QhbjD-g.png)
![multi_metric_comparison](https://hackmd.io/_uploads/SyBXnZiDWl.png) -->

## 2026/3/10
:::info
- [x] 彙整目前結果匯報給醫生，詢問未來方向
- [x] literature survey PFT預測上肺葉還是下肺葉是主要肺氣腫區域
- [x] 研究國家級人體資料庫平台
:::

### Result
用肺功能曲線預測 CPFE 空間主導性

#### 臨床問題

CPFE 患者（上葉肺氣腫＋下葉肺纖維化）因兩種病灶效應互相抵銷，FVC / FEV1 數值**看起來正常**，導致臨床無法判斷：**目前到底是哪葉在惡化？**

#### 核心想法

雖然總量數值被抵銷，但這兩種病理在**呼氣動態曲線**上會留下不同形狀：

| 主導病灶 | 曲線特徵 |
|---|---|
| 上葉肺氣腫 | 後段凹陷（氣道提早塌陷） |
| 下葉纖維化 | 前段陡峭凸起（氣流快速排出） |

→ 讀取整條流量-容積曲線，預測「上葉主導」或「下葉主導」。


COPDGene 已證明此方法在單純 COPD 可行（AUC 0.80），但**從未有人將它應用在 CPFE 混合表型**。


<!-- CPFE 病例稀少，改用**孿生網路（Siamese Network）成對比較**，讓模型判斷「兩位患者中誰的下葉纖維化更嚴重」，使資料量從 $N$ 擴增至 $O(N^2)$。
 -->
只需少量 **PFT 曲線＋CT** 的病患資料。

### 研究國家級人體資料庫平台
申請至少要三個月以上

## 2026/3/17
:::info
- [x] 從CT去預測病人PFT有無angle survey
- [x] 跟醫生check資料集的正常異常是否用angle去判斷
:::

### Result
醫生使用ATS標準去判斷正常以及異常

### Survey
最大呼氣流速-容積曲線 (MEFV) 的「凹陷程度 (Concavity)」、「杓狀凹陷（Scooped-out）」、「下降夾角（Angle）」

期刊論文，採用單一標量數值（如 FEV1/FVC < 0.70 或是單獨的 FEV1 預測值）作為標註基準（Ground Truth）。

臨床主觀性帶來的標籤雜訊（Label Noise）：
在傳統醫學中，「杓狀凹陷」通常是醫師用肉眼主觀判讀的，不同醫師的標準落差極大。如果直接拿醫師主觀的「有/無凹陷」標籤去訓練，會產生嚴重的標籤雜訊，導致模型無法收斂。過去的文獻為了避開這個問題，一律退而求其次，採用絕對客觀的 GOLD 數值準則。
![S__42672197](https://hackmd.io/_uploads/BJ7s2rL9bl.jpg)

### Potential Research Directions
1. 利用夾角角度判斷正常異常
2. 用CT去預測連續1D PFT Flow-Volume Curve

## 2026/3/24
:::info
- [x] 測量與分析資料集角度
- [x] 重分類資料集
- [x] nnMamba training
:::

### Result
166.5°
![patient_angle_table_en](https://hackmd.io/_uploads/S1FFkUMsZe.png)
![total_cm](https://hackmd.io/_uploads/BkYYWcq5Ze.png)
Accuracy:0.87

## 2026/3/31
:::info
- [x] 整理凹陷面積算法
- [x] 病人角度直方圖
- [x] 報告進度給醫生
:::

### Result 
![patient_angle_histogram](https://hackmd.io/_uploads/HyJ8xrGsZe.png)
1. 找出最高呼氣流量 (PEF)： 
先在最大呼氣流量-容積 (MEFV) 曲線圖（Y軸為流量，X軸為容積）上，找到患者呼氣流量的最高峰值
2. 取最高值的一半 (half-PEF)： 
將這個最高流量數值除以 2，得到一半的最高呼氣流量
3. 標示兩個交點： 
在圖表的 Y 軸對準這個 half-PEF 的數值，畫一條水平線過去，這條水平線會與 MEFV 曲線相交於兩個點
4. 計算 a： 
這兩個交點對應到 X 軸（容積）的數值相減，得出的兩個交點之間的容積差距，就是數值 a
![image](https://hackmd.io/_uploads/rysNvrzs-g.png)



* 阻塞指數 (Obstructive Index, OI)： 
結合早期幾何指標與現代影像技術。2019 年經 CT 掃描證實其與肺氣腫的關聯，並將 4.38 確立為區分中重度肺氣腫的精確切點。

* 塌陷角算法 (Angle of Collapse, AC)： 
基於電腦演算尋找轉折點並自動擬合迴歸線。明確定義了 131°（異常/肺氣腫）與 152°（正常）的分類閥值，近年更延伸應用於診斷氣喘-COPD重疊症 (ACO)。

* 凹陷角度與形狀因子 (β Angle & Shape Factor)： 
運用三角函數與關鍵流量點 (如 PEF, FEF50, FVC 等) 直接計算曲線凹陷程度與初始角。這套公式在評估氣流受限（如成人氣喘）與檢視肺功能測試品質上極具實用性。

* 幾何面積與偏差算法 (Area & Deviation)： 
透過比對實際曲線與「理想直線/三角形」的差異來量化。從早期計算垂直距離積分的「凹陷指數」，發展至 2024 年最新的「表面比法」，後者藉由數位重取樣與幾何梯度，能更精細地監測呼吸器患者的肺部狀況。

### 醫生進度報告
{%preview https://hackmd.io/uESglcOFS3KAUIm2OE0ikQ?view=#/ %}

## 2026/4/7
:::info
- [x] 做角度regression
- [x] survey CTtoOI(阻塞指數)
:::

### Result
先經過 `Stem` 進行初步卷積特徵擷取與降採樣，再依序通過 `Stage 1`、`Stage 2`、`Stage 3` 三個特徵抽取階段。每個 stage 內都包含卷積與多個 `ResidualMambaBlock`，用來同時學習局部特徵與長距離空間關係。接著，模型會將三個 stage 的輸出分別做 global average pooling，得到三個不同尺度的特徵向量，之後將它們串接成單一向量。最後，這個多尺度特徵向量會送入 `MLP head`，透過全連接層逐步轉換，輸出一個連續數值，作為病人 CT 對應的預測塌陷角度。簡單來說，此模型的核心概念是：先抽取多層次影像特徵，再融合不同尺度資訊，最後完成角度回歸預測。

{%preview https://hackmd.io/@kc22zFlwRBKP6GihZ3SYWg/HJoLh_qs-g %}
![total_scatter](https://hackmd.io/_uploads/ryeGvFoi-e.png)

> R² ：看模型整體擬合能力（評估模型能解釋數據變異的比例，越接近 1 代表擬合度越好）。
> 
> Pearson ：看預測和真實值的趨勢相關性（衡量兩者在線性趨勢上的一致程度，不考慮具體數值的絕對落差，只看變化趨勢是否同步）。

### OI survey
目前的相關研究主要停留在以下幾個層次：

預測傳統肺功能參數：利用胸部 CT 影像去預測 FEV1、FVC、FEV1/FVC 比值或肺活量等傳統的純量數值 。

預測整體氣流受限 ： Mochizuki 團隊，在 2025 年研究中，利用多種 CT 影像特徵（如氣道壁厚度、定量肺氣腫與目測的小葉中心型肺氣腫）來預測整體的「氣流受限」狀態，而沒有直接將 AI 的預測標的設定為 OI 數值。

合成或分析幾何曲線：雖然已有前沿研究在嘗試從單一吸氣相 CT 生成動態的參數響應映射（PRM），或是利用神經網絡從既有的流量-容積曲線去逆向區分肺氣腫與氣道疾病表型，但還沒有人將 CT 預測技術直接對接到底層的幾何 OI 公式上。

## 2026/4/14
:::info
- [x] 把正規化角度方法統一
- [x] 用swinUnetV2做regression
- [x] 問醫生資料集吸氣還是吐氣相
:::

### Result
mamba 5 min
![total_scatter](https://hackmd.io/_uploads/BJoEFO7h-g.png)
swinUnetV2 20 min
![total_scatter](https://hackmd.io/_uploads/r1NLt_Q3bx.png)


{%preview https://github.com/nvlabs/mambavision?tab=readme-ov-file %}


![image](https://hackmd.io/_uploads/B1QqU64nbx.png)

mamba vision 6 min
![total_scatter](https://hackmd.io/_uploads/SylwyAN2Wl.png)

## 2026/4/21
:::info
- [x] 做fev1 post ref %資料集
- [x] swinUnetV2做分類 
- [x] mamba做分類 
- [x] mambavision 做分類 
:::

### Result
GOLD分級標準
預測值 = 實際FEV1/ FEV1 預測值(依照身高、年齡、體重計算)
GOLD 1 (輕度)： FEV1 ≥ 80% 預測值
GOLD 2 (中度)： 50% ≤ FEV1 < 80% 預測值
GOLD 3 (重度)： 30% ≤ FEV1 < 50% 預測值
GOLD 4 (極重度)： FEV1 < 30% 預測值

醫院資料集
GOLD 1 (輕度): 24
GOLD 2 (中度): 11
GOLD 3 (重度): 13
GOLD 4 (極重度): 6

mamba 5 fold mean_accuracy: 0.44546
![total_confusion_matrix](https://hackmd.io/_uploads/Sy6sDzAhbx.png)


3 fold [class-weighted cross entropy](https://hackmd.io/@kc22zFlwRBKP6GihZ3SYWg/S1OBPf0nbx)

mamba 
mean_accuracy: 0.42593
![total_confusion_matrix](https://hackmd.io/_uploads/Hk9L7M03Zg.png)

swinunet 
mean_accuracy: 0.44444
![total_confusion_matrix](https://hackmd.io/_uploads/SkRvUG0hbg.png)

mamba vision
mean_accuracy: 0.5
![total_confusion_matrix](https://hackmd.io/_uploads/ByGzOGAh-x.png)


## 2026/4/28
:::info
- [x] 加入新的病人
- [x] GOLD資料平衡
- [x] 用131°（異常/肺氣腫）與 152°（正常） 分資料集 分三類
:::

### Result
#### GOLD
GOLD 1: 36
GOLD 2: 11
GOLD 3: 13
GOLD 4: 6
total: 66
總資料數變成 144 筆
驗證集只取原始CT
Fold 1: total 22
  GOLD1=12, GOLD2=3, GOLD3=5, GOLD4=2
Fold 2: total 22
  GOLD1=12, GOLD2=4, GOLD3=4, GOLD4=2
Fold 3: total 22
  GOLD1=12, GOLD2=4, GOLD3=4, GOLD4=2
ACC: 0.57576
![total_confusion_matrix](https://hackmd.io/_uploads/SknoGxITbg.png)

#### Angle
[來源](https://link.springer.com/article/10.1186/1465-9921-14-131)
Emphysema/Abnormal (<=131°): 14 -> 47
Intermediate (132-151°):     5 -> 47
Normal (>=152°):             47 -> 47
ACC: 0.68461
![total_confusion_matrix](https://hackmd.io/_uploads/SyBS5BDabx.png)

## 2026/5/5
:::info
- [x] (角度)採少類平衡 隨機取 each epoch
- [x] (角度)Data Augment
:::

### Result
採少類平衡 隨機取 each epoch
Acc: 0.63956
![total_confusion_matrix](https://hackmd.io/_uploads/ry3ZFV1C-x.png)
100/class
train: class 0=11, class 1=4, class 2=37
valid: class 0=3, class 1=1, class 2=10
Acc: 0.75934
![total_confusion_matrix](https://hackmd.io/_uploads/r11I0PlR-x.png)

> 小角度旋轉：最多 ±5 度
> 小幅平移：最多 ±3%
> 小幅縮放：0.97 到 1.03 倍
> 亮度/強度縮放：0.98 到 1.02 倍
> 強度平移：-0.05 到 0.05
> 加一點 Gaussian noise：std = 0.02

## 2026/5/12
:::info
- [x] (角度)採少類平衡 隨機取 each epoch Date Aug x12
- [x] (角度)拉到200張
- [x] (角度)拉到150 or 300張
- [x] (角度)分兩類
- [x] (gold)拉到200張
- [x] (gold)拉到36張
- [x] 論文題目
:::

### Result
(角度)採少類平衡 隨機取 each epoch Date Aug x12
Acc: 0.423
![total_confusion_matrix](https://hackmd.io/_uploads/ry_jn-P0Zg.png)

(角度)拉到200張
Acc: 0.757
![total_confusion_matrix](https://hackmd.io/_uploads/ryF4aWw0-l.png)

(角度)拉到300張
Acc: 0.759
![total_confusion_matrix](https://hackmd.io/_uploads/rJFO7YY0Ze.png)


(角度)分兩類
Emphysema/Abnormal (<=131°): 14
Normal (>=152°): 47
Acc: 0.77
![total_confusion_matrix](https://hackmd.io/_uploads/BJ5KzXPAbx.png)

(角度)分兩類 100/class
Acc: 0.869
![total_confusion_matrix](https://hackmd.io/_uploads/H1mwVPd0bg.png)

(gold)拉到200張
Acc: 0.56
![total_confusion_matrix](https://hackmd.io/_uploads/ByoRRtYCZg.png)

(gold)拉到36張
Acc: 0.56
![total_confusion_matrix](https://hackmd.io/_uploads/r1weJcYA-e.png)

論文題目：
1. 量化 CT 影像之 COPD 分類與肺功能塌陷角角度分類
2. 結合 CT 影像量化分析與 nnMamba 模型之 COPD 正常異常分類與塌陷角度分析研究
3. 胸部 CT 影像於 COPD 輔助診斷之研究：結合定量特徵分類與塌陷角度預測

最終題目：
胸部 CT 影像於 COPD 輔助診斷之研究

## 2026/5/19
:::info
- [x] 針對角度方向優化
:::


## Result
(角度分兩類)TAP-CT
logistic
Acc: 0.853
![angle_binary_extreme_logistic_confusion_matrix](https://hackmd.io/_uploads/SJRS-CbJMx.png)

(角度分兩類)TAP-CT + HybridMamba
Acc: 0.919
![total_confusion_matrix](https://hackmd.io/_uploads/SkNSb0-kze.png)

(角度分三類)TAP-CT
logistic
Acc: 0.789
![angle_3class_logistic_confusion_matrix](https://hackmd.io/_uploads/HkTrz0bJGg.png)


(角度分三類)TAP-CT(TAP-B-3D) + HybridMamba
Acc: 0.82
![total_confusion_matrix](https://hackmd.io/_uploads/H16J6Tzyzx.png)

(角度分三類)TAP-CT(TAP-S-2.5D)+ HybridMamba
Acc: 0.835
![total_confusion_matrix](https://hackmd.io/_uploads/r1MPFgQJGx.png)



[Google CT Embeding](https://research.google/blog/taking-medical-imaging-embeddings-3d/)
[TAP-CT](https://arxiv.org/abs/2512.00872)