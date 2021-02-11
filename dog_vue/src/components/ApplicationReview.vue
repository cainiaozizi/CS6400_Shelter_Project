<template>
  <div class="container">
    <div class="container mt-4 mb-5">
      <h3>Adoption Application Review</h3> 
    </div>
    <table class="table table-hover mt-4">
      <thead>
        <tr>
          <th scope="col">Selection</th>
          <th scope="col">Application ID</th>
          <th scope="col">Application Date</th>
          <th scope="col">First Name</th>
          <th scope="col">Last Name</th>
          <th scope="col">Email Address</th>
          <th scope="col">Phone Number</th>
          <th scope="col">Street</th>
          <th scope="col">City</th>
          <th scope="col">State</th>
          <th scope="col">Zip Code</th>
          <th scope="col">Co-Applicant First Name</th>
          <th scope="col">Co-Applicant Last Name</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(ar, index) in applicationReview" :key="index"> 
            <th scope="row">
              <button type="button"
                class="btn btn-success btn-sm"
                v-on:click="submitSelection(ar.application_ID, true)"
              >Accepted</button>
              <button type="button"
                class="mt-2 btn btn-dark btn-sm" 
                v-on:click="submitSelection(ar.application_ID, false)"
              >Rejected
              </button>
          </th>
          <td>{{ar.application_ID}}</td>
          <td>{{ar.application_Date}}</td>
          <td>{{ar.first_name}}</td>
          <td>{{ar.last_name}}</td>
          <td>{{ar.email_address}}</td>
          <td>{{ar.phone_number}}</td>
          <td>{{ar.street}}</td>
          <td>{{ar.city}}</td>
          <td>{{ar.state}}</td>
          <td>{{ar.zip_code}}</td>
          <td>{{ar.coapplicant_first_name}}</td>
          <td>{{ar.coapplicant_last_name}}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'ApplicationReview',
  
  data() {
    return {
      applicationReview: [],
      reportError: '',
    };
  },
  
  mounted: function() {
    this.applicationReview = [];
    this.getData();
  },

  methods: {

    getData: function() {

      var url = "http://127.0.0.1:5000/api/applicationreview";

      var yourConfig = {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'JWT ' + this.$auth.getAccessToken()
        }
      }

      this.applicationReview = [];
      this.$axios
      .get(url, yourConfig)
      .then(response => {
        if (typeof response.data.application_ID != 'undefined') {
          this.applicationReview.push(response.data);
        } else {
            for (var i = 0; i < response.data.length; i++) {
            this.applicationReview.push(response.data[i]);
            }
        }
      })
    },

    submitSelection: function(application_ID, status) {

      let data = {
        'application_ID': application_ID,
      }
      if (status) {

        var urlTrue = "http://127.0.0.1:5000/api/applicationapprove/" + application_ID;
        var yourConfigTrue = {
          headers: {
            "Content-Type": "application/json",
            "Authorization": "JWT " + this.$auth.getAccessToken()
          }
        }

        this.$axios
        .post(urlTrue, data, yourConfigTrue)
        .then(response => {
          if (response.data != null) {
            this.$swal('Something went wrong, please try again later.');
            return;
          }
          //success
          this.getData();
        
        })
        .catch((error) => {
          console.log(error);
        })
      } else {
        var urlFalse = "http://127.0.0.1:5000/api/applicationreject/" + application_ID;
        var yourConfigFalse = {
          headers: {
              "Content-Type": "application/json",
              "Authorization": "JWT " + this.$auth.getAccessToken()
        }
        }

        this.$axios
        .post(urlFalse, data, yourConfigFalse)
        .then(response => {
          if (response.data != null) {
            this.$swal('Something went wrong, please try again later.');
            return;
          }

          //success
          this.getData();
        
        })
        .catch((error) => {
          console.log(error);
        })

      }
    }
  }
};
</script>

<style>

</style>