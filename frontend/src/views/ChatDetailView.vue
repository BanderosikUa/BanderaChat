<template>
        <!-- <ChatSidebar></ChatSidebar> -->
        <ChatItem :key="selectedChat"></ChatItem>
</template>
  
<script>

// import ChatSidebar from '@/components/ChatSidebar.vue'
import ChatItem from '@/components/ChatItem.vue';

export default {
    components: {
        // ChatSidebar,
        ChatItem
    },
    data() {
        return {
            selectedChat: null
        }
    },
    created(){
        console.log(this.$route.params.id)
        this.selectedChat = this.$route.params.id
    },

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
  