export default function ({ store, redirect }) {
  if (!store.state.app.me.token) {
    return redirect('/login')
  }
}
