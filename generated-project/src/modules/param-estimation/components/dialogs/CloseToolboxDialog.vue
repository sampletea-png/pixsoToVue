<script setup lang="ts">
import AppDialog from '@/components/AppDialog.vue';
import AppButton from '@/components/AppButton.vue';
import AppIcon from '@/components/AppIcon.vue';
import { useUiStore } from '../../stores/ui';

// 容器-1：标题栏 × 触发的关闭确认弹窗（480×168，Cancel / OK）
const ui = useUiStore();

function close(): void {
  ui.closeToolboxVisible = false;
}

function onOk(): void {
  close();
  // TODO: 交互待确认 —— OK 的真实关闭行为（退出应用/返回宿主）在 Web 端无对应语义，暂仅关闭弹窗
}
</script>

<template>
  <AppDialog title="Close toolbox" :width="480" @close="close">
    <div class="close-toolbox__content">
      <!-- 设计稿为 Icon/General/Status/error 圆形叹号警告图标（琥珀黄） -->
      <AppIcon class="close-toolbox__warning" name="warning" :size="24" />
      <!-- TODO: 设计稿原文拼写 "paramter"（疑 parameter），按原稿保留 -->
      <p class="close-toolbox__text">Close the paramter estimation toolbox?</p>
    </div>
    <template #footer>
      <AppButton @click="close">Cancel</AppButton>
      <AppButton type="primary" @click="onOk">OK</AppButton>
    </template>
  </AppDialog>
</template>

<style scoped>
.close-toolbox__content {
  display: flex;
  align-items: center;
  gap: var(--spacing-base);
  padding: var(--spacing-sm) 0 var(--spacing-md);
}

.close-toolbox__warning {
  color: var(--color-caution);
}

.close-toolbox__text {
  margin: 0;
  color: var(--color-text);
}
</style>
