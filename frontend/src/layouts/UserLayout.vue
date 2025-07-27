<script>
import NavBar from '@/components/NavBar.vue';
import axios from 'axios';

export default {
  components: { NavBar },
  data() {
    return {
      user: null
    }
  },
  async mounted() {
    try {
      const res = await axios.get('/auth/check');
      console.log(res.data)
      if (res.data.authenticated && res.data.role === "user") {
        this.user = {
          fullname : res.data.fullname,
          email: res.data.email,
          role: res.data.role
        }
      }
    } catch (err) {
      console.error("Failed to fetch user info", err)
    }
  }
};
</script>

<template>
  <div>
    <NavBar  :user = "user" />
    <router-view />
  </div>
</template>


