<script setup lang="ts">
import { computed } from 'vue';

const props = withDefaults(
  defineProps<{
    /** 图标名；未知名称回退为首字母方块 */
    name: string;
    /** 边长（px） */
    size?: number;
  }>(),
  {
    size: 16,
  },
);

/**
 * TODO: 图标库 —— 以下为按设计稿手绘的最简 SVG（16 viewBox，stroke=currentColor），
 * 待接入正式图标库后整体替换；设计稿中的矢量碎片（形状结合/编组）不再逐一还原。
 */
const ICONS: Record<string, string> = {
  close: '<path d="M4 4l8 8M12 4l-8 8"/>',
  minimize: '<path d="M3.5 12.5h9"/>',
  maximize: '<rect x="3.5" y="3.5" width="9" height="9" rx="1"/>',
  run: '<path d="M5 3.5v9l7-4.5z" fill="currentColor" stroke="none" stroke-linejoin="round"/>',
  stop: '<rect x="4" y="4" width="8" height="8" rx="1" fill="currentColor" stroke="none"/>',
  save: '<path d="M3.5 3.5h7l2 2v7h-9z"/><path d="M5.5 6.5v-3h5v3"/><path d="M5.5 12.5v-4h5v4"/>',
  import: '<path d="M8 2.5v7M5.5 7L8 9.5L10.5 7"/><path d="M3 11v2.5h10V11"/>',
  export: '<path d="M8 9.5v-7M5.5 5L8 2.5L10.5 5"/><path d="M3 11v2.5h10V11"/>',
  refresh: '<path d="M13 8a5 5 0 1 1-1.5-3.5"/><path d="M12.8 2v2.6h-2.6"/>',
  settings:
    '<circle cx="8" cy="8" r="2"/>' +
    '<path d="M8 2.5v2M8 11.5v2M2.5 8h2M11.5 8h2M4.1 4.1l1.4 1.4M10.5 10.5l1.4 1.4M11.9 4.1l-1.4 1.4M5.5 10.5l-1.4 1.4"/>',
  plus: '<path d="M8 3.5v9M3.5 8h9"/>',
  edit: '<path d="M3 13l.6-2.6L10 4l2 2-6.4 6.4z"/><path d="M9 5l2 2"/>',
  delete:
    '<path d="M3.5 4.5h9M6.5 4.5v-1h3v1M4.5 4.5l.5 8h6l.5-8"/>' +
    '<path d="M6.8 6.5v4M9.2 6.5v4"/>',
  chart: '<path d="M3 3v10h10"/><path d="M5.5 10.5v-3M8 10.5v-5M10.5 10.5v-2M13 10.5v-4"/>',
  report:
    '<path d="M4 2.5h6l2 2v9H4z"/><path d="M10 2.5v2h2"/>' +
    '<path d="M6 8h4M6 10.5h4"/>',
  simulation: '<path d="M2.5 8h2l1.5-4 2.5 8 1.5-4h3.5"/>',
  sensitivity:
    '<path d="M5 3v10M8 3v10M11 3v10"/>' +
    '<circle cx="5" cy="10" r="1.5"/><circle cx="8" cy="6" r="1.5"/><circle cx="11" cy="9" r="1.5"/>',
  tuning:
    '<path d="M3 5h10M3 8h10M3 11h10"/>' +
    '<circle cx="10" cy="5" r="1.5"/><circle cx="6" cy="8" r="1.5"/><circle cx="9" cy="11" r="1.5"/>',
  'chevron-down': '<path d="M4 6l4 4 4-4"/>',
  search: '<circle cx="7" cy="7" r="3.5"/><path d="M9.8 9.8L13 13"/>',
  warning:
    '<circle cx="8" cy="8" r="5.5"/>' +
    '<path d="M8 5v3.5"/><circle cx="8" cy="11" r="0.6" fill="currentColor" stroke="none"/>',
};

const svg = computed<string | null>(() => ICONS[props.name] ?? null);

/** 回退：名称首字母 */
const letter = computed<string>(() =>
  props.name ? props.name.charAt(0).toUpperCase() : '?',
);
</script>

<template>
  <span
    class="app-icon"
    :style="{ width: `${size}px`, height: `${size}px` }"
    aria-hidden="true"
  >
    <svg
      v-if="svg"
      :viewBox="'0 0 16 16'"
      fill="none"
      stroke="currentColor"
      stroke-width="1.5"
      stroke-linecap="round"
      stroke-linejoin="round"
      v-html="svg"
    />
    <!-- TODO: 图标库 —— 未知名称占位，接入图标库后移除 -->
    <span v-else class="app-icon__fallback">{{ letter }}</span>
  </span>
</template>

<style scoped>
.app-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: none;
  line-height: 1;
}

.app-icon svg {
  width: 100%;
  height: 100%;
  display: block;
}

.app-icon__fallback {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  border: 1px solid currentColor;
  border-radius: var(--radius-sm);
  font-size: var(--font-size-base);
  transform: scale(0.85);
}
</style>
