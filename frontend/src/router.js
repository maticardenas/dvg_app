// import Vue from 'vue'
// import VueRouter from 'vue-router'
import { createRouter, createWebHistory } from 'vue-router'

import BlogPost from '@/components/BlogPost'
import PostAuthor from '@/components/PostAuthor'
import PostsByTag from '@/components/PostsByTag'
import AllPosts from '@/components/AllPosts'

// Vue.use(VueRouter)

const routes = [
  { path: '/author/:username', component: PostAuthor },
  { path: '/post/:slug', component: BlogPost },
  { path: '/tag/:tag', component: PostsByTag },
  { path: '/', component: AllPosts },
]

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
})
export default router