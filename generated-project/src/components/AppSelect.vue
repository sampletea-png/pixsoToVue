<script lang="ts">
export interface SelectOption {
  label: string;
  value: string | number;
}
</script>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue';
import AppIcon from './AppIcon.vue';

const props = withDefaults(
  defineProps<{
    /** 当前选中值 */
    value?: string | number | null;
    options: SelectOption[];
    placeholder?: string;
    disabled?: boolean;
  }>(),
  {
    value: null,
    placeholder: 'Select',
    disabled: false,
  },
);

const emit = defineEmits<{
  (e: 'update:value', value: string | number): void;
  (e: 'change', value: string | number): void;
}>();

const open = ref(false);
const root = ref<HTMLElement | null>(null);

const selectedLabel = computed<string>(() => {
  const hit = props.options.find((o) => o.value === props.value);
  return hit ? hit.label : '';
});

function toggle(): void {
  if (props.disabled) return;
  open.value = !open.value;
}

function choose(opt: SelectOption): void {
  open.value = false;
  if (opt.value === props.value) return;
  emit('update:value', opt.value);
  emit('change', opt.value);
}

function onDocClick(ev: MouseEvent): void {
  if (root.value && !root.value.contains(ev.target as Node)) {
    open.value = false;
  }
}

onMounted(() => document.addEventListener('click', onDocClick));
onBeforeUnmount(() => document.removeEventListener('click', onDocClick));
</script>

<template>
  <div
    ref="root"
    class="app-select"
    :class="{ 'is-open': open, 'is-disabled': disabled }"
  >
    <button
      type="button"
      class="app-select__control"
      :disabled="disabled"
      :aria-expanded="open"
      @click="toggle"
    >
      <span
        class="app-select__value"
        :class="{ 'is-placeholder': !selectedLabel }"
      >
        {{ selectedLabel || placeholder }}
      </span>
      <AppIcon class="app-select__arrow" name="chevron-down" :size="12" />
    </button>
    <ul v-if="open" class="app-select__dropdown" role="listbox">
      <li
        v-for="opt in options"
        :key="opt.value"
        class="app-select__option"
        :class="{ 'is-selected': opt.value === value }"
        role="option"
        :aria-selected="opt.value === value"
        @click="choose(opt)"
      >
        {{ opt.label }}
      </li>
      <li v-if="options.length === 0" class="app-select__option is-empty">
        No options
      </li>
    </ul>
  </div>
</template>

<style scoped>
.app-select {
  position: relative;
  display: inline-block;
  min-width: 108px;
  font-size: var(--font-size-base);
}

.app-select__control {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--spacing-sm);
  width: 100%;
  height: 24px;
  padding: 0 var(--spacing-sm);
  box-sizing: border-box;
  border: 1px solid var(--color-border-input);
  border-radius: var(--radius-base);
  background: var(--color-surface);
  color: var(--color-text);
  font-size: var(--font-size-base);
  cursor: pointer;
}

.app-select.is-open .app-select__control {
  border-color: var(--color-primary);
}

.app-select__control:disabled {
  background: var(--color-border);
  color: var(--color-text-disabled);
  cursor: not-allowed;
}

.app-select__value {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.app-select__value.is-placeholder {
  color: var(--color-text-muted);
}

.app-select__arrow {
  flex: none;
  color: var(--color-icon);
  transition: transform 0.1s ease;
}

.app-select.is-open .app-select__arrow {
  transform: rotate(180deg);
}

.app-select__dropdown {
  position: absolute;
  left: 0;
  right: 0;
  top: calc(100% + 2px);
  z-index: 120;
  margin: 0;
  padding: var(--spacing-xs) 0;
  list-style: none;
  max-height: 240px;
  overflow-y: auto;
  background: var(--color-surface);
  border: 1px solid var(--color-border-strong);
  border-radius: var(--radius-base);
  box-shadow: var(--shadow-dialog);
}

.app-select__option {
  padding: var(--spacing-xs) var(--spacing-sm);
  color: var(--color-text);
  cursor: pointer;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.app-select__option:hover {
  background: var(--color-primary-light);
}

.app-select__option.is-selected {
  background: var(--color-primary-light);
  color: var(--color-primary);
}

.app-select__option.is-empty {
  color: var(--color-text-muted);
  cursor: default;
}

.app-select__option.is-empty:hover {
  background: transparent;
}
</style>
