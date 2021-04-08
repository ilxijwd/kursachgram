<template>
  <v-row justify="center" align="center">
    <v-col cols="12" sm="6">
      <v-card :loading="loading">
        <v-card-title>Register</v-card-title>
        <v-card-subtitle>
          Already registered?
          <nuxt-link to="/login">Click here to log in</nuxt-link>
        </v-card-subtitle>
        <v-card-text>
          <v-container>
            <v-row>
              <v-btn @click.stop="DEBUGCreateAccount('ilxijwd')">
                ilxijwd
              </v-btn>
              <v-spacer />
              <v-btn @click.stop="DEBUGCreateAccount('iluxan')"> iluxan </v-btn>
            </v-row>
            <v-row justify="center">
              <transition name="appear">
                <v-avatar v-if="avatarBase64" size="128">
                  <img :src="avatarBase64" alt="" />
                </v-avatar>
              </transition>
            </v-row>
          </v-container>
          <v-form ref="form" v-model="valid">
            <v-file-input
              ref="avatarInput"
              v-model="avatar"
              :rules="avatarRules"
              prepend-icon=""
              truncate-length="15"
              show-size
              accept="image/png, image/jpeg, image/jpg"
              placeholder="Pick an avatar"
              label="Avatar"
              @change="fileOnChangeEvent"
            >
              <template v-if="!avatar" #append-outer>
                <v-icon>mdi-camera</v-icon>
              </template>
            </v-file-input>
            <v-text-field
              v-model="username"
              type="text"
              label="Username"
              :counter="20"
              :rules="usernameRules"
              :loading="loading"
              required
            />
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
              </template></v-text-field
            >
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
      registrationError: '',
      avatar: null,
      avatarBase64: '',
      avatarRules: [
        required('Avatar'),
        (v) => v?.size < 1000000 || 'Avatar size should be less than 1 MB',
      ],
      username: '',
      usernameRules: [required('Username'), less('Username', 20)],
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
    this.unsubscribe = this.$store.subscribe((mutation) => {
      if (mutation.type === 'auth/SET_LOGIN_DATA') {
        this.loading = false
        this.$router.push('/chats')
      }
    })
  },
  beforeDestroy() {
    this.unsubscribe()
  },
  methods: {
    DEBUGCreateAccount(nickname) {
      this.username = nickname
      this.email =
        nickname === 'iluxan' ? 'syaivo01@gmail.com' : 'ilxijwd@gmail.com'
      this.password = 'ayylmao69'
    },
    fileToBase64(file) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader()
        reader.readAsDataURL(file)
        reader.onload = () => resolve(reader.result)
        reader.onerror = (error) => reject(error)
      })
    },
    async fileOnChangeEvent() {
      this.avatarBase64 = this.avatar
        ? await this.fileToBase64(this.avatar)
        : ''
    },
    async submit() {
      if (!this.$refs.form.validate()) return
      this.loading = true

      await this.$store.dispatch('$nuxtSocket/emit', {
        label: 'main',
        evt: 'register',
        msg: {
          username: this.username,
          email: this.email,
          password: this.password,
          avatar_base64: this.avatarBase64,
        },
      })
    },
  },
}
</script>
