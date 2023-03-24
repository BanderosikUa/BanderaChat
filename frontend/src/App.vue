<template>
  <NavbarItem v-if="!$route.meta.hideNavbar"></NavbarItem>
  <div class="main">
    <router-view/>
  </div>
</template>

<style>
#app{
  display: flex;
}

.main{
  width: 100%;
}

*{
  box-sizing: border-box;
  font-family: 'Poppins', sans-serif;
}
/* 
.main.container{
  padding: 30px;
  display: flex;

} */

body{
  background: rgb(229, 229, 229);
}
</style>

<script>
import NavbarItem from '@/components/NavbarItem.vue'

export default {
  components: {
    NavbarItem
  }
}
</script>
