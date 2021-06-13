import colors from 'vuetify/es5/util/colors'

export default {
  ssr: false,

  head: {
    titleTemplate: '%s - client',
    title: 'client',
    htmlAttrs: {
      lang: 'en',
    },
    meta: [
      { charset: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { hid: 'description', name: 'description', content: '' },
    ],
    link: [{ rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' }],
  },

  css: [
    '~/assets/animations/appear.scss',
    '~/assets/animations/slide-right.scss',
    '~/assets/animations/flip.scss',
  ],

  plugins: [],

  components: true,

  buildModules: ['@nuxtjs/eslint-module', '@nuxtjs/vuetify', '@nuxtjs/moment'],

  modules: ['@nuxtjs/axios', 'nuxt-socket-io'],

  axios: {},

  io: {
    sockets: [
      {
        name: 'main',
        url: 'http://localhost:8000',
        vuex: {
          mutations: [
            'connect --> socket/RESET_ERROR',
            'connect_error --> socket/NO_CONNECTION',
            'disconnect --> socket/NO_CONNECTION',
            'error --> socket/SET_ERROR',
            'logged_in --> app/LOGGED_IN',
            'logged_out --> app/LOGGED_OUT',
            'users --> app/USERS',
            'user_online --> app/USER_ONLINE',
            'user_offline --> app/USER_OFFLINE',
            'chat_created --> app/CHAT_CREATED',
            'chat_renamed --> app/CHAT_RENAMED',
            'chat_deleted --> app/CHAT_DELETED',
            'message_sent --> app/MESSAGE_SENT',
          ],
        },
        namespaces: {},
      },
    ],
  },

  vuetify: {
    customVariables: ['~/assets/variables.scss'],
    theme: {
      dark: true,
      themes: {
        dark: {
          primary: colors.blue.darken2,
          accent: colors.grey.darken3,
          secondary: colors.amber.darken3,
          info: colors.teal.lighten1,
          warning: colors.amber.base,
          error: colors.deepOrange.accent4,
          success: colors.green.accent3,
        },
      },
    },
  },

  build: {},
}
