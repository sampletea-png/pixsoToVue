<script setup lang="ts">
withDefaults(
  defineProps<{
    /** 主按钮 #1a77fd / 次按钮 #eeeff1 */
    type?: 'primary' | 'default';
    disabled?: boolean;
  }>(),
  {
    type: 'default',
    disabled: false,
  },
);

const emit = defineEmits<{
  (e: 'click', ev: MouseEvent): void;
}>();
</script>

<template>
  <button
    type="button"
    class="app-button"
    :class="`app-button--${type}`"
    :disabled="disabled"
    @click="emit('click', $event)"
  >
    <slot />
  </button>
</template>

<style scoped>
.app-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 26px;
  padding: 0 var(--spacing-md);
  border: none;
  border-radius: var(--radius-md);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-regular);
  line-height: 1;
  cursor: pointer;
  white-space: nowrap;
}

.app-button--primary {
  background: var(--color-primary);
  color: var(--color-surface);
}

.app-button--primary:hover:not(:disabled) {
  filter: brightness(1.08);
}

.app-button--default {
  background: var(--color-border);
  color: var(--color-text);
}

.app-button--default:hover:not(:disabled) {
  background: var(--color-border-strong);
}

.app-button:disabled {
  cursor: not-allowed;
  opacity: 0.5;
}
</style>
