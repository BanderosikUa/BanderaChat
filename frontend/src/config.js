const config = {
    wsUrl: 'ws://localhost:5002',
    imageUrl: 'http://localhost:5002/media/',
}
  
if (process.env.NODE_ENV === 'production') {
    config.wsUrl = 'ws://localhost:5002',
    config.imageUrl = 'http://localhost:5002/media/'
}
  
export default config
