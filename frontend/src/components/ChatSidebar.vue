<template>
    <div class="sidebar active col-3">
        <header>
            <span>Chats</span>
            <ul class="list-inline">
                <li class="list-inline-item">
                    <div>
                        <button @click="createChatGroup" class="btn btn-light" id="Tooltip-Add-Group">
                            <i class='bx bxs-group'></i>
                        </button>
                        <chat-create-popup ref="chatCreatePopup" @create="addChat"></chat-create-popup>
                        <!-- <v-select :options="userList" label="name"></v-select> -->
                        <!-- <chat-create-popup ></chat-create-popup> -->
                    </div>
                </li>
                <li class="list-inline-item">
                    <button class="btn btn-light" id="Tooltip-New-Chat">
                        <i class="bx bxs-chat"></i>
                    </button>
                </li>
            </ul>
        </header>
        <form>
            <input type="text" class="form-control" placeholder="Search chat">
        </form>
        <div class="sidebar-body">
            <perfect-scrollbar class="scrollbar-container" :settings="scrollbarSettings">
                <ul class="list-group list-group-flash">
                    <li v-for="chat in chats" :key="chat.id" @click="selectChat(chat.id)" class="list-group-item open-chat">
                        <figure class="avatar avatar-state-success">
                            <!-- <img 
                                src="https://i.pinimg.com/736x/80/17/86/80178693d1d0c7e0ec688707b02ecc0b.jpg"
                                class="rounded-circle" alt="avatar"> -->
                            <img :src="getImageUrl(chat.photo)" class="rounded-circle" alt="avatar">
                        </figure>
                        <div class="users-list-body">
                            <h5>{{ chat.title }}</h5>
                            <p>What's up, how are you?</p>
                            <div class="users-list-action action-toggle">
                                <div class="new-message-count">3</div>
                                <div class="dropdown"><a aria-haspopup="true" class="" aria-expanded="false"><i
                                            class="ti ti-more"></i></a>
                                    <div tabindex="-1" role="menu" aria-hidden="true" class="dropdown-menu"><button
                                            type="button" tabindex="0" role="menuitem"
                                            class="dropdown-item">Profile</button><button type="button" tabindex="0"
                                            role="menuitem" class="dropdown-item">Delete</button></div>
                                </div>
                            </div>
                        </div>

                    </li>
                </ul>
            </perfect-scrollbar>
        </div>
    </div>


    <RouterView class="router-view" v-slot="{ Component }">
        <Transition>
            <component :is="Component"></component>
        </Transition>
    </RouterView>
</template>
  
<script>
import axios from 'axios'
import ChatCreatePopup from './ChatCreatePopup.vue'
import ProfileDialog from './ProfileDialog.vue'
// import Swal from 'sweetalert2';
import vSelect from 'vue-select'
import { getImageUrl } from "./utils"

export default {
    components:{
        ChatCreatePopup,
        vSelect,
        ProfileDialog
    },
    data() {
        return {
            chats: [],
        }
    },
    async created() {
        try {
            const response = await axios.get('chats?limit=100')

            console.log(response)

            this.chats = response.data.chats
        } catch (e) {
            console.log(e)
        }
    },
    methods: {
        getImageUrl,
        selectChat(chat) {
            console.log(chat)
            this.$router.push({ name: 'chat-detail', params: { id: chat } });
        },
        createChatGroup() {
            this.$refs.chatCreatePopup.openDialog();
        },
        addChat(chat) {
            console.log(chat)
            this.chats.push(chat)
        }
    },
}

</script>
  
<style scoped>
.sidebar {
    background: #fff;
    border-radius: 5px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    height: 95vh;
}

.scrollbar-container {
    position: relative;
    height: 100%;
}
.sidebar>header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 80px;
    font-weight: 700;
    border-radius: 0;
    font-size: larger;
}

.sidebar>form input[type=text] {
    border-radius: 5px;
    border: none;
    height: auto;
    padding: 10px 15px;
    background-color: #ebebeb;
}

.sidebar-group .sidebar>form {
    padding: 10px 20px;
    margin-bottom: 1rem;
}

.sidebar>header ul {
    margin-top: revert;
}

.list-group-flush {
    border-radius: 0;
}

.list-group {
    display: flex;
    flex-direction: column;
    padding-left: 0;
    margin-bottom: 0;
    border-radius: 0.25rem;
}

ul {
    margin-top: 0;
}

.sidebar-body{
    height: 75vh;
}

/* .ps {
    height: 95vh;
} */


.sidebar-group .sidebar .list-group-item {
    padding: 20px;
    display: flex;
    cursor: pointer;
}

.sidebar-group .sidebar .list-group-item .users-list-body {
    flex: 1 1;
    position: relative;
    min-width: 0;
    display: flex;
    flex-direction: column;
}

.sidebar-group .sidebar .list-group-item .users-list-body h5 {
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden;
    font-size: 16px;
    font-weight: 600;
    margin-bottom: 0.2rem;
    line-height: 1;
}

.sidebar-group .sidebar .list-group-item .users-list-body p {
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden;
    margin-bottom: 0;
    color: #969696;
}

.sidebar-group .sidebar .list-group-item .users-list-body .users-list-action {
    position: absolute;
    right: 0;
    top: 0;
    background: #fff;
    box-shadow: -8px 1px 10px 5px #fff;
    bottom: 0;
    padding: 0 5px;
}

.sidebar-group .sidebar .list-group-item .users-list-body .users-list-action .new-message-count {
    width: 23px;
    display: flex;
    align-items: center;
    justify-content: center;
    line-height: 0;
    font-size: 13px;
    height: 23px;
    background-color: #3db16b;
    color: #fff;
    border-radius: 50%;
}
</style>
  