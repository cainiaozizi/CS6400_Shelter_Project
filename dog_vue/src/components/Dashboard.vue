<template>
  <header>
    <div class="d-flex align-items-center mt-4 mb-4">
      <div class="container row">
        <div class="col">
          <h1>Dashboard</h1> 
        </div>
        <div class="col" v-if="searchResults.length >= 15">
          <h3 class="text-danger">No Available Spaces</h3>
        </div>
          <div class="col" v-if="searchResults.length < 15">
            <h3>Available Space: {{15 - searchResults.length}}</h3>
          </div>
          <div class="col" v-if="searchResults.length < 15">
            <button
              id="add-dog-button" type="button" class="btn btn-success"
            >
              <router-link :to="{path: '/dashboard/add-dog'}">
                Add Dog
              </router-link>
            </button>
          </div>
        </div>
      </div>
    <div class="list-group">
      <button @click="searchApplicant()" type="button" 
        class="btn btn-info btn-sm mb-1">
        Add New Applicant
      </button>
      <button v-if="isAdmin" @click="applicationReview()" type="button" 
        class="btn btn-info btn-sm mb-1">
        Review of Adoption Applications
      </button>
      <button v-if="isAdmin" @click="animalControlReport()" type="button" 
        class="btn btn-secondary btn-sm mb-1">
        Animal Control Report
      </button>
      <button v-if="isAdmin" @click="monthlyAdoptionReport()" type="button" 
        class="btn btn-secondary btn-sm mb-1">
        Monthly Adoption Report
      </button>
      <button v-if="isAdmin" @click="expenseAnalysisReport()" type="button" 
        class="btn btn-secondary btn-sm mb-1">
        Expense Analysis Report
      </button>
      <button v-if="isAdmin" @click="volunteerLookup()" type="button" 
        class="btn btn-warning btn-smmb-1">
        Volunteer Lookup
      </button>
    </div>
    <div class="mt-4">
        <table class="table table-hover">
          <thead>
            <tr>
              <th>Dog ID</th>
              <th>Name</th>
              <th>Breed</th>
              <th>Sex</th>
              <th>Alteration Status</th>
              <th>Age</th>
              <th>Adoptability Status</th>
            </tr>
          </thead>
          <tbody id="search-results">
            <tr v-for="(dog, index) in searchResults" :key="index"
              v-on:click="selectedDog(dog.dog_ID)">
              <td>{{dog.dog_ID}}</td>
              <td>{{dog.dog_name}}</td>
              <td>{{dog.breed_name}}</td>
              <td>{{dog.sex}}</td>
              <td>{{dog.alteration_status}}</td>
              <td>{{dog.age}}</td>
              <td>{{dog.adoptability_status}}</td>
            </tr>
          </tbody>
        </table>
    </div>
  </header>
</template>

<script>
export default {
  name: 'Dashboard',

  data() {
    return {
      searchResults: [],
      searchError: '',
      isAdmin: false
    };
  },

  mounted: function() {
    console.log('HEY I AM HERE IN DASHBOARD');
    this.$eventBus.$emit('ARRIVING IN DASHBOARD');

    this.searchResults = [];
    this.getData();

    this.$auth.isAdmin();

    this.$eventBus.$on('IS_ADMIN', (is_admin) => {
      this.isAdmin = is_admin;
    });
  },

  destroyed:function(){
    this.$eventBus.$emit('LEAVING DASHBOARD');
  },

  methods: {
    searchApplicant() {
      this.$router.push('/dashboard/search-applicant');
    },
    applicationReview() {
      this.$router.push('/dashboard/application-review');
    },
    animalControlReport() {
      this.$router.push('/dashboard/animal-control-report');
    },
    monthlyAdoptionReport() {
      this.$router.push('/dashboard/monthly-adoption-report');
    },
    expenseAnalysisReport() {
      this.$router.push('/dashboard/expense-analysis-report');
    },
    volunteerLookup() {
      this.$router.push('/dashboard/volunteer-lookup');
    },
    selectedDog(dogID) {
      this.$router.push('/dashboard/dog-detail/edit-dog/' + dogID);
    },

    getData: function() {

      var url = "http://127.0.0.1:5000/api/dog_dashboard";

      var yourConfig = {
        headers: {
            "Content-Type": "application/json",
            "Authorization": "JWT " + this.$auth.getAccessToken()
       }
      }

      this.$axios
      .get(url, yourConfig)
      .then(response => {
        if (typeof response.data != 'undefined' && response.data.length) {
           this.searchResults = response.data;
        }
      })
      .catch((error) => {
        if(error.response.status == 404) {
          this.$router.push('/login');
        }
      })
    },

  }
};
</script>

<style>
  #search-results td{
    cursor: pointer;
    color: blue;
  }
  #search-results td:hover {
    text-decoration: underline;
  }
   #search-results tr:hover {
   background-color: rgb(192, 237, 255);
  }
  #add-dog-button a{
    color: #FFFFFF;
  }
</style>