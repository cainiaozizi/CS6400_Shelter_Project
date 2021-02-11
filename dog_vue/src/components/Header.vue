<template>
  <header>
    <div class="d-flex justify-content-between align-items-center mt-4">
      <div class="container"> 
        <div class="row">
          <div class="col-6 text-warning">
           <h1>Mo's Mutt House</h1>
           <span v-if="loggedIn" class="text-secondary">Current user:</span>
           <span v-if="loggedIn" class="text-info font-weight-bold">
              {{ loggedInUsername }}
            </span>
          </div>
          <div class="col" v-if="loggedIn && showDashboard">
            <button v-on:click="dashboard()" type="button" 
              class="btn btn-success">
              Dashboard
            </button>
          </div>
          <div class="col" v-if="loggedIn">
            <button @click="logout()" type="button" 
              class="btn btn-info">
              Logout
            </button>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'Header',
  data() {
    return {
        loggedIn: false,
        showDashboard: true,
        loggedInUsername:''
    };
  },

  mounted: function () {
    let token = this.$auth.getAccessToken();
    if (token) {
      this.loggedIn = true;
    }

    this.loggedInUsername = this.$auth.getUsername();

    this.$eventBus.$on('USER_LOGGED_IN', () => {
        this.loggedIn = true;
    });

    this.$eventBus.$on('USER_LOGGED_OUT', () => {
      this.loggedIn = false;
      this.$router.push('/login');
    });

    if (this.$route.path === '/dashboard') {
      this.showDashboard = false;
    }

    this.$eventBus.$on('ARRIVING IN DASHBOARD', () => {
      this.showDashboard = false;
    });
    this.$eventBus.$on('LEAVING DASHBOARD', () => {
      this.showDashboard = true;
    });
  },
  
  methods: {
    logout() {
      this.$auth.logout();
    },

    dashboard() {
      this.$router.push('/dashboard');
    }
  }
};
</script>

<style>

</style>