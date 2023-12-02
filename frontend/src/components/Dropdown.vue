<template>
  <component
    :is="tag"
    class="dropdown"
    :class="{ show: isOpen }"
    @click="toggleDropDown"
    v-click-outside="closeDropDown"
  >
    <a
      class="dropdown-toggle btn-rotate"
      :class="titleClasses"
      data-toggle="dropdown"
    >
      <slot name="title">
        <i :class="icon"></i>
        <span class="notification"
          >{{ title }}
          <b class="caret"></b>
        </span>
      </slot>
    </a>
    <ul class="dropdown-menu" :class="{ show: isOpen }">
      <slot></slot>
    </ul>
  </component>
</template>

<script>
import { $on, $off, $once, $emit } from '../utils/gogocodeTransfer'
export default {
  props: {
    tag: {
      type: String,
      default: 'li',
    },
    title: String,
    icon: String,
    titleClasses: [String, Object, Array],
  },
  data() {
    return {
      isOpen: false,
    }
  },
  methods: {
    toggleDropDown() {
      this.isOpen = !this.isOpen
      $emit(this, 'change', this.isOpen)
    },
    closeDropDown() {
      this.isOpen = false
      $emit(this, 'change', false)
    },
  },
  emits: ['change'],
}
</script>
