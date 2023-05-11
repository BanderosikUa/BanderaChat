const config = {
    wsUrl: 'ws://localhost:5000'
}
  
if (process.env.NODE_ENV === 'production') {
    config.wsUrl = 'ws://34.120.190.133'
}
  
export default config
