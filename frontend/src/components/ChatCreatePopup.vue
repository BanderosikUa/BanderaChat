<template>
  <v-dialog v-model="dialog" max-width="500">
    <v-card>
      <header>
        <v-card-title><v-icon class='bx bxs-group'></v-icon>Create a new chat group</v-card-title>
      </header>
      <v-card-text>
        <v-form ref="form">
          <v-text-field v-model="groupName" label="Group name" :rules="rules"></v-text-field>
          <v-autocomplete v-model="selectedUsers" :items="users" label="Users" item-title="username" item-value="id"
            multiple chips :rules="[v => !!v || 'Item is required']" required></v-autocomplete>
          <v-file-input accept="image/png, image/jpeg, image/png" placeholder="Pick an photo" label="Photo"
            v-model="photo"></v-file-input>
          <v-card-actions class="justify-end">
            <v-btn color="purple" variant="elevated" @click="onSubmit">Create</v-btn>
            <v-btn @click="closeDialog">Cancel</v-btn>
          </v-card-actions>
        </v-form>
      </v-card-text>
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
      photo: null,
      chat: null,
      rules: [
        v => v.length > 0 || "This field are required"
      ],
    };
  },
  methods: {
    async onSubmit() {
      if (!this.$refs.form.validate()) {
        console.log('no validate')
        return;
      }

      const users = Object.keys(this.selectedUsers).map(key => {
        return { id: this.selectedUsers[key] };
      });
      const data = { title: this.groupName, participants: users}
      await axios.post('chats', data).then(async response => {
        console.log(response.data)
        if (response.data.status === true) {
          if (this.photo !== null) {
            const formData = new FormData();
            formData.append('photo', this.photo[0]);
            await axios.post(`chats/${response.data.chat.id}/upload`, formData).then(response => {
              console.log(response.data)
              this.chat = response.data.chat
            }).catch(e => {
              console.log(e)
              alert(JSON.stringify(e.response.data.detail, null, 2))
            })
          }else{
            this.chat = response.data.chat
          }
        }
      }).catch(e => {
        console.log(e)
        alert(JSON.stringify(e.response.data.detail, null, 2))
        
      })
      
      this.$emit("create", this.chat)
      this.closeDialog();
    },
    openDialog() {
      this.dialog = true;
    },
    closeDialog() {
      this.dialog = false;
    },
  },
  async created() {
    await axios.get('users?limit=100').then(response => {
      console.log(response.data)
      if (response.data.status === true) {
        this.users = response.data.users
      }
    }).catch(e => {
      console.log(e)
      alert(JSON.stringify(e.response.data.detail, null, 2))

    })
  }
};
</script>

<style scoped>
header {
  padding: 20px 30px;
  background-color: #f5f5f5;
  align-items: center;
}
</style>
