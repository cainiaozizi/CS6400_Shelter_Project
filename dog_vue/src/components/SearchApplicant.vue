<template>
  <div class="container">

  <div class="container mt-4 mb-5">
  </div>
  <div class="container">
    <h5>Search for Applicant</h5> 
  </div>

    <form class="mb-3">
      <div class="input-group">
        <input
          v-on:keydown.13.prevent="search()"
          v-model="searchEmail"
          type="text"
          class="form-control"
          placeholder="Enter Applicant Email Address..."
        >
        <div class="input-group-append">
          <button 
            @click="search()" 
            type = "button" 
            class="btn btn-secondary"
          >Search
          </button>
        </div>
      </div>
      <div class="container mt-4 text-info" 
        v-if="searchResults.length">
        <h5>Results:</h5>
        <table class="table">
          <thead>
            <tr>
              <th>First Name</th>
              <th>Last Name</th>
              <th>Email Address</th>
              <th>Phone Number</th>
              <th>Street</th>
              <th>City</th>
              <th>Zip</th>
              <th>Co-Applicant Last Name</th>
            </tr>
          </thead>
          <tbody id="search-results">
            <tr v-for="(sr, index) in searchResults" :key="index" 
              v-on:click="selectedApplicant(sr.email_address)">
                <td>{{sr.first_name}}</td>
                <td>{{sr.last_name}}</td>
                <td>{{sr.email_address}}</td>
                <td>{{sr.phone_number}}</td>
                <td>{{sr.street}}</td>
                <td>{{sr.city}}</td>
                <td>{{sr.zip}}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </form>
    <form class="container" v-if="showAddForm">
      <h5 class="text-danger mb-4">No Applicant Found</h5>
      <h5 class="text-info">Enter Applicant Information</h5>
      <div class="input-group align-items-center mt-4">
        <span class="font-weight-bold">First Name:</span>
        <pre> </pre>
        <input
          v-on:keydown.13.prevent="submitApplicantInfo()"
          v-model="firstName"
          type="text"
          class="form-control"
          required
        >
        <pre>   </pre>
        <span class="font-weight-bold">Last Name:</span>
        <pre>   </pre>
        <input
          v-on:keydown.13.prevent="submitApplicantInfo()"
          v-model="lastName"
          type="text"
          class="form-control"
          required
        >
      </div>
      <div class="input-group mt-3 mb-3 align-items-center">
        <span class="font-weight-bold">Email Address:</span>
        <pre>   </pre>
        <input
          v-on:keydown.13.prevent="submitApplicantInfo()"
          v-model="email"
          type="text"
          class="form-control"
          required
        >
        <pre>   </pre>
        <span class="font-weight-bold">Phone Number: </span>
        <pre> </pre>
        <input
          v-on:keydown.13.prevent="submitApplicantInfo()"
          v-model="phoneNumber"
          type="text"
          class="form-control"
          maxlength=10
          required
        >
      </div>
      <div class="input-group align-items-center mt-4">
        <span class="font-weight-bold">Street:</span>
        <pre> </pre>
        <input
          required
          v-on:keydown.13.prevent="submitApplicantInfo()"
          v-model="street"
          type="text"
          class="form-control"
        >
        <pre> </pre>
        <span class="font-weight-bold">City:</span>
        <pre> </pre>
        <input
          required
          v-on:keydown.13.prevent="submitApplicantInfo()"
          v-model="city"
          type="text"
          class="form-control"
        >
        <pre> </pre>
        <span class="font-weight-bold">State:</span>
        <pre> </pre>
        <input
          required
          v-on:keydown.13.prevent="submitApplicantInfo()"
          v-model="state"
          type="text"
          class="form-control"
        >
        <pre> </pre>
        <span class="font-weight-bold">Zip Code:</span>
        <pre> </pre>
        <input
          required
          v-on:keydown.13.prevent="submitApplicantInfo()"
          v-model="zipCode"
          type="text"
          class="form-control"
        >
      </div>
      <div class="input-group-append mt-5">
        <button 
          @click="submitApplicantInfo()" 
          type = "button" 
          Class="btn btn-secondary"
          >Submit
        </button>
      </div>
    </form>
  </div>
</template>

<script>

export default {
  name: 'NewAdoptionApplication',
  
  data() {
    return {
      searchEmail: '',
      searchResults: [],
      searchError: '',
      firstName: '',
      lastName: '',
      email: '',
      phoneNumber: '',
      street: '',
      city: '',
      state: '',
      zipCode: '',
      showAddForm: false
    };
  },
  
  methods: {
    search: function() {
      this.getData(this.searchEmail);
    },

    selectedApplicant(email) {
      this.$router.push('/dashboard/search-applicant/new-application/' + email);
    },

    getData: function(searchEmail) {
      if (!this.validEmail(this.searchEmail)) {
        this.$swal('Valid email address required.');
        this.showAddForm = false;
        return;
      } 

      searchEmail = searchEmail.toLowerCase();
      this.searchResults = [];
      this.searchError = '';
      this.showAddForm = false;

      var url = "http://127.0.0.1:5000/api/applicant/" + searchEmail;
      var yourConfig = {
        headers: {
            "Content-Type": 'application/json',
           'Authorization': "JWT " + this.$auth.getAccessToken()
        }
      }

      this.$axios
      .get(url, yourConfig)
      .then(response => {
        if (typeof response.data.email_address != 'undefined') {
           this.searchResults.push(response.data);
        } else {
            for (var i = 0; i < response.data.length; i++) {
                this.searchResults.push(response.data[i]);
            }
        } 
      })
      .catch((error) => {
        this.showAddForm = true;
        if(error.response.status == 404) {
          if (typeof error.response.data.message != 'undefined') {
            this.searchError = error.response.data.message;
          } else if (error.response.status == 401) {
            this.searchError = 'Records Not Found';
          }
        }
      })
    },

    validEmail: function(searchEmail) {
      var re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(searchEmail);
    },

    submitApplicantInfo: function() {
      if ((this.firstName == '' || !this.firstName)
        || (this.lastName == '' || !this.lastName)
        || (this.email == '' || !this.email)
        || (this.phoneNumber == '' || !this.phoneNumber)
        || (this.street == '' || !this.street)
        || (this.city == '' || !this.city)
        || (this.state == '' || !this.state)
        || (this.zipCode == '' || !this.zipCode)
      ) {
       this.$swal('All fields are required');
       return;
      }

      if (this.phoneNumber.length > 10) {
        this.$swal('Phone number cannot be longer than 10 digits.');
        return;
      }

      let data = {
        'first_name': this.firstName,
        'last_name': this.lastName,
        'email_address': this.email,
        'phone_number': this.phoneNumber,
        'street': this.street,
        'city': this.city,
        'state': this.state,
        'zip_code': this.zipCode
      }

      var url = "http://127.0.0.1:5000/api/applicant/" + this.email;
      var yourConfig = {
        headers: {
            "Content-Type": "application/json",
            "Authorization": "JWT " + this.$auth.getAccessToken()
       }
      }

      this.$axios
      .post(url, data, yourConfig)
      .then(response => {
        console.log(response);
        this.$swal('Information submitted.');
        this.$router.push('/dashboard/search-applicant/new-application/' + this.email);
      })
      .catch((error) => {
        console.log(error);
        this.$swal('Applicant already exists');
      })
    }
  }
};
</script>

<style>

</style>