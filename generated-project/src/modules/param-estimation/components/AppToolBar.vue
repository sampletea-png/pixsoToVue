<script setup lang="ts">
import { ref } from 'vue';
import IconButton from '@/components/IconButton.vue';
import AppSelect from '@/components/AppSelect.vue';
import { useUiStore } from '../stores/ui';
import { useEstimationStore } from '../stores/estimation';

const ui = useUiStore();
const estimation = useEstimationStore();

/** TODO: 交互待确认 —— 设计稿仅有 English 一个选项证据，语言切换为 mock */
const language = ref('en');
const languageOptions = [{ label: 'English', value: 'en' }];

/** TODO: 交互待确认 —— import/export/save/refresh 的具体行为无画板佐证，仅占位 */
function noop(): void {
  /* placeholder */
}
</script>

<template>
  <div class="tool-bar">
    <div class="tool-bar__left">
      <IconButton icon="import" @click="noop" />
      <IconButton icon="export" @click="noop" />
      <IconButton icon="save" @click="noop" />
      <IconButton icon="settings" @click="ui.algorithmVisible = true" />
      <IconButton icon="refresh" @click="noop" />
      <span class="tool-bar__lang-label">Language</span>
      <AppSelect v-model:value="language" :options="languageOptions" />
    </div>
    <div class="tool-bar__right">
      <IconButton
        icon="run"
        :disabled="estimation.runState === 'running'"
        @click="estimation.run()"
      />
      <IconButton
        icon="stop"
        :disabled="estimation.runState === 'stopped'"
        @click="estimation.stop()"
      />
    </div>
  </div>
</template>

<style scoped>
.tool-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 40px;
  padding: 0 var(--spacing-base);
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
}

.tool-bar__left {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}

.tool-bar__lang-label {
  margin-left: var(--spacing-sm);
  font-size: var(--font-size-base);
  color: var(--color-text-secondary);
}

.tool-bar__right {
  display: flex;
  align-items: center;
  gap: var(--spacing-xs);
}
</style>
