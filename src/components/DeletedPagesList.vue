<template lang="pug">
  section.section
    div.container
      h1.title Deleted pages
      hr
      div(v-if="error")
        server-error
      div(v-if="!error")
        aside.menu
          ul.menu-list
            li(v-if="pages.length > 0" v-for="page in pages")
              router-link(:to="{ name: 'EditPage', params: { pageId: page.id } }") {{ page.name }}
            span(v-if="pages.length === 0") No deleted pages
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
      pages: [],
      error: false
    }
  },
  methods: {
    async loadData() {
      try {
        const response = await this.$store.getters.axios.get(`${Vue.config.SERVER_URL}deleted_pages`)
        this.pages = response.data
        this.error = false
      } catch (error) {
        console.error(error)
        this.error = true
      }
    }
  },
  async created() {
    await this.loadData()
  }
}
</script>
