<template>
  <div class="chat-history" :class="{ collapsed: isCollapsed }">
    <button @click="addNewChat" class="add-chat-button">
      <img src="@/assets/images/add_chat.svg" alt="添加" />
    </button>
    <ul v-if="!isCollapsed">
      <li
        v-for="(chat, index) in chatHistory"
        :key="index"
        @click="loadChat(index)"
        :class="{ selected: index === currentChatIndex }"
      >
        <div class="chat-title">{{ chat.title }}</div>
      </li>
    </ul>
  </div>
</template>

<script>
import { mapState, mapActions } from "vuex";

export default {
  name: "ChatHistory",
  computed: {
    ...mapState(["chatHistory", "currentChatIndex"]),
  },
  data() {
    return {
      isCollapsed: false,
    };
  },
  methods: {
    ...mapActions(["loadChat", "addNewChat"]),
    toggleCollapse() {
      this.isCollapsed = !this.isCollapsed;
      this.$emit("toggle-collapse", this.isCollapsed);
    },
  },
};
</script>

<style scoped>
.chat-history {
  border-right: 1px solid #ccc;
  width: 15%;
  overflow-y: auto;
  transition: width 0.3s, padding 0.3s;
  height: calc(100vh - 60px); /* 减去 Header 的高度 */
}
.chat-history.collapsed {
  width: 0;
  padding: 0;
}
.add-chat-button {
  margin: 5px;
  padding: 5px;
  border: none;
  background-color: #f5f5f5;
  cursor: pointer;
  border-radius: 4px;
}
.add-chat-button img {
  width: 25px;
  height: 25px;
}
.add-chat-button:hover {
  background-color: #e0e0e0;
}
.add-chat-button:active {
  background-color: #ccc;
}
button {
  margin-bottom: 10px;
}
ul {
  list-style: none;
  padding: 0;
  margin: 0;
  max-height: calc(
    100vh - 60px - 50px
  ); /* 调整高度以适应屏幕，减去按钮的高度 */
  overflow-y: auto; /* 超出时滚动 */
}
li {
  padding: 10px;
  border-bottom: 1px solid #ccc;
  cursor: pointer;
}
li:hover {
  background-color: #f5f5f5;
}
li.selected {
  background-color: #e0e0e0;
}
.chat-title {
  font-size: 16px;
  font-weight: bold;
}
</style>
