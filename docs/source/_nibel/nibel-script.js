document.addEventListener('DOMContentLoaded', () => {
  // 处理 div.icons 元素
  document.querySelectorAll('div.icons a[aria-label]').forEach(el => el.title = el.ariaLabel);

  // 添加 tippy-skip 类
  document.querySelectorAll('li.toctree-l1.has-children a, div.toc-tree a').forEach(el => el.classList.add('tippy-skip'));

});
