<script setup lang="ts">
withDefaults(
  defineProps<{
    /** 输入值 */
    value?: string | number;
    /** 原生 input type */
    type?: string;
    placeholder?: string;
    disabled?: boolean;
  }>(),
  {
    value: '',
    type: 'text',
    placeholder: '',
    disabled: false,
  },
);

const emit = defineEmits<{
  (e: 'update:value', value: string): void;
}>();

function onInput(ev: Event): void {
  emit('update:value', (ev.target as HTMLInputElement).value);
}
</script>

<template>
  <input
    class="app-input"
    :type="type"
    :value="value"
    :placeholder="placeholder"
    :disabled="disabled"
    @input="onInput"
  />
</template>

<style scoped>
.app-input {
  width: 100%;
  height: 24px;
  padding: 0 var(--spacing-sm);
  box-sizing: border-box;
  border: 1px solid var(--color-border-input);
  border-radius: var(--radius-base);
  background: var(--color-surface);
  color: var(--color-text);
  font-size: var(--font-size-base);
  outline: none;
}

.app-input::placeholder {
  color: var(--color-text-muted);
}

.app-input:focus {
  border-color: var(--color-primary);
}

.app-input:disabled {
  background: var(--color-border);
  color: var(--color-text-disabled);
  cursor: not-allowed;
}
</style>
