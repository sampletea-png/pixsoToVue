<script setup lang="ts">
withDefaults(
  defineProps<{
    checked: boolean;
    label?: string;
    disabled?: boolean;
  }>(),
  {
    label: '',
    disabled: false,
  },
);

const emit = defineEmits<{
  (e: 'update:checked', value: boolean): void;
}>();

function onChange(ev: Event): void {
  emit('update:checked', (ev.target as HTMLInputElement).checked);
}
</script>

<template>
  <label
    class="app-checkbox"
    :class="{ 'is-checked': checked, 'is-disabled': disabled }"
  >
    <input
      class="app-checkbox__input"
      type="checkbox"
      :checked="checked"
      :disabled="disabled"
      @change="onChange"
    />
    <span class="app-checkbox__box" aria-hidden="true" />
    <span v-if="label" class="app-checkbox__label">{{ label }}</span>
  </label>
</template>

<style scoped>
.app-checkbox {
  display: inline-flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: var(--font-size-base);
  color: var(--color-text);
  cursor: pointer;
  user-select: none;
}

.app-checkbox__input {
  position: absolute;
  width: 1px;
  height: 1px;
  opacity: 0;
  pointer-events: none;
}

.app-checkbox__box {
  position: relative;
  flex: none;
  width: 16px;
  height: 16px;
  box-sizing: border-box;
  border: 1px solid var(--color-border-input);
  border-radius: var(--radius-sm);
  background: var(--color-surface);
  transition: background 0.1s ease, border-color 0.1s ease;
}

/* 对勾：CSS 折线 */
.app-checkbox__box::after {
  content: '';
  position: absolute;
  left: 4px;
  top: 1px;
  width: 5px;
  height: 9px;
  box-sizing: border-box;
  border: solid var(--color-surface);
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
  opacity: 0;
}

.app-checkbox.is-checked .app-checkbox__box {
  background: var(--color-primary);
  border-color: var(--color-primary);
}

.app-checkbox.is-checked .app-checkbox__box::after {
  opacity: 1;
}

.app-checkbox.is-disabled {
  cursor: not-allowed;
  color: var(--color-text-disabled);
}

.app-checkbox.is-disabled .app-checkbox__box {
  background: var(--color-border);
  border-color: var(--color-border-strong);
}

.app-checkbox.is-disabled.is-checked .app-checkbox__box {
  background: var(--color-border-strong);
}
</style>
