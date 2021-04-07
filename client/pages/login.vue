<template>
  <v-row justify="center" align="center">
    <v-col cols="12" sm="12" md="10" lg="8" xl="4">
      <v-card :loading="loading">
        <v-card-title>Login</v-card-title>
        <v-card-subtitle>
          Not registered?
          <nuxt-link to="/register">Click here to register</nuxt-link>
        </v-card-subtitle>
        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-text-field
              v-model="email"
              type="email"
              label="Email"
              :counter="50"
              :rules="emailRules"
              :loading="loading"
              required
            />
            <v-text-field
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              label="Password"
              :rules="passwordRules"
              :loading="loading"
              required
            >
              <template #append-outer>
                <v-btn icon @click.stop="showPassword = !showPassword">
                  <v-icon v-if="showPassword">mdi-eye-off</v-icon>
                  <v-icon v-else>mdi-eye</v-icon>
                </v-btn>
              </template>
            </v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="blue darken-2" :loading="loading" @click.stop="submit">
            Submit
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
  </v-row>
</template>

<script>
export default {
  layout: 'non-authorized',
  middleware({ store, redirect }) {
    if (store.state.auth.token) return redirect('/chats')
  },
  data() {
    const required = (field) => (v) => !!v || `${field} is required`
    const less = (field, length) => (v) =>
      v?.length <= length ||
      `${field} must be less than ${length} characters long`
    const more = (field, length) => (v) =>
      v?.length >= length ||
      `${field} must be more than ${length} characters long`

    return {
      valid: true,
      loading: false,
      socket: null,
      email: '',
      emailRules: [
        required('Email'),
        less('Email', 50),
        (v) => /.+@.+\..+/.test(v) || 'Invalid email',
      ],
      password: '',
      showPassword: false,
      passwordRules: [
        required('Password'),
        less('Password', 50),
        more('Password', 6),
      ],
    }
  },
  mounted() {
    this.socket = this.$nuxtSocket({})
  },
  methods: {
    submit() {
      if (!this.$refs.form.validate()) return
      this.loading = true
      const { email, password } = this
      this.socket.emit('login', { email, password }, (res) => {
        this.loading = false
        if (res.success) {
          this.$store.commit('auth/SET_TOKEN', res.token)
          this.$store.commit('auth/SET_ACCOUNT_DATA', res.account_data)
          this.$router.push('/chats')
        } else this.$store.commit('auth/SET_REQUEST_ERROR', res.error)
      })
    },
  },
}
</script>
