<script lang="ts">
export interface DataTableColumn {
  /** 对应行数据的字段名，也是 cell slot 的定位依据 */
  key: string;
  /** 表头文案 */
  title: string;
  /** 列宽，数字按 px 处理；缺省自适应 */
  width?: number | string;
}

export type DataTableRow = Record<string, unknown>;
</script>

<script setup lang="ts">
import type { CSSProperties } from 'vue';

const props = withDefaults(
  defineProps<{
    columns: DataTableColumn[];
    rows: DataTableRow[];
    /** 选中行下标，-1 表示无选中 */
    selectedIndex?: number;
    /** 行唯一键字段名，缺省用下标 */
    rowKey?: string;
    /** 追加行 class（如按行数据给整行底色） */
    rowClass?: (row: DataTableRow, index: number) => string;
  }>(),
  {
    selectedIndex: -1,
    rowKey: '',
    rowClass: undefined,
  },
);

const emit = defineEmits<{
  (e: 'select', index: number, row: DataTableRow): void;
  /** 双击单元格触发，由父级决定是否进入编辑态 */
  (e: 'cell-edit', index: number, key: string, value: unknown): void;
}>();

function colStyle(col: DataTableColumn): CSSProperties | undefined {
  if (col.width == null) return undefined;
  const w = typeof col.width === 'number' ? `${col.width}px` : col.width;
  return { width: w, minWidth: w };
}

function keyOf(row: DataTableRow, index: number): string | number {
  return props.rowKey ? (row[props.rowKey] as string | number) : index;
}

function onRowClick(index: number, row: DataTableRow): void {
  emit('select', index, row);
}

function onCellDblClick(index: number, key: string, row: DataTableRow): void {
  emit('cell-edit', index, key, row[key]);
}
</script>

<template>
  <div class="data-table">
    <table class="data-table__table">
      <thead>
        <tr>
          <th
            v-for="col in columns"
            :key="col.key"
            :style="colStyle(col)"
            scope="col"
          >
            <slot name="header" :column="col">{{ col.title }}</slot>
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(row, i) in rows"
          :key="keyOf(row, i)"
          class="data-table__row"
          :class="[{ 'is-selected': i === selectedIndex }, rowClass?.(row, i)]"
          @click="onRowClick(i, row)"
        >
          <td
            v-for="col in columns"
            :key="col.key"
            :style="colStyle(col)"
            @dblclick="onCellDblClick(i, col.key, row)"
          >
            <slot
              name="cell"
              :row="row"
              :column="col"
              :row-index="i"
              :value="row[col.key]"
              >{{ row[col.key] }}</slot
            >
          </td>
        </tr>
        <tr v-if="rows.length === 0">
          <td class="data-table__empty" :colspan="columns.length">No data</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.data-table {
  overflow-y: auto;
  overflow-x: auto;
  background: var(--color-surface);
  border-radius: var(--radius-base);
  font-size: var(--font-size-base);
  color: var(--color-text);
}

.data-table__table {
  width: 100%;
  border-collapse: collapse;
  table-layout: auto;
}

.data-table__table th {
  position: sticky;
  top: 0;
  z-index: 1;
  padding: var(--spacing-xs) var(--spacing-base);
  background: var(--color-bg);
  color: var(--color-text-secondary);
  font-weight: var(--font-weight-regular);
  text-align: left;
  white-space: nowrap;
}

.data-table__table td {
  padding: var(--spacing-xs) var(--spacing-base);
  height: 28px;
  box-sizing: border-box;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 斑马纹 */
.data-table__row:nth-child(even) td {
  background: var(--color-bg-subtle);
}

.data-table__row {
  cursor: pointer;
}

.data-table__row:hover td {
  background: var(--color-primary-light);
}

/* 行选中底色（优先级高于斑马纹与 hover） */
.data-table__row.is-selected td,
.data-table__row.is-selected:hover td {
  background: var(--color-primary-light);
}

.data-table__empty {
  text-align: center;
  color: var(--color-text-muted);
  cursor: default;
}
</style>
