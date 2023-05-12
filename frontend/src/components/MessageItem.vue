<template>
    <div class="message" :class="messageType" v-if="isDirect">
        <div class="message-item" :class="messageType">
            <div class="message-content">{{ message.message }}</div>
            <div class="message-action">{{ message.time }}</div>
            <!-- <i v-if="message.type === 'outgoing-message'" class="ti-double-check text-info"></i> -->
        </div>
    </div>
    <div class="message" :class="messageType" v-else>
        <div class="message-header-user">
            <figure class="avatar avatar-state-success">
              <img :src="message.user.photo" class="rounded-circle"
                alt="avatar">
            </figure>
            <!-- <div>
              <h5>{{ chat.title }}</h5>
              <small class="text-muted"><i>Online</i></small>
            </div> -->
        </div>
        <div class="message-item" :class="messageType">
            <h9>{{ message.user.username }}</h9>
            <div class="message-content">
                {{ message.message }}
            </div>
            <div class="message-action">{{ message.time }}</div>
            <!-- <i v-if="message.type === 'outgoing-message'" class="ti-double-check text-info"></i> -->
        </div>
    </div>
</template>

<script>
export default{
    props: {
        message: {
            type: Object,
            default: () => {}
        },
        isDirect: {
            type: Boolean,
            default: () => true
        }
    },
    data(){
        return {}
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
.message:last-child {
    margin-bottom: 0;
}

.message {
    max-width: 75%;
    display: flex;
    /* margin-bottom: 20px; */
}

.message-item .message-content {
    background: #fff;
    border-radius: 5px;
    padding: 10px 20px;
}
.messages .message-item .message-action {
    color: #828282;
    margin-top: 5px;
    font-style: italic;
    font-size: 12px;
}

.messages .message.outgoing-message {
    margin-left: auto;
}

.messages .message.outgoing-message .message-header-user {
    display: none;
}
.messages .message.outgoing-message h9 {
    display: none;
}


.messages .message .outgoing-message .message-content {
    background-color: #cdcdcd;
}

.message-header-user {
  display: flex;
  align-items: center;
}
</style>
