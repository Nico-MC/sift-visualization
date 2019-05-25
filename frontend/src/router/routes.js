const routes = [
  {
    path: '/',
    name: '',
    component: () => import('layouts/layout.vue'),
    children: [
      { path: '', component: () => import('pages/sift.vue') }
    ]
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
