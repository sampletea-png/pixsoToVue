<script setup lang="ts">
import { computed, type Component } from 'vue';
import AppTitleBar from './components/AppTitleBar.vue';
import AppToolBar from './components/AppToolBar.vue';
import SideNav from './components/SideNav.vue';
import MainTabs from './components/MainTabs.vue';
import StatusBar from './components/StatusBar.vue';
import ParametersPanel from './components/panels/ParametersPanel.vue';
import PortsPanel from './components/panels/PortsPanel.vue';
import DatasetsPanel from './components/panels/DatasetsPanel.vue';
import ResultsPanel from './components/panels/ResultsPanel.vue';
import ConvergenceMonitor from './components/views/ConvergenceMonitor.vue';
import ReportView from './components/views/ReportView.vue';
import SimulationResponse from './components/views/SimulationResponse.vue';
import ParameterSensitivity from './components/views/ParameterSensitivity.vue';
import ManualTuning from './components/views/ManualTuning.vue';
import CloseToolboxDialog from './components/dialogs/CloseToolboxDialog.vue';
import ParametersDialog from './components/dialogs/ParametersDialog.vue';
import AddParametersDialog from './components/dialogs/AddParametersDialog.vue';
import ArrayTableEditorDialog from './components/dialogs/ArrayTableEditorDialog.vue';
import AlgorithmDialog from './components/dialogs/AlgorithmDialog.vue';
import DatasetWorkspaceDialog from './components/dialogs/DatasetWorkspaceDialog.vue';
import ApplyResultDialog from './components/dialogs/ApplyResultDialog.vue';
import { useUiStore, type NavKey, type TabKey } from './stores/ui';

const ui = useUiStore();

// 左侧面板随导航切换（TODO: 容器-8/9/10 设计稿存在导航高亮与面板内容不一致的存疑项，按「面板随导航」实现）
const panels: Record<NavKey, Component> = {
  parameters: ParametersPanel,
  ports: PortsPanel,
  datasets: DatasetsPanel,
  results: ResultsPanel,
};
const activePanel = computed(() => panels[ui.activeNav]);

// 主区视图随页签切换
const views: Record<TabKey, Component> = {
  convergence: ConvergenceMonitor,
  report: ReportView,
  simulation: SimulationResponse,
  sensitivity: ParameterSensitivity,
  manual: ManualTuning,
};
const activeView = computed(() => views[ui.activeTab]);
</script>

<template>
  <div class="app-stage">
    <div class="app-window">
      <AppTitleBar />
      <AppToolBar />
      <div class="app-window__body">
        <SideNav />
        <aside class="app-window__panel">
          <component :is="activePanel" />
        </aside>
        <main class="app-window__main">
          <MainTabs />
          <div class="app-window__view">
            <component :is="activeView" />
          </div>
        </main>
      </div>
      <StatusBar />
      <!-- 7 个弹窗：按 ui store visible 渲染；二级弹窗（AddParameters/ArrayEditor）DOM 序在后，层叠于 ParametersDialog 之上 -->
      <CloseToolboxDialog v-if="ui.closeToolboxVisible" />
      <ParametersDialog v-if="ui.parametersVisible" />
      <AddParametersDialog v-if="ui.addParametersVisible" />
      <ArrayTableEditorDialog v-if="ui.arrayEditorVisible" />
      <AlgorithmDialog v-if="ui.algorithmVisible" />
      <DatasetWorkspaceDialog v-if="ui.datasetWorkspaceVisible" />
      <ApplyResultDialog v-if="ui.applyResultVisible" />
    </div>
  </div>
</template>

<style scoped>
.app-stage {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-border-strong);
  overflow: auto;
}

/* 桌面工具形态：1480×980 定宽居中 */
.app-window {
  display: flex;
  flex-direction: column;
  width: 1480px;
  height: 980px;
  flex: none;
  background: var(--color-bg);
  box-shadow: var(--shadow-dialog);
  overflow: hidden;
}

.app-window__body {
  flex: 1;
  min-height: 0;
  display: flex;
}

.app-window__panel {
  width: 328px;
  flex: none;
  background: var(--color-surface);
  border-right: 1px solid var(--color-border);
  overflow: hidden;
}

.app-window__main {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.app-window__view {
  flex: 1;
  min-height: 0;
}
</style>
