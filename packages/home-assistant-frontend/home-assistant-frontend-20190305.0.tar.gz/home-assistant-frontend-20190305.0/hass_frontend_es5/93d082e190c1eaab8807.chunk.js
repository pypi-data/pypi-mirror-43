(window.webpackJsonp=window.webpackJsonp||[]).push([[61],{747:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);var _polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(3),_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(20),_mixins_localize_mixin__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(107),_common_util_compute_rtl__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(83);function _typeof(obj){if("function"===typeof Symbol&&"symbol"===typeof Symbol.iterator){_typeof=function _typeof(obj){return typeof obj}}else{_typeof=function _typeof(obj){return obj&&"function"===typeof Symbol&&obj.constructor===Symbol&&obj!==Symbol.prototype?"symbol":typeof obj}}return _typeof(obj)}function _templateObject(){var data=_taggedTemplateLiteral(["\n      <style>\n        paper-toast {\n          z-index: 1;\n        }\n      </style>\n\n      <ha-toast\n        id=\"toast\"\n        dir=\"[[_rtl]]\"\n        no-cancel-on-outside-click=\"[[_cancelOnOutsideClick]]\"\n      ></ha-toast>\n    "]);_templateObject=function _templateObject(){return data};return data}function _taggedTemplateLiteral(strings,raw){if(!raw){raw=strings.slice(0)}return Object.freeze(Object.defineProperties(strings,{raw:{value:Object.freeze(raw)}}))}function _classCallCheck(instance,Constructor){if(!(instance instanceof Constructor)){throw new TypeError("Cannot call a class as a function")}}function _defineProperties(target,props){for(var i=0,descriptor;i<props.length;i++){descriptor=props[i];descriptor.enumerable=descriptor.enumerable||!1;descriptor.configurable=!0;if("value"in descriptor)descriptor.writable=!0;Object.defineProperty(target,descriptor.key,descriptor)}}function _createClass(Constructor,protoProps,staticProps){if(protoProps)_defineProperties(Constructor.prototype,protoProps);if(staticProps)_defineProperties(Constructor,staticProps);return Constructor}function _possibleConstructorReturn(self,call){if(call&&("object"===_typeof(call)||"function"===typeof call)){return call}return _assertThisInitialized(self)}function _assertThisInitialized(self){if(void 0===self){throw new ReferenceError("this hasn't been initialised - super() hasn't been called")}return self}function _get(target,property,receiver){if("undefined"!==typeof Reflect&&Reflect.get){_get=Reflect.get}else{_get=function _get(target,property,receiver){var base=_superPropBase(target,property);if(!base)return;var desc=Object.getOwnPropertyDescriptor(base,property);if(desc.get){return desc.get.call(receiver)}return desc.value}}return _get(target,property,receiver||target)}function _superPropBase(object,property){while(!Object.prototype.hasOwnProperty.call(object,property)){object=_getPrototypeOf(object);if(null===object)break}return object}function _getPrototypeOf(o){_getPrototypeOf=Object.setPrototypeOf?Object.getPrototypeOf:function _getPrototypeOf(o){return o.__proto__||Object.getPrototypeOf(o)};return _getPrototypeOf(o)}function _inherits(subClass,superClass){if("function"!==typeof superClass&&null!==superClass){throw new TypeError("Super expression must either be null or a function")}subClass.prototype=Object.create(superClass&&superClass.prototype,{constructor:{value:subClass,writable:!0,configurable:!0}});if(superClass)_setPrototypeOf(subClass,superClass)}function _setPrototypeOf(o,p){_setPrototypeOf=Object.setPrototypeOf||function _setPrototypeOf(o,p){o.__proto__=p;return o};return _setPrototypeOf(o,p)}var NotificationManager=function(_LocalizeMixin){_inherits(NotificationManager,_LocalizeMixin);function NotificationManager(){_classCallCheck(this,NotificationManager);return _possibleConstructorReturn(this,_getPrototypeOf(NotificationManager).apply(this,arguments))}_createClass(NotificationManager,[{key:"ready",value:function ready(){_get(_getPrototypeOf(NotificationManager.prototype),"ready",this).call(this);Promise.all([__webpack_require__.e(1),__webpack_require__.e(28)]).then(__webpack_require__.bind(null,389))}},{key:"showDialog",value:function showDialog(_ref){var message=_ref.message;this.$.toast.show(message)}},{key:"_computeRTLDirection",value:function _computeRTLDirection(hass){return Object(_common_util_compute_rtl__WEBPACK_IMPORTED_MODULE_3__.a)(hass)?"rtl":"ltr"}}],[{key:"template",get:function get(){return Object(_polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_0__.a)(_templateObject())}},{key:"properties",get:function get(){return{hass:Object,_cancelOnOutsideClick:{type:Boolean,value:!1},_rtl:{type:String,computed:"_computeRTLDirection(hass)"}}}}]);return NotificationManager}(Object(_mixins_localize_mixin__WEBPACK_IMPORTED_MODULE_2__.a)(_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_1__.a));customElements.define("notification-manager",NotificationManager)}}]);
//# sourceMappingURL=93d082e190c1eaab8807.chunk.js.map