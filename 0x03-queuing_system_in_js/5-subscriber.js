import redis from 'redis';

const subscriber = redis.createClient();

subscriber.on('connect', () => {
  console.log('Redis client connected to the server');
});

subscriber.on('error', (err) => {
  console.log(`Redis client not connected to the server: ${err}`);
});

const channelName = 'holberton school channel'
subscriber.subscribe(channelName);

subscriber.on('message', (channel, message) => {
  console.log(`Received message from channel ${channel}: ${message}`);
  if (message === 'KILL_SERVER') {
    subscriber.unsubscribe(channelName);
    subscriber.quit();
  }
});
