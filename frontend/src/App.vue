<template>
  <div id="app">
    <Header />
    <div class="container">
      <ChatHistory @toggle-collapse="handleToggleCollapse" ref="chatHistory" />
      <div class="chat-area" :class="{ 'full-width': isChatHistoryCollapsed }">
        <button class="toggle-button" @click="toggleChatHistory">
          {{ isChatHistoryCollapsed ? '展开' : '折叠' }}
        </button>
        <ChatDetail />
      </div>
    </div>
  </div>
</template>

<script>
import Header from './components/Header.vue';
import ChatHistory from './components/ChatHistory.vue';
import ChatDetail from './components/ChatDetail.vue';
import { mapActions } from 'vuex';

export default {
  components: {
    Header,
    ChatHistory,
    ChatDetail
  },
  data() {
    return {
      isChatHistoryCollapsed: false
    };
  },
  methods: {
    ...mapActions(['loadChat']),
    handleToggleCollapse(isCollapsed) {
      this.isChatHistoryCollapsed = isCollapsed;
    },
    toggleChatHistory() {
      this.$refs.chatHistory.toggleCollapse();
    }
  },
  mounted() {
    this.loadChat(0); // 加载默认会话
  }
};
</script>

<style>
/* 添加一些基本样式 */
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
}
#app {
  display: flex;
  flex-direction: column;
  height: 100vh;
}
.container {
  display: flex;
  flex: 1;
  width: 100%;
  height: calc(100vh - 60px); /* 减去 Header 的高度 */
}
.chat-area {
  display: flex;
  flex-direction: column;
  width: 85%;
  transition: width 0.3s;
  position: relative;
}
.chat-area.full-width {
  width: 100%;
}
.toggle-button {
  position: absolute;
  top: 10px;
  left: 10px;
  padding: 5px 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.toggle-button:hover {
  background-color: #0056b3;
}
</style>
