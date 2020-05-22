<template>
  <div class="home">
    <RegisterTaskComponent />
  </div>
</template>

<script>
// @ is an alias to /src
import RegisterTaskComponent from '@/components/RegisterTaskComponent.vue'

export default {
  name: 'RegisterTask',
  components: {
    RegisterTaskComponent
  }
}
</script>
