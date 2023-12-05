<template>
  <div v-html="text"></div>
  <!-- 使用 v-html 来渲染 HTML -->
</template>

<script>
export default {
  props: ["title", "text"], // 使用 title 和 text props
};
</script>
