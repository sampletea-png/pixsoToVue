<script setup lang="ts">
withDefaults(
  defineProps<{
    checked: boolean;
    label: string;
    disabled?: boolean;
  }>(),
  {
    disabled: false,
  },
);

const emit = defineEmits<{
  (e: 'update:checked', value: boolean): void;
}>();

function onSelect(): void {
  emit('update:checked', true);
}
</script>

<template>
  <label
    class="app-radio"
    :class="{ 'is-checked': checked, 'is-disabled': disabled }"
  >
    <input
      class="app-radio__input"
      type="radio"
      :checked="checked"
      :disabled="disabled"
      @change="onSelect"
    />
    <span class="app-radio__dot" aria-hidden="true" />
    <span class="app-radio__label">{{ label }}</span>
  </label>
</template>

<style scoped>
.app-radio {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: var(--font-size-base);
  color: var(--color-text);
  cursor: pointer;
  user-select: none;
}

.app-radio__input {
  position: absolute;
  width: 1px;
  height: 1px;
  opacity: 0;
  pointer-events: none;
}

.app-radio__dot {
  position: relative;
  flex: none;
  width: 16px;
  height: 16px;
  box-sizing: border-box;
  border: 1px solid var(--color-border-input);
  border-radius: 50%;
  background: var(--color-surface);
  transition: border-color 0.1s ease;
}

/* 选中内圆点 */
.app-radio__dot::after {
  content: '';
  position: absolute;
  left: 50%;
  top: 50%;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-primary);
  transform: translate(-50%, -50%) scale(0);
  transition: transform 0.1s ease;
}

/* 设计稿：选中项标签为主色 */
.app-radio.is-checked {
  color: var(--color-primary);
}

.app-radio.is-checked .app-radio__dot {
  border-color: var(--color-primary);
}

.app-radio.is-checked .app-radio__dot::after {
  transform: translate(-50%, -50%) scale(1);
}

.app-radio.is-disabled {
  cursor: not-allowed;
  color: var(--color-text-disabled);
}

.app-radio.is-disabled .app-radio__dot {
  background: var(--color-border);
  border-color: var(--color-border-strong);
}
</style>
