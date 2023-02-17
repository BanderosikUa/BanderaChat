<template>
    <nav class="sidebar">
        <header>
            <div class="image-text">
                <span class="image">
                    <img src="../assets/logo.png">
                </span>
            </div>
        </header>
        <ul class="menu-links">
            <!-- <li class="nav-link">
                <a href="Chats">
                    <i class='bx bx-chat icon'></i>
                </a>
            </li> -->
            <li class="nav-link">
                <router-link to="Chats">
                    <i class='bx bx-chat icon'></i>
                </router-link>
            </li>
            <li class="nav-link">
                <a href="Friends">
                    <i class='bx bx-user icon'></i>
                </a>
            </li>
            <li class="nav-link">
                <a href="Favorites">
                    <i class='bx bx-star icon'></i>
                </a>
            </li>
            <li class="nav-link brackets">
                <a href="#">
                    <i class='bx bx-pencil icon'></i>
                </a>
            </li>
            <li class="nav-link">
                <a href="#">
                    <i class='bx bx-cog icon'></i>
                </a>
            </li>
            <li class="nav-link">
                <a href="#">
                    <i class='bx bx-power-off icon'></i>
                </a>
            </li>
            

        </ul>
    </nav>
</template>

<style scoped>

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
*{
    font-family: 'Poppins', sans-serif;
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}
body{
    height: 100vh;

}
.sidebar{
    text-align: center;
    top: 0;
    left: 0;
    height: 100vh;
    width: 70px;
    background: rgb(255, 255, 255);
}

.sidebar .image-text img{
    padding-top: 10px;
    padding-bottom: 10px;
    width: 40px;
    border-radius: 6px;
    border-width: 2px;
}

.sidebar .image-text{
    background: green;
}

.menu-links{
    height: calc(var(--vh, 1vh)*90);
    display: flex;
    flex-direction: column;
    padding: 0;
    margin: 0;
}
.sidebar li{
    padding: 10px;
    height: 50px;
    margin-top: 10px;
    list-style: none;
}
.sidebar li .icon{
    font-size: 25px;
}

.sidebar li a{
    height: 100%;
    width: 100%;
    padding: 11px 0;
}

.sidebar li.brackets{
    margin-top: auto;
}
</style>
