export default () => ({
  loading: false,
  currentErrorCode: -1,
  errors: [
    {
      code: 0,
      title: 'Lost connection',
      description:
        'Lost connection to the messanger server, application cannot work without a connection to the server',
    },
    {
      code: 1,
      title: 'Not authenticated',
      description: 'You are not authenticated, please login or register',
    },
    {
      code: 2,
      title: 'Invalid authentication token',
      description:
        'Your authentication token lifetime has expired or is not valid',
    },
    {
      code: 3,
      title: 'Invalid request data',
      description:
        'Data that has been sent by socket.io to the server seems invalid',
    },
    {
      code: 4,
      title: 'Invalid credentials',
      description: 'User with this email does not exist',
    },
    {
      code: 5,
      title: 'Invalid credentials',
      description: 'Incorrect password',
    },
    {
      code: 6,
      title: 'Registration failed',
      description: 'This email is already in use',
    },
    {
      code: 7,
      title: 'Login not required',
      description: 'You are already logged in',
    },
    {
      code: 8,
      title: 'Chat not found',
      description: 'Chat was not found by your request',
    },
    {
      code: 9,
      title: 'Access denied',
      description: 'You are not the chat owner',
    },
    {
      code: 10,
      title: 'Group creation error',
      description: 'Not enough participants to create a group chat',
    },
  ],
})
