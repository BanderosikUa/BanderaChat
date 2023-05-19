<template>
  <div class="content col-9">
    <!-- Hello World {{ id }} -->
    <div class="chat" v-if="isLoading">
      <div class="direct" v-if="chat.is_direct">
        <div class="chat-header">
          <div class="chat-header-user">
            <figure class="avatar avatar-state-success">
              <img :src="chat.photo" class="rounded-circle" alt="avatar">
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
                      type="button" tabindex="0" role="menuitem" class="dropdown-item">Profile</button><button
                      type="button" tabindex="0" role="menuitem" class="dropdown-item">Add to archive</button><button
                      type="button" tabindex="0" role="menuitem" class="dropdown-item">Delete</button>
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
              <button class="btn-floating btn btn-primary"><i class='bx bxs-send'></i></button>
            </div>
          </form>
        </div>
      </div>
      <div class="group" v-else>
        <div class="chat-header">
          <div class="chat-header-user">
            <figure class="avatar avatar-state-success">
              <img :src="chat.photo" class="rounded-circle" alt="avatar">
            </figure>
            <div>
              <h5>{{ chat.title }}</h5>
              <small class="text-muted"><i>{{ chat.participants.length }} Members</i></small>
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
                      type="button" tabindex="0" role="menuitem" class="dropdown-item">Profile</button><button
                      type="button" tabindex="0" role="menuitem" class="dropdown-item">Add to archive</button><button
                      type="button" tabindex="0" role="menuitem" class="dropdown-item">Delete</button>
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
              <message-item v-for="message in messages" :key="message.id" :message="message"
                :is-direct="chat.is_direct"></message-item>
            </div>
          </div>
        </perfect-scrollbar>
        <div class="chat-footer">
          <form @submit.prevent="sendMessage">
            <input v-model="newMessage" placeholder="Write a message." type="text" class="form-control form-control">
            <div class="form-buttons">
              <button class="btn-floating btn btn-light"><i class='bx bx-paperclip'></i></button>
              <button class="btn-floating btn btn-light"><i class='bx bxs-microphone'></i></button>
              <button class="btn-floating btn btn-primary"><i class='bx bxs-send'></i></button>
            </div>
          </form>
        </div>
      </div>
    </div>
    <div class="chat" v-else>
      <span v-if="isLostWs">WebSocket connection lost, please reload a page!</span>
      <span v-else>Loading</span>
    </div>
  </div>
</template>

<script>
// import io from 'socket.io-client'
import axios from 'axios'
import MessageItem from "@/components/MessageItem.vue"


export default {
  components: {
    MessageItem,
  },
  data() {
    return {
      messages: [],
      chat: null,
      user: null,
      newMessage: '',
      connection: null,
      isLoading: false,
      isLostWs: false,
    }
  },
  async created() {
    await axios.get('auth/me').then(response => {
      console.log(response.data)
      if (response.data.status === true) {
          this.user = response.data.user
      }
    }).catch(e => {
        console.log(e)
        alert(JSON.stringify(e.response.data.detail, null, 2))

    })
    
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
        this.messages.push({ message: this.newMessage, created_at: time, type: 'own', user: this.user})

        const data = { action: "send_message", message: this.newMessage }
        this.connection.send(JSON.stringify(data));

        this.newMessage = ''
        await this.$nextTick()
        this.scrollDown()
      }
    },
    async fetchData() {
      console.log(this.$route.params.id)
      await axios.get(`chats/${this.$route.params.id}`).then(response => {
        console.log(response.data)
        if (response.data.status === true) {
          this.chat = response.data.chat
          this.messages = response.data.messages

          this.isLoading = true

        }
      }).catch(e => {
        console.log(e)
        alert(JSON.stringify(e.response.data, null, 2))

      })
      await this.$nextTick()
      this.scrollDown();
    },
    connectWs() {
      if (this.connection !== null) {
        this.connection.close()
      }

      console.log("Starting connection to WebSocket Server")
      const vm = this;
      this.connection = new WebSocket(`${this.$config.wsUrl}/chats/${this.$route.params.id}/ws?token=${localStorage.getItem('access_token')}`)

      // Send ping message periodically
      const pingInterval = setInterval(() => {
        if (this.connection.readyState === WebSocket.OPEN) {
          this.connection.send(JSON.stringify({ action: "ping" }));
        }
      }, 5000); // Adjust the interval as needed (e.g., every 5 seconds)

      this.connection.onmessage = function (event) {
        let data = JSON.parse(event.data)
        if (data.action === "newMessage") {
          vm.messages.push({ message: data.message.message, created_at: data.message.created_at, type: data.message.type, user: data.user })
        }
      }

      this.connection.onopen = function (event) {
        console.log(event)
        console.log("Successfully connected to the echo websocket server...")
      }

      this.connection.onclose = function (event) {
        console.log(event)
        console.log("Disconneted from websocket server")
        this.isLoading = true;
        this.isLostWs = true;
        clearInterval(pingInterval);
      }
    },
    scrollDown() {
      const messagesContainer = this.$refs.messages.$el
      messagesContainer.scrollTop = messagesContainer.scrollHeight
    },
  },
}
</script>

<style scoped>
.content {
  display: flex;
  height: 95vh;
}

.chat {
  flex: 1 1;
  display: flex;
  flex-direction: column;
}

.chat .direct {
  flex: 1 1;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.chat .group {
  flex: 1 1;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.chat-header {
  display: flex;
  justify-content: space-between;
  border-bottom: 2px solid #e1e1e1;
  padding-bottom: 20px;
}

.chat-header .chat-header-user {
  display: flex;
  align-items: center;
}

.chat-header .chat-header-user h5 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 0;
  line-height: 1;
}

.scrollbar-container {
  position: relative;
  height: 100%;
}

.chat-footer {
  border-top: 2px solid #e1e1e1;
  padding-top: 20px;
}

.chat-footer form {
  display: flex;
  padding: 10px;
  border-radius: 5px;
  align-items: center;
  background-color: #fff;
}

.chat-footer form input[type=text] {
  border: none;
  background-color: inherit;
}

.chat-footer form .form-buttons {
  display: flex;
}

.chat-footer form .form-buttons .btn {
  margin-left: 0.5rem;
}

.chat-body .messages {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}


</style>
