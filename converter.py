import tkinter as tk
from tkinter import messagebox

# ==========================================
# 核心演算法區：手寫進位轉換（嚴禁使用 int(s, 2) 或 hex()）
# ==========================================

def manual_dec_to_any(n, base):
    """
    將十進位(n)轉換為指定進位(base: 2 或 16)。
    原理：除法取餘數（輾轉相除法）。
    """
    if n == 0:
        return "0"
    
    # 定義對應表，處理 16 進位的 A-F
    digits = "0123456789ABCDEF"
    result = ""
    temp_n = n
    
    while temp_n > 0:
        remainder = temp_n % base       # 取得餘數
        result = digits[remainder] + result  # 將餘數加在字串最左邊
        temp_n //= base                # 取得商數繼續除
    return result

def manual_any_to_dec(s, base):
    """
    將指定進位字串(s)轉換回十進位。
    原理：加權加乘法（底數的次方倍）。
    """
    digits = "0123456789ABCDEF"
    s = s.upper().strip() # 轉大寫並去除空格
    decimal_val = 0
    power = 0
    
    # 從字串的最右邊（個位數）開始處理到左邊
    for i in range(len(s) - 1, -1, -1):
        char = s[i]
        val = digits.find(char) # 找出該字元代表的數值
        
        # 防呆：檢查輸入是否符合該進位的範圍
        if val == -1 or val >= base:
            raise ValueError("非法字元")
            
        # 累加：數值 * (底數 ^ 次方)
        decimal_val += val * (base ** power)
        power += 1
    return decimal_val

# ==========================================
# GUI 介面邏輯區
# ==========================================

def perform_conversion():
    """點擊 Convert 按鈕後的動作"""
    try:
        # 取得三個輸入框的內容
        b_input = entry_bin.get().strip()
        d_input = entry_dec.get().strip()
        h_input = entry_hex.get().strip()

        # 判斷使用者在哪個框輸入，並統一轉成「十進位」作為中繼站
        if d_input:
            # 十進位字串轉整數（手寫邏輯，不使用 int()）
            target_dec = 0
            for char in d_input:
                if '0' <= char <= '9':
                    target_dec = target_dec * 10 + (ord(char) - ord('0'))
                else:
                    raise ValueError
        elif b_input:
            target_dec = manual_any_to_dec(b_input, 2)
        elif h_input:
            target_dec = manual_any_to_dec(h_input, 16)
        else:
            return # 都沒輸入就不執行

        # 根據中繼的十進位，更新所有框框（達成互相轉換）
        entry_bin.delete(0, tk.END)
        entry_bin.insert(0, manual_dec_to_any(target_dec, 2))
        
        entry_dec.delete(0, tk.END)
        entry_dec.insert(0, str(target_dec))
        
        entry_hex.delete(0, tk.END)
        entry_hex.insert(0, manual_dec_to_any(target_dec, 16))

    except Exception:
        messagebox.showerror("格式錯誤", "請輸入符合進位制的有效數字！")

def clear_all():
    """清除所有輸入框內容"""
    entry_bin.delete(0, tk.END)
    entry_dec.delete(0, tk.END)
    entry_hex.delete(0, tk.END)

# ==========================================
# 視窗版面配置 (Tkinter)
# ==========================================

root = tk.Tk()
root.title("Binary / Decimal / Hex Converter")
root.geometry("500x250")

# 標題標籤 (Grid 佈局)
tk.Label(root, text="Binary", font=('Arial', 10, 'bold')).grid(row=0, column=0, pady=10)
tk.Label(root, text="Decimal", font=('Arial', 10, 'bold')).grid(row=0, column=1, pady=10)
tk.Label(root, text="Hexadecimal", font=('Arial', 10, 'bold')).grid(row=0, column=2, pady=10)

# 輸入框
entry_bin = tk.Entry(root, justify='center')
entry_bin.grid(row=1, column=0, padx=10, ipady=5)

entry_dec = tk.Entry(root, justify='center')
entry_dec.grid(row=1, column=1, padx=10, ipady=5)

entry_hex = tk.Entry(root, justify='center')
entry_hex.grid(row=1, column=2, padx=10, ipady=5)

# 功能按鈕
btn_convert = tk.Button(root, text="Convert", width=45, bg="#f0f0f0", command=perform_conversion)
btn_convert.grid(row=2, column=0, columnspan=3, pady=20)

btn_clear = tk.Button(root, text="Clear", width=45, bg="#f0f0f0", command=clear_all)
btn_clear.grid(row=3, column=0, columnspan=3, pady=5)

# 啟動視窗主迴圈
root.mainloop()