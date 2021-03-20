<template>
  <v-app dark>
    <v-app-bar app fixed>
      <v-app-bar-nav-icon />
      <v-tabs color="white" centered>
        <v-tabs-slider color="white" />
        <v-tab @click.stop="$router.push('/chats')">
          <v-badge dot :value="messages"> Чаты </v-badge>
        </v-tab>
        <v-tab @click.stop="$router.push('/calls')">
          <v-badge dot :value="calls"> Звонки </v-badge>
        </v-tab>
      </v-tabs>
      <v-btn icon>
        <v-icon>mdi-magnify</v-icon>
      </v-btn>
    </v-app-bar>
    <v-main>
      <v-container>
        <transition name="slide-right">
          <nuxt />
        </transition>
      </v-container>
    </v-main>
    <v-footer app fixed class="flex justify-center">
      <v-speed-dial
        v-model="fab"
        absolute
        bottom
        right
        transition="slide-y-reverse-transition"
      >
        <template #activator>
          <v-btn v-model="fab" color="blue darken-2" dark fab>
            <v-icon v-if="fab"> mdi-close </v-icon>
            <v-icon v-else> mdi-plus </v-icon>
          </v-btn>
        </template>
        <v-btn fab dark small color="red">
          <v-icon>mdi-delete</v-icon>
        </v-btn>
        <v-btn fab dark small color="indigo">
          <v-icon>mdi-account-group</v-icon>
        </v-btn>
      </v-speed-dial>
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      messages: 1,
      calls: 0,
      fab: false,
    }
  },
}
</script>

<style lang="scss">
.slide-right-enter-active,
.slide-right-leave-active {
  transition-duration: 0.5s;
  transition-property: height, opacity, transform;
  transition-timing-function: cubic-bezier(0.55, 0, 0.1, 1);
  overflow: hidden;
}

.slide-right-leave-active {
  opacity: 0;
  transform: translate(100px, 0);
}

.slide-right-enter {
  opacity: 0;
  transform: translate(-100px, 0);
}
</style>
