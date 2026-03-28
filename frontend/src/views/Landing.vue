<script>
import Features from '@/components/Features.vue';
import Footer from '@/components/Footer.vue';
import Header from '@/components/Header.vue';
import Hero from '@/components/Hero.vue';
import HowItWorks from '@/components/HowItWorks.vue';
import Pricing from '@/components/Pricing.vue';
import Stats from '@/components/Stats.vue';



export default {
  name: 'App',
  components: {
    Header,
    Hero,
    Features,
    HowItWorks,
    Stats,
    Pricing,
    Footer
  }
}
</script>

<template>
  <div id="app">
    <Header />
    <Hero />
    <Features />
    <HowItWorks />
    <Stats />
    <Pricing />
    <Footer />
  </div>
</template>

