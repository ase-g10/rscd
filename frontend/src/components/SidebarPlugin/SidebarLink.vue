<template>
  <component
    v-bind="$attrs"
    :is="tag"
    @click="hideSidebar"
    class="nav-item"
    tag="li"
  >
    <a class="nav-link">
      <slot>
        <i v-if="icon" :class="icon"></i>
        <p>{{ name }}</p>
      </slot>
    </a>
  </component>
</template>

<script>
function inheriltClassAndStyle() {
  const attrs = this.$attrs
  attrs.class && this.$el.classList.add(attrs.class)
  attrs.style &&
    Object.entries(attrs.style).forEach(([k, v]) => {
      this.$el.style[k] = v
    })
}
export default {
  name: 'sidebar-link',
  inheritAttrs: false,
  inject: {
    autoClose: {
      default: true,
    },
    addLink: {
      default: () => {},
    },
    removeLink: {
      default: () => {},
    },
  },
  props: {
    name: String,
    icon: String,
    tag: {
      type: String,
      default: 'router-link',
    },
  },
  methods: {
    hideSidebar() {
      if (this.autoClose) {
        this.$sidebar.displaySidebar(false)
      }
    },
    isActive() {
      return this.$el.classList.contains('active')
    },
  },
  beforeUnmount() {
    if (this.$el && this.$el.parentNode) {
      this.$el.parentNode.removeChild(this.$el)
    }
    if (this.removeLink) {
      this.removeLink(this)
    }
  },
  mounted() {
    if (this.addLink) {
      this.addLink(this)
    }
    inheriltClassAndStyle.call(this)
  },
}
</script>
