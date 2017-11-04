<template lang="pug">
  div.container
    section.section
      div(v-if="error")
        server-error
      div.content(v-else)
        div(v-if="categories.length > 0" v-for="category of categories")
          h2.subtitle {{ category.name }}
          hr
          aside.menu
            ul.menu-list
              li(v-if="category.pages.length > 0" v-for="page in category.pages")
                router-link(:to="{ name: 'ViewPage', params: { category: category.name, page: page.name } }") {{ page.name }}
              span(v-if="category.pages.length === 0") No pages in this category
          div.spacer
        div(v-if="categories.length === 0 && !loading")
          p No pages have been created.
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
      loading: true,
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
    } finally {
      this.loading = false
    }
  }
}
</script>

<style lang="stylus" scoped>
.spacer
  height 1em
</style>
