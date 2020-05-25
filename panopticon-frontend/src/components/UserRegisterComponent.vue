<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="6">
        <v-form ref="form" lazy-validation v-model="valid">
          <v-text-field label="Name" v-model="name"></v-text-field>
          <v-text-field label="E-Mail" v-model="email"></v-text-field>
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
          <v-btn color="success" class="mr-4" @click="submit">Sign Up</v-btn>
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";
import router from "@/router";

export default {
  name: "UserRegisterComponent",
  data: () => ({
    valid: true,
    show1: false,
    email: "",
    password: "",
    name: ""
  }),
  methods: {
    submit() {
      axios
        .post(
          `${process.env.VUE_APP_BACKEND_URL}/users/register`,
          {
            name: this.name,
            email: this.email,
            password: this.password
          },
          {
            headers: {
              "Access-Control-Allow-Headers": "Content-Type",
              "Access-Control-Allow-Origin": "*",
              "Content-Type": "application/json"
            }
          }
        )
        .then(() => {
          router.push({
            name: "login"
          });
        });
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
