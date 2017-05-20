<template lang="pug">
  section.section
    div.container
      div(v-if="error")
        server-error
      div.content(v-if="!error && currentPage")
        nav.level
          div.level-left
            div.level-item
              h1.title History for {{ currentPage.name }}
          div.level-right
            div.level-item
              router-link.button(
                :to="{ name: 'ViewPage', params: { category: currentPage.category_name, page: currentPage.name } }"
              )
                b-icon(icon="arrow-left")
                span Back to page
        hr
        table.table
          thead
            tr
              th Edit id
              th Name
              th Category
              th Editor
              th Timestamp
              th Approver
          tfoot
          tbody
            tr(v-for="history in histories")
              td {{ history.id }}
              td {{ history.new_name }}
              td {{ history.category_name }}
              td {{ history.user_name }}
              td {{ history.timestamp_print }}
              td {{ history.approved_by }}
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
      currentPage: null,
      histories: []
    }
  },
  methods: {
    async loadData() {
      try {
        const pageResponse = await this.$store.getters.axios.get(`${Vue.config.SERVER_URL}page/${this.$route.params.pageId}`)
        this.currentPage = pageResponse.data
        const historyResponse = await this.$store.getters.axios.get(`${Vue.config.SERVER_URL}history/${this.$route.params.pageId}`)
        this.histories = historyResponse.data
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
