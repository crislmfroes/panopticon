<template>
  <div class="home">
    <ListTasksComponent />
  </div>
</template>

<script>
// @ is an alias to /src
import ListTasksComponent from '@/components/ListTasksComponent.vue'

export default {
  name: 'ListTasks',
  components: {
    ListTasksComponent
  }
}
</script>
