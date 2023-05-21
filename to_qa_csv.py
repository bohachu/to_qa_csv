import argparse
import datetime
import glob
import hashlib
import os
from functools import reduce

from openai_chat_thread import openai_chat_thread_taiwan

DEFAULT_START_TAG = '--start_ai--'
DEFAULT_END_TAG = '--end_ai--'
DEFAULT_CHUNK_SIZE = 5000
DEFAULT_MODEL = 'gpt-4'
DEFAULT_THREADS = 5
DEFAULT_PROMPT = f"\n\n-- 以下是處理規則\n" \
                 f" 001 把「內容」剖析為一問一答的 .csv 有 question,answer 兩個欄位" \
                 f" 002 注意!無論question或answer都必須翻譯為繁體中文,不可以是英文" \
                 f" 003 .csv question 欄位是內容的提問" \
                 f" 004 .csv answer 是內容的回答" \
                 f" 005 請把 {DEFAULT_START_TAG} 作為要開始撰寫.csv的起始標示" \
                 f" 006 請把 {DEFAULT_END_TAG} 作為要結束.csv的結束標示" \
                 f" 007 欄位cell值請都用雙引號處理過並且相容於內容當中有斷行、空白、或逗點" \
                 f" 008 .csv 內容必須注意 escape 字元處理妥適" \
                 f" 009 請分析「內容」之後，在 .csv 創作出「一個」最具「矛盾衝突性」的震撼 question 並寫入「一個」最有「啟發讀者潛力」的 answer" \
                 f" \n\n-- 以下是「內容」:\n"
DEFAULT_INPUT_FOLDER = 'data/users/cbh_cameo_tw/youtube_transcript/'
DEFAULT_OUTPUT_FOLDER = 'data/users/'
DEFAULT_USER = 'cbh@cameo.tw'


def in_tag_response(all_response, start_tag=DEFAULT_START_TAG, end_tag=DEFAULT_END_TAG, is_print=True):
    start = all_response.find(start_tag)
    end = all_response.find(end_tag)
    if start != -1 and end != -1:
        result = all_response[start + len(start_tag):end].strip()
        if is_print:
            print("\nin_tag_response,result:\n", result)
        return result
    else:
        print("in_tag_response start or end marker not found.")
        return ''


def prompt_to_ai(prompt, model='gpt-4', is_print=True):
    q = openai_chat_thread_taiwan(prompt, model)
    lst = []
    while True:
        response = q.get()
        if response is None:
            break
        else:
            lst.append(response)
        if is_print:
            print(response, end="", flush=True)
    join_str = ''.join(lst)
    return join_str


def multi_replace(original_string, lst=['@', ':', '.'], replacement='_'):
    return reduce(lambda str1, ch: str1.replace(ch, replacement), lst, original_string)


def convert_to_csv(input_folder=DEFAULT_INPUT_FOLDER,
                   user=DEFAULT_USER,
                   output_folder=DEFAULT_OUTPUT_FOLDER,
                   prompt=DEFAULT_PROMPT,
                   model='gpt-4',
                   force=False,
                   chunk_size=DEFAULT_CHUNK_SIZE):
    with open(input_folder, 'r', encoding='utf-8') as file:
        content = file.read()

    content_chunks = [content[i:i + chunk_size] for i in range(0, len(content), chunk_size)]

    for chunk in content_chunks:
        hash_object = hashlib.sha256(chunk.encode('utf-8'))
        hex_dig = hash_object.hexdigest()

        date_str = datetime.datetime.utcnow().strftime('%Y-%m-%d')
        time_str = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H_%M_%SZ')
        csv_file_name = f'type_to_qa_csv_time_{time_str}_sha_{hex_dig}.csv'

        combined_folder = os.path.join(output_folder, multi_replace(user), 'to_qa_csv', date_str)
        output_path = os.path.join(combined_folder, csv_file_name)

        existing_files = glob.glob(os.path.join(combined_folder, '**', f'*{hex_dig}*.*'),
                                   recursive=True)
        if not force and existing_files:
            print(f"{hex_dig} 已經存在，跳過製作")
            continue

        prompt_str = prompt + chunk
        print('\nprompt_str:\n', prompt_str)
        qa_data = prompt_to_ai(prompt_str, model)

        if not os.path.exists(os.path.dirname(output_path)):
            os.makedirs(os.path.dirname(output_path))

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            in_tag = in_tag_response(qa_data)
            f.write(in_tag)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input_folder', default=DEFAULT_INPUT_FOLDER, help='指定要搜尋的目錄')
    parser.add_argument('-u', '--user', default=DEFAULT_USER, help='使用者名稱')
    parser.add_argument('-o', '--output_folder', default=DEFAULT_OUTPUT_FOLDER, help='輸出 .csv 檔案的目錄')
    parser.add_argument('-e', '--extensions', nargs='*', default=['*.txt', '*.json'], help='要搜尋的檔案副檔名')
    parser.add_argument('-p', '--prompt',
                        default=DEFAULT_PROMPT,
                        help='給 AI model 的題詞')
    parser.add_argument('-t', '--threads', type=int, default=DEFAULT_THREADS, help='指定多少 threads 同時進行轉換作業')
    parser.add_argument('-m', '--model', default=DEFAULT_MODEL, help='要使用的 AI model 名稱')
    parser.add_argument('-f', '--force', default="", help='是否強制重新製作輸出檔案')
    parser.add_argument('-c', '--chunk_size', type=int, default=DEFAULT_CHUNK_SIZE, help='切割片段以多少字元為切割')

    args = parser.parse_args()

    all_files = []
    for ext in args.extensions:
        all_files.extend(glob.glob(f'{args.input_folder}/**/{ext}', recursive=True))

    for filepath in all_files:
        convert_to_csv(filepath, args.user, args.output_folder, args.prompt, args.model, args.force,
                       args.chunk_size)


if __name__ == "__main__":
    main()
