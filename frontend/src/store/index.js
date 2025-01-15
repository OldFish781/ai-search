import { createStore } from 'vuex';

export default createStore({
  state: {
    chatHistory: JSON.parse(localStorage.getItem('chatHistory')) || [{ title: '默认对话', messages: [] }],
    chatMessages: [],
    currentChatIndex: 0
  },
  mutations: {
    setChatMessages(state, { messages, index }) {
      state.chatMessages = messages;
      state.currentChatIndex = index;
    },
    addMessage(state, { sender, text }) {
      state.chatMessages.push({ sender, text });
    },
    saveChat(state) {
      if (state.currentChatIndex === -1) {
        state.chatHistory.push({ title: `对话 ${state.chatHistory.length + 1}`, messages: [...state.chatMessages] });
        state.currentChatIndex = state.chatHistory.length - 1;
      } else {
        state.chatHistory[state.currentChatIndex].messages = [...state.chatMessages];
      }
      localStorage.setItem('chatHistory', JSON.stringify(state.chatHistory));
    },
    updateChatHistory(state) {
      if (state.currentChatIndex !== -1) {
        state.chatHistory[state.currentChatIndex].messages = [...state.chatMessages];
        // 将当前会话移动到最前面
        const currentChat = state.chatHistory.splice(state.currentChatIndex, 1)[0];
        state.chatHistory.unshift(currentChat);
        state.currentChatIndex = 0;
      }
      localStorage.setItem('chatHistory', JSON.stringify(state.chatHistory));
    },
    addNewChat(state) {
      state.chatHistory.unshift({ title: `对话 ${state.chatHistory.length + 1}`, messages: [] });
      state.currentChatIndex = 0;
      state.chatMessages = [];
      localStorage.setItem('chatHistory', JSON.stringify(state.chatHistory));
    }
  },
  actions: {
    loadChat({ commit, state }, index) {
      const messages = state.chatHistory[index].messages || [];
      commit('setChatMessages', { messages, index });
    },
    sendMessage({ commit }, { sender, text }) {
      commit('addMessage', { sender, text });
      commit('updateChatHistory');
    },
    addNewChat({ commit }) {
      commit('addNewChat');
    }
  }
});
