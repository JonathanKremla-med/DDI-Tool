<template>
  <div>
    <h2>Drug Interaction Graph</h2>
    <div id="cy" style="width: 100%; height: 500px;"></div>
    <button @click="goBack">← Back</button>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useInteractionStore } from '../stores/interactions'
import cytoscape from 'cytoscape'

const store = useInteractionStore()
const route = useRoute()
const router = useRouter()

const goBack = () => router.push('/results')

onMounted(async () => {
  const drugs = store.drugs
  const interactions = store.interactions
  const params = new URLSearchParams()

  const nodes = new Set()
  const edges = []

    interactions.forEach(({ drug1, drug2, level }) => {
    nodes.add(drug1)
    nodes.add(drug2)

    const color = {
      "Major": "red",
      "Moderate": "orange",
      "Minor": "green"
    }[level] || "gray"

    edges.push({
data: {
    id: `${drug1}-${drug2}`,
    source: drug1,
    target: drug2,
    color: color
  }
})
  })

  const cy = cytoscape({
    container: document.getElementById('cy'),
    elements: [
      ...Array.from(nodes).map(d => ({ data: { id: d, label: d } })),
      ...edges
    ],
    style: [
      {
        selector: 'node',
        style: {
          label: 'data(label)',
          'background-color': '#007acc',
          color: '#fff',
          'text-valign': 'center',
          'text-halign': 'center',
          'font-size': 14,
          width: 50,
          height: 50,
          'border-width': 2,
          'border-color': '#333'
        }
      },
      {
        selector: 'edge',
        style: {
          width: 3,
          'line-color': 'data(color)',
          'target-arrow-color': 'data(color)',
          'target-arrow-shape': 'triangle'
        }
      }
    ],
  })
  cy.resize()
  cy.layout({ name: 'circle', fit: true, padding: 50 }).run()
})
</script>
<style>
#app{
	text-align: ;
}
</style>


