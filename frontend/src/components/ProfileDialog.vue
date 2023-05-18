<template>
    <v-dialog v-model="dialog" max-width="500">
        <v-card>
            <header>
                <v-card-title><v-icon class='bx bx-pencil'></v-icon>Profile</v-card-title>
            </header>
            <v-card-text>
                <v-form ref="form">
                    <v-text-field v-model="username" label="Username" :rules="rules"></v-text-field>
                    <v-text-field v-model="email" label="Email" :rules="rules"></v-text-field>


                    <v-file-input prepend-icon="" accept="image/png, image/jpeg, image/png" placeholder="Pick a photo"
                        label="Photo" v-model="photo">
                        <template #prepend-inner>
                            <figure class="avatar avatar-state-success">
                                <img :src="user.photo" class="rounded-circle" alt="avatar">
                            </figure>
                        </template>

                    </v-file-input>
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
            user: null,
            username: '',
            photo: null,
            email: "",

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

            const data = { username: this.username, email: this.email }
            await axios.patch('auth/me', data).then(async response => {
                console.log(response.data)
                if (response.data.status === true) {
                    this.user = response.data.user
                }
            }).catch(e => {
                console.log(e)
                alert(JSON.stringify(e.response.data.detail, null, 2))
            })

            if (this.photo !== null) {
                const formData = new FormData();
                formData.append('photo', this.photo[0]);
                await axios.post(`auth/me/upload`, formData).then(response => {
                    console.log(response.data)
                    this.user = response.data.user
                }).catch(e => {
                    console.log(e)
                    alert(JSON.stringify(e.response.data.detail, null, 2))
                })

            }

            this.$emit("create", this.user)
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
        await axios.get('auth/me').then(response => {
            console.log(response.data)
            if (response.data.status === true) {
                this.user = response.data.user
                this.username = this.user.username
                this.email = this.user.email
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
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 0;
    height: 2.5rem;
    width: 2.5rem;
    border-radius: 50%;
    margin-right: 1rem;
}

.v-field__prepend-inner {
    align-items: center;
    display: flex;
    justify-content: center;
    height: 100%;
    /* padding-top: var(--v-input-padding-top, 10px); */
}
</style>
  