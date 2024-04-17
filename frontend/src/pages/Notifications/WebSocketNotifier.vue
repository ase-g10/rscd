<template>
  <div>
  </div>
</template>

<script>

export default {
  data() {
    return {
      ws: null
    };
  },
  mounted() {
    this.connectWebSocket();
    console.log("connect ws")
    // 在组件挂载时调用方法，建立WebSocket连接
  },
  methods: {
    connectWebSocket() {
      // 建立WebSocket连接
      this.ws = new WebSocket('ws://127.0.0.1:8000/ws/notifications/');

      // 监听WebSocket连接打开事件
      this.ws.onopen = () => {
        console.log('WebSocket连接已打开');
      };

      // 监听WebSocket消息事件
      this.ws.onmessage = (event) => {
        // 收到WebSocket消息时弹出通知
        const notificationData = JSON.parse(event.data);
        console.log("messageeeee")
        this.showNotification(notificationData.message);
      };

      // 监听WebSocket连接关闭事件
      this.ws.onclose = () => {
        console.log('WebSocket连接已关闭');
      };

      // 监听WebSocket错误事件
      this.ws.onerror = (error) => {
        console.error('WebSocket发生错误:', error);
      };
    },
    showNotification(message) {
      console.log({body:message})
      let json = JSON.stringify(message)
      //显示出message所有信息
      // const bodyText = `${message.longitude}, Latitude: ${message.latitude}`;
      const bodyText = json
      console.log(bodyText)
      if ('Notification' in window && Notification.permission === 'granted') {
        window.alert(bodyText)
        console.log("here")
      } else if ('Notification' in window && Notification.permission !== 'denied') {
        Notification.requestPermission().then((permission) => {
          if (permission === 'granted') {
          }
        });
      }
    }
  }
};
</script>
