<script setup>
import { ref, onMounted } from 'vue'
import ChartComponent from '@/components/ChartComponent.vue'
import axios from 'axios'

const revenueData = ref(null)
const occupancyData = ref(null)
const durationData = ref(null)

onMounted(async () => {
  const [rev, occ, dur] = await Promise.all([
    axios.get('/admin/analytics/revenue'),
    axios.get('/admin/analytics/occupancy'),
    axios.get('/admin/analytics/average-duration')
  ])

  revenueData.value = {
    labels: rev.data.map(d => d.lot),
    datasets: [{ label: 'Revenue', data: rev.data.map(d => d.revenue), backgroundColor: '#4ade80' }]
  }

  occupancyData.value = {
    labels: occ.data.map(d => d.lot),
    datasets: [
      { label: 'Available', data: occ.data.map(d => d.available), backgroundColor: '#60a5fa' },
      { label: 'Occupied', data: occ.data.map(d => d.occupied), backgroundColor: '#f87171' }
    ]
  }

  durationData.value = {
    labels: dur.data.map(d => d.lot),
    datasets: [{ label: 'Avg. Duration (hrs)', data: dur.data.map(d => d.avg_duration), backgroundColor: '#fbbf24' }]
  }
})
</script>

<template>
  <div class="container mb-5">
    <h2 class="text-center py-4 fw-bold fs-4">Admin Parking Analytics</h2>

    <div class="row g-4">
      <div class="col-12 col-md-10 offset-md-1">
        <div class="card shadow-sm p-4">
          <ChartComponent
            title="Revenue per Lot"
            :chartData="revenueData"
            type="bar"
          />
        </div>
      </div>

      <div class="col-12 col-md-10 offset-md-1">
        <div class="card shadow-sm p-4">
          <ChartComponent
            title="Occupancy Rate per Lot"
            :chartData="occupancyData"
            type="bar-stacked"
          />
        </div>
      </div>

      <div class="col-12 col-md-10 offset-md-1">
        <div class="card shadow-sm p-4">
          <ChartComponent
            title="Average Parking Duration per Lot"
            :chartData="durationData"
            type="bar"
          />
        </div>
      </div>
    </div>
  </div>
</template>



