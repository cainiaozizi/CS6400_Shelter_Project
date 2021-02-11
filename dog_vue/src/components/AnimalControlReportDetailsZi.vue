<template>
    <b-container class="mt-4">
        <h2>Animal Control Report Details 1 -- Surrendered Dog</h2>
         <div>
            <table class="table table-hover">
                <tbody>
                <tr>
                    <th>Dog ID</th>
                    <th>Breed Name</th>
                    <th>Sex</th>
                    <th>Alteration_Status</th>
                    <th>Microchip ID</th>
                    <th>Surrender Date</th>  
                </tr>

                <tr v-for="item in DetailReport1" 
                    v-bind:key="item.year_month">
                    <td>{{item.dog_ID}}</td>
                    <td>{{item.breed_name}}</td>
                    <td>{{item.sex}}</td>
                    <td>{{item.alteration_status}}</td>
                    <td>{{item.microchip_ID}}</td>
                    <td>{{item.surrender_date}}</td>   
                </tr>
                </tbody>
            </table>
         </div>

        <h2>Animal Control Report Details 2 --- Adopted Dog</h2>
         <div>
            <table class="table table-hover">
                <tbody>
                <tr>
                    <th>Dog ID</th>
                    <th>Breed Name</th>
                    <th>Sex</th>
                    <th>Alteration_Status</th>
                    <th>Microchip ID</th>
                    <th>Surrender Date</th>
                    <th>Days in Rescue</th>
                </tr>

                <tr v-for="item in DetailReport2" 
                    v-bind:key="item.year_month">
                    <td>{{item.dog_ID}}</td>
                    <td>{{item.breed_name}}</td>
                    <td>{{item.sex}}</td>
                    <td>{{item.alteration_status}}</td>
                    <td>{{item.microchip_ID}}</td>
                    <td>{{item.surrender_date}}</td>
                    <td>{{item.days_in_rescue}}</td>    
                </tr>
                </tbody>
            </table>
         </div>

<router-link :to="'/dog_dashboard/' + this.useremail">
  <button id="myButton" class="foo bar">Go to Dashboard</button>
</router-link>
       
    </b-container>
</template>

<style lang="scss" scoped>
</style>

<script>
import axios from 'axios'
export default {
    name: 'AnimalControlReportDetails',
    data () {
        return {
            DetailReport1: [],
            DetailReport2: [],
            isAdmin : 0,
            cur_year_month: this.$route.path.substr(this.$route.path.lastIndexOf('/') + 1),
            useremail: localStorage.getItem('useremail')
        }
    },
    methods:{    
        display_rp1(){
             var url =  'http://127.0.0.1:5000/api/reports/animal_control_detail_1/'+ this.cur_year_month;
            var yourConfig = {
                headers: {
                'Content-Type': 'application/json',
                'Authorization': 'JWT ' + this.$auth.getAccessToken()
                }
            }
            axios.get(url, yourConfig).then((res) => {
            this.DetailReport1 = res.data
            console.log('DetailReport1: ', this.DetailReport1)
            })
        },
        display_rp2(){
            var url =  'http://127.0.0.1:5000/api/reports/animal_control_detail_2/'+ this.cur_year_month;
            var yourConfig = {
                headers: {
                'Content-Type': 'application/json',
                'Authorization': 'JWT ' + this.$auth.getAccessToken()
                }
            }
            axios.get(url, yourConfig).then((res) => {
            this.DetailReport2 = res.data
            console.log('DetailReport2: ', this.DetailReport2)
            })    
        },
    },
    
    created(){
            console.log("in dashborad created()")
            this.display_rp1()
            this.display_rp2()
    }
}
</script>