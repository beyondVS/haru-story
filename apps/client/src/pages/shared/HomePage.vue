<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { fetchServiceStatus } from '../../api/client'

const status = ref('연결 확인 중')
const checking = ref(false)

async function checkConnection() {
  checking.value = true
  status.value = '연결 확인 중'
  try {
    status.value = (await fetchServiceStatus()) ? '서버 연결됨' : '서버 연결 실패'
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
    <h1>하루 이야기</h1>
    <p role="status">{{ status }}</p>
    <button type="button" :disabled="checking" @click="checkConnection">다시 확인</button>
  </main>
</template>
