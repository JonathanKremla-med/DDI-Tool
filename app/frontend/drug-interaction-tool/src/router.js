import { createRouter, createWebHistory } from 'vue-router'
import Home from './views/Home.vue'
import Results from './views/Results.vue'
import Results_Graph from './views/Results_Graph.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/results', name: 'Results', component: Results },
  { path: '/results-graph', name: 'Results_Graph', component: Results_Graph }
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
})

