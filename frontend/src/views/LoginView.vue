<template>
    <div class="login-container">
        <div class="wrapper">
            <div class="form-box login">
                <h2>Login</h2>
                <form @submit.prevent="handleLogin">
                    <div class="input-box">
                        <span class="icon"><i class='bx bxs-envelope'></i></span>
                        <input type="email" name="email" v-model="email" required>
                        <label>Email</label>
                    </div>
                    <div class="input-box">
                        <span class="icon"><i class='bx bxs-lock-alt' ></i></span>
                        <input type="password" name="password" v-model="password" required>
                        <label>Password</label>
                    </div>
                    <div class="remember-forgot">
                        <label for="">
                            <input type="checkbox" >Remember me
                        </label>
                        <a href="#">Forgot password?</a>
                    </div>
                    <button type="submit" class="btn">Login</button>
                    <div class="login-register" @click="makeActive">
                        <p>Don't have an account?
                        <a href="#" class="register-link">Register</a>
                        </p>
                    </div>
                </form>
            </div>
            <div class="form-box register">
                <h2>Registration</h2>
                <form @submit.prevent="handleRegister">
                    <div class="input-box">
                        <span class="icon"><i class='bx bxs-envelope'></i></span>
                        <input type="email" name="email" v-model="email" required>
                        <label>Email</label>
                    </div>
                    <div class="input-box">
                        <span class="icon"><i class='bx bxs-user'></i></span>
                        <input type="text" name="username" v-model="username" required>
                        <label>Username</label>
                    </div>
                    <div class="input-box">
                        <span class="icon"><i class='bx bxs-lock-alt' ></i></span>
                        <input type="password" name="password" v-model="password" required>
                        <label>Password</label>
                    </div>
                    <div class="input-box">
                        <span class="icon"><i class='bx bxs-lock-alt'></i></span>
                        <input type="password" v-model="passwordConfirm" required>
                        <label>Password Confirmation</label>
                    </div>
                    <div class="remember-forgot">
                        <label for="">
                            <input type="checkbox" >I agree to the term and conditions
                        </label>
                        <!-- <a href="#">Forgot password?</a> -->
                    </div>
                    <button type="submit" class="btn">Register</button>
                    <div class="login-register" >
                        <p>Already have an account?
                        <a href="#" class="login-link" @click="removeActive">Login</a>
                        </p>
                    </div>
                </form>
            </div> 
        </div>
    </div>
</template>

<style scoped>
.login-container{
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    background-image: url("../assets/background.jpg");
    background-size: cover;
    background-position: center;
}
.sidebar{
    display: none;
}
.wrapper{
    position: relative;
    width: 400px;
    height: 440px;
    background: transparent;
    border: 2px solid rgba(255, 255, 255, .5);
    border-radius: 20px;
    backdrop-filter: blur(20px);
    box-shadow: 0 0 30px rgba(0, 0, 0, .5);
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    transition: height .2s ease;
}


.wrapper.active{
    height: 600px;
}

.wrapper .form-box.login{
    transition: transform .18s ease;
    transform: translateX(0);

}
.wrapper.active .form-box.login{
    transition: none;
    transform: translateX(-400px);
}

.wrapper .form-box.register{
    position: absolute;
    transition: none;
    transform: translateX(400px);

}
.wrapper.active .form-box.register{
    transition: transform .18s ease;
    transform: translateX(0);
}
.wrapper .form-box{
    width: 100%;
    padding: 40px;
}

.form-box h2{
    font-size: 2em;
    text-align: center;
}

.input-box{
    position: relative;
    width: 100%;
    height: 50px;
    border-bottom: 2px solid #162938;
    margin: 30px 0;
}

.input-box label{
    position: absolute;
    top: 50%;
    left: 5px;
    transform: translateY(-50%);
    font-size: 1em;
    color: #162938;
    font-weight: 500;
    pointer-events: none;
    transition: .5s;
}

.input-box input:focus~label,
.input-box input:valid~label{
    top: -5px;
}


.input-box input{
    width: 100%;
    height: 100%;
    background: transparent;
    border: none;
    outline: none;
    font-size: 1em;
    color: #162938;
}

.input-box .icon{
    position: absolute;
    right: 8px;
    font-size: 1.2em;
    color: #162938;
    line-height: 57px;
}

.remember-forgot{
    font-size: .9em;
    color: #162938;
    font-weight: 500;
    margin: -15px 0 15px;
    display: flex;
    justify-content: space-between;
}

.remember-forgot label input{
    accent-color: #162938;
    margin-right: 3px;
}

.remember-forgot a{
    color: #162938;
    text-decoration: none;

}

.remember-forgot a:hover{
    text-decoration: underline;
}

.btn{
    width: 100%;
    height: 45px;
    background: #162938;
    border: none;
    outline: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 1em;
    color: #ffff;
    font-weight: 500;
}

.login-register{
    font-size: .9em;
    color: #162938;
    text-align: center;
    font-weight: 500;
    margin: 25px 0 10px;
}

</style>

<script>
import axios from 'axios'

export default{
    methods: {
        makeActive() {
            const wrapper = document.querySelector('.wrapper')
            wrapper.classList.add('active')
        },
        removeActive() {
            const wrapper = document.querySelector('.wrapper')
            wrapper.classList.remove('active')
        },
        async handleRegister(){
            const data = {
                email: this.email,
                username: this.username,
                password: this.password,
                passwordConfirm: this.passwordConfirm,
            }
            await axios.post('auth/register', data).then(response => {
                if (response.data.status === "success"){
                    const wrapper = document.querySelector('.wrapper')
                    wrapper.classList.remove('active')
                }
            }).catch(e =>{
                console.log(e)
                alert(JSON.stringify(e.response.data.detail, null, 2))

            })
        },
        async handleLogin(){
            const data = {
                email: this.email,
                password: this.password,
            }
            await axios.post('auth/login', data).then(response => {
                console.log(response.data)
                if (response.data.status === "success"){
                    localStorage.setItem('access_token', response.data.access_token)
                    axios.defaults.headers.common['Authorization'] = 'Bearer ' + localStorage.getItem('access_token');
                    this.$router.push('/home')
                }
            }).catch(e =>{
                console.log(e)
                alert(JSON.stringify(e.response.data.detail, null, 2))

            })
        }
    }
}
</script>
