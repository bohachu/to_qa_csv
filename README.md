# To QA CSV Converter

這個工具負責將文字檔(.txt)或者 JSON 檔(.json)作為輸入，並產生對應的問答 (question, answer) .csv 檔案。此程式可用於將自然語言資料轉換為問答資料，讓用戶可以更有效地解析文件。

## 安裝 Installation

透過 PyPI 安裝:

```bash
python3 -m pip install to-qa-csv
```

透過 GitHub 下載並安裝:

```bash
python3 -m pip install git+https://github.com/bohachu/to_qa_csv.git
```

## 使用方法 Usage

### 命令行界面 (Command Line Interface, CLI)

通過命令行界面使用 `to_qa_csv`，範例如下：

```bash
to_qa_csv -i input_folder -u your_user_name -o output_folder -e .txt .json -p "Your prompt" -t 2 -m gpt-4 -f -c 5000
```

以下是各個參數的說明：
- `-i` or `--input_folder`: 輸入文件的資料夾，將會搜尋這個資料夾中的.txt 和 .json 文件
- `-u` or `--user`: 使用者名稱
- `-o` or `--output_folder`: 輸出 .csv 檔案的目錄
- `-e` or `--extensions`: 指定要搜尋的檔案副檔名，以空格隔開，例如: .txt .json
- `-p` or `--prompt`: 給 AI model 的題詞
- `-t` or `--threads`: 指定多少 threads 同時進行轉換作業
- `-m` or `--model`: 要使用的 AI model 名稱，例如: gpt-4
- `-f` or `--force`: 是否強制重新製作輸出檔案
- `-c` or `--chunk_size`: 切割片段以多少字元為切割

### 使用Python模組 (Python Module)

導入 `to_qa_csv` 模組並使用 `to_qa_csv` 函數，範例如下：

```python
from to_qa_csv import to_qa_csv

to_qa_csv(input_folder="/path/to/input/folder",
          user="your_user_name",
          output_folder="/path/to/output/folder",
          extensions=[".txt", ".json"],
          prompt="your_prompt",
          threads=2,
          model="gpt-4",
          force=True,
          chunk_size=5000)

## 設計過程prompt
```
2023-05-21 21:13 Bowen, 增添 README.md 完整說明
- python3 -m to_pip -v 1.0.1 -n to-qa-csv to_qa_csv.py

2023-05-21 16:51 Bowen Chiu prompt
修改偵測 chunk 製作為 sha 256 hex 字串之後，如果輸出的目錄當中有包含檔案名稱有 hex_dig 存在的檔案名字就跳過這個檔案不要製作了 （不要呼叫 prompt_to_ai），改為印出 hex_dig 這個字串已經存在的提示訊息就好
請告訴我該改哪些片段就好

2023-05-21 15:32 Bowen Chiu prompt
處理輸入的 .json 檔案一個就過大了，所以請讓輸入參數多新增一個參數是切割片段以多少字元為切割，預設是 1000 代表不管中文英文字元，都是以 1000 字元切割餵入 prompt_to_ai 每次餵入一次就產生一個 .csv 檔案這樣。當然 1000 要可以參數修改。給我完整修改後程式碼

2023-05-21 15:22 Bowen Chiu prompt
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