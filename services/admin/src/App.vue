<script setup lang="ts">
import { onMounted, ref } from 'vue'

const status = ref('연결 확인 중')
const checking = ref(false)

async function checkConnection() {
  checking.value = true
  status.value = '연결 확인 중'
  try {
    const response = await fetch('/graphql', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query: 'query ServiceStatus { serviceStatus }' }),
      signal: AbortSignal.timeout(5000),
    })
    const result: { data?: { serviceStatus?: string } } = await response.json()
    status.value = response.ok && result.data?.serviceStatus === 'ok'
      ? '서버 연결됨'
      : '서버 연결 실패'
  } catch {
    status.value = '서버 연결 실패'
  } finally {
    checking.value = false
  }
}

onMounted(checkConnection)
</script>

<template>
  <main>
    <h1>하루 이야기 관리자</h1>
    <p role="status">{{ status }}</p>
    <button type="button" :disabled="checking" @click="checkConnection">다시 확인</button>
  </main>
</template>

<style>
:root {
  font-family: system-ui, sans-serif;
  color: #1f2937;
  background: #f2f5f9;
}

body {
  margin: 0;
}

main {
  max-width: 48rem;
  margin: 10vh auto;
  padding-inline: 1.5rem;
}

button {
  font: inherit;
  padding: 0.5rem 0.8rem;
}
</style>
