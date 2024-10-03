<template>
    <div>
        <h3>Hi {{ user.username }}</h3>
    </div>
</template>

<script>
import axios from 'axios'

export default{
    data(){
        return {
            user: null
        }
    },
    async created(){
        try{
            const response = await axios.get('users/me')

        this.user = response.data.user
        } catch(e){
            console.log(e)
        }
    }
}

</script>
