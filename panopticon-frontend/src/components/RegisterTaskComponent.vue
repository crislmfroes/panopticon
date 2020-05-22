<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="6">
        <v-form ref="form" lazy-validation v-model="valid">
          <v-text-field label="Task Name"></v-text-field>
          <v-simple-table>
            <thead>
              <tr>
                <th>Category Name</th>
                <th>Is Thing</th>
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
                  <v-btn @click="removeLabel(i)" class="mr-4" color="error">Remove</v-btn>
                </td>
              </tr>
            </tbody>
          </v-simple-table>
          <v-btn @click="addLabel()" class="mr-4" color="secondary">Add Label</v-btn>
          <v-file-input label="Images"></v-file-input>
          <v-btn color="success" class="mr-4" @click="validate">Register Task</v-btn>
        </v-form>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "RegisterTaskComponent",
  data: () => ({
    valid: true,
    labelFields: [{ name: "" }]
  }),
  methods: {
    addLabel() {
      this.labelFields.push({
        name: ""
      });
    },
    removeLabel(index) {
      this.labelFields.splice(index, 1);
    },
    validate() {
      this.$refs.form.validate();
    }
  }
};
</script>
