<template>
  <div class="sidebar-group chats container">
    <div class="row sidebar-row">
      <ChatSidebar @chat-selected="selectedChat = $event"></ChatSidebar>
      <ChatItem v-if="selectedChat" :id="selectedChat"></ChatItem>
    </div>
  </div>
</template>

<script>
// import axios from 'axios'
// import PerfectScrollbar from 'vue3-perfect-scrollbar'
import ChatSidebar from '@/components/ChatSidebar.vue'
import ChatItem from '@/components/ChatItem.vue';

export default {
  components: {
    ChatSidebar,
    ChatItem
  },
  data() {
    return {
      selectedChat: null
    }
  },
  mounted() {
    // Retrieve the selected ID from local storage and set it as the selectedId
    const selectedChat = localStorage.getItem('selectedChat');
    console.log(selectedChat)
    if (selectedChat) {
      this.selectedChat = parseInt(selectedChat);
    }
  },
  watch: {
    // Watch the selectedId property and store it in local storage when it changes
    selectedChat(newId) {
      localStorage.setItem('selectedChat', newId.toString());
    }
  }
}
</script>

<style>


.container{
    margin-left: 20px;
}

.sidebar-row {
  padding-top: 20px;
}

figure.avatar>img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.rounded-circle {
    border-radius: 50% !important;
}

img {
    vertical-align: middle;
}

figure.avatar {
    display: inline-block;
    margin-bottom: 0;
    height: 2.5rem;
    width: 2.5rem;
    border-radius: 50%;
    margin-right: 1rem;
}

</style>
