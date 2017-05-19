<template lang="pug">
  div.container
    section.section
      div(v-if="error")
        server-error
      div.content(v-else)
        div(v-for="category of categories")
          h2.subtitle {{ category.name }}
          hr
          aside.menu
            ul.menu-list
              li(v-for="page in category.pages")
                router-link(:to="{ name: 'ViewPage', params: { category: category.name, page: page.name } }") {{ page.name }}
</template>

<script>
import Vue from 'vue'
import ServerError from '../components/ServerError'


export default {
  components: {
    ServerError
  },
  data() {
    return {
      error: false,
      categories: []
    }
  },
  async created() {
    try {
      const response = await this.$store.getters.axios.get(`${Vue.config.SERVER_URL}index`)
      this.categories = response.data
      this.error = false
    } catch (error) {
      console.error(error)
      this.error = true
    }
  }
}
</script>
