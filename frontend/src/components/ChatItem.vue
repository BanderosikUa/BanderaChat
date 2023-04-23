<template>
  <div class="content col-9">
    <!-- Hello World {{ id }} -->
    <div class="chat">
      <div class="chat-header">
        <div class="chat-header-user">
          <figure class="avatar avatar-state-success">
            <img src="https://i.pinimg.com/736x/80/17/86/80178693d1d0c7e0ec688707b02ecc0b.jpg" class="rounded-circle"
              alt="avatar">
          </figure>
          <div>
            <h5>Townsend Seary</h5>
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
            <div v-for="(message, index) in messages" :key="index" class="message-item" :class="message.type">
              <div class="message-content">{{ message.content }}</div>
              <div class="message-action">{{ message.time }}
                <!-- <i v-if="message.type === 'outgoing-message'" class="ti-double-check text-info"></i> -->
              </div>
            </div>
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
  </div>
</template>

<script>
import io from 'socket.io-client'


export default {
  props: {
    id: {
      type: Number,
      required: true
    }
  },
  data(){
    return {
      messages: [
        { content: 'What are you doing this?', time: '01:20 PM', type: 'incoming-message' },
        { content: 'What are you doing this?', time: '01:20 PM', type: 'incoming-message' },
        { content: 'What are you doing this?', time: '01:20 PM', type: 'incoming-message' },
        { content: 'What are you doing this?', time: '01:20 PM', type: 'incoming-message' },
        { content: 'What are you doing this?', time: '01:20 PM', type: 'incoming-message' },
        { content: 'What are you doing this?', time: '01:20 PM', type: 'incoming-message' },
        { content: 'What are you doing this?', time: '01:20 PM', type: 'incoming-message' },
        { content: 'What are you doing this?', time: '01:20 PM', type: 'incoming-message' },
        { content: 'What are you doing this?', time: '01:20 PM', type: 'incoming-message' },
      ],
      newMessage: '',
    }
  },
  mounted() {
    this.socket = io(`chats/${this.id}/ws`)

    this.socket.on('connect', () => {
      console.log('Connected to server')
    })

    this.socket.on('message', (data) => {
      console.log('Received message:', data)
      this.addMessage(data)
    })
  },
  methods: {
    async sendMessage() {
      if (this.newMessage.trim() !== '') {
        const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
        this.messages.push({ content: this.newMessage, time: time, type: 'outgoing-message' })
        this.newMessage = ''
        
        await this.$nextTick()
        this.scrollDown()
      }
    },
    scrollDown() {
      const messagesContainer = this.$refs.messages.$el
      messagesContainer.scrollTop = messagesContainer.scrollHeight
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

.chat .chat-body .messages .message-item:last-child {
    margin-bottom: 0;
}

.chat .chat-body .messages .message-item {
    max-width: 75%;
    /* margin-bottom: 20px; */
}

.chat .chat-body .messages .message-item .message-content {
    background: #fff;
    border-radius: 5px;
    padding: 10px 20px;
}
.chat .chat-body .messages .message-item .message-action {
    color: #828282;
    margin-top: 5px;
    font-style: italic;
    font-size: 12px;
}

.chat .chat-body .messages .message-item.outgoing-message {
    margin-left: auto;
}

.chat .chat-body .messages .message-item.outgoing-message .message-content {
    background-color: #cdcdcd;
}

</style>
