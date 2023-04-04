import {createRouter, createWebHistory} from 'vue-router'

// 路由列表
const routes = [
    {
        meta: {
            title: "登录页面",
            keepAlive: true
        },
        path: '/',         // uri访问地址
        name: "layout",
        component: () => import("../views/layout/index.vue"),
        redirect: '/person',
        children: []
    },
    {
        meta: {
            title: "登录页面",
            keepAlive: true
        },
        path: '/login',         // uri访问地址
        name: "login",
        component: () => import("../views/login/index.vue")
    },
]

// 路由对象实例化
const router = createRouter({
    // history, 指定路由的模式
    history: createWebHistory(),
    // 路由列表
    routes,
});


// 暴露路由对象
export default router