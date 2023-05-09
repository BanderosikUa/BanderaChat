<template>
  <div class="content col-9">
    <!-- Hello World {{ id }} -->
    <div class="chat" v-if="isLoading">
      <div class="chat-header">
        <div class="chat-header-user">
          <figure class="avatar avatar-state-success">
            <img :src="chat.photo" class="rounded-circle"
              alt="avatar">
          </figure>
          <div>
            <h5>{{ chat.title }}</h5>
            <small class="text-muted"><i>Online</i></small>
          </div>
        </div>
        <div class="chat-header-action">
          <ul class="list-inline">
            <li class="list-inline-item" data-toggle="tooltip" title="Detail">
              <div class="dropdown">
                <span data-bs-toggle="dropdown" aria-expanded="false" aria-haspopup="true" class="">
                  <button class="btn btn-secondary"><i class='bx bx-dots-horizontal-rounded'></i></button>
                </span>
                <div tabindex="-1" role="menu" aria-hidden="true" class="dropdown-menu dropdown-menu-right"><button
                    type="button" tabindex="0" role="menuitem" class="dropdown-item">Profile</button><button type="button"
                    tabindex="0" role="menuitem" class="dropdown-item">Add to archive</button><button type="button"
                    tabindex="0" role="menuitem" class="dropdown-item">Delete</button>
                  <div tabindex="-1" class="dropdown-divider"></div><button type="button" tabindex="0" role="menuitem"
                    class="dropdown-item">Block</button>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </div>
      <perfect-scrollbar class="scrollbar-container" :settings="scrollbarSettings" ref="messages">
        <div class="chat-body">
          <div class="messages">
            <message-item v-for="message in messages" :key="message.id" :message="message"></message-item>
          </div>
        </div>
      </perfect-scrollbar>
      <div class="chat-footer">
        <form @submit.prevent="sendMessage">
          <input v-model="newMessage" placeholder="Write a message." type="text" class="form-control form-control">
          <div class="form-buttons">
                <button class="btn-floating btn btn-light"><i class='bx bx-paperclip'></i></button>
                <button class="btn-floating btn btn-light"><i class='bx bxs-microphone'></i></button>
                <button class="btn-floating btn btn-primary"><i class='bx bxs-send' ></i></button></div>
        </form>
      </div>
    </div>
    <div class="chat" v-else>
      Loading
    </div>
  </div>
</template>

<script>
// import io from 'socket.io-client'
import axios from 'axios'
import MessageItem from "./MessageItem.vue"


export default {
  components: {
    MessageItem,
  },
  data(){
    return {
      messages: [],
      chat: null, 
      newMessage: '',
      connection: null,
      isLoading: false,
    }
  },
  async created(){
    
    this.$watch(
      () => this.$route.params,
      () => {
        this.fetchData()
        this.connectWs()
      },
      // fetch the data when the view is created and the data is
      // already being observed
      { immediate: true }
      )
  },
  // computed: { key () { if(this.$route.name == 'chat-detail') { return this.$route.name } else { return this.$route.fullPath } } },
  methods: {
    async sendMessage() {
      if (this.newMessage.trim() !== '') {
        const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        this.messages.push({ message: this.newMessage, created_at: time, type: 'own' })
        
        const data = {action: "send_message", message: this.newMessage}
        this.connection.send(JSON.stringify(data));
        
        this.newMessage = ''
        await this.$nextTick()
        this.scrollDown()
      }
    },
    async fetchData(){
      try{
          const response = await axios.get(`chats/${this.$route.params.id}`)

          console.log(response)
          if (response.data.status === true){
            this.chat = response.data.chat
            this.messages = response.data.messages
            
            this.isLoading = true

            await this.$nextTick()
            this.scrollDown();
          }
          } catch(e){
              console.log(e)
      }
    },
    connectWs(){
      console.log("Starting connection to WebSocket Server")
      const vm = this;
      this.connection = new WebSocket(`ws://127.0.0.1:5000/chats/${this.$route.params.id}/ws?token=${localStorage.getItem('access_token')}`)

      this.connection.onmessage = function(event) {
        let data = JSON.parse(event.data)
        if (data.action === "newMessage"){
          vm.messages.push({message: data.message.message, created_at: data.message.created_at, type: data.message.type})
        }
      }

      this.connection.onopen = function(event) {
        console.log(event)
        console.log("Successfully connected to the echo websocket server...")
      }
    },
    scrollDown() {
      const messagesContainer = this.$refs.messages.$el
      messagesContainer.scrollTop = messagesContainer.scrollHeight
    }
  },
  computed: {
    messageType(){
      return {
        "outgoing-message": this.message.type === "own",
        "": this.message.type === "other"
      }
    }
  }
}
</script>

<style scoped>
.content{
  display: flex;
  height: 95vh;
}

.chat {
  flex: 1 1;
  display: flex;
  flex-direction: column;
}

.chat .chat-header {
  display: flex;
  justify-content: space-between;
  border-bottom: 2px solid #e1e1e1;
  padding-bottom: 20px;
}

.chat .chat-header .chat-header-user {
  display: flex;
  align-items: center;
}

.chat .chat-header .chat-header-user h5 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 0;
  line-height: 1;
}

.scrollbar-container {
    position: relative;
    height: 100%;
}


.chat .chat-footer {
  border-top: 2px solid #e1e1e1;
  padding-top: 20px;
}

.chat .chat-footer form {
  display: flex;
  padding: 10px;
  border-radius: 5px;
  align-items: center;
  background-color: #fff;
}

.chat .chat-footer form input[type=text] {
    border: none;
    background-color: inherit;
}

.chat .chat-footer form .form-buttons {
    display: flex;
}

.chat .chat-footer form .form-buttons .btn {
    margin-left: 0.5rem;
}

.chat .chat-body .messages {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}

</style>
