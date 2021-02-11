<template>
  <div class="container">
    <div class="container mt-4 mb-5">
      <h3>Expense Analysis Report</h3> 
    </div>
    <table class="table table-hover mt-4">
      <tbody>
        <tr>
          <th>Vendor</th>
          <th>Total Spent</th>
        </tr>
        <tr v-for="(er, index) in expenseReport" :key="index"> 
          <td>{{er.vendor_name}}</td>
          <td>{{er.total}}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>

export default {
  name: 'ExpenseAnalysisReport',
  
  data() {
    return {
      expenseReport: [],
      reportError: ''
    };
  },

  mounted: function() {
    this.expenseReport = [];
    this.getData();
  },
  
  methods: {

    getData: function() {
      this.expenseReport = [];

      var url = "http://127.0.0.1:5000/api/reports/expense_report";

      var yourConfig = {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'JWT ' + this.$auth.getAccessToken()
        }
      }

      this.$axios
      .get(url, yourConfig)
      .then(response => {
        if (typeof response.data.vendor_name != 'undefined') {
           this.expenseReport.push(response.data);
        } else {
            for (var i = 0; i < response.data.length; i++) {
                this.expenseReport.push(response.data[i]);
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