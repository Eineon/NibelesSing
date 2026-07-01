# Configuration file for the Sphinx documentation builder.

import re
import os
import datetime
from sphinx.application import Sphinx


SYMBOL_MAP = {
    "\\<--": "←",
    "\\-->": "→",
    "\\<->": "↔",
    "\\<==": "⇐",
    "\\==>": "⇒",
    "\\<=>": "⇔",
    "\\<>": "⋄",
    "\\<=": "≤",
    "\\>=": "≥",
    "\\!=": "≠",
    "\\~=": "≈",
    "\\+-": "±",
}

GRID_SIZE = {
    "L": "12",
    "M": "6",
    "S": "4",
    "A": "auto"
}

CARD_RULES = [
    {
        "key": re.compile(r"【(sign):([^】:]+):?([^】]*)】"),
        "value": [" {hyper}`", "{type=badge,color=secondary,outline=true}` "],
    },
    {
        "key": re.compile(r"【(cell):([^】:]+):?([^】]*)】"),
        "value": ["{hyper}`", "`"],
    },
    {
        "key": re.compile(r"【(word):([^】:]+):?([^】]*)】"),
        "value": ["{hyper}`", "`"],
    },
    {
        "key": re.compile(r"【(term):([^】:]+):?([^】]*)】"),
        "value": ["{term}`", "`"],
    },
]

NODE_RULES = [
    {
        "key": re.compile(r"\[\[grid-([^:]+):((?:(?!\]\])[\s\S])*)\]\]", re.MULTILINE),
        "value": lambda m: (
            f"\n:::{{grid-item}}\n:columns: {GRID_SIZE[m.group(1)]}\n{m.group(2).strip()}\n:::\n"
        ),
    },
    {
        "key": re.compile(r"（(.*?):(.*?)）"),
        "value": lambda m: (
            f'<ruby class="annot">{m.group(1)}<rt class="up-note">{m.group(2)}</rt></ruby>'
        ),
    },
    {
        "key": re.compile(r"［(.*?)］"),
        "value": lambda m: (f' <span class="form">⦗{m.group(1)}⦘</span> '),
    },
    {
        "key": re.compile(r"\*\*(.*?)\*\*"),
        "value": lambda m: (f'<span class="word">{m.group(1)}</span>'),
    },
]


def process_content(source):
    """应用所有替换规则到文本内容"""
    content = source[0]
    for symbol in sorted(SYMBOL_MAP, key=lambda k: -len(k)):
        content = content.replace(symbol, SYMBOL_MAP[symbol])

    for rule in CARD_RULES:
        def card_rep(m, r=rule):
            t0, t1, t2 = m.groups()
            part = r["value"]
            brL = "『" if t0 == "cell" else ""
            brR = "』" if t0 == "cell" else ""
            return f"{part[0]}{brL}{t2.replace('@', t1) if t2 else t1}{brR} <{t1}>{part[1]}"
        content = rule["key"].sub(card_rep, content)

    for rule in NODE_RULES:
        content = rule["key"].sub(rule["value"], content)

    source[0] = content


def handle_source_read(app: Sphinx, docname: str, source: list):
    """处理source-read事件"""
    file_path = app.env.doc2path(docname)
    if os.path.splitext(file_path)[1] == ".md":
        process_content(source)


def setup(app: Sphinx):
    """Sphinx扩展入口"""
    app.connect("source-read", handle_source_read)
    return {"version": "0.1", "parallel_read_safe": True}


# -- General configuration
extensions = [
    "sphinx.ext.todo",
    # "myst_parser",
    "myst_nb",
    "sphinx_design",
    "sphinx_design_elements",
    "sphinx_copybutton",
    "sphinx_tippy",
    "sphinx_togglebutton",
    "sphinxcontrib.mermaid",
]
myst_enable_extensions = [
    "amsmath",  # AMS 数学公式
    "attrs_block",  # 区块属性
    "attrs_inline",  # 行内属性
    "colon_fence",  # 冒号的代码围栏
    "deflist",  # 定义列表
    "dollarmath",  # 行内数学公式
    "fieldlist",  # 字段列表
    "html_admonition",  # HTML 警告
    "html_image",  # HTML 图像
    "linkify",  # 链接
    "replacements",  # 排版文本转换
    # "smartquotes",  # 智能引号
    "strikethrough",  # 删除线
    "substitution",  # 替换
    "tasklist",  # 任务列表
]

myst_substitutions = {
    # "替换对象": "替换内容",
}

myst_url_schemes = {
    "en-wiki": "https://en.wikipedia.org/wiki/{{path}}#{{fragment}}",
    "zh-wiki": "https://zh.wikipedia.org/wiki/{{path}}#{{fragment}}",
    "baike": "https://baike.baidu.com/item/{{path}}#{{fragment}}",
    "gh-issue": {
        "url": "https://github.com/Eineon/nibelessing/issues/{{path}}#{{fragment}}",
        "title": "议题#{{path}}",
        "classes": ["github"],
    },
}

# 确保目标唯一
myst_heading_anchors = 4

todo_include_todos = True

togglebutton_hint = "展示隐藏内容"

tippy_props = {
    "placement": "auto-start",
    "maxWidth": 720,
    "theme": "material",
    "interactive": True,
    "duration": [200, 400],
    "delay": [200, 0],
}
tippy_skip_anchor_classes = (
    "headerlink",
    "sd-stretched-link",
    "sd-rounded-pill",
    "tippy-skip",
)

suppress_warnings = ["myst.xref_missing"]

source_suffix = [".md"]
master_doc = "index"

# -- Project information

language = "zh_CN"
project = "银雾止颂"
version = release = "Nibelessing"
now = datetime.datetime.now()
copyright = f"2026-{now.year}, Eineon"
author = "ネオン様"

# -- Options for HTML output
html_title = "银雾止颂"
# html_logo = "_nibel/.png"
# html_favicon = "_nibel/.svg"
html_static_path = ["_nibel"]
html_css_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.1/css/all.min.css",
    "https://unpkg.com/tippy.js@6/animations/scale.css",
    "nibel-style.css",
]
html_js_files = ["nibel-script.js"]
templates_path = ["_nibel/templet"]

# -- HTML theme settings
html_show_sphinx = False
html_last_updated_fmt = "%Y/%m/%d"
html_theme = "furo"
html_theme_options = {
    "sidebar_hide_name": True,
    "navigation_with_keys": True,
    "light_css_variables": {
        # 文本颜色
        "color-foreground-muted": "hsl(265, 100%, 45%)",
        # 元素颜色
        "color-brand-primary": "hsl(345, 100%, 45%)",
        "color-brand-content": "hsl(185, 100%, 45%)",
        "color-brand-visited": "var(--color-brand-content)",
        "color-highlight-on-target": "var(--color-highlight-vertical)",
        "color-brand-word": "hsl(205, 100%, 45%)",
        # 其他样式
        "admonition-title-font-size": ".9rem",
    },
    "dark_css_variables": {
        # 文本颜色
        "color-foreground-muted": "hsl(265, 100%, 65%)",
        # 元素颜色
        "color-brand-primary": "hsl(345, 100%, 60%)",
        "color-brand-content": "hsl(185, 100%, 60%)",
        "color-brand-visited": "var(--color-brand-content)",
        "color-highlight-on-target": "var(--color-highlight-vertical)",
        "color-brand-word": "hsl(205, 100%, 60%)",
        # 其他样式
        "admonition-title-font-size": ".9rem",
    },
    "footer_icons": [
        {
            "name": "更新日志",
            "url": "https://github.com/Eineon/nibelessing/commits/main",
            "html": "",
            "class": "fa-solid fa-code-commit",
        },
        {
            "name": "GitHub",
            "url": "https://github.com/Eineon/nibelessing",
            "html": "",
            "class": "fa-brands fa-github",
        },
        {
            "name": "Read the Docs",
            "url": "https://app.readthedocs.org/projects/nibelessing",
            "html": """
                <svg x="0px" y="0px" viewBox="-125 217 360 360" xml:space="preserve">
                  <path fill="currentColor" d="M39.2,391.3c-4.2,0.6-7.1,4.4-6.5,8.5c0.4,3,2.6,5.5,5.5,6.3 c0,0,18.5,6.1,50,8.7c25.3,2.1,54-1.8,54-1.8c4.2-0.1,7.5-3.6,7.4-7.8c-0.1-4.2-3.6-7.5-7.8-7.4c-0.5,0-1,0.1-1.5,0.2 c0,0-28.1,3.5-50.9,1.6c-30.1-2.4-46.5-7.9-46.5-7.9C41.7,391.3,40.4,391.1,39.2,391.3z M39.2,353.6c-4.2,0.6-7.1,4.4-6.5,8.5 c0.4,3,2.6,5.5,5.5,6.3c0,0,18.5,6.1,50,8.7c25.3,2.1,54-1.8,54-1.8c4.2-0.1,7.5-3.6,7.4-7.8c-0.1-4.2-3.6-7.5-7.8-7.4 c-0.5,0-1,0.1-1.5,0.2c0,0-28.1,3.5-50.9,1.6c-30.1-2.4-46.5-7.9-46.5-7.9C41.7,353.6,40.4,353.4,39.2,353.6z M39.2,315.9 c-4.2,0.6-7.1,4.4-6.5,8.5c0.4,3,2.6,5.5,5.5,6.3c0,0,18.5,6.1,50,8.7c25.3,2.1,54-1.8,54-1.8c4.2-0.1,7.5-3.6,7.4-7.8 c-0.1-4.2-3.6-7.5-7.8-7.4c-0.5,0-1,0.1-1.5,0.2c0,0-28.1,3.5-50.9,1.6c-30.1-2.4-46.5-7.9-46.5-7.9 C41.7,315.9,40.4,315.8,39.2,315.9z M39.2,278.3c-4.2,0.6-7.1,4.4-6.5,8.5c0.4,3,2.6,5.5,5.5,6.3c0,0,18.5,6.1,50,8.7 c25.3,2.1,54-1.8,54-1.8c4.2-0.1,7.5-3.6,7.4-7.8c-0.1-4.2-3.6-7.5-7.8-7.4c-0.5,0-1,0.1-1.5,0.2c0,0-28.1,3.5-50.9,1.6 c-30.1-2.4-46.5-7.9-46.5-7.9C41.7,278.2,40.4,278.1,39.2,278.3z M-13.6,238.5c-39.6,0.3-54.3,12.5-54.3,12.5v295.7 c0,0,14.4-12.4,60.8-10.5s55.9,18.2,112.9,19.3s71.3-8.8,71.3-8.8l0.8-301.4c0,0-25.6,7.3-75.6,7.7c-49.9,0.4-61.9-12.7-107.7-14.2 C-8.2,238.6-10.9,238.5-13.6,238.5z M19.5,257.8c0,0,24,7.9,68.3,10.1c37.5,1.9,75-3.7,75-3.7v267.9c0,0-19,10-66.5,6.6 C59.5,536.1,19,522.1,19,522.1L19.5,257.8z M-3.6,264.8c4.2,0,7.7,3.4,7.7,7.7c0,4.2-3.4,7.7-7.7,7.7c0,0-12.4,0.1-20,0.8 c-12.7,1.3-21.4,5.9-21.4,5.9c-3.7,2-8.4,0.5-10.3-3.2c-2-3.7-0.5-8.4,3.2-10.3c0,0,0,0,0,0c0,0,11.3-6,27-7.5 C-16,264.9-3.6,264.8-3.6,264.8z M-11,302.6c4.2-0.1,7.4,0,7.4,0c4.2,0.5,7.2,4.3,6.7,8.5c-0.4,3.5-3.2,6.3-6.7,6.7 c0,0-12.4,0.1-20,0.8c-12.7,1.3-21.4,5.9-21.4,5.9c-3.7,2-8.4,0.5-10.3-3.2c-2-3.7-0.5-8.4,3.2-10.3c0,0,11.3-6,27-7.5 C-20.5,302.9-15.2,302.7-11,302.6z M-3.6,340.2c4.2,0,7.7,3.4,7.7,7.7s-3.4,7.7-7.7,7.7c0,0-12.4-0.1-20,0.7 c-12.7,1.3-21.4,5.9-21.4,5.9c-3.7,2-8.4,0.5-10.3-3.2c-2-3.7-0.5-8.4,3.2-10.3c0,0,11.3-6,27-7.5C-16,340.1-3.6,340.2-3.6,340.2z"></path>
                </svg>
            """,
            "class": "",
        },
    ],
    "source_repository": "https://github.com/Eineon/nibelessing/",
    "source_branch": "main",
    "source_directory": "docs/source/",
}

# -- Options for HTMLHelp output
htmlhelp_basename = "银雾止颂"

# -- Options for EPUB output
epub_show_urls = "footnote"
