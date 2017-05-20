<template lang="pug">
  section.section
    div.container
      div(v-if="error")
        server-error
      div.content(v-if="!error && currentPage")
        nav.level
          div.level-left
            div.level-item
              h1.title History for "{{ currentPage.name }}"
          div.level-right
            div.level-item
              router-link.button(:to="pageUrlData")
                b-icon(icon="arrow-left")
                span Back to page
        hr
        table.table(v-if="showingList")
          thead
            tr
              th View
              th Global id
              th Page name
              th Category
              th Editor
              th Timestamp
          tfoot
          tbody
            tr(v-for="history in histories")
              td
                b-tooltip(label="View this version" type="is-dark")
                  a.button-control(@click="viewVersion(history.id)")
                    b-icon(icon="eye")
              td {{ history.id }}
              td {{ history.new_name }}
              td {{ history.category_name }}
              td {{ history.user_name }}
              td {{ history.timestamp_print }}
        div(v-if="!showingList")
          nav.level
            div.level-left
              div.level-item
                button.button(@click="viewList")
                  b-icon(icon="arrow-left")
                  span Show list
            div.level-right
              div.level-item
                button.button.is-warning(@click="rollback")
                  b-icon(icon="undo")
                  span Rollback to this version
          textarea#revisionContent.textarea(v-model="revisionContent" disabled="true")
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
      histories: [],
      showingList: true,
      selectedVersion: 0
    }
  },
  computed: {
    pageUrlData() {
      return { name: 'ViewPage', params: { category: this.currentPage.category_name, page: this.currentPage.name } }
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
    },
    viewVersion(historyId) {
      this.showingList = false
      this.revisionContent = this.histories.filter(e => e.id === historyId)[0].new_content
      this.selectedVersion = historyId
    },
    viewList() {
      this.showingList = true
      this.selectedVersion = 0
    },
    rollback() {
      this.$dialog.confirm({
        title: 'Confirm',
        message: 'Are you sure that you want to roll this page back to this version?',
        type: 'is-warning',
        hasIcon: true,
        onConfirm: async () => {
          try {
            const response = await this.$store.getters.axios.put(`${Vue.config.SERVER_URL}rollback/${this.selectedVersion}`)
            this.$toast.open({
              message: 'Page saved',
              type: 'is-success'
            })
            this.$router.push({ name: 'ViewPage', params: { category: response.data.category, page: response.data.name } })
          } catch (error) {
            console.error(error)
            Vue.nextTick(() => {
              this.$dialog.alert({
                message: 'There was an error making the change',
                type: 'is-danger',
                hasIcon: true
              })
            })
          }
        }
      })
    }
  },
  async created() {
    await this.loadData()
  }
}
</script>

<style lang="stylus" scoped>
.button-control
  color black
  padding-right 5px

#revisionContent
  height 65vh
</style>
