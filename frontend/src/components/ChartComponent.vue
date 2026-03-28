<script setup>
import { Bar, Line } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, LineElement, CategoryScale, LinearScale, PointElement } from 'chart.js'
ChartJS.register(Title, Tooltip, Legend, BarElement, LineElement, CategoryScale, LinearScale, PointElement)

const props = defineProps({
  title: String,
  chartData: Object,
  type: String
})

const options = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: { legend: { position: 'top' }, title: { display: false } },
  height: 300
}
</script>

<template>
  <div v-if="chartData">
    <h3 class="font-semibold mb-2">{{ title }}</h3>

    <Bar
      v-if="type === 'bar'"
      :data="chartData"
      :options="options"
    />
    <Bar
      v-else-if="type === 'bar-stacked'"
      :data="chartData"
      :options="{ ...options, scales: { x: { stacked: true }, y: { stacked: true } } }"
    />
    <Bar
      v-else-if="type === 'horizontal-bar'"
      :data="chartData"
      :options="{ ...options, indexAxis: 'y' }"
    />
    <Line
      v-else
      :data="chartData"
      :options="options"
    />
  </div>
  <div v-else class="text-gray-400 text-sm">Loading...</div>
</template>

<style scoped>
div {
  height: 300px;
}
</style>
