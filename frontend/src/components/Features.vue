<script>
export default {
  name: "Features",
  data() {
    return {
      features: [
        {
          icon: "fas fa-map-marker-alt",
          title: "Find Nearby Spots",
          description:
            "Discover available parking spots near your destination with real-time availability updates.",
          bgColor: "bg-primary",
        },
        {
          icon: "fas fa-clock",
          title: "Instant Booking",
          description:
            "Reserve your parking spot in seconds and get guaranteed availability when you arrive.",
          bgColor: "bg-info",
        },
        {
          icon: "fas fa-credit-card",
          title: "Cashless Payments",
          description:
            "Pay securely through the app with multiple payment options and automatic receipts.",
          bgColor: "bg-success",
        },
        {
          icon: "fas fa-chart-bar",
          title: "Expense Tracking",
          description:
            "Monitor your parking expenses with detailed breakdowns and spending analytics.",
          bgColor: "bg-warning",
        },
        {
          icon: "fas fa-calendar",
          title: "Monthly Reports",
          description:
            "Get comprehensive monthly reports of your parking history and spending patterns.",
          bgColor: "bg-secondary",
        },
        {
          icon: "fas fa-shield-alt",
          title: "Secure & Reliable",
          description:
            "Your data and payments are protected with bank-level security and encryption.",
          bgColor: "bg-danger",
        },
      ],
    };
  },
  methods: {
    async triggerInstall() {
      console.log("🟦 triggerInstall called");
      if (window.deferredPrompt) {
        const promptEvent = window.deferredPrompt;
        promptEvent.prompt(); // 👉 Show install banner

        const choice = await promptEvent.userChoice;
        if (choice.outcome === "accepted") {
          console.log("✅ User accepted the A2HS prompt");
        } else {
          console.log("❌ User dismissed the A2HS prompt");
        }

        window.deferredPrompt = null; // ⚠️ Reset the event
      } else {
        console.log("❗Install prompt not available yet");
      }
    },
  },
};
</script>

<template>
  <section id="features" class="py-5 bg-light">
    <div class="container py-5">
      <div class="row justify-content-center text-center mb-5">
        <div class="col-lg-8">
          <h2 class="display-4 fw-bold mb-4">
            Everything You Need for
            <span class="gradient-text">Smart Parking</span>
          </h2>
          <p class="lead text-muted">
            From finding the perfect spot to tracking your expenses, we've got
            every aspect of parking covered.
          </p>
        </div>
      </div>

      <div class="row g-4">
        <div
          v-for="(feature, index) in features"
          :key="index"
          class="col-lg-4 col-md-6"
        >
          <div class="card feature-card h-100 p-4">
            <div class="card-body text-center">
              <div
                :class="`p-3 rounded-circle d-inline-flex mb-4 ${feature.bgColor}`"
              >
                <i :class="`${feature.icon} text-white fs-4`"></i>
              </div>
              <h5 class="card-title fw-bold mb-3">{{ feature.title }}</h5>
              <p class="card-text text-muted">{{ feature.description }}</p>
            </div>
          </div>
        </div>
      </div>

      <div class="row mt-5">
        <div class="col-12">
          <div
            class="card gradient-bg text-white p-5 position-relative overflow-hidden"
          >
            <div class="position-absolute top-0 end-0 opacity-25">
              <div
                class="bg-white rounded-circle"
                style="
                  width: 200px;
                  height: 200px;
                  transform: translate(50%, -50%);
                "
              ></div>
            </div>
            <div class="position-absolute bottom-0 start-0 opacity-25">
              <div
                class="bg-white rounded-circle"
                style="
                  width: 150px;
                  height: 150px;
                  transform: translate(-50%, 50%);
                "
              ></div>
            </div>

            <div class="text-center position-relative">
              <h3 class="display-5 fw-bold mb-4">
                Ready to Transform Your Parking Experience?
              </h3>
              <p class="lead mb-4">
                Join thousands of smart parkers who save time and money every
                day.
              </p>
              <button
                class="btn btn-light btn-lg px-5 py-3 rounded-pill fw-semibold text-primary"
                @click="triggerInstall"
              >
                Download Now - It's Free
              </button>
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

.gradient-text {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.feature-card {
  transition: all 0.3s ease;
  border: none;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 25px rgba(0, 0, 0, 0.15);
}
</style>
