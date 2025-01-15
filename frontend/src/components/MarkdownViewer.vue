<template>
  <div class="markdown-content" v-html="compiledMarkdown"></div>
</template>

<script>
import { ref, watch } from 'vue';
import markdownIt from 'markdown-it';
import markdownItKatex from 'markdown-it-katex';
import markdownItAnchor from 'markdown-it-anchor';
import markdownItTableOfContents from 'markdown-it-table-of-contents';

export default {
  name: 'MarkdownViewer',
  props: {
    content: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const md = markdownIt({
      html: true,
      linkify: true,
      typographer: true,
    })
      .use(markdownItKatex) // 支持数学公式
      .use(markdownItAnchor) // 支持标题锚点
      .use(markdownItTableOfContents); // 支持目录生成

    const compiledMarkdown = ref(md.render(props.content));

    watch(
      () => props.content,
      (newContent) => {
        try {
          compiledMarkdown.value = md.render(newContent);
        } catch (error) {
          console.error('Markdown 渲染失败:', error);
          compiledMarkdown.value = '<p>渲染失败，请检查内容格式是否正确。</p>';
        }
      },
    );

    return {
      compiledMarkdown,
    };
  },
};
</script>

<style scoped>
/* 通用 Markdown 样式 */
.markdown-content {
  font-family: Arial, sans-serif;
  line-height: 1.6;
  color: #333;
  background: #fff;
  padding: 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

/* 列表缩进样式 */
.markdown-content ul,
.markdown-content ol {
  margin-left: 20px; /* 列表整体缩进 */
  padding-left: 20px; /* 列表内部缩进 */
}

.markdown-content ul li,
.markdown-content ol li {
  margin-bottom: 8px; /* 列表项间距 */
}

/* 标题样式 */
.markdown-content h1 {
  font-size: 1.8em;
  margin-top: 16px;
  margin-bottom: 8px;
  border-bottom: 2px solid #ddd;
  padding-bottom: 4px;
}

.markdown-content h2 {
  font-size: 1.6em;
  margin-top: 16px;
  margin-bottom: 8px;
}

.markdown-content h3 {
  font-size: 1.4em;
  margin-top: 12px;
  margin-bottom: 8px;
}

.markdown-content h4,
.markdown-content h5,
.markdown-content h6 {
  font-size: 1.2em;
  margin-top: 8px;
  margin-bottom: 4px;
}

/* 代码块样式 */
.markdown-content pre {
  background: #f5f5f5;
  padding: 16px;
  border-radius: 4px;
  overflow-x: auto;
  font-family: 'Courier New', Courier, monospace;
  font-size: 0.9em;
}

.markdown-content code {
  background: #f5f5f5;
  padding: 2px 4px;
  border-radius: 4px;
  font-family: 'Courier New', Courier, monospace;
  font-size: 0.9em;
}

/* 表格样式 */
.markdown-content table {
  width: 100%;
  border-collapse: collapse;
  margin: 16px 0;
}

.markdown-content th,
.markdown-content td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.markdown-content th {
  background-color: #f9f9f9;
}

/* 支持数学公式的样式 */
.katex {
  font-size: 1.1em;
}
</style>
