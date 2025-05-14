import { defineStore } from 'pinia'

export const useInteractionStore = defineStore('interactions', {
  state: () => ({
    drugs: [],
    interactions: []
  }),
  actions: {
    setDrugs(drugList) {
      this.drugs = drugList
    },
    setInteractions(results) {
      this.interactions = results
    }
  }
})

