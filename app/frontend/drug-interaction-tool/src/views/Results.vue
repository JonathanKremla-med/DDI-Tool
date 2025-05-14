<template>
  <div>
    <h1>Results</h1>
    <router-link :to="{ name: 'Results_Graph', query: route.query }">
  🔍 	View as Graph
    </router-link>
    <div v-if="loading">Loading interactions...</div>
    <ul v-else>
      <li v-for="(item, index) in interactions" :key="index">
        {{ item.drug1 }} + {{ item.drug2 }} → <strong>{{ item.level }}</strong>
      </li>
    </ul>
    <button @click="goBack">← Back</button>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useInteractionStore } from '../stores/interactions'

const store = useInteractionStore()
const route = useRoute()
const router = useRouter()
const loading = ref(true)
const interactions = ref([])

const fetchInteractions = async () => {
  const params = new URLSearchParams()
  const drugs = route.query.drug
  const drugList = Array.isArray(drugs) ? drugs : [drugs]

	drugList.forEach(drug => params.append("drugs", drug))

  console.log(params.toString())
  try {
	const res = await fetch(`http://localhost:8000/interactions?${params.toString()}`)
	const data = await res.json()
	console.log(data)
	interactions.value = data.interactions
  } catch (err) {
    console.error("Error fetching data", err)
  } finally {
    store.setDrugs(drugs.value)
    store.setInteractions(interactions.value)
    loading.value = false
  }
}

const goBack = () => router.push('/')

onMounted(fetchInteractions)
</script>

