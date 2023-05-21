

## 設計過程prompt
```
2023-05-21 15:22 Bowen Chiu
-- 我想製作 to_qa_csv.py
目的: 讀取任意純文字檔案，可以是 .txt .json .csv 或任意純文字檔案，適當切割之後讓chatgpt api可以消化(因為gpt-4有max 8k tokens最大限制), 最終轉換為 .csv 一問一答， .csv 欄位有兩個：question, answer

用法: 同時要支援 cli 可以參數運用

用法: 同時要支援 import 套件可以運用呼叫

輸入參數: 使用者名稱，預設是 cbh@cameo.tw

輸入參數: 指定一個 folder，該目錄底下可以有一堆子目錄

輸入參數: 指定一個或多個副檔名，例如 *.txt *.json 甚至 * 就可以抓取多層子目錄底下的每一個檔案來處理

輸入參數: 可以指定轉換變成哪一國語言的 prompt, 預設是: -- 檔案轉換\n請將以下的純文字當中的內容，盡可能忠於原貌的，盡可能越詳細越好仔細的，轉換為 .csv 格式，欄位有 question,answer 兩個欄位，回答時用 --csv_start-- 作為.csv起始，然後回答結尾用 --csv_end-- 作為結束

輸入參數: 可以指定 multi threads 最多有多少 threads 進行轉換作業，預設是 5 threads

輸入參數: 轉換的AI model 預設是 gpt-3.5-turbo, 也可以指定是 gpt-4 或其他

防止重做: 事先判斷，如果輸出的檔案 sha 256 hex 比對時已經存在，就跳過不要重新製作，不要呼叫 prompt_to_ai
 轉換，節省時間與成本

強迫重做: 參數如果有 force 參數，就不管輸出檔案是否存在，一律重新呼叫 prompt_to_ai 製作 .csv 輸出

輸入參數: 輸出檔案群 .csv 要放到哪個folder底下，預設目錄是放在 data/users/[使用者名稱]/to_qa_csv/[日期]/*.csv

輸出檔案群.csv檔名規則: 輸出的.csv只有question,answer兩個欄位，然後他的預設檔名舉例是這樣 data/users/cbh_cameo_tw/to_qa_csv/2023-05-21/type_to_qa_csv_time_2023-05-21T04_21_18Z_sha_2ef7bde608ce5404e97d5f042f95f89f1c232871.csv

輸出檔案群.csv檔名規則: 通用的預設輸出檔名規則如下，data/users/cbh_cameo_tw/to_qa_csv/[輸出當天日期]/type_to_qa_csv_time_[輸出當天的UTC時間包含TZ字元]_sha_[sha 256 hex的字串結果].csv

最新程式碼請參考: 請呼叫 openai_chat_thread_taiwan AI轉換純文字片段轉為.csv的字串部分的轉換，程式碼請用這個:
from openai_chat_thread import openai_chat_thread_taiwan
def prompt_to_ai(prompt,model='gpt-4'):
    q = openai_chat_thread_taiwan(prompt,model)
    lst = []
    while True:
        response = q.get()
        if response is None:
            break
        else:
            lst.append(response)
        print(response, end="", flush=True)
    join_str = ''.join(lst)
    return join_str
```