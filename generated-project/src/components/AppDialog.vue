<script setup lang="ts">
import AppIcon from './AppIcon.vue';

withDefaults(
  defineProps<{
    /** 弹窗标题 */
    title: string;
    /** 弹窗宽度，数字按 px 处理 */
    width?: number | string;
  }>(),
  {
    width: 480,
  },
);

const emit = defineEmits<{
  (e: 'close'): void;
}>();

function formatWidth(w: number | string): string {
  return typeof w === 'number' ? `${w}px` : w;
}
</script>

<template>
  <!-- 设计稿弹窗无遮罩：position:fixed 居中 + 投影 -->
  <div
    class="app-dialog"
    :style="{ width: formatWidth(width) }"
    role="dialog"
    :aria-label="title"
  >
    <header class="app-dialog__header">
      <!-- TODO: 品牌 LOGO 占位方块，待接入正式资源 -->
      <span class="app-dialog__logo" aria-hidden="true" />
      <h2 class="app-dialog__title">{{ title }}</h2>
      <button
        type="button"
        class="app-dialog__close"
        aria-label="Close"
        @click="emit('close')"
      >
        <AppIcon name="close" :size="12" />
      </button>
    </header>
    <div class="app-dialog__body">
      <slot />
    </div>
    <footer v-if="$slots.footer" class="app-dialog__footer">
      <slot name="footer" />
    </footer>
  </div>
</template>

<style scoped>
.app-dialog {
  position: fixed;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  z-index: 100;
  display: flex;
  flex-direction: column;
  max-height: 90vh;
  background: var(--color-surface);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-dialog);
  font-size: var(--font-size-base);
  color: var(--color-text);
}

.app-dialog__header {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md) var(--spacing-md) var(--spacing-sm);
}

.app-dialog__logo {
  flex: none;
  width: 20px;
  height: 20px;
  border-radius: var(--radius-base);
  background: var(--color-primary);
}

.app-dialog__title {
  flex: 1;
  margin: 0;
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-bold);
  line-height: 20px;
}

.app-dialog__close {
  flex: none;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  padding: 0;
  border: none;
  background: transparent;
  color: var(--color-text-muted);
  cursor: pointer;
  border-radius: var(--radius-base);
}

.app-dialog__close:hover {
  color: var(--color-text);
  background: var(--color-border);
}

.app-dialog__body {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: var(--spacing-sm) var(--spacing-md) var(--spacing-md);
}

.app-dialog__footer {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: var(--spacing-sm);
  padding: 0 var(--spacing-md) var(--spacing-md);
}
</style>
