import { defineStore } from 'pinia';
import { ref } from 'vue';

export type NavKey = 'parameters' | 'ports' | 'datasets' | 'results';
export type TabKey =
  | 'convergence'
  | 'report'
  | 'simulation'
  | 'sensitivity'
  | 'manual';

/**
 * 页内 UI 状态：导航/页签激活、弹窗显隐、列表选中态。
 * 16 画板 = 同一窗口的状态组合，全部为页内状态，不走路由。
 */
export const useUiStore = defineStore('param-estimation-ui', () => {
  // 左侧导航（容器-2 基准：Parameters 激活）
  const activeNav = ref<NavKey>('parameters');
  // 主区页签（容器-2 基准：Convergence Monitor 激活）
  const activeTab = ref<TabKey>('convergence');

  // 7 个弹窗显隐（本阶段仅状态，弹窗组件下一阶段实现）
  const closeToolboxVisible = ref(false);
  const parametersVisible = ref(false);
  const addParametersVisible = ref(false);
  const arrayEditorVisible = ref(false);
  const algorithmVisible = ref(false);
  const datasetWorkspaceVisible = ref(false);
  const applyResultVisible = ref(false);

  // 选中态（-1 = 无选中）
  /** 当前数据集行（容器-8：高亮行为 "Prewiew Dataset 05"，新行序下下标为 5） */
  const selectedDatasetIndex = ref(5);
  /** 当前结果行（容器-9/394：Result #4 仅复选框勾选，无行高亮，默认无选中） */
  const selectedResultIndex = ref(-1);
  /** 参数面板/表格当前行 */
  const selectedParamIndex = ref(-1);

  function setNav(nav: NavKey): void {
    activeNav.value = nav;
  }

  function setTab(tab: TabKey): void {
    activeTab.value = tab;
  }

  return {
    activeNav,
    activeTab,
    closeToolboxVisible,
    parametersVisible,
    addParametersVisible,
    arrayEditorVisible,
    algorithmVisible,
    datasetWorkspaceVisible,
    applyResultVisible,
    selectedDatasetIndex,
    selectedResultIndex,
    selectedParamIndex,
    setNav,
    setTab,
  };
});
