(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["vendors~page--src--apps--content--account-access-view-vue~page--src--apps--content--content-view-vue"],{

/***/ "./node_modules/vue-lazy-hydration/dist/LazyHydrate.esm.js":
/*!*****************************************************************!*\
  !*** ./node_modules/vue-lazy-hydration/dist/LazyHydrate.esm.js ***!
  \*****************************************************************/
/*! exports provided: default, hydrateOnInteraction, hydrateSsrOnly, hydrateWhenIdle, hydrateWhenVisible */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
eval("__webpack_require__.r(__webpack_exports__);\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"hydrateOnInteraction\", function() { return hydrateOnInteraction; });\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"hydrateSsrOnly\", function() { return hydrateSsrOnly; });\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"hydrateWhenIdle\", function() { return hydrateWhenIdle; });\n/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, \"hydrateWhenVisible\", function() { return hydrateWhenVisible; });\nfunction _defineProperty(obj, key, value) {\n  if (key in obj) {\n    Object.defineProperty(obj, key, {\n      value: value,\n      enumerable: true,\n      configurable: true,\n      writable: true\n    });\n  } else {\n    obj[key] = value;\n  }\n\n  return obj;\n}\n\nfunction ownKeys(object, enumerableOnly) {\n  var keys = Object.keys(object);\n\n  if (Object.getOwnPropertySymbols) {\n    var symbols = Object.getOwnPropertySymbols(object);\n    if (enumerableOnly) symbols = symbols.filter(function (sym) {\n      return Object.getOwnPropertyDescriptor(object, sym).enumerable;\n    });\n    keys.push.apply(keys, symbols);\n  }\n\n  return keys;\n}\n\nfunction _objectSpread2(target) {\n  for (var i = 1; i < arguments.length; i++) {\n    var source = arguments[i] != null ? arguments[i] : {};\n\n    if (i % 2) {\n      ownKeys(Object(source), true).forEach(function (key) {\n        _defineProperty(target, key, source[key]);\n      });\n    } else if (Object.getOwnPropertyDescriptors) {\n      Object.defineProperties(target, Object.getOwnPropertyDescriptors(source));\n    } else {\n      ownKeys(Object(source)).forEach(function (key) {\n        Object.defineProperty(target, key, Object.getOwnPropertyDescriptor(source, key));\n      });\n    }\n  }\n\n  return target;\n}\n\nvar observers = new Map();\nfunction createObserver(options) {\n  if (typeof IntersectionObserver === \"undefined\") return null;\n  var optionKey = JSON.stringify(options);\n  if (observers.has(optionKey)) return observers.get(optionKey);\n  var observer = new IntersectionObserver(function (entries) {\n    entries.forEach(function (entry) {\n      // Use `intersectionRatio` because of Edge 15's\n      // lack of support for `isIntersecting`.\n      // See: https://github.com/w3c/IntersectionObserver/issues/211\n      var isIntersecting = entry.isIntersecting || entry.intersectionRatio > 0;\n      if (!isIntersecting || !entry.target.hydrate) return;\n      entry.target.hydrate();\n    });\n  }, options);\n  observers.set(optionKey, observer);\n  return observer;\n}\nfunction loadingComponentFactory(resolvableComponent, options) {\n  return _objectSpread2({\n    render: function render(h) {\n      var tag = this.$el ? this.$el.tagName : \"div\"; // eslint-disable-next-line no-underscore-dangle\n\n      if (!this.$el) resolvableComponent._resolve();\n      return h(tag);\n    }\n  }, options);\n}\nfunction resolvableComponentFactory(component) {\n  var resolve;\n  var promise = new Promise(function (newResolve) {\n    resolve = newResolve;\n  }); // eslint-disable-next-line no-underscore-dangle\n\n  promise._resolve = function () {\n    resolve(typeof component === \"function\" ? component() : component);\n  };\n\n  return promise;\n}\n\nvar isServer = typeof window === \"undefined\";\nfunction hydrateWhenIdle(component) {\n  var _ref = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {},\n      ignoredProps = _ref.ignoredProps;\n\n  if (isServer) return component;\n  var resolvableComponent = resolvableComponentFactory(component);\n  var loading = loadingComponentFactory(resolvableComponent, {\n    props: ignoredProps,\n    mounted: function mounted() {\n      // If `requestIdleCallback()` or `requestAnimationFrame()`\n      // is not supported, hydrate immediately.\n      if (!(\"requestIdleCallback\" in window) || !(\"requestAnimationFrame\" in window)) {\n        // eslint-disable-next-line no-underscore-dangle\n        resolvableComponent._resolve();\n\n        return;\n      }\n\n      var id = requestIdleCallback(function () {\n        // eslint-disable-next-line no-underscore-dangle\n        requestAnimationFrame(resolvableComponent._resolve);\n      }, {\n        timeout: this.idleTimeout\n      });\n\n      var cleanup = function cleanup() {\n        return cancelIdleCallback(id);\n      };\n\n      resolvableComponent.then(cleanup);\n    }\n  });\n  return function () {\n    return {\n      component: resolvableComponent,\n      delay: 0,\n      loading: loading\n    };\n  };\n}\nfunction hydrateWhenVisible(component) {\n  var _ref2 = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {},\n      ignoredProps = _ref2.ignoredProps,\n      observerOptions = _ref2.observerOptions;\n\n  if (isServer) return component;\n  var resolvableComponent = resolvableComponentFactory(component);\n  var observer = createObserver(observerOptions);\n  var loading = loadingComponentFactory(resolvableComponent, {\n    props: ignoredProps,\n    mounted: function mounted() {\n      var _this = this;\n\n      // If Intersection Observer API is not supported, hydrate immediately.\n      if (!observer) {\n        // eslint-disable-next-line no-underscore-dangle\n        resolvableComponent._resolve();\n\n        return;\n      } // eslint-disable-next-line no-underscore-dangle\n\n\n      this.$el.hydrate = resolvableComponent._resolve;\n\n      var cleanup = function cleanup() {\n        return observer.unobserve(_this.$el);\n      };\n\n      resolvableComponent.then(cleanup);\n      observer.observe(this.$el);\n    }\n  });\n  return function () {\n    return {\n      component: resolvableComponent,\n      delay: 0,\n      loading: loading\n    };\n  };\n}\nfunction hydrateSsrOnly(component) {\n  if (isServer) return component;\n  var resolvableComponent = resolvableComponentFactory(component);\n  var loading = loadingComponentFactory(resolvableComponent);\n  return function () {\n    return {\n      component: resolvableComponent,\n      delay: 0,\n      loading: loading\n    };\n  };\n}\nfunction hydrateOnInteraction(component) {\n  var _ref3 = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : {},\n      _ref3$event = _ref3.event,\n      event = _ref3$event === void 0 ? \"focus\" : _ref3$event,\n      ignoredProps = _ref3.ignoredProps;\n\n  if (isServer) return component;\n  var resolvableComponent = resolvableComponentFactory(component);\n  var events = Array.isArray(event) ? event : [event];\n  var loading = loadingComponentFactory(resolvableComponent, {\n    props: ignoredProps,\n    mounted: function mounted() {\n      var _this2 = this;\n\n      events.forEach(function (eventName) {\n        // eslint-disable-next-line no-underscore-dangle\n        _this2.$el.addEventListener(eventName, resolvableComponent._resolve, {\n          capture: true,\n          once: true\n        });\n      });\n    }\n  });\n  return function () {\n    return {\n      component: resolvableComponent,\n      delay: 0,\n      loading: loading\n    };\n  };\n}\nvar LazyHydrate = {\n  props: {\n    idleTimeout: {\n      default: 2000,\n      type: Number\n    },\n    onInteraction: {\n      type: [Array, Boolean, String]\n    },\n    ssrOnly: {\n      type: Boolean\n    },\n    triggerHydration: {\n      default: false,\n      type: Boolean\n    },\n    whenIdle: {\n      type: Boolean\n    },\n    whenVisible: {\n      type: [Boolean, Object]\n    }\n  },\n  data: function data() {\n    return {\n      hydrated: isServer\n    };\n  },\n  watch: {\n    triggerHydration: {\n      immediate: true,\n      handler: function handler(hydrate) {\n        if (hydrate) this.hydrate();\n      }\n    }\n  },\n  computed: {\n    interactionEvents: function interactionEvents() {\n      if (!this.onInteraction) return [];\n      if (this.onInteraction === true) return [\"focus\"];\n      return Array.isArray(this.onInteraction) ? this.onInteraction : [this.onInteraction];\n    }\n  },\n  mounted: function mounted() {\n    var _this3 = this;\n\n    if (this.$el.childElementCount === 0) {\n      // No SSR rendered content, hydrate immediately.\n      this.hydrate();\n      return;\n    }\n\n    if (this.ssrOnly) return;\n    this.interactionEvents.forEach(function (eventName) {\n      _this3.$el.addEventListener(eventName, _this3.hydrate, {\n        capture: true,\n        once: true\n      });\n    });\n\n    if (this.interactionEvents.length) {\n      this.interaction = function () {\n        _this3.interactionEvents.forEach(function (eventName) {\n          return _this3.$el.removeEventListener(eventName, _this3.hydrate);\n        });\n      };\n    }\n\n    if (this.whenIdle) {\n      // If `requestIdleCallback()` or `requestAnimationFrame()`\n      // is not supported, hydrate immediately.\n      if (!(\"requestIdleCallback\" in window) || !(\"requestAnimationFrame\" in window)) {\n        this.hydrate();\n        return;\n      }\n\n      var id = requestIdleCallback(function () {\n        requestAnimationFrame(function () {\n          _this3.hydrate();\n        });\n      }, {\n        timeout: this.idleTimeout\n      });\n\n      this.idle = function () {\n        return cancelIdleCallback(id);\n      };\n    }\n\n    if (this.whenVisible) {\n      var options = this.whenVisible === true ? {} : this.whenVisible;\n      var observer = createObserver(options); // If Intersection Observer API is not supported, hydrate immediately.\n\n      if (!observer) {\n        this.hydrate();\n        return;\n      }\n\n      this.$el.hydrate = this.hydrate;\n      observer.observe(this.$el);\n\n      this.visible = function () {\n        observer.unobserve(_this3.$el);\n        delete _this3.$el.hydrate;\n      };\n    }\n  },\n  beforeDestroy: function beforeDestroy() {\n    this.cleanup();\n  },\n  methods: {\n    cleanup: function cleanup() {\n      var _this4 = this;\n\n      var handlers = [\"idle\", \"interaction\", \"visible\"];\n      handlers.forEach(function (handler) {\n        if (handler in _this4) {\n          _this4[handler]();\n\n          delete _this4[handler];\n        }\n      });\n    },\n    hydrate: function hydrate() {\n      this.hydrated = true;\n      this.cleanup();\n    }\n  },\n  render: function render(h) {\n    if (!this.$scopedSlots.default && !this.$slots.default) return null;\n    var child = this.$scopedSlots.default ? this.$scopedSlots.default({\n      hydrated: this.hydrated\n    }) : this.$slots.default[0];\n    if (this.hydrated) return child;\n    var tag = this.$el ? this.$el.tagName : \"div\";\n    var vnode = h(tag); // Special thanks to Rahul Kadyan for the following lines of code.\n    // https://github.com/znck\n\n    vnode.asyncFactory = {};\n    vnode.isComment = true;\n    return vnode;\n  }\n};\n\n/* harmony default export */ __webpack_exports__[\"default\"] = (LazyHydrate);\n\n\n\n//# sourceURL=webpack:///./node_modules/vue-lazy-hydration/dist/LazyHydrate.esm.js?");

/***/ })

}]);