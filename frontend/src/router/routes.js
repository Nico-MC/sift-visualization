
const routes = [
  {
    path: '/',
    name: '',
    component: () => import('layouts/layout.vue'),
    children: [
      { path: '', component: () => import('pages/sift.vue') }
    ]
  },
  {
    path: '/get',
    name: 'get',
    component: () => import('components/ping.vue')
  }
]

// Always leave this as last one
if (process.env.MODE !== 'ssr') {
  routes.push({
    path: '*',
    component: () => import('pages/Error404.vue')
  })
}

export default routes
