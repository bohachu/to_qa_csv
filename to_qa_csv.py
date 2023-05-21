import os
import glob
import csv
import datetime
import hashlib
from pathlib import Path
import argparse
from openai_chat_thread import openai_chat_thread_taiwan


def prompt_to_ai(prompt, model='gpt-4'):
    q = openai_chat_thread_taiwan(prompt, model)
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


def convert_to_csv(input_file, output_dir, user, prompt, model='gpt-4', force=False):
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    hash_object = hashlib.sha256(content.encode('utf-8'))
    hex_dig = hash_object.hexdigest()

    date_str = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    time_str = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H_%M_%SZ')
    csv_file_name = f'type_to_qa_csv_time_{time_str}_sha_{hex_dig}.csv'

    output_path = os.path.join(output_dir, user, 'to_qa_csv', date_str, csv_file_name)

    if not force and os.path.exists(output_path):
        return

    prompt_str = prompt + content

    qa_data = prompt_to_ai(prompt_str, model)

    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path))

    with open(output_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['question', 'answer'])
        for qa_pair in qa_data.split('--csv_end--'):
            q, a = qa_pair.split('--csv_start--')
            csv_writer.writerow([q.strip(), a.strip()])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_folder', help='指定要搜尋的目錄')
    parser.add_argument('output_folder', help='輸出 .csv 檔案的目錄')
    parser.add_argument('-u', '--user', default='cbh@cameo.tw', help='使用者名稱')
    parser.add_argument('-e', '--extensions', nargs='*', default=['*.txt', '*.json'], help='要搜尋的檔案副檔名')
    parser.add_argument('-l', '--language_prompt',
                        default="-- 請將以下的純文字當中的內容，盡可能忠於原貌的，盡可能越詳細越好仔細的，轉換為 .csv 格式，欄位有 question,answer 兩個欄位，回答時用 --csv_start-- 作為.csv起始，然後回答結尾用 --csv_end-- 作為結束",
                        help='指定轉換成哪個國家語言的 prompt')
    parser.add_argument('-t', '--threads', type=int, default=5, help='指定多少 threads 同時進行轉換作業')
    parser.add_argument('-m', '--model', default='gpt-3.5-turbo', help='要使用的 AI model 名稱')
    parser.add_argument('-f', '--force', action='store_true', help='是否強制重新製作輸出檔案')

    args = parser.parse_args()

    all_files = []
    for ext in args.extensions:
        all_files.extend(glob.glob(f'{args.input_folder}/**/{ext}', recursive=True))

    for filepath in all_files:
        convert_to_csv(filepath, args.output_folder, args.user, args.language_prompt, args.model, args.force)


if __name__ == "__main__":
    main()