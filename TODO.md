

格式問題

[高] PDF 缺少封面後的空白頁。程式有預留頁面，但空白頁沒有輸出。目前順序是封面、書名頁、審定書。見 main.tex (line 48)、blankpage.tex (line 1)。
[高] 審定書仍是模板示意頁，誌謝也仍是範例文字。見 signpage.pdf、thanks.tex (line 2)。
[高] 頁面邊界不符合規範：目前上方 4.5 cm、下方 0.75 cm，規範為上方 2.5 cm、下方 2.75 cm。編譯紀錄也出現 geometry 過度設定警告。見 main.tex (line 36)、main.log (line 1014)。
[高] 本文實際使用雙倍行距，不是規範要求的 1.5 倍行距。雖然入口設為 1.5，章節環境又包了一層 spacing{2}。見 main.tex (line 32)、ntut-report.cls (line 570)。
[高] 節標題目前使用 20 pt，規範要求 18 pt；標題下方也保留額外間距。見 ntut-report.cls (line 445)、ntut-report.cls (line 891)。
[高] RQ3 同一段落出現 Pearson 0.6699 與 0.523，但未說明差異。若前者是五折平均、後者是合併測試樣本結果，需明確標示。見 chapter4-results.tex (line 160)、chapter4-results.tex (line 201)。
[高] 第三章 WA% 公式需要 lumen 與 wall 體積，但前文又表示部分個案可能只有氣管或氣道遮罩近似值。老師很可能追問實際計算方式。見 chapter3-methods.tex (line 78)、chapter3-methods.tex (line 117)。
[高] 醫院提供 CT 與 PFT 資料，但全文未找到 IRB、倫理審查、去識別化或資料使用說明。見 chapter3-methods.tex (line 18)。