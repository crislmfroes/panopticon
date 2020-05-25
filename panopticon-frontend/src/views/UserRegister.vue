<template>
  <div class="home">
    <UserRegisterComponent />
  </div>
</template>

<script>
// @ is an alias to /src
import UserRegisterComponent from '@/components/UserRegisterComponent.vue'

export default {
  name: 'UserRegister',
  components: {
    UserRegisterComponent
  }
}
</script>
