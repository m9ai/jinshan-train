#!/usr/bin/env python3
"""构建脚本：压缩 HTML/CSS/JS 到 dist/ 目录。"""
import re, os, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = ROOT
OUT = os.path.join(ROOT, 'dist')

def minify_html(text):
    # 移除 HTML 注释（保留条件注释）
    text = re.sub(r'<!--(?!\[if).*?-->', '', text, flags=re.DOTALL)
    # 压缩空白
    text = re.sub(r'>\s+<', '><', text)
    text = re.sub(r'\s{2,}', ' ', text)
    # 去除行首尾空白
    return text.strip()

def minify_css(text):
    # 移除注释
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    # 移除多余空白
    text = re.sub(r'\s*([{}:;,])\s*', r'\1', text)
    text = re.sub(r';\s*}', '}', text)
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()

def minify_js(text):
    # 保留单行注释中的代码（如 URL），仅删纯注释行
    lines = []
    for line in text.split('\n'):
        s = line.strip()
        if s.startswith('//') and not s.startswith('//='):
            continue
        lines.append(line)
    text = '\n'.join(lines)
    # 移除多行注释
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    # 压缩空白
    text = re.sub(r'\s*([{}();,:+\-*/<>=!&|?])\s*', r'\1', text)
    text = re.sub(r'\s{2,}', ' ', text)
    text = re.sub(r'\n\s*\n', '\n', text)
    return text.strip()

def process():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT, exist_ok=True)

    # HTML 文件
    for fname in ['index.html', 'privacy.html', 'disclaimer.html', 'support.html']:
        src_path = os.path.join(SRC, fname)
        with open(src_path, 'r', encoding='utf-8') as f:
            raw = f.read()
        mini = minify_html(raw)
        with open(os.path.join(OUT, fname), 'w', encoding='utf-8') as f:
            f.write(mini)

    # CSS
    with open(os.path.join(SRC, 'style.css'), 'r', encoding='utf-8') as f:
        raw = f.read()
    mini = minify_css(raw)
    with open(os.path.join(OUT, 'style.css'), 'w', encoding='utf-8') as f:
        f.write(mini)

    # JS
    with open(os.path.join(SRC, 'script.js'), 'r', encoding='utf-8') as f:
        raw = f.read()
    mini = minify_js(raw)
    with open(os.path.join(OUT, 'script.js'), 'w', encoding='utf-8') as f:
        f.write(mini)

    # 复制静态资源
    asset_src = os.path.join(SRC, 'assets')
    asset_out = os.path.join(OUT, 'assets')
    if os.path.exists(asset_src):
        shutil.copytree(asset_src, asset_out)

    # 复制 CNAME（如有）
    cname = os.path.join(SRC, 'CNAME')
    if os.path.exists(cname):
        shutil.copy2(cname, OUT)

    # 复制 sitemap.xml
    sitemap = os.path.join(SRC, 'sitemap.xml')
    if os.path.exists(sitemap):
        shutil.copy2(sitemap, OUT)

    # 统计
    for fname in os.listdir(OUT):
        if fname == 'assets':
            continue
        fp = os.path.join(OUT, fname)
        orig = os.path.getsize(os.path.join(SRC, fname)) if os.path.exists(os.path.join(SRC, fname)) else 0
        size = os.path.getsize(fp)
        if orig:
            pct = (1 - size / orig) * 100
            print(f'  {fname:<20} {orig:>6,} → {size:>6,} bytes ({pct:.0f}% 压缩)')
        else:
            print(f'  {fname:<20} {"-":>6} → {size:>6,} bytes')

    print(f'\n构建完成 → {OUT}/')

if __name__ == '__main__':
    process()
