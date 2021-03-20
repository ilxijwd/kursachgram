<template>
  <div></div>
</template>

<script>
export default {
  mounted() {
    this.socket = this.$nuxtSocket({ persist: true })
  },
}
</script>
