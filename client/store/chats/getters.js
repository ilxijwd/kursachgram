export default {
  ONLINE_USERS: (state) => state.users.filter((u) => u.online),
  SORTED_USERS_BY_ONLINE: (state) =>
    Array.from(state.users).sort((u, _) => (u.online ? -1 : 1)),
  CHAT_AVATAR: (state) => (chatId, currentUserId) => {
    const chat = state.chats.find((c) => c.id === chatId)
    if (!chat) return ''
    return chat.participants_ids.length > 2
      ? chat.avatar_base64
      : state.users.find(
          (u) => u.id === chat.participants_ids.find((p) => p !== currentUserId)
        ).avatar_base64
  },
}
