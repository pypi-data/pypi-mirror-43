(window.webpackJsonp=window.webpackJsonp||[]).push([[36],{178:function(module,__webpack_exports__,__webpack_require__){"use strict";var index_es=__webpack_require__(209);function isEntityId(value){if("string"!==typeof value){return"entity id should be a string"}if(!value.includes(".")){return"entity id should be in the format 'domain.entity'"}return!0}function isIcon(value){if("string"!==typeof value){return"icon should be a string"}if(!value.includes(":")){return"icon should be in the format 'mdi:icon'"}return!0}__webpack_require__.d(__webpack_exports__,"a",function(){return struct});var struct=Object(index_es.a)({types:{"entity-id":isEntityId,icon:isIcon}})},222:function(module,__webpack_exports__,__webpack_require__){"use strict";var lit_element__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(5),_common_dom_fire_event__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(44),_components_entity_ha_entity_picker__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(174);function _typeof(obj){if("function"===typeof Symbol&&"symbol"===typeof Symbol.iterator){_typeof=function _typeof(obj){return typeof obj}}else{_typeof=function _typeof(obj){return obj&&"function"===typeof Symbol&&obj.constructor===Symbol&&obj!==Symbol.prototype?"symbol":typeof obj}}return _typeof(obj)}function _templateObject4(){var data=_taggedTemplateLiteral(["\n      <style>\n        .entities {\n          padding-left: 20px;\n        }\n      </style>\n    "]);_templateObject4=function _templateObject4(){return data};return data}function _templateObject3(){var data=_taggedTemplateLiteral(["\n            <ha-entity-picker\n              .hass=\"","\"\n              .value=\"","\"\n              .index=\"","\"\n              @change=\"","\"\n              allow-custom-entity\n            ></ha-entity-picker>\n          "]);_templateObject3=function _templateObject3(){return data};return data}function _templateObject2(){var data=_taggedTemplateLiteral(["\n      ","\n      <h3>Entities</h3>\n      <div class=\"entities\">\n        ","\n        <ha-entity-picker\n          .hass=\"","\"\n          @change=\"","\"\n        ></ha-entity-picker>\n      </div>\n    "]);_templateObject2=function _templateObject2(){return data};return data}function _templateObject(){var data=_taggedTemplateLiteral([""]);_templateObject=function _templateObject(){return data};return data}function _taggedTemplateLiteral(strings,raw){if(!raw){raw=strings.slice(0)}return Object.freeze(Object.defineProperties(strings,{raw:{value:Object.freeze(raw)}}))}function _classCallCheck(instance,Constructor){if(!(instance instanceof Constructor)){throw new TypeError("Cannot call a class as a function")}}function _defineProperties(target,props){for(var i=0,descriptor;i<props.length;i++){descriptor=props[i];descriptor.enumerable=descriptor.enumerable||!1;descriptor.configurable=!0;if("value"in descriptor)descriptor.writable=!0;Object.defineProperty(target,descriptor.key,descriptor)}}function _createClass(Constructor,protoProps,staticProps){if(protoProps)_defineProperties(Constructor.prototype,protoProps);if(staticProps)_defineProperties(Constructor,staticProps);return Constructor}function _possibleConstructorReturn(self,call){if(call&&("object"===_typeof(call)||"function"===typeof call)){return call}return _assertThisInitialized(self)}function _assertThisInitialized(self){if(void 0===self){throw new ReferenceError("this hasn't been initialised - super() hasn't been called")}return self}function _getPrototypeOf(o){_getPrototypeOf=Object.setPrototypeOf?Object.getPrototypeOf:function _getPrototypeOf(o){return o.__proto__||Object.getPrototypeOf(o)};return _getPrototypeOf(o)}function _inherits(subClass,superClass){if("function"!==typeof superClass&&null!==superClass){throw new TypeError("Super expression must either be null or a function")}subClass.prototype=Object.create(superClass&&superClass.prototype,{constructor:{value:subClass,writable:!0,configurable:!0}});if(superClass)_setPrototypeOf(subClass,superClass)}function _setPrototypeOf(o,p){_setPrototypeOf=Object.setPrototypeOf||function _setPrototypeOf(o,p){o.__proto__=p;return o};return _setPrototypeOf(o,p)}var HuiEntityEditor=function(_LitElement){_inherits(HuiEntityEditor,_LitElement);function HuiEntityEditor(){var _getPrototypeOf2,_this;_classCallCheck(this,HuiEntityEditor);for(var _len=arguments.length,args=Array(_len),_key=0;_key<_len;_key++){args[_key]=arguments[_key]}_this=_possibleConstructorReturn(this,(_getPrototypeOf2=_getPrototypeOf(HuiEntityEditor)).call.apply(_getPrototypeOf2,[this].concat(args)));_this.hass=void 0;_this.entities=void 0;return _this}_createClass(HuiEntityEditor,[{key:"render",value:function render(){var _this2=this;if(!this.entities){return Object(lit_element__WEBPACK_IMPORTED_MODULE_0__.e)(_templateObject())}return Object(lit_element__WEBPACK_IMPORTED_MODULE_0__.e)(_templateObject2(),this.renderStyle(),this.entities.map(function(entityConf,index){return Object(lit_element__WEBPACK_IMPORTED_MODULE_0__.e)(_templateObject3(),_this2.hass,entityConf.entity,index,_this2._valueChanged)}),this.hass,this._addEntity)}},{key:"_addEntity",value:function _addEntity(ev){var target=ev.target;if(""===target.value){return}var newConfigEntities=this.entities.concat({entity:target.value});target.value="";Object(_common_dom_fire_event__WEBPACK_IMPORTED_MODULE_1__.a)(this,"entities-changed",{entities:newConfigEntities})}},{key:"_valueChanged",value:function _valueChanged(ev){var target=ev.target,newConfigEntities=this.entities.concat();if(""===target.value){newConfigEntities.splice(target.index,1)}else{newConfigEntities[target.index]=Object.assign({},newConfigEntities[target.index],{entity:target.value})}Object(_common_dom_fire_event__WEBPACK_IMPORTED_MODULE_1__.a)(this,"entities-changed",{entities:newConfigEntities})}},{key:"renderStyle",value:function renderStyle(){return Object(lit_element__WEBPACK_IMPORTED_MODULE_0__.e)(_templateObject4())}}],[{key:"properties",get:function get(){return{hass:{},entities:{}}}}]);return HuiEntityEditor}(lit_element__WEBPACK_IMPORTED_MODULE_0__.a);customElements.define("hui-entity-editor",HuiEntityEditor)},267:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.d(__webpack_exports__,"a",function(){return processEditorEntities});function processEditorEntities(entities){return entities.map(function(entityConf){if("string"===typeof entityConf){return{entity:entityConf}}return entityConf})}},752:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);__webpack_require__.d(__webpack_exports__,"HuiEntitiesCardEditor",function(){return HuiEntitiesCardEditor});var lit_element__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(5),_polymer_paper_dropdown_menu_paper_dropdown_menu__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(130),_polymer_paper_item_paper_item__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(127),_polymer_paper_listbox_paper_listbox__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(129),_polymer_paper_toggle_button_paper_toggle_button__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(195),_process_editor_entities__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(267),_common_structs_struct__WEBPACK_IMPORTED_MODULE_6__=__webpack_require__(178),_common_dom_fire_event__WEBPACK_IMPORTED_MODULE_7__=__webpack_require__(44),_config_elements_style__WEBPACK_IMPORTED_MODULE_8__=__webpack_require__(192),_components_entity_state_badge__WEBPACK_IMPORTED_MODULE_9__=__webpack_require__(173),_components_hui_theme_select_editor__WEBPACK_IMPORTED_MODULE_10__=__webpack_require__(253),_components_hui_entity_editor__WEBPACK_IMPORTED_MODULE_11__=__webpack_require__(222),_components_ha_card__WEBPACK_IMPORTED_MODULE_12__=__webpack_require__(179),_components_ha_icon__WEBPACK_IMPORTED_MODULE_13__=__webpack_require__(164);function _typeof(obj){if("function"===typeof Symbol&&"symbol"===typeof Symbol.iterator){_typeof=function _typeof(obj){return typeof obj}}else{_typeof=function _typeof(obj){return obj&&"function"===typeof Symbol&&obj.constructor===Symbol&&obj!==Symbol.prototype?"symbol":typeof obj}}return _typeof(obj)}function _defineProperty(obj,key,value){if(key in obj){Object.defineProperty(obj,key,{value:value,enumerable:!0,configurable:!0,writable:!0})}else{obj[key]=value}return obj}function _templateObject2(){var data=_taggedTemplateLiteral(["\n      ","\n      <div class=\"card-config\">\n        <paper-input\n          label=\"Title\"\n          .value=\"","\"\n          .configValue=\"","\"\n          @value-changed=\"","\"\n        ></paper-input>\n        <hui-theme-select-editor\n          .hass=\"","\"\n          .value=\"","\"\n          .configValue=\"","\"\n          @theme-changed=\"","\"\n        ></hui-theme-select-editor>\n        <paper-toggle-button\n          ?checked=\"","\"\n          .configValue=\"","\"\n          @change=\"","\"\n          >Show Header Toggle?</paper-toggle-button\n        >\n      </div>\n      <hui-entity-editor\n        .hass=\"","\"\n        .entities=\"","\"\n        @entities-changed=\"","\"\n      ></hui-entity-editor>\n    "]);_templateObject2=function _templateObject2(){return data};return data}function _templateObject(){var data=_taggedTemplateLiteral([""]);_templateObject=function _templateObject(){return data};return data}function _taggedTemplateLiteral(strings,raw){if(!raw){raw=strings.slice(0)}return Object.freeze(Object.defineProperties(strings,{raw:{value:Object.freeze(raw)}}))}function _classCallCheck(instance,Constructor){if(!(instance instanceof Constructor)){throw new TypeError("Cannot call a class as a function")}}function _defineProperties(target,props){for(var i=0,descriptor;i<props.length;i++){descriptor=props[i];descriptor.enumerable=descriptor.enumerable||!1;descriptor.configurable=!0;if("value"in descriptor)descriptor.writable=!0;Object.defineProperty(target,descriptor.key,descriptor)}}function _createClass(Constructor,protoProps,staticProps){if(protoProps)_defineProperties(Constructor.prototype,protoProps);if(staticProps)_defineProperties(Constructor,staticProps);return Constructor}function _possibleConstructorReturn(self,call){if(call&&("object"===_typeof(call)||"function"===typeof call)){return call}return _assertThisInitialized(self)}function _assertThisInitialized(self){if(void 0===self){throw new ReferenceError("this hasn't been initialised - super() hasn't been called")}return self}function _getPrototypeOf(o){_getPrototypeOf=Object.setPrototypeOf?Object.getPrototypeOf:function _getPrototypeOf(o){return o.__proto__||Object.getPrototypeOf(o)};return _getPrototypeOf(o)}function _inherits(subClass,superClass){if("function"!==typeof superClass&&null!==superClass){throw new TypeError("Super expression must either be null or a function")}subClass.prototype=Object.create(superClass&&superClass.prototype,{constructor:{value:subClass,writable:!0,configurable:!0}});if(superClass)_setPrototypeOf(subClass,superClass)}function _setPrototypeOf(o,p){_setPrototypeOf=Object.setPrototypeOf||function _setPrototypeOf(o,p){o.__proto__=p;return o};return _setPrototypeOf(o,p)}var entitiesConfigStruct=_common_structs_struct__WEBPACK_IMPORTED_MODULE_6__.a.union([{entity:"entity-id",name:"string?",icon:"icon?"},"entity-id"]),cardConfigStruct=Object(_common_structs_struct__WEBPACK_IMPORTED_MODULE_6__.a)({type:"string",title:"string|number?",theme:"string?",show_header_toggle:"boolean?",entities:[entitiesConfigStruct]}),HuiEntitiesCardEditor=function(_LitElement){_inherits(HuiEntitiesCardEditor,_LitElement);function HuiEntitiesCardEditor(){var _getPrototypeOf2,_this;_classCallCheck(this,HuiEntitiesCardEditor);for(var _len=arguments.length,args=Array(_len),_key=0;_key<_len;_key++){args[_key]=arguments[_key]}_this=_possibleConstructorReturn(this,(_getPrototypeOf2=_getPrototypeOf(HuiEntitiesCardEditor)).call.apply(_getPrototypeOf2,[this].concat(args)));_this.hass=void 0;_this._config=void 0;_this._configEntities=void 0;return _this}_createClass(HuiEntitiesCardEditor,[{key:"setConfig",value:function setConfig(config){config=cardConfigStruct(config);this._config=config;this._configEntities=Object(_process_editor_entities__WEBPACK_IMPORTED_MODULE_5__.a)(config.entities)}},{key:"render",value:function render(){if(!this.hass){return Object(lit_element__WEBPACK_IMPORTED_MODULE_0__.e)(_templateObject())}return Object(lit_element__WEBPACK_IMPORTED_MODULE_0__.e)(_templateObject2(),_config_elements_style__WEBPACK_IMPORTED_MODULE_8__.a,this._title,"title",this._valueChanged,this.hass,this._theme,"theme",this._valueChanged,!1!==this._config.show_header_toggle,"show_header_toggle",this._valueChanged,this.hass,this._configEntities,this._valueChanged)}},{key:"_valueChanged",value:function _valueChanged(ev){if(!this._config||!this.hass){return}var target=ev.target;if("title"===target.configValue&&target.value===this._title||"theme"===target.configValue&&target.value===this._theme){return}if(ev.detail&&ev.detail.entities){this._config.entities=ev.detail.entities;this._configEntities=Object(_process_editor_entities__WEBPACK_IMPORTED_MODULE_5__.a)(this._config.entities)}else if(target.configValue){if(""===target.value){delete this._config[target.configValue]}else{this._config=Object.assign({},this._config,_defineProperty({},target.configValue,target.checked!==void 0?target.checked:target.value))}}Object(_common_dom_fire_event__WEBPACK_IMPORTED_MODULE_7__.a)(this,"config-changed",{config:this._config})}},{key:"_title",get:function get(){return this._config.title||""}},{key:"_theme",get:function get(){return this._config.theme||"Backend-selected"}}],[{key:"properties",get:function get(){return{hass:{},_config:{},_configEntities:{}}}}]);return HuiEntitiesCardEditor}(lit_element__WEBPACK_IMPORTED_MODULE_0__.a);customElements.define("hui-entities-card-editor",HuiEntitiesCardEditor)}}]);
//# sourceMappingURL=aa0b73131ebbd894651c.chunk.js.map