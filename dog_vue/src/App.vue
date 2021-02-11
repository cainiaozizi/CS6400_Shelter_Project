<template>
  <div id="main-app" class="container">
    <Header/>
    <router-view></router-view>
  </div>
</template>

<script>
import Header from "./components/Header";

export default {
  name: "MainApp",
  
  components: {
    Header
  }
};
</script>




