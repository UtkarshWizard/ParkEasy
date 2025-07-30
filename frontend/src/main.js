import axios from "axios";
import { createApp } from "vue";
import App from "./App.vue";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";
import router from "./router";
import "bootstrap-icons/font/bootstrap-icons.css";

axios.defaults.baseURL = "http://localhost:5000";
axios.defaults.withCredentials = true;

window.deferredPrompt = null;

window.addEventListener("beforeinstallprompt", (e) => {
  console.log("📦 beforeinstallprompt event fired");
  e.preventDefault();
  window.deferredPrompt = e;
});

if ("serviceWorker" in navigator) {
  navigator.serviceWorker.register("/service-worker.js");
}

createApp(App).use(router).mount("#app");
