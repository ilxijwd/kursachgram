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

  buildModules: ['@nuxtjs/eslint-module', '@nuxtjs/vuetify'],

  modules: [
    '@nuxtjs/axios',
    'nuxt-socket-io',
    [
      'nuxt-vuex-localstorage',
      {
        localStorage: ['auth'],
      },
    ],
  ],

  axios: {},

  io: {
    sockets: [
      {
        url: 'http://localhost:8000',
        vuex: {
          mutations: [
            'connect --> socket/CONNECTED',
            'connect_error --> socket/NO_CONNECTION',
            'disconnect --> socket/NO_CONNECTION',
            'invalid_token --> socket/INVALID_TOKEN',
            'not_registered --> socket/NOT_REGISTERED',
            'users --> chats/SET_USERS',
            'user_online --> chats/SET_USER_ONLINE',
            'user_offline --> chats/SET_USER_OFFLINE',
            'chat_created --> chats/CREATE_CHAT',
            'chat_renamed --> chats/RENAME_CHAT',
            'chat_deleted --> chats/DELETE_CHAT',
            'message_sent --> chats/RECEIVE_MESSAGE',
            'message_deleted --> chats/DELETE_MESSAGE',
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
