// Определим несколько маршрутов
// Каждый маршрут должен отображаться на компонент.

const routes=[
    {path:'/home',component:home},
    {path:'/department',component:department}
]

// Создаем экземпляр роутера и передаем опцию `routes`
// Здесь можно указать дополнительные параметры
const router = VueRouter.createRouter({
  // 4. Предоставляем реализацию истории для использования. Для простоты мы используем хеш-историю.
  history: VueRouter.createWebHashHistory(),
  routes, // сокращение от `routes: routes`
})
  // 5. Create and mount the root instance.
  const app = Vue.createApp({})
// Убедитесь, что вы _используете_ экземпляр маршрутизатора, чтобы
// все приложение поддерживает маршрутизатор.
  app.use(router)
  
  app.mount('#app')

// Теперь приложение запущено!