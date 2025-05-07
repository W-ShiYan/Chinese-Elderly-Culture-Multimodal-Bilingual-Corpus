import requests
from bs4 import BeautifulSoup
import os
import git
import shutil

# 定义网页爬取函数
def crawl_webpage(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # 提取文本内容，这里简单提取所有可见文本
        text = soup.get_text()
        return text
    except requests.RequestException as e:
        print(f"网页爬取出错: {e}")
        return None

# 定义本地文件处理函数
def process_local_files(local_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for root, dirs, files in os.walk(local_dir):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                output_file_path = os.path.join(output_dir, file)
                with open(output_file_path, 'w', encoding='utf-8') as out_f:
                    out_f.write(content)
            except Exception as e:
                print(f"处理本地文件 {file_path} 出错: {e}")

# 定义上传到 GitHub 函数
def upload_to_github(repo_path, remote_url, commit_message):
    try:
        if not os.path.exists(repo_path):
            repo = git.Repo.clone_from(remote_url, repo_path)
        else:
            repo = git.Repo(repo_path)

        # 添加所有更改
        repo.git.add(all=True)
        # 提交更改
        repo.git.commit(m=commit_message)
        # 推送更改到远程仓库
        origin = repo.remote(name='origin')
        origin.push()
        print("成功上传到 GitHub")
    except git.GitCommandError as e:
        print(f"GitHub 操作出错: {e}")

# 主函数
def main():
    # 网页爬取部分
    urls = [
        "https://example.com/page1",
        "https://example.com/page2"
    ]
    web_corpus_dir = "corpus/web"
    if not os.path.exists(web_corpus_dir):
        os.makedirs(web_corpus_dir)
    for i, url in enumerate(urls):
        text = crawl_webpage(url)
        if text:
            file_name = f"web_page_{i}.txt"
            file_path = os.path.join(web_corpus_dir, file_name)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(text)

    # 本地文件处理部分
    local_dir = "local_data"
    local_corpus_dir = "corpus/local"
    process_local_files(local_dir, local_corpus_dir)

    # 上传到 GitHub 部分
    repo_path = "ChineseElderlyCultureCorpus"
    remote_url = "https://github.com/yourusername/ChineseElderlyCultureCorpus.git"
    commit_message = "更新语料库内容"
    upload_to_github(repo_path, remote_url, commit_message)

if __name__ == "__main__":
    main()    
