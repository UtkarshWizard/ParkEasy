<script setup>
import { ref, onMounted } from 'vue'
import ChartComponent from '@/components/ChartComponent.vue'
import axios from 'axios'

const freqData = ref(null)
const durationData = ref(null)

onMounted(async () => {
  const [freq, durations] = await Promise.all([
    axios.get('/user/analytics/frequent-lots'),
    axios.get('/user/analytics/recent-durations')
  ])

  freqData.value = {
    labels: freq.data.map(d => d.lot),
    datasets: [{ label: 'Times Used', data: freq.data.map(d => d.count), backgroundColor: '#38bdf8' }]
  }

  durationData.value = {
    labels: durations.data.map(d => d.date),
    datasets: [{ label: 'Duration (hrs)', data: durations.data.map(d => d.duration), borderColor: '#34d399', fill: true }]
  }
})
</script>

<template>
  <div class="container my-5">
    <h2 class="text-center mb-4 fw-bold fs-4">Your Parking Analytics</h2>

    <div class="row g-4">
      <div class="col-12 col-md-10 offset-md-1">
        <div class="card shadow-sm p-4">
          <ChartComponent
            title="Most Frequently Used Lots"
            :chartData="freqData"
            type="horizontal-bar"
          />
        </div>
      </div>

      <div class="col-12 col-md-10 offset-md-1">
        <div class="card shadow-sm p-4">
          <ChartComponent
            title="Recent Parking Durations"
            :chartData="durationData"
            type="line"
          />
        </div>
      </div>
    </div>
  </div>
</template>

