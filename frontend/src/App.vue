<script setup lang="ts">
import { computed, nextTick, ref } from "vue";

type Role = "user" | "assistant";

interface ChatMessage {
  role: Role;
  content: string;
}

const input = ref("");
const messages = ref<ChatMessage[]>([
  {
    role: "assistant",
    content: "你好，我是你的 AI 助手。有什么想聊的？",
  },
]);
const isSending = ref(false);
const errorMessage = ref("");
const messagesEl = ref<HTMLElement | null>(null);

const canSend = computed(() => input.value.trim().length > 0 && !isSending.value);

async function scrollToBottom() {
  await nextTick();
  messagesEl.value?.scrollTo({
    top: messagesEl.value.scrollHeight,
    behavior: "smooth",
  });
}

function appendToMessage(index: number, chunk: string) {
  const message = messages.value[index];
  if (!message) return;

  messages.value[index] = {
    ...message,
    content: message.content + chunk,
  };
}

async function readStream(response: Response, messageIndex: number) {
  if (!response.body) {
    throw new Error("浏览器不支持流式响应");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder("utf-8");

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;

    appendToMessage(messageIndex, decoder.decode(value, { stream: true }));
    await scrollToBottom();
  }

  const remaining = decoder.decode();
  if (remaining) {
    appendToMessage(messageIndex, remaining);
  }
}

async function sendMessage() {
  const content = input.value.trim();
  if (!content || isSending.value) return;

  errorMessage.value = "";
  input.value = "";
  messages.value.push({ role: "user", content });
  messages.value.push({ role: "assistant", content: "" });

  const assistantIndex = messages.value.length - 1;

  isSending.value = true;
  await scrollToBottom();

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        messages: messages.value.slice(1, assistantIndex).map((message) => ({
          role: message.role,
          content: message.content,
        })),
      }),
    });

    if (!response.ok) {
      throw new Error(`请求失败：${response.status}`);
    }

    await readStream(response, assistantIndex);

    if (!messages.value[assistantIndex]?.content.trim()) {
      messages.value[assistantIndex] = {
        role: "assistant",
        content: "我暂时没有收到有效回复。",
      };
    }
  } catch (error) {
    if (!messages.value[assistantIndex]?.content) {
      messages.value.splice(assistantIndex, 1);
    }

    errorMessage.value =
      error instanceof Error ? error.message : "发送失败，请稍后再试。";
  } finally {
    isSending.value = false;
    await scrollToBottom();
  }
}
</script>

<template>
  <main class="app-shell">
    <section class="chat-panel" aria-label="AI 对话">
      <header class="chat-header">
        <div>
          <p class="eyebrow">My Assistant</p>
          <h1>AI 对话助手</h1>
        </div>
        <span class="status-dot" title="连接到本地后端"></span>
      </header>

      <div ref="messagesEl" class="message-list">
        <article
          v-for="(message, index) in messages"
          :key="`${message.role}-${index}`"
          class="message-row"
          :class="message.role"
        >
          <div class="message-bubble" :class="{ typing: isSending && !message.content }">
            {{ message.content || "思考中..." }}
          </div>
        </article>
      </div>

      <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>

      <form class="composer" @submit.prevent="sendMessage">
        <textarea
          v-model="input"
          rows="1"
          placeholder="输入消息，按 Enter 发送"
          @keydown.enter.exact.prevent="sendMessage"
        ></textarea>
        <button type="submit" :disabled="!canSend">
          {{ isSending ? "发送中" : "发送" }}
        </button>
      </form>
    </section>
  </main>
</template>
