<template>
  <div class="sidebar-group chats container">
    <div class="row">
      <div class="sidebar active col-3">
        <header>
          <span>Chats</span>
          <ul class="list-inline">
            <li class="list-inline-item">
              <div>
                <button class="btn btn-light" id="Tooltip-Add-Group">
                  <i class='bx bxs-group'></i>
                </button>
              </div>
            </li>
            <li class="list-inline-item"><button class="btn btn-light" id="Tooltip-New-Chat"><i
                  class="bx bxs-chat"></i></button></li>
          </ul>
        </header>
        <form></form>
        <div class="sidebar-body "></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.sidebar {
  background: #fff;
  border-radius: 5px;
  margin-right: 30px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
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
.sidebar>header ul{
  margin-top: revert;
}
</style>
