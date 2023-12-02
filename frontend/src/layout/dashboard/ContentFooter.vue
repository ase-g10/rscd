<template>
  <footer class="footer">
    <div class="container-fluid d-flex flex-wrap justify-content-between">
      <nav>
        <ul>
          <li>
            <router-link :to="{ path: '/admin' }">Dashboard</router-link>
          </li>
        </ul>
      </nav>
      <div class="copyright d-flex flex-wrap">
        &copy; Coded with
        <i class="fa fa-heart heart"></i> by
        <a
          href="https://github.com/Group10-ResponseSystemToCityDisaster"
          target="_blank"
        >
          &nbsp; Group 10.</a
        >&nbsp; Designed by
        <a
          href="https://github.com/Group10-ResponseSystemToCityDisaster"
          target="_blank"
          >&nbsp; Group 10.</a
        >
      </div>
    </div>
  </footer>
</template>

<script>
export default {}
</script>
