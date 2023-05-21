import argparse
import datetime
import glob
import hashlib
import os

from openai_chat_thread import openai_chat_thread_taiwan

DEFAULT_START_TAG = '--start_ai--'
DEFAULT_END_TAG = '--end_ai--'


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


def convert_to_csv(input_file, output_dir, user, prompt, model='gpt-4', force=False, chunk_size=1000):
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    content_chunks = [content[i:i + chunk_size] for i in range(0, len(content), chunk_size)]

    for chunk in content_chunks:
        hash_object = hashlib.sha256(chunk.encode('utf-8'))
        hex_dig = hash_object.hexdigest()

        date_str = datetime.datetime.utcnow().strftime('%Y-%m-%d')
        time_str = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H_%M_%SZ')
        csv_file_name = f'type_to_qa_csv_time_{time_str}_sha_{hex_dig}.csv'

        output_path = os.path.join(output_dir, user, 'to_qa_csv', date_str, csv_file_name)

        # 檢查包含 hex_dig 的檔案是否已經存在
        existing_files = glob.glob(os.path.join(output_dir, user, 'to_qa_csv', '**', f'*{hex_dig}*.*'), recursive=True)
        if not force and existing_files:
            print(f"{hex_dig} 已經存在，跳過製作")
            continue

        prompt_str = prompt + chunk

        qa_data = prompt_to_ai(prompt_str, model)

        if not os.path.exists(os.path.dirname(output_path)):
            os.makedirs(os.path.dirname(output_path))

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            in_tag = in_tag_response(qa_data)
            f.write(in_tag)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_folder', help='指定要搜尋的目錄')
    parser.add_argument('output_folder', help='輸出 .csv 檔案的目錄')
    parser.add_argument('-u', '--user', default='cbh@cameo.tw', help='使用者名稱')
    parser.add_argument('-e', '--extensions', nargs='*', default=['*.txt', '*.json'], help='要搜尋的檔案副檔名')
    parser.add_argument('-l', '--language_prompt',
                        default=f"-- 請將以下的純文字當中的內容，盡可能忠於原貌的，盡可能越詳細越好仔細的，轉換翻譯為繁體中文描述的 .csv 格式，欄位有 question,answer 兩個欄位，回答時用 {DEFAULT_START_TAG} 作為.csv起始，然後回答結尾用 {DEFAULT_END_TAG} 作為結束",
                        help='指定轉換成哪個國家語言的 prompt')
    parser.add_argument('-t', '--threads', type=int, default=5, help='指定多少 threads 同時進行轉換作業')
    parser.add_argument('-m', '--model', default='gpt-3.5-turbo', help='要使用的 AI model 名稱')
    parser.add_argument('-f', '--force', action='store_true', help='是否強制重新製作輸出檔案')
    parser.add_argument('-c', '--chunk_size', type=int, default=1000, help='切割片段以多少字元為切割')

    args = parser.parse_args()

    all_files = []
    for ext in args.extensions:
        all_files.extend(glob.glob(f'{args.input_folder}/**/{ext}', recursive=True))

    for filepath in all_files:
        convert_to_csv(filepath, args.output_folder, args.user, args.language_prompt, args.model, args.force,
                       args.chunk_size)


if __name__ == "__main__":
    main()
