<template>
  <nav>
    <button
      v-for="tab in tabs"
      :key="tab.name"
      :class="{ active: selectedTab === tab.name }"
      @click="selectTab(tab.name)"
    >
      {{ tab.label }}
    </button>
  </nav>
</template>

<script setup>
import { ref } from 'vue';

const tabs = [
  { name: 'deposit', label: '정기예금' },
  { name: 'saving', label: '적금' },
  { name: 'fund', label: '펀드' },
  { name: 'tax', label: '절세금융상품' },
];

const selectedTab = ref('deposit');

const selectTab = (tabName) => {
  selectedTab.value = tabName;
};
</script>

<style scoped>
nav {
  display: flex;
  margin-bottom: 20px;
}

nav button {
  padding: 10px 20px;
  margin-right: 10px;
  border: 1px solid #ccc;
  background-color: #f9f9f9;
  cursor: pointer;
}

nav button.active {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
}
</style>