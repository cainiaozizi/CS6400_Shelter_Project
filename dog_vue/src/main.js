import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import VolunteerLookup from "./components/VolunteerLookup"
import Adoption from "./components/Adoption"
import NewAdoptionApplication from "./components/NewAdoptionApplication"
import SelectedApplication from "./components/SelectedApplication"
import ApplicationReview from "./components/ApplicationReview"
import LogIn from "./components/LogIn"
import MonthlyAdoptionReport from "./components/MonthlyAdoptionReport"
import ExpenseAnalysisReport from "./components/ExpenseAnalysisReport"
import NotFound from "./components/NotFound"
import Dashboard from "./components/Dashboard"
import AddDogZi from "./components/AddDogZi"
import SearchApplicant from "./components/SearchApplicant"
import AddExpenseZi from "./components/AddExpenseZi"
import EditDogZi from "./components/EditDogZi"
import AnimalControlReportZi from "./components/AnimalControlReportZi"
import AnimalControlReportDetailsZi from './components/AnimalControlReportDetailsZi'

import axios from "axios"
import EventBus from './services/event-bus'
import auth from './services/auth'

import "bootstrap"
import "bootstrap/dist/css/bootstrap.css"
import VueSweetalert2 from 'vue-sweetalert2';
import {BootstrapVue, BootstrapVueIcons} from 'bootstrap-vue'
import ElementUI from "element-ui"
import 'element-ui/lib/theme-chalk/index.css'
import moment  from 'moment';

//import {library} from "@fortawesome/fontawesome-svg-core";
//import {
//  faPlus, faMinus, faTrash, faCheck
//} from "@fortawesome/free-solid-svg-icons"
//library.add(faPlus, faMinus, faTrash, faCheck);

Vue.use(VueSweetalert2 );
Vue.use(VueRouter);
Vue.use(ElementUI);
Vue.use(BootstrapVueIcons);
Vue.use(BootstrapVue);
Vue.prototype.$axios = axios;
Vue.prototype.$eventBus = EventBus;

auth.$eventBus = EventBus;
auth.$axios = axios;
Vue.prototype.$auth = auth;
Vue.prototype.$moment = moment;


Vue.config.productionTip = false


//Register routes
const routes = [
  {path: '/', component: Dashboard},
  {path: '/login', component: LogIn},
  {path: '/dashboard', component: Dashboard},
  {path: '/dashboard/add-dog', component: AddDogZi},
  {path: '/dashboard/dog-detail/edit-dog/:dogID', component: EditDogZi},
  {path: '/dashboard/dog-detail/add-expense/:dogID', component: AddExpenseZi},
  
  {path: '/dashboard/dog-detail/adoption', component: Adoption},

  {path: '/dashboard/dog-detail/adoption/selected-application/:email', 
    component: SelectedApplication},
  
  {path: '/dashboard/search-applicant', 
    component: SearchApplicant},

  {path: '/dashboard/search-applicant/new-application/:email', 
    component: NewAdoptionApplication},

  {path: '/dashboard/application-review', 
    component: ApplicationReview},

  {path: '/dashboard/animal-control-report', 
    component: AnimalControlReportZi},

  {path: '/dashboard/animal-control-report-details/:year_month', 
    component: AnimalControlReportDetailsZi},

  {path: '/dashboard/monthly-adoption-report', 
    component: MonthlyAdoptionReport},

  {path: '/dashboard/expense-analysis-report', 
    component: ExpenseAnalysisReport},

  {path: '/dashboard/volunteer-lookup', 
    component: VolunteerLookup},

  {path: '*', component: NotFound}
];

const router = new VueRouter({
  mode: 'history',
  routes: routes
});

const private_routes = [
  '/',
  '/dashboard/dog-detail/adoption',
  '/dashboard/dog-detail/adoption/selected-application',
  '/dashboard/new-adoption-application',
  '/dashboard/application-review',
  '/dashboard/animal-control-report',
  '/dashboard/monthly-adoption-report',
  '/dashboard/expense-analysis-report',
  '/dashboard/volunteer-lookup',
];

router.beforeEach((to, from, next) => {
  let token = localStorage.getItem('token');

  if(private_routes.indexOf(to.path) !== -1 && !token) {
      router.push('/login');
      return false;
  }

  next();
});


//Mount the main app component
new Vue({
  render: h => h(App),
  router
}).$mount('#app')
