
<template>
  <header class="header">
    <img src="@/assets/images/favicon.ico" alt="Logo" class="logo" />
    <h1>AI-Search</h1>
  </header>
</template>

<script>
export default {
  name: 'Header'
};
</script>

<style scoped>
.header {
  display: flex;
  align-items: center;
  background-color: #f5f5f5;
  border-bottom: 1px solid #ccc;
}
.logo {
  height: 48px;
  margin-right: 10px;
}
h1 {
  margin: 0;
  font-size: 24px;
}
</style>
