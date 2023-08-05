(window.webpackJsonp=window.webpackJsonp||[]).push([[57],{179:function(module,__webpack_exports__,__webpack_require__){"use strict";var index_es=__webpack_require__(186);function isEntityId(value){if("string"!==typeof value){return"entity id should be a string"}if(!value.includes(".")){return"entity id should be in the format 'domain.entity'"}return!0}function isIcon(value){if("string"!==typeof value){return"icon should be a string"}if(!value.includes(":")){return"icon should be in the format 'mdi:icon'"}return!0}__webpack_require__.d(__webpack_exports__,"a",function(){return struct});const struct=Object(index_es.a)({types:{"entity-id":isEntityId,icon:isIcon}})},186:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.d(__webpack_exports__,"a",function(){return superstruct});class StructError extends TypeError{static format(attrs){const{type,path,value}=attrs,message=`Expected a value of type \`${type}\`${path.length?` for \`${path.join(".")}\``:""} but received \`${JSON.stringify(value)}\`.`;return message}constructor(attrs){const message=StructError.format(attrs);super(message);const{data,path,value,reason,type,errors=[]}=attrs;this.data=data;this.path=path;this.value=value;this.reason=reason;this.type=type;this.errors=errors;if(!errors.length){errors.push(this)}if(Error.captureStackTrace){Error.captureStackTrace(this,this.constructor)}else{this.stack=new Error().stack}}}var toString=Object.prototype.toString,kindOf=function kindOf(val){if(void 0===val)return"undefined";if(null===val)return"null";var type=typeof val;if("boolean"===type)return"boolean";if("string"===type)return"string";if("number"===type)return"number";if("symbol"===type)return"symbol";if("function"===type){return isGeneratorFn(val)?"generatorfunction":"function"}if(isArray(val))return"array";if(isBuffer(val))return"buffer";if(isArguments(val))return"arguments";if(isDate(val))return"date";if(isError(val))return"error";if(isRegexp(val))return"regexp";switch(ctorName(val)){case"Symbol":return"symbol";case"Promise":return"promise";case"WeakMap":return"weakmap";case"WeakSet":return"weakset";case"Map":return"map";case"Set":return"set";case"Int8Array":return"int8array";case"Uint8Array":return"uint8array";case"Uint8ClampedArray":return"uint8clampedarray";case"Int16Array":return"int16array";case"Uint16Array":return"uint16array";case"Int32Array":return"int32array";case"Uint32Array":return"uint32array";case"Float32Array":return"float32array";case"Float64Array":return"float64array";}if(isGeneratorObj(val)){return"generator"}type=toString.call(val);switch(type){case"[object Object]":return"object";case"[object Map Iterator]":return"mapiterator";case"[object Set Iterator]":return"setiterator";case"[object String Iterator]":return"stringiterator";case"[object Array Iterator]":return"arrayiterator";}return type.slice(8,-1).toLowerCase().replace(/\s/g,"")};function ctorName(val){return val.constructor?val.constructor.name:null}function isArray(val){if(Array.isArray)return Array.isArray(val);return val instanceof Array}function isError(val){return val instanceof Error||"string"===typeof val.message&&val.constructor&&"number"===typeof val.constructor.stackTraceLimit}function isDate(val){if(val instanceof Date)return!0;return"function"===typeof val.toDateString&&"function"===typeof val.getDate&&"function"===typeof val.setDate}function isRegexp(val){if(val instanceof RegExp)return!0;return"string"===typeof val.flags&&"boolean"===typeof val.ignoreCase&&"boolean"===typeof val.multiline&&"boolean"===typeof val.global}function isGeneratorFn(name,val){return"GeneratorFunction"===ctorName(name)}function isGeneratorObj(val){return"function"===typeof val.throw&&"function"===typeof val.return&&"function"===typeof val.next}function isArguments(val){try{if("number"===typeof val.length&&"function"===typeof val.callee){return!0}}catch(err){if(-1!==err.message.indexOf("callee")){return!0}}return!1}function isBuffer(val){if(val.constructor&&"function"===typeof val.constructor.isBuffer){return val.constructor.isBuffer(val)}return!1}const IS_STRUCT="@@__STRUCT__@@",KIND="@@__KIND__@@";function isStruct(value){return!!(value&&value[IS_STRUCT])}function resolveDefaults(defaults,value){return"function"===typeof defaults?defaults(value):defaults}var _extends=Object.assign||function(target){for(var i=1,source;i<arguments.length;i++){source=arguments[i];for(var key in source){if(Object.prototype.hasOwnProperty.call(source,key)){target[key]=source[key]}}}return target};class Kind{constructor(name,type,validate){this.name=name;this.type=type;this.validate=validate}}function any(schema,defaults$$1,options){if(isStruct(schema)){return schema[KIND]}if(schema instanceof Kind){return schema}switch(kindOf(schema)){case"array":{return 1<schema.length?tuple(schema,defaults$$1,options):list(schema,defaults$$1,options)}case"function":{return func(schema,defaults$$1,options)}case"object":{return object(schema,defaults$$1,options)}case"string":{let required=!0,type;if(schema.endsWith("?")){required=!1;schema=schema.slice(0,-1)}if(schema.includes("|")){const scalars=schema.split(/\s*\|\s*/g);type=union(scalars,defaults$$1,options)}else if(schema.includes("&")){const scalars=schema.split(/\s*&\s*/g);type=intersection(scalars,defaults$$1,options)}else{type=scalar(schema,defaults$$1,options)}if(!required){type=optional(type,void 0,options)}return type}}if(!1){}else{throw new Error(`Invalid schema: ${schema}`)}}function dict(schema,defaults$$1,options){if("array"!==kindOf(schema)||2!==schema.length){if(!1){}else{throw new Error(`Invalid schema: ${schema}`)}}const obj=scalar("object",void 0,options),keys=any(schema[0],void 0,options),values=any(schema[1],void 0,options),name="dict",type=`dict<${keys.type},${values.type}>`,validate=value=>{const resolved=resolveDefaults(defaults$$1);value=resolved?_extends({},resolved,value):value;const[error]=obj.validate(value);if(error){error.type=type;return[error]}const ret={},errors=[];for(let k in value){const v=value[k],[e,r]=keys.validate(k);if(e){const allE=e.errors||[e];allE.forEach(singleE=>{singleE.path=[k].concat(singleE.path);singleE.data=value;errors.push(singleE)});continue}k=r;const[e2,r2]=values.validate(v);if(e2){const allE2=e2.errors||[e2];allE2.forEach(singleE=>{singleE.path=[k].concat(singleE.path);singleE.data=value;errors.push(singleE)});continue}ret[k]=r2}if(errors.length){const first=errors[0];first.errors=errors;return[first]}return[void 0,ret]};return new Kind(name,type,validate)}function en(schema,defaults$$1,options){if("array"!==kindOf(schema)){if(!1){}else{throw new Error(`Invalid schema: ${schema}`)}}const name="enum",type=schema.map(s=>{try{return JSON.stringify(s)}catch(e){return s+""}}).join(" | "),validate=(value=resolveDefaults(defaults$$1))=>{return schema.includes(value)?[void 0,value]:[{data:value,path:[],value,type}]};return new Kind(name,type,validate)}function enums(schema,defaults$$1,options){const e=en(schema,void 0,options),l=list([e],defaults$$1,options);return l}function func(schema,defaults$$1,options){if("function"!==kindOf(schema)){if(!1){}else{throw new Error(`Invalid schema: ${schema}`)}}const name="function",type="<function>",validate=(value=resolveDefaults(defaults$$1),data)=>{const result=schema(value,data);let failure={path:[],reason:null},isValid;switch(kindOf(result)){case"boolean":{isValid=result;break}case"string":{isValid=!1;failure.reason=result;break}case"object":{isValid=!1;failure=_extends({},failure,result);break}default:{if(!1){}else{throw new Error(`Invalid result: ${result}`)}}}return isValid?[void 0,value]:[_extends({type,value,data:value},failure)]};return new Kind(name,type,validate)}function instance(schema,defaults$$1,options){const name="instance",type=`instance<${schema.name}>`,validate=(value=resolveDefaults(defaults$$1))=>{return value instanceof schema?[void 0,value]:[{data:value,path:[],value,type}]};return new Kind(name,type,validate)}function inter(schema,defaults$$1,options){if("object"!==kindOf(schema)){if(!1){}else{throw new Error(`Invalid schema: ${schema}`)}}const ks=[],properties={};for(const key in schema){ks.push(key);const s=schema[key],kind=any(s,void 0,options);properties[key]=kind}const name="interface",type=`{${ks.join()}}`,validate=value=>{const resolved=resolveDefaults(defaults$$1);value=resolved?_extends({},resolved,value):value;const errors=[],ret=value;for(const key in properties){let v=value[key];const kind=properties[key];if(v===void 0){const d=defaults$$1&&defaults$$1[key];v=resolveDefaults(d,value)}const[e,r]=kind.validate(v,value);if(e){const allE=e.errors||[e];allE.forEach(singleE=>{singleE.path=[key].concat(singleE.path);singleE.data=value;errors.push(singleE)});continue}if(key in value||r!==void 0){ret[key]=r}}if(errors.length){const first=errors[0];first.errors=errors;return[first]}return[void 0,ret]};return new Kind(name,type,validate)}function lazy(schema,defaults$$1,options){if("function"!==kindOf(schema)){if(!1){}else{throw new Error(`Invalid schema: ${schema}`)}}let kind,struct;const name="lazy",type=`lazy...`,compile=value=>{struct=schema();kind.name=struct.kind;kind.type=struct.type;kind.validate=struct.validate;return kind.validate(value)};kind=new Kind(name,type,compile);return kind}function list(schema,defaults$$1,options){if("array"!==kindOf(schema)||1!==schema.length){if(!1){}else{throw new Error(`Invalid schema: ${schema}`)}}const array=scalar("array",void 0,options),element=any(schema[0],void 0,options),name="list",type=`[${element.type}]`,validate=(value=resolveDefaults(defaults$$1))=>{const[error,result]=array.validate(value);if(error){error.type=type;return[error]}value=result;const errors=[],ret=[];for(let i=0;i<value.length;i++){const v=value[i],[e,r]=element.validate(v);if(e){const allE=e.errors||[e];allE.forEach(singleE=>{singleE.path=[i].concat(singleE.path);singleE.data=value;errors.push(singleE)});continue}ret[i]=r}if(errors.length){const first=errors[0];first.errors=errors;return[first]}return[void 0,ret]};return new Kind(name,type,validate)}function literal(schema,defaults$$1,options){const name="literal",type=`literal: ${JSON.stringify(schema)}`,validate=(value=resolveDefaults(defaults$$1))=>{return value===schema?[void 0,value]:[{data:value,path:[],value,type}]};return new Kind(name,type,validate)}function object(schema,defaults$$1,options){if("object"!==kindOf(schema)){if(!1){}else{throw new Error(`Invalid schema: ${schema}`)}}const obj=scalar("object",void 0,options),ks=[],properties={};for(const key in schema){ks.push(key);const s=schema[key],kind=any(s,void 0,options);properties[key]=kind}const name="object",type=`{${ks.join()}}`,validate=(value=resolveDefaults(defaults$$1))=>{const[error]=obj.validate(value);if(error){error.type=type;return[error]}const errors=[],ret={},valueKeys=Object.keys(value),propertiesKeys=Object.keys(properties),keys=new Set(valueKeys.concat(propertiesKeys));keys.forEach(key=>{let v=value[key];const kind=properties[key];if(v===void 0){const d=defaults$$1&&defaults$$1[key];v=resolveDefaults(d,value)}if(!kind){const e={data:value,path:[key],value:v};errors.push(e);return}const[e,r]=kind.validate(v,value);if(e){const allE=e.errors||[e];allE.forEach(singleE=>{singleE.path=[key].concat(singleE.path);singleE.data=value;errors.push(singleE)});return}if(key in value||r!==void 0){ret[key]=r}});if(errors.length){const first=errors[0];first.errors=errors;return[first]}return[void 0,ret]};return new Kind(name,type,validate)}function optional(schema,defaults$$1,options){return union([schema,"undefined"],defaults$$1,options)}function partial(schema,defaults$$1,options){if("object"!==kindOf(schema)){if(!1){}else{throw new Error(`Invalid schema: ${schema}`)}}const obj=scalar("object",void 0,options),ks=[],properties={};for(const key in schema){ks.push(key);const s=schema[key],kind=any(s,void 0,options);properties[key]=kind}const name="partial",type=`{${ks.join()},...}`,validate=(value=resolveDefaults(defaults$$1))=>{const[error]=obj.validate(value);if(error){error.type=type;return[error]}const errors=[],ret={};for(const key in properties){let v=value[key];const kind=properties[key];if(v===void 0){const d=defaults$$1&&defaults$$1[key];v=resolveDefaults(d,value)}const[e,r]=kind.validate(v,value);if(e){const allE=e.errors||[e];allE.forEach(singleE=>{singleE.path=[key].concat(singleE.path);singleE.data=value;errors.push(singleE)});continue}if(key in value||r!==void 0){ret[key]=r}}if(errors.length){const first=errors[0];first.errors=errors;return[first]}return[void 0,ret]};return new Kind(name,type,validate)}function scalar(schema,defaults$$1,options){if("string"!==kindOf(schema)){if(!1){}else{throw new Error(`Invalid schema: ${schema}`)}}const{types}=options,fn=types[schema];if("function"!==kindOf(fn)){if(!1){}else{throw new Error(`Invalid type: ${schema}`)}}const kind=func(fn,defaults$$1,options),name="scalar",type=schema,validate=value=>{const[error,result]=kind.validate(value);if(error){error.type=type;return[error]}return[void 0,result]};return new Kind(name,type,validate)}function tuple(schema,defaults$$1,options){if("array"!==kindOf(schema)){if(!1){}else{throw new Error(`Invalid schema: ${schema}`)}}const kinds=schema.map(s=>any(s,void 0,options)),array=scalar("array",void 0,options),name="tuple",type=`[${kinds.map(k=>k.type).join()}]`,validate=(value=resolveDefaults(defaults$$1))=>{const[error]=array.validate(value);if(error){error.type=type;return[error]}const ret=[],errors=[],length=Math.max(value.length,kinds.length);for(let i=0;i<length;i++){const kind=kinds[i],v=value[i];if(!kind){const e={data:value,path:[i],value:v};errors.push(e);continue}const[e,r]=kind.validate(v);if(e){const allE=e.errors||[e];allE.forEach(singleE=>{singleE.path=[i].concat(singleE.path);singleE.data=value;errors.push(singleE)});continue}ret[i]=r}if(errors.length){const first=errors[0];first.errors=errors;return[first]}return[void 0,ret]};return new Kind(name,type,validate)}function union(schema,defaults$$1,options){if("array"!==kindOf(schema)){if(!1){}else{throw new Error(`Invalid schema: ${schema}`)}}const kinds=schema.map(s=>any(s,void 0,options)),name="union",type=kinds.map(k=>k.type).join(" | "),validate=(value=resolveDefaults(defaults$$1))=>{const errors=[];for(const k of kinds){const[e,r]=k.validate(value);if(!e){return[void 0,r]}errors.push(e)}errors[0].type=type;return errors};return new Kind(name,type,validate)}function intersection(schema,defaults$$1,options){if("array"!==kindOf(schema)){if(!1){}else{throw new Error(`Invalid schema: ${schema}`)}}const types=schema.map(s=>any(s,void 0,options)),name="intersection",type=types.map(t=>t.type).join(" & "),validate=(value=resolveDefaults(defaults$$1))=>{let v=value;for(const t of types){const[e,r]=t.validate(v);if(e){e.type=type;return[e]}v=r}return[void 0,v]};return new Kind(name,type,validate)}const Kinds={any,dict,enum:en,enums,function:func,instance,interface:inter,lazy,list,literal,object,optional,partial,scalar,tuple,union,intersection},TYPES=["arguments","array","boolean","buffer","error","float32array","float64array","function","generatorfunction","int16array","int32array","int8array","map","null","number","object","promise","regexp","set","string","symbol","uint16array","uint32array","uint8array","uint8clampedarray","undefined","weakmap","weakset"],Types={any:value=>value!==void 0};TYPES.forEach(type=>{Types[type]=value=>kindOf(value)===type});Types.date=value=>"date"===kindOf(value)&&!isNaN(value);function superstruct(config={}){const types=_extends({},Types,config.types||{});function struct(schema,defaults$$1,options={}){if(isStruct(schema)){schema=schema.schema}const kind=Kinds.any(schema,defaults$$1,_extends({},options,{types}));function Struct(data){if(this instanceof Struct){if(!1){}else{throw new Error("Invalid `new` keyword!")}}return Struct.assert(data)}Object.defineProperty(Struct,IS_STRUCT,{value:!0});Object.defineProperty(Struct,KIND,{value:kind});Struct.kind=kind.name;Struct.type=kind.type;Struct.schema=schema;Struct.defaults=defaults$$1;Struct.options=options;Struct.assert=value=>{const[error,result]=kind.validate(value);if(error){throw new StructError(error)}return result};Struct.test=value=>{const[error]=kind.validate(value);return!error};Struct.validate=value=>{const[error,result]=kind.validate(value);if(error){return[new StructError(error)]}return[void 0,result]};return Struct}Object.keys(Kinds).forEach(name=>{const kind=Kinds[name];struct[name]=(schema,defaults$$1,options)=>{const type=kind(schema,defaults$$1,_extends({},options,{types})),s=struct(type,defaults$$1,options);return s}});return struct}const struct=superstruct()},383:function(module,__webpack_exports__,__webpack_require__){"use strict";var codemirror__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(384),codemirror__WEBPACK_IMPORTED_MODULE_0___default=__webpack_require__.n(codemirror__WEBPACK_IMPORTED_MODULE_0__),codemirror_mode_yaml_yaml__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(447),codemirror_mode_yaml_yaml__WEBPACK_IMPORTED_MODULE_1___default=__webpack_require__.n(codemirror_mode_yaml_yaml__WEBPACK_IMPORTED_MODULE_1__),codemirror_lib_codemirror_css__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(448),codemirror_lib_codemirror_css__WEBPACK_IMPORTED_MODULE_2___default=__webpack_require__.n(codemirror_lib_codemirror_css__WEBPACK_IMPORTED_MODULE_2__),_common_dom_fire_event__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(44),_common_util_compute_rtl__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(83);class HuiYamlEditor extends HTMLElement{constructor(){super();this._hass=void 0;this.codemirror=void 0;this._value=void 0;codemirror__WEBPACK_IMPORTED_MODULE_0___default.a.commands.save=cm=>{Object(_common_dom_fire_event__WEBPACK_IMPORTED_MODULE_3__.a)(cm.getWrapperElement(),"yaml-save")};this._value="";const shadowRoot=this.attachShadow({mode:"open"});shadowRoot.innerHTML=`
            <style>
              ${codemirror_lib_codemirror_css__WEBPACK_IMPORTED_MODULE_2___default.a}
              .CodeMirror {
                height: var(--code-mirror-height, auto);
                direction: var(--code-mirror-direction, ltr);
              }
              .CodeMirror-scroll {
                max-height: var(--code-mirror-max-height, --code-mirror-height);
              }
              .CodeMirror-gutters {
                border-right: 1px solid var(--paper-input-container-color, var(--secondary-text-color));
                background-color: var(--paper-dialog-background-color, var(--primary-background-color));
                transition: 0.2s ease border-right;
              }
              .CodeMirror-focused .CodeMirror-gutters {
                border-right: 2px solid var(--paper-input-container-focus-color, var(--primary-color));;
              }
              .CodeMirror-linenumber {
                color: var(--paper-dialog-color, var(--primary-text-color));
              }
              .rtl .CodeMirror-vscrollbar {
                right: auto;
                left: 0px;
              }
              .rtl-gutter {
                width: 20px;
              }
            </style>`}set hass(hass){this._hass=hass;if(this._hass){this.setScrollBarDirection()}}set value(value){if(this.codemirror){if(value!==this.codemirror.getValue()){this.codemirror.setValue(value)}}this._value=value}get value(){return this.codemirror.getValue()}get hasComments(){return this.shadowRoot.querySelector("span.cm-comment")?!0:!1}connectedCallback(){if(!this.codemirror){this.codemirror=codemirror__WEBPACK_IMPORTED_MODULE_0___default()(this.shadowRoot,{value:this._value,lineNumbers:!0,mode:"yaml",tabSize:2,autofocus:!0,viewportMargin:Infinity,gutters:this._hass&&Object(_common_util_compute_rtl__WEBPACK_IMPORTED_MODULE_4__.a)(this._hass)?["rtl-gutter","CodeMirror-linenumbers"]:[]});this.setScrollBarDirection();this.codemirror.on("changes",()=>this._onChange())}else{this.codemirror.refresh()}}_onChange(){Object(_common_dom_fire_event__WEBPACK_IMPORTED_MODULE_3__.a)(this,"yaml-changed",{value:this.codemirror.getValue()})}setScrollBarDirection(){if(!this.codemirror){return}this.codemirror.getWrapperElement().classList.toggle("rtl",Object(_common_util_compute_rtl__WEBPACK_IMPORTED_MODULE_4__.a)(this._hass))}}window.customElements.define("hui-yaml-editor",HuiYamlEditor)},750:function(module,__webpack_exports__,__webpack_require__){"use strict";__webpack_require__.r(__webpack_exports__);var lit_element__WEBPACK_IMPORTED_MODULE_0__=__webpack_require__(5),lit_html_directives_class_map__WEBPACK_IMPORTED_MODULE_1__=__webpack_require__(63),js_yaml__WEBPACK_IMPORTED_MODULE_2__=__webpack_require__(444),js_yaml__WEBPACK_IMPORTED_MODULE_2___default=__webpack_require__.n(js_yaml__WEBPACK_IMPORTED_MODULE_2__),_polymer_app_layout_app_header_layout_app_header_layout__WEBPACK_IMPORTED_MODULE_3__=__webpack_require__(135),_polymer_app_layout_app_header_app_header__WEBPACK_IMPORTED_MODULE_4__=__webpack_require__(134),_polymer_app_layout_app_toolbar_app_toolbar__WEBPACK_IMPORTED_MODULE_5__=__webpack_require__(111),_material_mwc_button__WEBPACK_IMPORTED_MODULE_6__=__webpack_require__(73),_polymer_paper_icon_button_paper_icon_button__WEBPACK_IMPORTED_MODULE_7__=__webpack_require__(96),_polymer_paper_spinner_paper_spinner__WEBPACK_IMPORTED_MODULE_8__=__webpack_require__(173),_common_structs_struct__WEBPACK_IMPORTED_MODULE_9__=__webpack_require__(179),_components_ha_icon__WEBPACK_IMPORTED_MODULE_10__=__webpack_require__(164),_resources_styles__WEBPACK_IMPORTED_MODULE_11__=__webpack_require__(56),_components_hui_yaml_editor__WEBPACK_IMPORTED_MODULE_12__=__webpack_require__(383);const lovelaceStruct=_common_structs_struct__WEBPACK_IMPORTED_MODULE_9__.a.interface({title:"string?",views:["object"],resources:_common_structs_struct__WEBPACK_IMPORTED_MODULE_9__.a.optional(["object"])});class LovelaceFullConfigEditor extends lit_element__WEBPACK_IMPORTED_MODULE_0__.a{constructor(...args){super(...args);this.hass=void 0;this.lovelace=void 0;this.closeEditor=void 0;this._saving=void 0;this._changed=void 0;this._generation=void 0}static get properties(){return{hass:{},lovelace:{},closeEditor:{},_saving:{},_changed:{}}}render(){return lit_element__WEBPACK_IMPORTED_MODULE_0__.e`
      <app-header-layout>
        <app-header>
          <app-toolbar>
            <paper-icon-button
              icon="hass:close"
              @click="${this._closeEditor}"
            ></paper-icon-button>
            <div main-title>
              ${this.hass.localize("ui.panel.lovelace.editor.raw_editor.header")}
            </div>
            <div
              class="save-button
              ${Object(lit_html_directives_class_map__WEBPACK_IMPORTED_MODULE_1__.a)({saved:!1===this._saving||!0===this._changed})}"
            >
              ${this._changed?this.hass.localize("ui.panel.lovelace.editor.raw_editor.unsaved_changes"):this.hass.localize("ui.panel.lovelace.editor.raw_editor.saved")}
            </div>
            <mwc-button raised @click="${this._handleSave}"
              >${this.hass.localize("ui.panel.lovelace.editor.raw_editor.save")}</mwc-button
            >
          </app-toolbar>
        </app-header>
        <div class="content">
          <hui-yaml-editor
            .hass="${this.hass}"
            @yaml-changed="${this._yamlChanged}"
            @yaml-save="${this._handleSave}"
          >
          </hui-yaml-editor>
        </div>
      </app-header-layout>
    `}firstUpdated(){this.yamlEditor.value=js_yaml__WEBPACK_IMPORTED_MODULE_2___default.a.safeDump(this.lovelace.config);this.yamlEditor.codemirror.clearHistory();this._generation=this.yamlEditor.codemirror.changeGeneration(!0)}static get styles(){return[_resources_styles__WEBPACK_IMPORTED_MODULE_11__.a,lit_element__WEBPACK_IMPORTED_MODULE_0__.c`
        :host {
          --code-mirror-height: 100%;
        }

        app-header-layout {
          height: 100vh;
        }

        app-toolbar {
          background-color: var(--dark-background-color, #455a64);
          color: var(--dark-text-color);
        }

        .comments {
          font-size: 16px;
        }

        .content {
          height: calc(100vh - 68px);
        }

        hui-code-editor {
          height: 100%;
        }

        .save-button {
          opacity: 0;
          font-size: 14px;
          padding: 0px 10px;
        }

        .saved {
          opacity: 1;
        }
      `]}_yamlChanged(){if(!this._generation){return}this._changed=!this.yamlEditor.codemirror.isClean(this._generation);if(this._changed&&!window.onbeforeunload){window.onbeforeunload=()=>{return!0}}else if(!this._changed&&window.onbeforeunload){window.onbeforeunload=null}}_closeEditor(){if(this._changed){if(!confirm("You have unsaved changes, are you sure you want to exit?")){return}}window.onbeforeunload=null;if(this.closeEditor){this.closeEditor()}}async _handleSave(){this._saving=!0;if(this.yamlEditor.hasComments){if(!confirm("Your config contains comment(s), these will not be saved. Do you want to continue?")){return}}let value;try{value=js_yaml__WEBPACK_IMPORTED_MODULE_2___default.a.safeLoad(this.yamlEditor.value)}catch(err){alert(`Unable to parse YAML: ${err}`);this._saving=!1;return}try{value=lovelaceStruct(value)}catch(err){alert(`Your config is not valid: ${err}`);return}try{await this.lovelace.saveConfig(value)}catch(err){alert(`Unable to save YAML: ${err}`)}this._generation=this.yamlEditor.codemirror.changeGeneration(!0);window.onbeforeunload=null;this._saving=!1;this._changed=!1}get yamlEditor(){return this.shadowRoot.querySelector("hui-yaml-editor")}}customElements.define("hui-editor",LovelaceFullConfigEditor)}}]);
//# sourceMappingURL=c679891f52dd82b0ed08.chunk.js.map