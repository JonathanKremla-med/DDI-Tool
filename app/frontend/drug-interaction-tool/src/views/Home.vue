<template>
  <div>
    <h1>Drug Interaction Checker</h1>
    <input v-model="currentInput" @keyup.enter="addDrug" placeholder="Enter drug name..." />
    <ul>
      <li v-for="(drug, index) in drugs" :key="index">
        {{ drug }}
        <button @click="removeDrug(index)">×</button>
      </li>
    </ul>
    <button :disabled="drugs.length < 2" @click="submit">Check Interactions</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const drugs = ref([])
const currentInput = ref("")

const addDrug = () => {
  const trimmed = currentInput.value.trim()
  if (trimmed && drugs.value.length < 5 && !drugs.value.includes(trimmed)) {
    drugs.value.push(trimmed)
    currentInput.value = ""
  }
}

const removeDrug = index => drugs.value.splice(index, 1)

const submit = () => {
  const params = new URLSearchParams()
  drugs.value.forEach(d => params.append("drug", d))
  router.push(`/results?${params.toString()}`)
}
</script>

