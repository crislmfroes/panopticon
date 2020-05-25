<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="12">
        <v-simple-table>
          <thead>
            <tr>
              <th>Task Name</th>
              <th>Image</th>
              <th>Number of Images</th>
              <th>Number of Labels</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(task, i) in tasks" v-bind:key="i">
              <td>{{task.name}}</td>
              <td>
                <v-img height="125" max-width="125" v-bind:contain="true" v-bind:src="imagePath(task)"></v-img>
              </td>
              <td>{{task.images.length}}</td>
              <td>{{task.labels.length}}</td>
              <td>
                <v-btn @click="deleteTask(i)" color="error">Delete</v-btn>
              </td>
            </tr>
          </tbody>
        </v-simple-table>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";
import store from "@/store";
import router from "@/router";

export default {
  name: "ListTasksComponent",
  data: () => ({
    valid: true,
    tasks: [],
    store: store
  }),
  mounted() {
    this.fetchTasks();
  },
  methods: {
    deleteTask(index) {
      const task = this.tasks[index];
      this.tasks.splice(index, 1);
      console.log(task._id.$oid);
      axios
        .post(
          `${process.env.VUE_APP_BACKEND_URL}/tasks/delete`,
          {
            id: task._id.$oid
          },
          {
            headers: {
              Authorization: `Bearer ${store.state.tokens.access}`,
              "Access-Control-Allow-Headers": "Content-Type, Authorization",
              "Access-Control-Allow-Origin": "*",
              "Content-Type": "application/json"
            }
          }
        )
        .then(() => {
          router.push({
            name: "task_list"
          });
        });
    },
    fetchTasks() {
      axios
        .get(`${process.env.VUE_APP_BACKEND_URL}/tasks/list`, {
          headers: {
            Authorization: `Bearer ${store.state.tokens.access}`,
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
            "Access-Control-Allow-Origin": "*",
            "Content-Type": "application/json"
          },
          crossDomain: true
        })
        .then(res => {
          console.log(res.data);
          this.tasks = res.data;
          this.tasks.forEach(task => {
            if (task.images.length > 0) {
              axios.post(
                `${process.env.VUE_APP_BACKEND_URL}/images/get`,
                {
                  user_id: store.state.user._id._$oid,
                  task_id: task._id.$oid,
                  id: task.images[0].$oid
                },
                {
                  headers: {
                    Authorization: `Bearer ${store.state.tokens.access}`,
                    "Access-Control-Allow-Headers": "Content-Type, Authorization",
                    "Access-Control-Allow-Origin": "*",
                    "Content-Type": "application/json"
                  },
                  crossDomain: true
                }
              ).then((res => {
                task.images.splice(0, 1, res.data)
                console.log(task);
                console.log(this.tasks);
              }));
            }
          });
        });
    },
    imagePath(task) {
      return (task.images.length > 0 && task.images[0].path !== undefined)
        ? `${process.env.VUE_APP_UPLOADS_URL}${task.images[0].path}`
        : "";
    }
  }
};
</script>
