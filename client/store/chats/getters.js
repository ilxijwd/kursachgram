export default {
  ONLINE_USERS: (state) => state.users.filter((u) => u.online),
  SORTED_USERS_BY_ONLINE: (state) =>
    Array.from(state.users).sort((u, _) => (u.online ? -1 : 1)),
}
