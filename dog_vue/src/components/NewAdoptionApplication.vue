<template>
  <div class="container">

  <div class="container mt-4 mb-5">
  </div>
  <div class="container">
    <h1>New Adoption Application</h1> 
  </div>
    <form class="mb-3">
      <div class="container mt-4 text-info">
        <table class="table">
          <thead>
            <tr>
              <td>First Name</td>
              <td>Last Name</td>
              <td>Email Address</td>
              <td>Phone Number</td>
              <td>Street</td>
              <td>City</td>
              <td>State</td>
              <td>Zip</td>
            </tr>
          </thead>
          <tbody class="mb-2">
              <tr>
                <th>{{details.first_name}}</th>
                <th>{{details.last_name}}</th>
                <th>{{details.email_address}}</th>
                <th>{{details.phone_number}}</th>
                <th>{{details.street}}</th>
                <th>{{details.city}}</th>
                <th>{{details.state}}</th>
                <th>{{details.zip_code}}</th>
            </tr>
          </tbody>
        </table>
      </div>
    </form>
    <form class="container">
      <h5 class="text-info">Enter Optional Co-Applicant Information</h5>
      <div class="input-group align-items-center mt-4">
        <span class="font-weight-bold">First Name:</span>
        <pre> </pre>
        <input
          v-on:keydown.13.prevent="submitApplicationInfo()"
          v-model="coAppFirstName"
          type="text"
          class="form-control"
        >
        <pre> </pre>
        <span class="font-weight-bold">Last Name:</span>
        <pre> </pre>
        <input
          v-on:keydown.13.prevent="submitApplicationInfo()"
          v-model="coAppLastName"
          type="text"
          class="form-control"
        >
        <pre> </pre>
        <span class="font-weight-bold">Date:</span>
        <pre> </pre>
        <datepicker v-model="applicationDate"></datepicker>


      </div>
      <div class="input-group-append mt-5">
        <button 
          @click="submitApplicationInfo()" 
          type = "button" 
          Class="btn btn-secondary"
          >Submit
        </button>
      </div>
    </form>
  </div>
</template>

<script>

import Datepicker from 'vuejs-datepicker';

export default {
  name: 'NewAdoptionApplication',
  
  data() {
    return {
      selectedEmail: '',
      searchEmail: '',
      coAppFirstName: '',
      coAppLastName: '',
      applicationDate: '',
      details: {
        last_name: '',
        first_name: '',
        email_address: '',
        phone_number: '',
        street: '',
        city: '',
        state: '',
        zip_code: ''
      },
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
      var url = "http://127.0.0.1:5000/api/applicant/" + this.selectedEmail;

      var yourConfig = {
        headers: {
            "Content-Type": "application/json",
            "Authorization": "JWT " + this.$auth.getAccessToken()
       }
      }

      this.$axios
      .get(url, yourConfig)
      .then(response => {
        if (typeof response.data[0].email_address != 'undefined') {
           this.details = response.data[0];
        }
      })
      .catch((error) => {
        if(error.response.status == 404) {
          this.$router.push('/dashboard/search-applicant');
        }
      })
    },

    submitApplicationInfo: function() {
      if(this.applicationDate == '' || !this.applicationDate) {
       this.$swal('Date is required.');
       return;
      }

      let data = {
        "coapplicant_first_name": this.coAppFirstName,
        "coapplicant_last_name": this.coAppLastName,
        "application_date": this.$moment(this.applicationDate).format('YYYY-MM-DD')
      }

      var url = "http://127.0.0.1:5000/api/applicant/" + this.details.email_address + "/addapplication";
      var yourConfig = {
        headers: {
            "Content-Type": "application/json",
            "Authorization": "JWT " + this.$auth.getAccessToken()
       }
      }
      console.log(url);
      this.$axios
      .post(url, data, yourConfig)
      .then(response => {
        if (response.data == null) {
          this.getApplicationID(this.details.email_address);
        }
      })
      .catch((error) => {
        console.log(error);
        this.$swal('Something is off, please try again later.');
      })
    },


    getApplicationID: function(searchEmail) {

      searchEmail = searchEmail.toLowerCase();
      this.searchError = '';

      var url = "http://127.0.0.1:5000/api/applicant/" + searchEmail + "/addapplication/success";

      var yourConfig = {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'JWT ' + this.$auth.getAccessToken()
        }
      }

      this.$axios
      .get(url, yourConfig)
      .then(response => {
        if (typeof response.data == 'undefined'
          || !response.data.length
          || typeof response.data[0].ApplicationID == 'undefined'
        ) {
          this.$swal('Something went wrong, please try again later.');
          return;
        }

        //this.$router.push('/dashboard/search-applicant/new-application/' + this.email);
        this.$swal('Information submitted. Your application id is '+response.data[0].ApplicationID);
        this.$router.push('/dashboard');
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