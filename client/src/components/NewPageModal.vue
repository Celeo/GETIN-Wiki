<template lang="pug">
div.modal-card
  header.modal-card-head
    p.modal-card-title New page
  section.modal-card-body
    b-field(label="Page name")
      b-input(
        v-model="name"
        placeholder="name"
        required
      )
    b-field(label="Category")
      b-select(placeholder="category" v-model="categoryId")
        option(
          v-for="category in categories"
          v-bind:value="category.id"
          v-bind:key="category.id"
        ) {{ category.name }}
  footer.modal-card-foot
      button.button(@click.prevent="$emit('close')") Close
      button.button.is-success(@click="save" v-bind:disabled="name === '' || categoryId === 0") Create
</template>

<script>
import Vue from 'vue'


export default {
  data() {
    return {
      name: '',
      categoryId: 0,
      categories: []
    }
  },
  async created() {
    try {
      const response = await this.$store.getters.axios.get(`${Vue.config.SERVER_URL}category`)
      this.categories = response.data
    } catch (error) {
      console.error(error)
      this.$dialog.alert({
        message: 'There was an error creating the new page',
        type: 'is-danger',
        hasIcon: true
      })
      this.$emit('close')
    }
  },
  methods: {
    async save() {
      try {
        const data = {
          name: this.name,
          category_id: this.categoryId
        }
        const response = await this.$store.getters.axios.post(`${Vue.config.SERVER_URL}page`, data)
        this.$router.push({
          name: 'ViewPage',
          params: {
            category: response.data.category,
            page: response.data.page
          }
        })
        this.$emit('close')
      } catch (error) {
        console.error(error)
        this.$dialog.alert({
          message: 'There was an error creating the new page',
          type: 'is-danger',
          hasIcon: true
        })
        this.$emit('close')
      }
    }
  }
}
</script>

<style scoped>
.modal-card {
    margin: 0 auto;
    width: auto;
}
</style>
