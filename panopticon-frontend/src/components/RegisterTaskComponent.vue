<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="12">
        <v-form ref="form" lazy-validation v-model="valid">
          <v-text-field label="Task Name" v-model="taskName"></v-text-field>
          <v-simple-table>
            <thead>
              <tr>
                <th>Category Name</th>
                <th>Is Thing</th>
                <th>Color</th>
                <th>Options</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(labelField, i) in labelFields" v-bind:key="i">
                <td>
                  <v-text-field label="Category Name" v-model="labelField.name"></v-text-field>
                </td>
                <td>
                  <v-checkbox label="Is Thing" v-model="labelField.isthing"></v-checkbox>
                </td>
                <td>
                  <v-color-picker label="Color" v-model="labelField.color"></v-color-picker>
                </td>
                <td>
                  <v-btn @click="removeLabel(i)" class="mr-4" color="error">Remove</v-btn>
                </td>
              </tr>
            </tbody>
          </v-simple-table>
          <v-btn @click="addLabel()" class="mr-4" color="secondary">Add Label</v-btn>
          <v-file-input v-model="file" label="Images"></v-file-input>
          <v-btn color="success" class="mr-4" @click="validate">Register Task</v-btn>
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";
import store from "@/store";
import router from "@/router";

export default {
  name: "RegisterTaskComponent",
  data: () => ({
    valid: true,
    labelFields: [],
    file: null,
    taskName: null
  }),
  methods: {
    addLabel() {
      this.labelFields.push({
        name: "",
        isthing: false
      });
    },
    removeLabel(index) {
      this.labelFields.splice(index, 1);
    },
    validate() {
      const formData = new FormData();
      this.labelFields.forEach(labelField => {
        console.log(labelField.isthing);
        formData.append("label", labelField.name);
        formData.append("isthing", labelField.isthing);
        formData.append(
          "color",
          parseInt(labelField.color.hex.replace("#", "0x"))
        );
      });
      formData.append("file", this.file);
      formData.append("name", this.taskName);
      axios
        .post(`${process.env.VUE_APP_BACKEND_URL}/tasks/create`, formData, {
          headers: {
            'Authorization': `Bearer ${store.state.tokens.access}`,
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "multipart/form-data",
          }
        })
        .then(res => {
          console.log(res);
          if (res.status === 200) {
            router.push({
              name: "task_list"
            });
          }
        });
    }
  }
};
</script>
