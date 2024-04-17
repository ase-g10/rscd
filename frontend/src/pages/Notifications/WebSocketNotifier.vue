<template>
  <div>
  </div>
</template>

<script>

import NotificationTemplate from "@/pages/Notifications/NotificationTemplate.vue";

export default {
  data() {
    return {
      ws: null,
      type: [ "success", "error", "danger"]
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
      // 解析JSON数据，如果jsonData已经是对象，则这一步不需要
    const disaster = message[0].fields; // 根据新的JSON结构访问数据
    console.log(disaster)
      // 格式化消息内容
    const content = `
      Disaster Alert: ${disaster.name}
      Type: ${disaster.type}
      Location: ${disaster.location}
      Latitude: ${disaster.latitude}
      Longitude: ${disaster.longitude}
      Radius: ${disaster.radius} meters
      Description: ${disaster.description || "No description provided."}
    `;
    if ('Notification' in window && Notification.permission === 'granted') {
      // window.alert(bodyText)
      console.log("here")
    } else if ('Notification' in window && Notification.permission !== 'denied') {
      Notification.requestPermission().then((permission) => {
        if (permission === 'granted') {
        }
      });
    }
    const color = Math.floor(Math.random() * 4 + 1);
     // 调用Notifications.vue中的notifyVue方法
    // 使用Notifications插件显示通知
    this.$notify({
      component: NotificationTemplate,
      icon: "ti-gift",
      horizontalAlign: 'center', // 可以是 'right', 'center', 'left'
      verticalAlign: 'top', // 可以是 'top' 或 'bottom'
      type: "error", // 'info', 'success', 'warning', 'danger' 或 ''
      title: "Emergency Alert", // 通知标题
      text: content, // 通知内容，展示了消息的整个内容
      dangerouslySetInnerHtml: true, // 如果你需要渲染 HTML，确保设置这个属性
      duration: 10000,
      customClass: 'notification-content'
    });
    }
  }
};
</script>
<style>
.notification-content {
  white-space: pre-line;
}</style>
