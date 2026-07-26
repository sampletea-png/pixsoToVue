import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  { path: '/', redirect: '/param-estimation' },
  { path: '/param-estimation', name: 'param-estimation', component: () => import('@/modules/param-estimation/index.vue') }
]

export default createRouter({
  history: createWebHistory(),
  routes,
})
