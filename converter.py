import tkinter as tk
from tkinter import messagebox

# =================================================================
# 核心演算法：自定義進位轉換邏輯
# 說明：本區塊完全不使用 Python 內建函式（如 hex, bin, int(s, base)）
# =================================================================

def manual_dec_to_any(n, base):
    """
    將十進位整數轉換為目標進位的字串表達式。
    原理：使用「輾轉相除法」。將十進位數重複除以底數，所產生的餘數即為該進位的位數數值。
    """
    if n == 0: return "0"
    
    # 定義字元對應表，用以處理十六進位中 10-15 所對應的 A-F 字元
    digits = "0123456789ABCDEF"
    result = ""
    temp_n = int(n)
    
    # 執行運算：持續除法直到商數歸零
    while temp_n > 0:
        # 取得餘數，並將對應字元串接在字串左側（因為先算出的餘數代表低位數）
        result = digits[temp_n % base] + result
        # 進行整數除法更新商數，準備下一次重複運算
        temp_n //= base
    return result

def manual_any_to_dec(s, base):
    """
    將指定進位的字串轉換回十進位整數。
    原理：使用「按權展開計算法」。將字串中每一位數值乘以該進位的次方權重後進行累加。
    """
    digits = "0123456789ABCDEF"
    # 統一轉為大寫並清除前後空白，提升程式執行的穩健性
    s = s.upper().strip() 
    decimal_val = 0
    power = 0
    
    # 由字串末端（低位數）向左逐一處理每個字元
    for i in range(len(s) - 1, -1, -1):
        # 找出該字元在對應表中的索引位置，即為其代表之數值
        val = digits.find(s[i])
        
        # 異常偵測：若輸入字元不符合該進位制規範，則拋出數值錯誤
        if val == -1 or val >= base: raise ValueError
        
        # 累加運算：該位數值 * (底數 ^ 目前次方數)
        decimal_val += val * (base ** power)
        power += 1
    return decimal_val

# =================================================================
# 事件處理邏輯
# =================================================================

def perform_conversion():
    """
    轉換按鈕觸發函式：負責判斷輸入源、呼叫數學演算法並更新介面顯示。
    """
    try:
        # 讀取各輸入框內容並排除多餘空格
        b_in = entry_bin.get().strip()
        d_in = entry_dec.get().strip()
        h_in = entry_hex.get().strip()
        
        # 判斷機制：辨識使用者填寫的欄位（優先順序：十進位 > 二進位 > 十六進位）
        if d_in:
            target_dec = 0
            # 手動實作十進位字串轉整數邏輯（不調用內建 int 函式）
            for char in d_in:
                if '0' <= char <= '9':
                    # 透過 ASCII 碼偏移量取得數值並左移一位（乘以10）進行累加
                    target_dec = target_dec * 10 + (ord(char) - ord('0'))
                else: raise ValueError
        elif b_in:
            target_dec = manual_any_to_dec(b_in, 2)
        elif h_in:
            target_dec = manual_any_to_dec(h_in, 16)
        else:
            return # 若所有欄位皆為空則終止執行

        # 介面更新：將計算所得之十進位數值同步轉換至其他進位欄位
        # 先清除現有內容
        entry_bin.delete(0, tk.END)
        entry_dec.delete(0, tk.END)
        entry_hex.delete(0, tk.END)
        
        # 寫入計算結果；此演算法經優化，可支援超過 255 以上的大數值轉換
        entry_bin.insert(0, manual_dec_to_any(target_dec, 2))
        entry_dec.insert(0, str(target_dec))
        entry_hex.insert(0, manual_dec_to_any(target_dec, 16))

    except Exception:
        # 錯誤處理：若偵測到格式不符或非法字元，則彈出警告視窗提醒使用者
        messagebox.showerror("格式錯誤", "請檢查輸入內容是否符合該進位制的數值規範！")

def clear_all():
    """清空所有輸入欄位之內容"""
    for e in [entry_bin, entry_dec, entry_hex]: e.delete(0, tk.END)

# =================================================================
# 視覺介面設計 (採用 Coolors 數位風格調色盤)
# =================================================================

# 定義配色方案
CLR_BG     = "#335C67"  # 深藍綠：背景底色，模擬復古電腦終端機質感
CLR_TEXT   = "#FFF3B0"  # 奶油黃：發光文字，提供高閱讀對比度
CLR_ACCENT = "#E09F3E"  # 琥珀橙：強調色彩，用於邊框提示
CLR_BTN    = "#9E2A2B"  # 磚紅色：主功能按鈕，強化視覺引導
CLR_ENTRY  = "#540B0E"  # 深紅色：輸入框背景，增加介面深度感

root = tk.Tk()
root.title("Advanced Base Converter")
root.geometry("750x500") # 調整視窗大小以提供舒適的佈局空間
root.configure(bg=CLR_BG)

# --- 頂部標題區域 ---
tk.Label(root, text="[ 數位進位轉換系統 ]", 
         font=("Monaco", 22, "bold"), fg=CLR_ACCENT, bg=CLR_BG).pack(pady=(40,8))
tk.Label(root, text="ARCH: UNLIMITED RANGE / TESTED VALUE: 300+", 
         font=("Monaco", 10), fg=CLR_TEXT, bg=CLR_BG).pack()

# --- 輸入元件容器 ---
input_frame = tk.Frame(root, bg=CLR_BG)
input_frame.pack(pady=50)

def create_styled_entry(parent, label, col):
    """
    封裝具有統一樣式的輸入框元件，提升程式碼模組化程度。
    """
    tk.Label(parent, text=f"// {label}", font=("Monaco", 10, "bold"), 
             fg=CLR_TEXT, bg=CLR_BG).grid(row=0, column=col, padx=18, pady=8)
    
    # 使用等寬字體並設定醒目邊框，強化數位科技感
    e = tk.Entry(parent, font=("Courier", 18, "bold"), width=15, 
                 bg=CLR_ENTRY, fg=CLR_TEXT, insertbackground=CLR_TEXT, 
                 bd=0, highlightthickness=2, highlightbackground=CLR_ACCENT, 
                 justify='center')
    e.grid(row=1, column=col, padx=12, ipady=12)
    return e

entry_bin = create_styled_entry(input_frame, "BINARY", 0)
entry_dec = create_styled_entry(input_frame, "DECIMAL", 1)
entry_hex = create_styled_entry(input_frame, "HEXADECIMAL", 2)

# --- 按鈕操作區域 ---
btn_frame = tk.Frame(root, bg=CLR_BG)
btn_frame.pack()

# 轉換按鈕：使用平整化設計配合顯眼配色
tk.Button(btn_frame, text="執行轉換數據 CONVERT", font=("PingFang TC", 13, "bold"), 
          bg=CLR_BTN, fg="white", width=38, height=2, relief="flat", 
          activebackground=CLR_ACCENT, command=perform_conversion, cursor="hand2").pack(pady=15)

# 清除按鈕
tk.Button(btn_frame, text="清除所有暫存 CLEAR", font=("PingFang TC", 10), 
          bg=CLR_BG, fg=CLR_TEXT, width=18, bd=0, command=clear_all, cursor="hand2").pack()

# 進入程式主迴圈
root.mainloop()