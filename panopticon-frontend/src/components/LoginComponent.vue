<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="6">
        <v-form ref="form" lazy-validation v-model="valid" >
          <v-text-field label="Username"></v-text-field>
          <v-text-field
            v-model="password"
            :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
            :type="show1 ? 'text' : 'password'"
            name="input-10-1"
            label="Password"
            hint="At least 8 characters"
            counter
            @click:append="show1 = !show1"
          ></v-text-field>
          <v-btn color="success" class="mr-4" @click="validate">Sign In</v-btn>
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "LoginComponent",
  data: () => ({
    valid: true,
    show1: false
  }),
  methods: {
    validate() {
      this.$refs.form.validate();
    },
    reset() {
      this.$refs.form.reset();
    },
    resetValidation() {
      this.$refs.form.resetValidation();
    }
  }
};
</script>
