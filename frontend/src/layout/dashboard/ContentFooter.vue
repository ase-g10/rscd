<template>
  <footer class="footer">
    <div class="container-fluid d-flex flex-wrap justify-content-between">
      <nav>
        <ul>
          <li>
            <router-link :to="{ path: '/maps' }">Dashboard</router-link>
          </li>
        </ul>
      </nav>
      <div class="copyright d-flex flex-wrap">
        &copy; Coded with
        <i class="fa fa-heart heart"></i> by
        <a href="https://github.com/ase-g10/rscd" target="_blank">
          &nbsp; Group 10.</a
        >&nbsp; Designed by
        <a href="https://github.com/ase-g10/rscd" target="_blank"
          >&nbsp; Group 10.</a
        >&nbsp; Check out the
        <a href="https://upup.iocky.com/s/rscd/" target="_blank"
          >&nbsp; Service Status.</a
        >
      </div>
    </div>
  </footer>
</template>

<script>
export default {};
</script>
