(window.webpackJsonp=window.webpackJsonp||[]).push([[60],{747:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);var _polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(3),_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(20),_mixins_localize_mixin__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(107),_common_util_compute_rtl__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(83);class NotificationManager extends Object(_mixins_localize_mixin__WEBPACK_IMPORTED_MODULE_2__.a)(_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_1__.a){static get template(){return _polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_0__.a`
      <style>
        paper-toast {
          z-index: 1;
        }
      </style>

      <ha-toast
        id="toast"
        dir="[[_rtl]]"
        no-cancel-on-outside-click="[[_cancelOnOutsideClick]]"
      ></ha-toast>
    `}static get properties(){return{hass:Object,_cancelOnOutsideClick:{type:Boolean,value:!1},_rtl:{type:String,computed:"_computeRTLDirection(hass)"}}}ready(){super.ready();Promise.all([__webpack_require__.e(1),__webpack_require__.e(27)]).then(__webpack_require__.bind(null,390))}showDialog({message}){this.$.toast.show(message)}_computeRTLDirection(hass){return Object(_common_util_compute_rtl__WEBPACK_IMPORTED_MODULE_3__.a)(hass)?"rtl":"ltr"}}customElements.define("notification-manager",NotificationManager)}}]);
//# sourceMappingURL=cd00b2ff9064f1e26dcb.chunk.js.map