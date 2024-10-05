/* prettier-ignore-start */

/* eslint-disable */

// @ts-nocheck

// noinspection JSUnusedGlobalSymbols

// This file is auto-generated by TanStack Router

import { createFileRoute } from '@tanstack/react-router'

// Import Routes

import { Route as rootRoute } from './routes/__root'
import { Route as BaseIndexImport } from './routes/_base/index'
import { Route as BaseVacancyIdImport } from './routes/_base/vacancy/$id'

// Create Virtual Routes

const BaseLazyImport = createFileRoute('/_base')()
const BaseRegisterLazyImport = createFileRoute('/_base/register')()
const BaseLoginLazyImport = createFileRoute('/_base/login')()

// Create/Update Routes

const BaseLazyRoute = BaseLazyImport.update({
  id: '/_base',
  getParentRoute: () => rootRoute,
} as any).lazy(() => import('./routes/_base.lazy').then((d) => d.Route))

const BaseIndexRoute = BaseIndexImport.update({
  path: '/',
  getParentRoute: () => BaseLazyRoute,
} as any)

const BaseRegisterLazyRoute = BaseRegisterLazyImport.update({
  path: '/register',
  getParentRoute: () => BaseLazyRoute,
} as any).lazy(() =>
  import('./routes/_base/register.lazy').then((d) => d.Route),
)

const BaseLoginLazyRoute = BaseLoginLazyImport.update({
  path: '/login',
  getParentRoute: () => BaseLazyRoute,
} as any).lazy(() => import('./routes/_base/login.lazy').then((d) => d.Route))

const BaseVacancyIdRoute = BaseVacancyIdImport.update({
  path: '/vacancy/$id',
  getParentRoute: () => BaseLazyRoute,
} as any)

// Populate the FileRoutesByPath interface

declare module '@tanstack/react-router' {
  interface FileRoutesByPath {
    '/_base': {
      id: '/_base'
      path: ''
      fullPath: ''
      preLoaderRoute: typeof BaseLazyImport
      parentRoute: typeof rootRoute
    }
    '/_base/login': {
      id: '/_base/login'
      path: '/login'
      fullPath: '/login'
      preLoaderRoute: typeof BaseLoginLazyImport
      parentRoute: typeof BaseLazyImport
    }
    '/_base/register': {
      id: '/_base/register'
      path: '/register'
      fullPath: '/register'
      preLoaderRoute: typeof BaseRegisterLazyImport
      parentRoute: typeof BaseLazyImport
    }
    '/_base/': {
      id: '/_base/'
      path: '/'
      fullPath: '/'
      preLoaderRoute: typeof BaseIndexImport
      parentRoute: typeof BaseLazyImport
    }
    '/_base/vacancy/$id': {
      id: '/_base/vacancy/$id'
      path: '/vacancy/$id'
      fullPath: '/vacancy/$id'
      preLoaderRoute: typeof BaseVacancyIdImport
      parentRoute: typeof BaseLazyImport
    }
  }
}

// Create and export the route tree

export const routeTree = rootRoute.addChildren({
  BaseLazyRoute: BaseLazyRoute.addChildren({
    BaseLoginLazyRoute,
    BaseRegisterLazyRoute,
    BaseIndexRoute,
    BaseVacancyIdRoute,
  }),
})

/* prettier-ignore-end */

/* ROUTE_MANIFEST_START
{
  "routes": {
    "__root__": {
      "filePath": "__root.tsx",
      "children": [
        "/_base"
      ]
    },
    "/_base": {
      "filePath": "_base.lazy.tsx",
      "children": [
        "/_base/login",
        "/_base/register",
        "/_base/",
        "/_base/vacancy/$id"
      ]
    },
    "/_base/login": {
      "filePath": "_base/login.lazy.tsx",
      "parent": "/_base"
    },
    "/_base/register": {
      "filePath": "_base/register.lazy.tsx",
      "parent": "/_base"
    },
    "/_base/": {
      "filePath": "_base/index.tsx",
      "parent": "/_base"
    },
    "/_base/vacancy/$id": {
      "filePath": "_base/vacancy/$id.tsx",
      "parent": "/_base"
    }
  }
}
ROUTE_MANIFEST_END */
