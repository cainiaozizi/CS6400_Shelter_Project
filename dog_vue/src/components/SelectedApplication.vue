<template>
  <div class="container">
    <div class="d-flex justify-content-between align-items-center mt-3 mb-4">
      <div class="container">
        <h3>Adoption: Most Recent Application</h3> 
      </div>
      <div class="alert alert-info col-md-2" role="alert">
        Application ID: 
       <span class="font-weight-bold">{{details.application_ID}}</span>
      </div>
    </div>
    <div class="container mb-2">
      <table class="table">
          <thead>
            <tr>
              <td>Application Date</td>
              <td>First Name</td>
              <td>Last Name</td>
              <td>Email Address</td>
              <td>Phone Number</td>
              <td>Co-Applicant First Name</td>
              <td>Co-Applicant Last Name</td>

            </tr>
          </thead>
          <tbody v-if="details"> 
            <tr>
                <th>{{details.application_date}}</th>
                <th>{{details.first_name}}</th>
                <th>{{details.last_name}}</th>
                <th>{{details.email_address}}</th>
                <th>{{details.phone_number}}</th>
                <th>{{details.coapplicant_first_name}}</th>
                <th>{{details.coapplicant_last_name}}</th>

            </tr>
          </tbody>
        </table>
    </div>
    <form class="container mt-3 mb-3">
      <div class="input-group align-items-center">
        <span class="font-weight-bold">Dog ID:</span>
        <pre> </pre>
        <input
          v-on:keydown.13.prevent="submitApplicationInfo()"
          v-model="dogID"
          type="text"
          class="form-control"
          placeholder="Enter ID of dog to be adopted ..."
          required
          >
      </div>
      <div class="d-flex justify-content-between align-items-center mt-3 mb-4">
        <span class="font-weight-bold" v-if="dogID > 0">
          Total Adoption Fee: {{feeResults.adoption_fee}}   
          <button v-if="!feeResults.adoption_fee"
            @click="getAdoptionFee(dogID)" 
            type = "button" 
            Class="btn btn-secondary btn-sm">Click for Total Adoption Fee
            </button></span>
    </div>

      <div class="input-group mt-3 mb-3 align-items-center">
        <span class="font-weight-bold">Date:</span>
        <pre>   </pre>
        <datepicker v-model="adoptionDate"></datepicker>
      </div>
      <div class="input-group-append">
        <button 
          @click="submitApplicationInfo()" 
          type = "button" 
          Class="btn btn-primary"
          >Submit
        </button>
      </div>
    </form>
  </div>
</template>

<script>

import Datepicker from 'vuejs-datepicker';

export default {
  name: 'SelectedApplication',
  
  data() {
    return {
      dogID: '',
      searchError: '',
      selectedEmail: '',
      details: {},
      adoptionDate: '',
      feeResults: [],
      searchFeeError: ''
    };
  },

  mounted: function() {
    if (typeof this.$route.params.email != 'undefined'){
      this.selectedEmail = this.$route.params.email;
      this.getDetails();
    }
  },
  
  methods: {
    getDetails: function() {

      var url = "http://127.0.0.1:5000/api/latestapplication/" + this.selectedEmail;

      var yourConfig = {
        headers: {
            "Content-Type": "application/json",
           "Authorization": "JWT " + this.$auth.getAccessToken()
       }
      }

      this.$axios
      .get(url, yourConfig)
      .then(response => {
        if ((typeof response == 'undefined') 
          || (typeof response.data == 'undefined')
          || (typeof response.data.email_address == 'undefined')
        ){
           this.$swal('Something went wrong, please try again later.');
           return;
        }

        this.details = response.data;
      })
      .catch((error) => {
        if(error.response.status == 404) {
          this.$router.push('/dashboard/dog-detail/adoption/selected-application/');
        }
      })
    },

    getAdoptionFee: function(dogID) {
      if (dogID == '') {
        return;
      }
      this.feeResults = [];
      this.searchError = '';

      var url = "http://127.0.0.1:5000/api/eligibleapplicationcoap/" + dogID;

      var yourConfig = {
        headers: {
            "Content-Type": 'application/json',
           'Authorization': "JWT " + this.$auth.getAccessToken()
        }
      }
      this.$axios
      .get(url, yourConfig)
      .then(response => {
        this.feeResults = response.data[0];
      })
      .catch((error) => {
        if(error.response.status == 404) {
          if (typeof error.response.data.message != 'undefined') {
            this.searchError = error.response.data.message;
          } else {
            this.searchError = 'Records Not Found';
          }
        }
      })
    },

    submitApplicationInfo: function() {
      if ((this.dogID == '' || !this.dogID)
        || (this.adoptionDate == '' || !this.adoptionDate)
      ) {
       this.$swal('All fields are required');
       return;
      }

      if (this.dogID.length > 4) {
        this.$swal('Dog ID cannot be longer than 4 digits.');
        return;
      }

      let data = {
        'dog_ID': this.dogID,
        'adoption_date':  this.$moment(this.adoptionDate).format('YYYY-MM-DD'),
        'adoption_fee': this.feeResults.adoption_fee.toString(),
        'application_ID': this.details.application_ID.toString()
      }
      console.log(data);

      var url = "http://127.0.0.1:5000/api/submitadoption";
      var yourConfig = {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'JWT ' + this.$auth.getAccessToken()
       }
      }

      this.$axios
      .post(url, data, yourConfig)
      .then(response => {
        console.log(response);
        this.$swal('Adoption completed.');
        this.$router.push('/dashboard');
      })
      .catch((error) => {
        console.log(error);
      })
    }
  },
  components: {
    Datepicker
  }
};
</script>

<style>

</style>