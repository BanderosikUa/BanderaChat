<template>
    <div class="message-item" :class="messageType">
        <div class="message-content">{{ message.message }}</div>
        <div class="message-action">{{ message.time }}</div>
        <!-- <i v-if="message.type === 'outgoing-message'" class="ti-double-check text-info"></i> -->
    </div>
</template>

<script>
export default{
    props: {
        message: {
            type: Object,
            default: () => {}
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
