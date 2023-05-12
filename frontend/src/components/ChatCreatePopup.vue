<template>
  <v-dialog v-model="dialog" max-width="500">
    <v-card>
      <header>
        <v-card-title><v-icon class='bx bxs-group'></v-icon>Create a new chat group</v-card-title>
      </header>
      <v-card-text>
        <v-form ref="form">
          <v-text-field v-model="groupName" label="Group name" required></v-text-field>
          <v-autocomplete v-model="selectedUsers" :items="users" label="Users" item-title="username" item-value="id" multiple chips></v-autocomplete>
        </v-form>
      </v-card-text>
      <v-card-actions class="justify-end">
        <v-btn color="purple" variant="elevated" @click="createChatGroup">Create</v-btn>
        <v-btn @click="closeDialog">Cancel</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      dialog: false,
      groupName: '',
      selectedUsers: [],
      users: [],
    };
  },
  methods: {
    async createChatGroup() {
      if (!this.$refs.form.validate()) {
        return;
      }

      // Send request to create chat group using this.groupName and this.selectedUsers
      // console.log('Group name:', this.groupName);
      // console.log('Selected users:', this.selectedUsers);
      const users = Object.keys(this.selectedUsers).map(key => {
        return { id: this.selectedUsers[key] };
      });
      const data = {title: this.groupName, participants: users}
      console.log(data)
      // const data = {}
      await axios.post('chats', data).then(response => {
          console.log(response.data)
          if (response.data.status === "success"){
            this.$router.replace("/chats")
          }
      }).catch(e =>{
          console.log(e)
          alert(JSON.stringify(e.response.data.detail, null, 2))

      })


      this.closeDialog();
    },
    openDialog() {
      this.dialog = true;
    },
    closeDialog() {
      this.dialog = false;
    },
  },
  async created(){
    await axios.get('auth/users?limit=100').then(response => {
        console.log(response.data)
        if (response.data.status === "success"){
          this.users = response.data.users
        }
    }).catch(e =>{
        console.log(e)
        alert(JSON.stringify(e.response.data.detail, null, 2))

    })
  }
};
</script>

<style scoped>
header{
  padding: 20px 30px;
  background-color: #f5f5f5;
  align-items: center;
}
</style>
