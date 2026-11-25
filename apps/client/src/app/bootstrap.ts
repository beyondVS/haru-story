import { createPinia } from 'pinia'
import { createApp } from 'vue'
import App from '../App.vue'
import { router } from './router'

export function bootstrap() {
  return createApp(App).use(createPinia()).use(router)
}
