(window.webpackJsonp=window.webpackJsonp||[]).push([[84],{171:function(module,__webpack_exports__,__webpack_require__){"use strict";var _polymer_polymer_polymer_legacy_js__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(2),_polymer_paper_styles_color_js__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(60),_polymer_paper_styles_color_js__WEBPACK_IMPORTED_MODULE_1___default=__webpack_require__.n(_polymer_paper_styles_color_js__WEBPACK_IMPORTED_MODULE_1__),_paper_spinner_styles_js__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(137),_paper_spinner_styles_js__WEBPACK_IMPORTED_MODULE_2___default=__webpack_require__.n(_paper_spinner_styles_js__WEBPACK_IMPORTED_MODULE_2__),_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(4),_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(3),_paper_spinner_behavior_js__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(114);function _templateObject(){var data=_taggedTemplateLiteral(["\n  <style include=\"paper-spinner-styles\"></style>\n\n  <div id=\"spinnerContainer\" class-name=\"[[__computeContainerClasses(active, __coolingDown)]]\" on-animationend=\"__reset\" on-webkit-animation-end=\"__reset\">\n    <div class=\"spinner-layer layer-1\">\n      <div class=\"circle-clipper left\"></div>\n      <div class=\"circle-clipper right\"></div>\n    </div>\n\n    <div class=\"spinner-layer layer-2\">\n      <div class=\"circle-clipper left\"></div>\n      <div class=\"circle-clipper right\"></div>\n    </div>\n\n    <div class=\"spinner-layer layer-3\">\n      <div class=\"circle-clipper left\"></div>\n      <div class=\"circle-clipper right\"></div>\n    </div>\n\n    <div class=\"spinner-layer layer-4\">\n      <div class=\"circle-clipper left\"></div>\n      <div class=\"circle-clipper right\"></div>\n    </div>\n  </div>\n"]);_templateObject=function _templateObject(){return data};return data}function _taggedTemplateLiteral(strings,raw){if(!raw){raw=strings.slice(0)}return Object.freeze(Object.defineProperties(strings,{raw:{value:Object.freeze(raw)}}))}/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/var template=Object(_polymer_polymer_lib_utils_html_tag_js__WEBPACK_IMPORTED_MODULE_4__.a)(_templateObject());template.setAttribute("strip-whitespace","");Object(_polymer_polymer_lib_legacy_polymer_fn_js__WEBPACK_IMPORTED_MODULE_3__.a)({_template:template,is:"paper-spinner",behaviors:[_paper_spinner_behavior_js__WEBPACK_IMPORTED_MODULE_5__.a]})},196:function(module,__webpack_exports__,__webpack_require__){"use strict";var polymer_legacy=__webpack_require__(2),iron_flex_layout=__webpack_require__(40),iron_control_state=__webpack_require__(32),iron_validatable_behavior=__webpack_require__(54),polymer_fn=__webpack_require__(4),polymer_dom=__webpack_require__(0),html_tag=__webpack_require__(3);function _templateObject(){var data=_taggedTemplateLiteral(["\n    <style>\n      :host {\n        display: inline-block;\n        position: relative;\n        width: 400px;\n        border: 1px solid;\n        padding: 2px;\n        -moz-appearance: textarea;\n        -webkit-appearance: textarea;\n        overflow: hidden;\n      }\n\n      .mirror-text {\n        visibility: hidden;\n        word-wrap: break-word;\n        @apply --iron-autogrow-textarea;\n      }\n\n      .fit {\n        @apply --layout-fit;\n      }\n\n      textarea {\n        position: relative;\n        outline: none;\n        border: none;\n        resize: none;\n        background: inherit;\n        color: inherit;\n        /* see comments in template */\n        width: 100%;\n        height: 100%;\n        font-size: inherit;\n        font-family: inherit;\n        line-height: inherit;\n        text-align: inherit;\n        @apply --iron-autogrow-textarea;\n      }\n\n      textarea::-webkit-input-placeholder {\n        @apply --iron-autogrow-textarea-placeholder;\n      }\n\n      textarea:-moz-placeholder {\n        @apply --iron-autogrow-textarea-placeholder;\n      }\n\n      textarea::-moz-placeholder {\n        @apply --iron-autogrow-textarea-placeholder;\n      }\n\n      textarea:-ms-input-placeholder {\n        @apply --iron-autogrow-textarea-placeholder;\n      }\n    </style>\n\n    <!-- the mirror sizes the input/textarea so it grows with typing -->\n    <!-- use &#160; instead &nbsp; of to allow this element to be used in XHTML -->\n    <div id=\"mirror\" class=\"mirror-text\" aria-hidden=\"true\">&nbsp;</div>\n\n    <!-- size the input/textarea with a div, because the textarea has intrinsic size in ff -->\n    <div class=\"textarea-container fit\">\n      <textarea id=\"textarea\" name$=\"[[name]]\" aria-label$=\"[[label]]\" autocomplete$=\"[[autocomplete]]\" autofocus$=\"[[autofocus]]\" inputmode$=\"[[inputmode]]\" placeholder$=\"[[placeholder]]\" readonly$=\"[[readonly]]\" required$=\"[[required]]\" disabled$=\"[[disabled]]\" rows$=\"[[rows]]\" minlength$=\"[[minlength]]\" maxlength$=\"[[maxlength]]\"></textarea>\n    </div>\n"],["\n    <style>\n      :host {\n        display: inline-block;\n        position: relative;\n        width: 400px;\n        border: 1px solid;\n        padding: 2px;\n        -moz-appearance: textarea;\n        -webkit-appearance: textarea;\n        overflow: hidden;\n      }\n\n      .mirror-text {\n        visibility: hidden;\n        word-wrap: break-word;\n        @apply --iron-autogrow-textarea;\n      }\n\n      .fit {\n        @apply --layout-fit;\n      }\n\n      textarea {\n        position: relative;\n        outline: none;\n        border: none;\n        resize: none;\n        background: inherit;\n        color: inherit;\n        /* see comments in template */\n        width: 100%;\n        height: 100%;\n        font-size: inherit;\n        font-family: inherit;\n        line-height: inherit;\n        text-align: inherit;\n        @apply --iron-autogrow-textarea;\n      }\n\n      textarea::-webkit-input-placeholder {\n        @apply --iron-autogrow-textarea-placeholder;\n      }\n\n      textarea:-moz-placeholder {\n        @apply --iron-autogrow-textarea-placeholder;\n      }\n\n      textarea::-moz-placeholder {\n        @apply --iron-autogrow-textarea-placeholder;\n      }\n\n      textarea:-ms-input-placeholder {\n        @apply --iron-autogrow-textarea-placeholder;\n      }\n    </style>\n\n    <!-- the mirror sizes the input/textarea so it grows with typing -->\n    <!-- use &#160; instead &nbsp; of to allow this element to be used in XHTML -->\n    <div id=\"mirror\" class=\"mirror-text\" aria-hidden=\"true\">&nbsp;</div>\n\n    <!-- size the input/textarea with a div, because the textarea has intrinsic size in ff -->\n    <div class=\"textarea-container fit\">\n      <textarea id=\"textarea\" name\\$=\"[[name]]\" aria-label\\$=\"[[label]]\" autocomplete\\$=\"[[autocomplete]]\" autofocus\\$=\"[[autofocus]]\" inputmode\\$=\"[[inputmode]]\" placeholder\\$=\"[[placeholder]]\" readonly\\$=\"[[readonly]]\" required\\$=\"[[required]]\" disabled\\$=\"[[disabled]]\" rows\\$=\"[[rows]]\" minlength\\$=\"[[minlength]]\" maxlength\\$=\"[[maxlength]]\"></textarea>\n    </div>\n"]);_templateObject=function _templateObject(){return data};return data}function _taggedTemplateLiteral(strings,raw){if(!raw){raw=strings.slice(0)}return Object.freeze(Object.defineProperties(strings,{raw:{value:Object.freeze(raw)}}))}/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/Object(polymer_fn.a)({_template:Object(html_tag.a)(_templateObject()),is:"iron-autogrow-textarea",behaviors:[iron_validatable_behavior.a,iron_control_state.a],properties:{value:{observer:"_valueChanged",type:String,notify:!0},bindValue:{observer:"_bindValueChanged",type:String,notify:!0},rows:{type:Number,value:1,observer:"_updateCached"},maxRows:{type:Number,value:0,observer:"_updateCached"},autocomplete:{type:String,value:"off"},autofocus:{type:Boolean,value:!1},inputmode:{type:String},placeholder:{type:String},readonly:{type:String},required:{type:Boolean},minlength:{type:Number},maxlength:{type:Number},label:{type:String}},listeners:{input:"_onInput"},get textarea(){return this.$.textarea},get selectionStart(){return this.$.textarea.selectionStart},get selectionEnd(){return this.$.textarea.selectionEnd},set selectionStart(value){this.$.textarea.selectionStart=value},set selectionEnd(value){this.$.textarea.selectionEnd=value},attached:function attached(){var IS_IOS=navigator.userAgent.match(/iP(?:[oa]d|hone)/);if(IS_IOS){this.$.textarea.style.marginLeft="-3px"}},validate:function validate(){var valid=this.$.textarea.validity.valid;if(valid){if(this.required&&""===this.value){valid=!1}else if(this.hasValidator()){valid=iron_validatable_behavior.a.validate.call(this,this.value)}}this.invalid=!valid;this.fire("iron-input-validate");return valid},_bindValueChanged:function _bindValueChanged(bindValue){this.value=bindValue},_valueChanged:function _valueChanged(value){var textarea=this.textarea;if(!textarea){return}if(textarea.value!==value){textarea.value=!(value||0===value)?"":value}this.bindValue=value;this.$.mirror.innerHTML=this._valueForMirror();this.fire("bind-value-changed",{value:this.bindValue})},_onInput:function _onInput(event){var eventPath=Object(polymer_dom.b)(event).path;this.value=eventPath?eventPath[0].value:event.target.value},_constrain:function _constrain(tokens){var _tokens;tokens=tokens||[""];if(0<this.maxRows&&tokens.length>this.maxRows){_tokens=tokens.slice(0,this.maxRows)}else{_tokens=tokens.slice(0)}while(0<this.rows&&_tokens.length<this.rows){_tokens.push("")}return _tokens.join("<br/>")+"&#160;"},_valueForMirror:function _valueForMirror(){var input=this.textarea;if(!input){return}this.tokens=input&&input.value?input.value.replace(/&/gm,"&amp;").replace(/"/gm,"&quot;").replace(/'/gm,"&#39;").replace(/</gm,"&lt;").replace(/>/gm,"&gt;").split("\n"):[""];return this._constrain(this.tokens)},_updateCached:function _updateCached(){this.$.mirror.innerHTML=this._constrain(this.tokens)}});var paper_input_char_counter=__webpack_require__(103),paper_input_container=__webpack_require__(104),paper_input_error=__webpack_require__(105),iron_form_element_behavior=__webpack_require__(53),paper_input_behavior=__webpack_require__(84);function paper_textarea_templateObject(){var data=paper_textarea_taggedTemplateLiteral(["\n    <style>\n      :host {\n        display: block;\n      }\n\n      :host([hidden]) {\n        display: none !important;\n      }\n\n      label {\n        pointer-events: none;\n      }\n    </style>\n\n    <paper-input-container no-label-float$=\"[[noLabelFloat]]\" always-float-label=\"[[_computeAlwaysFloatLabel(alwaysFloatLabel,placeholder)]]\" auto-validate$=\"[[autoValidate]]\" disabled$=\"[[disabled]]\" invalid=\"[[invalid]]\">\n\n      <label hidden$=\"[[!label]]\" aria-hidden=\"true\" for$=\"[[_inputId]]\" slot=\"label\">[[label]]</label>\n\n      <iron-autogrow-textarea class=\"paper-input-input\" slot=\"input\" id$=\"[[_inputId]]\" aria-labelledby$=\"[[_ariaLabelledBy]]\" aria-describedby$=\"[[_ariaDescribedBy]]\" bind-value=\"{{value}}\" invalid=\"{{invalid}}\" validator$=\"[[validator]]\" disabled$=\"[[disabled]]\" autocomplete$=\"[[autocomplete]]\" autofocus$=\"[[autofocus]]\" inputmode$=\"[[inputmode]]\" name$=\"[[name]]\" placeholder$=\"[[placeholder]]\" readonly$=\"[[readonly]]\" required$=\"[[required]]\" minlength$=\"[[minlength]]\" maxlength$=\"[[maxlength]]\" autocapitalize$=\"[[autocapitalize]]\" rows$=\"[[rows]]\" max-rows$=\"[[maxRows]]\" on-change=\"_onChange\"></iron-autogrow-textarea>\n\n      <template is=\"dom-if\" if=\"[[errorMessage]]\">\n        <paper-input-error aria-live=\"assertive\" slot=\"add-on\">[[errorMessage]]</paper-input-error>\n      </template>\n\n      <template is=\"dom-if\" if=\"[[charCounter]]\">\n        <paper-input-char-counter slot=\"add-on\"></paper-input-char-counter>\n      </template>\n\n    </paper-input-container>\n"],["\n    <style>\n      :host {\n        display: block;\n      }\n\n      :host([hidden]) {\n        display: none !important;\n      }\n\n      label {\n        pointer-events: none;\n      }\n    </style>\n\n    <paper-input-container no-label-float\\$=\"[[noLabelFloat]]\" always-float-label=\"[[_computeAlwaysFloatLabel(alwaysFloatLabel,placeholder)]]\" auto-validate\\$=\"[[autoValidate]]\" disabled\\$=\"[[disabled]]\" invalid=\"[[invalid]]\">\n\n      <label hidden\\$=\"[[!label]]\" aria-hidden=\"true\" for\\$=\"[[_inputId]]\" slot=\"label\">[[label]]</label>\n\n      <iron-autogrow-textarea class=\"paper-input-input\" slot=\"input\" id\\$=\"[[_inputId]]\" aria-labelledby\\$=\"[[_ariaLabelledBy]]\" aria-describedby\\$=\"[[_ariaDescribedBy]]\" bind-value=\"{{value}}\" invalid=\"{{invalid}}\" validator\\$=\"[[validator]]\" disabled\\$=\"[[disabled]]\" autocomplete\\$=\"[[autocomplete]]\" autofocus\\$=\"[[autofocus]]\" inputmode\\$=\"[[inputmode]]\" name\\$=\"[[name]]\" placeholder\\$=\"[[placeholder]]\" readonly\\$=\"[[readonly]]\" required\\$=\"[[required]]\" minlength\\$=\"[[minlength]]\" maxlength\\$=\"[[maxlength]]\" autocapitalize\\$=\"[[autocapitalize]]\" rows\\$=\"[[rows]]\" max-rows\\$=\"[[maxRows]]\" on-change=\"_onChange\"></iron-autogrow-textarea>\n\n      <template is=\"dom-if\" if=\"[[errorMessage]]\">\n        <paper-input-error aria-live=\"assertive\" slot=\"add-on\">[[errorMessage]]</paper-input-error>\n      </template>\n\n      <template is=\"dom-if\" if=\"[[charCounter]]\">\n        <paper-input-char-counter slot=\"add-on\"></paper-input-char-counter>\n      </template>\n\n    </paper-input-container>\n"]);paper_textarea_templateObject=function _templateObject(){return data};return data}function paper_textarea_taggedTemplateLiteral(strings,raw){if(!raw){raw=strings.slice(0)}return Object.freeze(Object.defineProperties(strings,{raw:{value:Object.freeze(raw)}}))}/**
@license
Copyright (c) 2015 The Polymer Project Authors. All rights reserved.
This code may only be used under the BSD style license found at
http://polymer.github.io/LICENSE.txt The complete set of authors may be found at
http://polymer.github.io/AUTHORS.txt The complete set of contributors may be
found at http://polymer.github.io/CONTRIBUTORS.txt Code distributed by Google as
part of the polymer project is also subject to an additional IP rights grant
found at http://polymer.github.io/PATENTS.txt
*/Object(polymer_fn.a)({_template:Object(html_tag.a)(paper_textarea_templateObject()),is:"paper-textarea",behaviors:[paper_input_behavior.a,iron_form_element_behavior.a],properties:{_ariaLabelledBy:{observer:"_ariaLabelledByChanged",type:String},_ariaDescribedBy:{observer:"_ariaDescribedByChanged",type:String},value:{type:String},rows:{type:Number,value:1},maxRows:{type:Number,value:0}},get selectionStart(){return this.$.input.textarea.selectionStart},set selectionStart(start){this.$.input.textarea.selectionStart=start},get selectionEnd(){return this.$.input.textarea.selectionEnd},set selectionEnd(end){this.$.input.textarea.selectionEnd=end},_ariaLabelledByChanged:function _ariaLabelledByChanged(ariaLabelledBy){this._focusableElement.setAttribute("aria-labelledby",ariaLabelledBy)},_ariaDescribedByChanged:function _ariaDescribedByChanged(ariaDescribedBy){this._focusableElement.setAttribute("aria-describedby",ariaDescribedBy)},get _focusableElement(){return this.inputElement.textarea}})},738:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);var _polymer_app_layout_app_header_layout_app_header_layout__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(135),_polymer_app_layout_app_header_app_header__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(134),_polymer_app_layout_app_toolbar_app_toolbar__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(111),_polymer_paper_input_paper_textarea__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(196),_polymer_paper_spinner_paper_spinner__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(171),_polymer_polymer_lib_utils_async__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(11),_polymer_polymer_lib_utils_debounce__WEBPACK_IMPORTED_MODULE_6__=__webpack_require__(19),_polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_7__=__webpack_require__(3),_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_8__=__webpack_require__(20),_components_ha_menu_button__WEBPACK_IMPORTED_MODULE_9__=__webpack_require__(136),_resources_ha_style__WEBPACK_IMPORTED_MODULE_10__=__webpack_require__(101);function _typeof(obj){if("function"===typeof Symbol&&"symbol"===typeof Symbol.iterator){_typeof=function _typeof(obj){return typeof obj}}else{_typeof=function _typeof(obj){return obj&&"function"===typeof Symbol&&obj.constructor===Symbol&&obj!==Symbol.prototype?"symbol":typeof obj}}return _typeof(obj)}function _templateObject(){var data=_taggedTemplateLiteral(["\n      <style include=\"ha-style iron-flex iron-positioning\"></style>\n      <style>\n        :host {\n          -ms-user-select: initial;\n          -webkit-user-select: initial;\n          -moz-user-select: initial;\n        }\n\n        .content {\n          padding: 16px;\n          direction: ltr;\n        }\n\n        .edit-pane {\n          margin-right: 16px;\n        }\n\n        .edit-pane a {\n          color: var(--dark-primary-color);\n        }\n\n        .horizontal .edit-pane {\n          max-width: 50%;\n        }\n\n        .render-pane {\n          position: relative;\n          max-width: 50%;\n        }\n\n        .render-spinner {\n          position: absolute;\n          top: 8px;\n          right: 8px;\n        }\n\n        paper-textarea {\n          --paper-input-container-input: {\n            @apply --paper-font-code1;\n          }\n        }\n\n        .rendered {\n          @apply --paper-font-code1;\n          clear: both;\n          white-space: pre-wrap;\n        }\n\n        .rendered.error {\n          color: red;\n        }\n      </style>\n\n      <app-header-layout has-scrolling-region>\n        <app-header slot=\"header\" fixed>\n          <app-toolbar>\n            <ha-menu-button\n              narrow=\"[[narrow]]\"\n              show-menu=\"[[showMenu]]\"\n            ></ha-menu-button>\n            <div main-title>Templates</div>\n          </app-toolbar>\n        </app-header>\n\n        <div class$=\"[[computeFormClasses(narrow)]]\">\n          <div class=\"edit-pane\">\n            <p>\n              Templates are rendered using the Jinja2 template engine with some\n              Home Assistant specific extensions.\n            </p>\n            <ul>\n              <li>\n                <a\n                  href=\"http://jinja.pocoo.org/docs/dev/templates/\"\n                  target=\"_blank\"\n                  >Jinja2 template documentation</a\n                >\n              </li>\n              <li>\n                <a\n                  href=\"https://home-assistant.io/docs/configuration/templating/\"\n                  target=\"_blank\"\n                  >Home Assistant template extensions</a\n                >\n              </li>\n            </ul>\n            <paper-textarea\n              label=\"Template editor\"\n              value=\"{{template}}\"\n              autofocus\n            ></paper-textarea>\n          </div>\n\n          <div class=\"render-pane\">\n            <paper-spinner\n              class=\"render-spinner\"\n              active=\"[[rendering]]\"\n            ></paper-spinner>\n            <pre class$=\"[[computeRenderedClasses(error)]]\">[[processed]]</pre>\n          </div>\n        </div>\n      </app-header-layout>\n    "]);_templateObject=function _templateObject(){return data};return data}function _taggedTemplateLiteral(strings,raw){if(!raw){raw=strings.slice(0)}return Object.freeze(Object.defineProperties(strings,{raw:{value:Object.freeze(raw)}}))}function _classCallCheck(instance,Constructor){if(!(instance instanceof Constructor)){throw new TypeError("Cannot call a class as a function")}}function _defineProperties(target,props){for(var i=0,descriptor;i<props.length;i++){descriptor=props[i];descriptor.enumerable=descriptor.enumerable||!1;descriptor.configurable=!0;if("value"in descriptor)descriptor.writable=!0;Object.defineProperty(target,descriptor.key,descriptor)}}function _createClass(Constructor,protoProps,staticProps){if(protoProps)_defineProperties(Constructor.prototype,protoProps);if(staticProps)_defineProperties(Constructor,staticProps);return Constructor}function _possibleConstructorReturn(self,call){if(call&&("object"===_typeof(call)||"function"===typeof call)){return call}return _assertThisInitialized(self)}function _assertThisInitialized(self){if(void 0===self){throw new ReferenceError("this hasn't been initialised - super() hasn't been called")}return self}function _getPrototypeOf(o){_getPrototypeOf=Object.setPrototypeOf?Object.getPrototypeOf:function _getPrototypeOf(o){return o.__proto__||Object.getPrototypeOf(o)};return _getPrototypeOf(o)}function _inherits(subClass,superClass){if("function"!==typeof superClass&&null!==superClass){throw new TypeError("Super expression must either be null or a function")}subClass.prototype=Object.create(superClass&&superClass.prototype,{constructor:{value:subClass,writable:!0,configurable:!0}});if(superClass)_setPrototypeOf(subClass,superClass)}function _setPrototypeOf(o,p){_setPrototypeOf=Object.setPrototypeOf||function _setPrototypeOf(o,p){o.__proto__=p;return o};return _setPrototypeOf(o,p)}var HaPanelDevTemplate=function(_PolymerElement){_inherits(HaPanelDevTemplate,_PolymerElement);function HaPanelDevTemplate(){_classCallCheck(this,HaPanelDevTemplate);return _possibleConstructorReturn(this,_getPrototypeOf(HaPanelDevTemplate).apply(this,arguments))}_createClass(HaPanelDevTemplate,[{key:"computeFormClasses",value:function computeFormClasses(narrow){return narrow?"content fit":"content fit layout horizontal"}},{key:"computeRenderedClasses",value:function computeRenderedClasses(error){return error?"error rendered":"rendered"}},{key:"templateChanged",value:function templateChanged(){var _this=this;if(this.error){this.error=!1}this._debouncer=_polymer_polymer_lib_utils_debounce__WEBPACK_IMPORTED_MODULE_6__.a.debounce(this._debouncer,_polymer_polymer_lib_utils_async__WEBPACK_IMPORTED_MODULE_5__.d.after(500),function(){_this.renderTemplate()})}},{key:"renderTemplate",value:function renderTemplate(){this.rendering=!0;this.hass.callApi("POST","template",{template:this.template}).then(function(processed){this.processed=processed;this.rendering=!1}.bind(this),function(error){this.processed=error&&error.body&&error.body.message||"Unknown error rendering template";this.error=!0;this.rendering=!1}.bind(this))}}],[{key:"template",get:function get(){return Object(_polymer_polymer_lib_utils_html_tag__WEBPACK_IMPORTED_MODULE_7__.a)(_templateObject())}},{key:"properties",get:function get(){return{hass:{type:Object},narrow:{type:Boolean,value:!1},showMenu:{type:Boolean,value:!1},error:{type:Boolean,value:!1},rendering:{type:Boolean,value:!1},template:{type:String,value:"Imitate available variables:\n{% set my_test_json = {\n  \"temperature\": 25,\n  \"unit\": \"\xB0C\"\n} %}\n\nThe temperature is {{ my_test_json.temperature }} {{ my_test_json.unit }}.\n\n{% if is_state(\"device_tracker.paulus\", \"home\") and\n      is_state(\"device_tracker.anne_therese\", \"home\") -%}\n  You are both home, you silly\n{%- else -%}\n  Anne Therese is at {{ states(\"device_tracker.anne_therese\") }}\n  Paulus is at {{ states(\"device_tracker.paulus\") }}\n{%- endif %}\n\nFor loop example:\n{% for state in states.sensor -%}\n  {%- if loop.first %}The {% elif loop.last %} and the {% else %}, the {% endif -%}\n  {{ state.name | lower }} is {{state.state_with_unit}}\n{%- endfor %}.",observer:"templateChanged"},processed:{type:String,value:""}}}}]);return HaPanelDevTemplate}(_polymer_polymer_polymer_element__WEBPACK_IMPORTED_MODULE_8__.a);customElements.define("ha-panel-dev-template",HaPanelDevTemplate)}}]);
//# sourceMappingURL=011458c27dd86aa16adf.chunk.js.map