<template>
  <div class="container">
    <div class="container mt-4 mb-5">
      <h3>Monthly Adoption Report</h3>
    </div>
    <table class="table table-hover mt-4">
      <tbody>
        <tr>
          <th>Adoption Month</th>
          <th>Breed Name</th>
          <th>Dogs Surrendered</th>
          <th>Dogs Adopted</th>
          <th>Total Expenses</th>
          <th>Total Fees</th>
          <th>Net Profit</th>
        </tr>
        <tr v-for="(mr, index) in monthlyReport" :key="index"> 
          <td>{{mr.adoption_month}}</td>
          <td>{{mr.breed_name}}</td>
          <td>{{mr.num_of_dog_surrender}}</td>
          <td>{{mr.num_of_dog_adopted}}</td>
          <td>{{mr.sum_dog_expense}}</td>
          <td>{{mr.sum_adoption_fee}}</td>
          <td>{{mr.net_profit}}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>

export default {
  name: 'MonthlyAdoptionReport',
  
  data() {
    return {
      monthlyReport: [],
      reportError: ''
    };
  },
  
  mounted: function() {
    this.monthlyReport = [];
    this.getData();
  },

  methods: {

    getData: function() {
      this.monthlyReport = [];

      var url = "http://127.0.0.1:5000/api/reports/adoption_report";
      var yourConfig = {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'JWT ' + this.$auth.getAccessToken()
        }
      }

      this.$axios
      .get(url, yourConfig)
      .then(response => {
        if (typeof response.data.num_of_dog_adopted != 'undefined') {
           this.monthlyReport.push(response.data);
        } else {
            for (var i = 0; i < response.data.length; i++) {
                this.monthlyReport.push(response.data[i]);
            }
        }
      })
      .catch((error) => {
        if(error.response.status == 404) {
          if (typeof error.response.data.message != 'undefined') {
            this.reportError = error.response.data.message;
          } else {
            this.reportError = 'Records Not Found';
          }
        }
      })
    }
  }
};
</script>

<style>
</style>