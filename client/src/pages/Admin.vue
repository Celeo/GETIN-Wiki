<template lang="pug">
  div
    role-management
    category-management
    deleted-pages-list
</template>

<script>
import RoleManagement from '../components/RoleManagement'
import CategoryManagement from '../components/CategoryManagement'
import DeletedPagesList from '../components/DeletedPagesList'


export default {
  components: {
    RoleManagement,
    CategoryManagement,
    DeletedPagesList
  }
}
</script>
