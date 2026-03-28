<script>
export default {
  name: 'Stats',
  data() {
    return {
      features: [
        {
          icon: 'fas fa-chart-line',
          title: 'Expense Analytics',
          description: 'Detailed breakdowns of your parking expenses with trends and insights to help you save money.',
          bgColor: 'bg-primary'
        },
        {
          icon: 'fas fa-calendar',
          title: 'Monthly Reports',
          description: 'Comprehensive monthly reports with parking history, spending patterns, and optimization tips.',
          bgColor: 'bg-info'
        },
        {
          icon: 'fas fa-dollar-sign',
          title: 'Budget Tracking',
          description: 'Set parking budgets and get alerts when you\'re approaching your limits.',
          bgColor: 'bg-success'
        },
        {
          icon: 'fas fa-clock',
          title: 'Time Analytics',
          description: 'Track how much time you save by booking spots in advance instead of searching.',
          bgColor: 'bg-warning'
        }
      ]
    }
  }
}
</script>

<template>
  <section class="py-5 gradient-bg text-white">
    <div class="container py-5">
      <div class="row justify-content-center text-center mb-5">
        <div class="col-lg-8">
          <h2 class="display-4 fw-bold mb-4">Track Your Parking Like a Pro</h2>
          <p class="lead opacity-75">
            Get detailed insights into your parking habits, expenses, and savings with our comprehensive analytics.
          </p>
        </div>
      </div>
      
      <div class="row g-4">
        <div 
          v-for="(feature, index) in features" 
          :key="index"
          class="col-lg-6 col-md-6"
        >
          <div class="d-flex align-items-start">
            <div :class="`p-3 rounded me-4 ${feature.bgColor}`">
              <i :class="`${feature.icon} text-white fs-4`"></i>
            </div>
            <div>
              <h5 class="fw-bold mb-3">{{ feature.title }}</h5>
              <p class="opacity-75">{{ feature.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<style>

.gradient-bg {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

</style>