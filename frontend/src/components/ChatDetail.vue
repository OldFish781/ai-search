<template>
    <div class="chat-detail">
        <div class="messages">
            <div v-for="(message, index) in chatMessages" :key="index" :class="['message', message.sender === 'A' ? 'right' : 'left']">
                <div class="avatar-container">
                    <img :src="message.sender === 'A' ? userAvatar : aiAvatar" alt="avatar" class="avatar" />
                    <div class="message-sender">{{ message.sender }}</div>
                </div>
                <div class="message-content">
                    <div class="message-text">
                        <markdown-viewer :content="message.text" />
                    </div>
                </div>
            </div>
        </div>
        <div class="input">
            <input v-model="newMessage" @keyup.enter="handleSendMessage" placeholder="输入消息..." :disabled="isSending" />
            <button @click="handleSendMessage" class="send-button" :disabled="isSending">
                <img src="@/assets/images/send.svg" alt="发送" />
            </button>
        </div>
    </div>
</template>

<script>
import { mapState, mapActions } from 'vuex';
import userAvatar from '@/assets/images/user-avatar.svg';
import aiAvatar from '@/assets/images/ai-avatar.svg';
import MarkdownViewer from './MarkdownViewer.vue';

export default {
  components: { MarkdownViewer },
    name: 'ChatDetail',
    data() {
        return {
            newMessage: '',
            isSending: false,
            userAvatar, // 用户头像路径
            aiAvatar // AI 头像路径
        };
    },
    computed: {
        ...mapState(['chatMessages'])
    },
    methods: {
        ...mapActions(['sendMessage']),
        async handleSendMessage() {
            if (this.newMessage.trim() && !this.isSending) {
                const userMessage = this.newMessage;
                this.sendMessage({ sender: 'A', text: userMessage });
                this.newMessage = '';
                this.isSending = true;

                try {
                    const response = await fetch('http://192.168.1.200:8181/search_and_summarize/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ message: userMessage, max_results: 5 })
                    });
                    const data = await response.json();
                    const aiMessage = data.summary;
                    this.sendMessage({ sender: 'AI', text: aiMessage });
                } catch (error) {
                    console.error('请求失败，请重试。', error);
                    // this.sendMessage({ sender: 'AI', text: '请求失败，请重试。' });
                } finally {
                    this.isSending = false;
                }
            }
        }
    }
};
</script>

<style scoped>
.chat-detail {
    display: flex;
    flex-direction: column;
    height: 100%;
}
.messages {
    flex: 1;
    overflow-y: auto;
    padding: 10px;
    background-color: #f9f9f9;
}
.message {
    display: flex;
    align-items: flex-start;
    margin-bottom: 10px;
}
.message.right {
    flex-direction: row-reverse;
}
.message.left {
    flex-direction: row;
}
.avatar-container {
    display: flex;
    flex-direction: column;
    align-items: center;
}
.avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin: 0 10px;
}
.message-content {
    max-width: 70%;
}
.message-text {
    border-radius: 10px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}
.message.right .message-text {
    background-color: #b5e2fe;
}
.message.left .message-text {
    background-color: #f1f0f0;
}
.message-sender {
    font-size: 12px;
    color: #888;
    text-align: center;
    margin-top: 5px;
}
.input {
    display: flex;
    align-items: center;
    border-top: 1px solid #ccc;
    padding: 10px;
    background-color: #fff;
}
input {
    flex: 1;
    padding: 10px;
    box-sizing: border-box;
    margin-right: 10px;
    border: 1px solid #ccc;
    border-radius: 5px;
}
.send-button {
    background: none;
    border: none;
    cursor: pointer;
    border-radius: 3px;
    background: #2070f2;
    padding: 5px 20px;
}
.send-button img {
    width: 24px;
    height: 24px;
}
.send-button:hover {
    background: #0056b3;
}
.send-button:active {
    background: #003f7f;
}
.send-button:disabled {
    background: #ccc;
    cursor: not-allowed;
}

h1, h2, h3, h4, h5, h6, li, tr, td, th, p {
    margin-left: 20px;
}
</style>
