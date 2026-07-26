<script setup lang="ts">
import AppIcon from './AppIcon.vue';

withDefaults(
  defineProps<{
    /** AppIcon 图标名 */
    icon: string;
    disabled?: boolean;
    /** 选中/激活态（主色高亮底） */
    active?: boolean;
  }>(),
  {
    disabled: false,
    active: false,
  },
);

const emit = defineEmits<{
  (e: 'click', ev: MouseEvent): void;
}>();
</script>

<template>
  <button
    type="button"
    class="icon-button"
    :class="{ 'is-active': active }"
    :disabled="disabled"
    @click="emit('click', $event)"
  >
    <AppIcon :name="icon" :size="16" />
  </button>
</template>

<style scoped>
.icon-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  padding: 0;
  border: none;
  border-radius: var(--radius-base);
  background: transparent;
  color: var(--color-icon);
  cursor: pointer;
}

.icon-button:hover:not(:disabled):not(.is-active) {
  background: var(--color-border);
}

.icon-button.is-active {
  background: var(--color-primary-light);
  color: var(--color-primary);
}

.icon-button:disabled {
  color: var(--color-text-disabled);
  cursor: not-allowed;
}
</style>
