<template>
  <NavbarItem></NavbarItem>
  <div class="main container">
    <router-view/>
  </div>
</template>

<style>
#app{
  display: flex;
}

*{
  box-sizing: border-box;
}

.main.container{
  padding: 30px;
  display: flex;

}

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
