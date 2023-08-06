(window.webpackJsonp=window.webpackJsonp||[]).push([[67],{163:function(e,t,s){"use strict";var r=s(180);t.a=(e=>void 0===e.attributes.friendly_name?Object(r.a)(e.entity_id).replace(/_/g," "):e.attributes.friendly_name||"")},167:function(e,t,s){"use strict";s.d(t,"a",function(){return o});var r=s(112);const a={alert:"hass:alert",automation:"hass:playlist-play",calendar:"hass:calendar",camera:"hass:video",climate:"hass:thermostat",configurator:"hass:settings",conversation:"hass:text-to-speech",device_tracker:"hass:account",fan:"hass:fan",group:"hass:google-circles-communities",history_graph:"hass:chart-line",homeassistant:"hass:home-assistant",homekit:"hass:home-automation",image_processing:"hass:image-filter-frames",input_boolean:"hass:drawing",input_datetime:"hass:calendar-clock",input_number:"hass:ray-vertex",input_select:"hass:format-list-bulleted",input_text:"hass:textbox",light:"hass:lightbulb",mailbox:"hass:mailbox",notify:"hass:comment-alert",person:"hass:account",plant:"hass:flower",proximity:"hass:apple-safari",remote:"hass:remote",scene:"hass:google-pages",script:"hass:file-document",sensor:"hass:eye",simple_alarm:"hass:bell",sun:"hass:white-balance-sunny",switch:"hass:flash",timer:"hass:timer",updater:"hass:cloud-upload",vacuum:"hass:robot-vacuum",water_heater:"hass:thermometer",weblink:"hass:open-in-new"};function o(e,t){if(e in a)return a[e];switch(e){case"alarm_control_panel":switch(t){case"armed_home":return"hass:bell-plus";case"armed_night":return"hass:bell-sleep";case"disarmed":return"hass:bell-outline";case"triggered":return"hass:bell-ring";default:return"hass:bell"}case"binary_sensor":return t&&"off"===t?"hass:radiobox-blank":"hass:checkbox-marked-circle";case"cover":return"closed"===t?"hass:window-closed":"hass:window-open";case"lock":return t&&"unlocked"===t?"hass:lock-open":"hass:lock";case"media_player":return t&&"off"!==t&&"idle"!==t?"hass:cast-connected":"hass:cast";case"zwave":switch(t){case"dead":return"hass:emoticon-dead";case"sleeping":return"hass:sleep";case"initializing":return"hass:timer-sand";default:return"hass:z-wave"}default:return console.warn("Unable to find icon for domain "+e+" ("+t+")"),r.a}}},168:function(e,t,s){"use strict";s.d(t,"a",function(){return o});s(101);const r=customElements.get("iron-icon");let a=!1;class o extends r{constructor(...e){super(...e),this._iconsetName=void 0}listen(e,t,r){super.listen(e,t,r),a||"mdi"!==this._iconsetName||(a=!0,s.e(59).then(s.bind(null,208)))}}customElements.define("ha-icon",o)},169:function(e,t,s){"use strict";function r(e){return e.substr(0,e.indexOf("."))}s.d(t,"a",function(){return r})},180:function(e,t,s){"use strict";function r(e){return e.substr(e.indexOf(".")+1)}s.d(t,"a",function(){return r})},181:function(e,t,s){"use strict";var r=s(5);function a(e){var t,s=c(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:s,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function o(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function i(e){return e.decorators&&e.decorators.length}function n(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function l(e,t){var s=e[t];if(void 0!==s&&"function"!=typeof s)throw new TypeError("Expected '"+t+"' to be a function");return s}function c(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var s=e[Symbol.toPrimitive];if(void 0!==s){var r=s.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}let d=function(e,t,s,r){var d=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(s){t.forEach(function(t){t.kind===s&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var s=e.prototype;["method","field"].forEach(function(r){t.forEach(function(t){var a=t.placement;if(t.kind===r&&("static"===a||"prototype"===a)){var o="static"===a?e:s;this.defineClassElement(o,t)}},this)},this)},defineClassElement:function(e,t){var s=t.descriptor;if("field"===t.kind){var r=t.initializer;s={enumerable:s.enumerable,writable:s.writable,configurable:s.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,s)},decorateClass:function(e,t){var s=[],r=[],a={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,a)},this),e.forEach(function(e){if(!i(e))return s.push(e);var t=this.decorateElement(e,a);s.push(t.element),s.push.apply(s,t.extras),r.push.apply(r,t.finishers)},this),!t)return{elements:s,finishers:r};var o=this.decorateConstructor(s,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,s){var r=t[e.placement];if(!s&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var s=[],r=[],a=e.decorators,o=a.length-1;o>=0;o--){var i=t[e.placement];i.splice(i.indexOf(e.key),1);var n=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,a[o])(n)||n);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);s.push.apply(s,c)}}return{element:e,finishers:r,extras:s}},decorateConstructor:function(e,t){for(var s=[],r=t.length-1;r>=0;r--){var a=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(a)||a);if(void 0!==o.finisher&&s.push(o.finisher),void 0!==o.elements){e=o.elements;for(var i=0;i<e.length-1;i++)for(var n=i+1;n<e.length;n++)if(e[i].key===e[n].key&&e[i].placement===e[n].placement)throw new TypeError("Duplicated element ("+e[i].key+")")}}return{elements:e,finishers:s}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var s=c(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var a=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:s,placement:r,descriptor:Object.assign({},a)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(a,"get","The property descriptor of a field descriptor"),this.disallowProperty(a,"set","The property descriptor of a field descriptor"),this.disallowProperty(a,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),s=l(e,"finisher"),r=this.toElementDescriptors(e.extras);return{element:t,finisher:s,extras:r}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var s=l(e,"finisher"),r=this.toElementDescriptors(e.elements);return{elements:r,finisher:s}},runClassFinishers:function(e,t){for(var s=0;s<t.length;s++){var r=(0,t[s])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,s){if(void 0!==e[t])throw new TypeError(s+" can't have a ."+t+" property.")}};return e}();if(r)for(var p=0;p<r.length;p++)d=r[p](d);var u=t(function(e){d.initializeInstanceElements(e,h.elements)},s),h=d.decorateClass(function(e){for(var t=[],s=function(e){return"method"===e.kind&&e.key===l.key&&e.placement===l.placement},r=0;r<e.length;r++){var a,l=e[r];if("method"===l.kind&&(a=t.find(s)))if(n(l.descriptor)||n(a.descriptor)){if(i(l)||i(a))throw new ReferenceError("Duplicated methods ("+l.key+") can't be decorated.");a.descriptor=l.descriptor}else{if(i(l)){if(i(a))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+l.key+").");a.decorators=l.decorators}o(l,a)}else t.push(l)}return t}(u.d.map(a)),e);return d.initializeClassElements(u.F,h.elements),d.runClassFinishers(u.F,h.finishers)}(null,function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[Object(r.f)()],key:"header",value:void 0},{kind:"get",static:!0,key:"styles",value:function(){return r.c`
      :host {
        background: var(
          --ha-card-background,
          var(--paper-card-background-color, white)
        );
        border-radius: var(--ha-card-border-radius, 2px);
        box-shadow: var(
          --ha-card-box-shadow,
          0 2px 2px 0 rgba(0, 0, 0, 0.14),
          0 1px 5px 0 rgba(0, 0, 0, 0.12),
          0 3px 1px -2px rgba(0, 0, 0, 0.2)
        );
        color: var(--primary-text-color);
        display: block;
        transition: all 0.3s ease-out;
      }
      .header:not(:empty) {
        font-size: 24px;
        letter-spacing: -0.012em;
        line-height: 32px;
        opacity: 0.87;
        padding: 24px 16px 16px;
      }
    `}},{kind:"method",key:"render",value:function(){return r.e`
      <div class="header">${this.header}</div>
      <slot></slot>
    `}}]}},r.a);customElements.define("ha-card",d)},182:function(e,t,s){"use strict";var r=s(3),a=s(24);s(85);customElements.define("ha-config-section",class extends a.a{static get template(){return r.a`
      <style include="iron-flex ha-style">
        .content {
          padding: 28px 20px 0;
          max-width: 1040px;
          margin: 0 auto;
        }

        .header {
          @apply --paper-font-display1;
          opacity: var(--dark-primary-opacity);
        }

        .together {
          margin-top: 32px;
        }

        .intro {
          @apply --paper-font-subhead;
          width: 100%;
          max-width: 400px;
          margin-right: 40px;
          opacity: var(--dark-primary-opacity);
        }

        .panel {
          margin-top: -24px;
        }

        .panel ::slotted(*) {
          margin-top: 24px;
          display: block;
        }

        .narrow.content {
          max-width: 640px;
        }
        .narrow .together {
          margin-top: 20px;
        }
        .narrow .header {
          @apply --paper-font-headline;
        }
        .narrow .intro {
          font-size: 14px;
          padding-bottom: 20px;
          margin-right: 0;
          max-width: 500px;
        }
      </style>
      <div class$="[[computeContentClasses(isWide)]]">
        <div class="header"><slot name="header"></slot></div>
        <div class$="[[computeClasses(isWide)]]">
          <div class="intro"><slot name="introduction"></slot></div>
          <div class="panel flex-auto"><slot></slot></div>
        </div>
      </div>
    `}static get properties(){return{hass:{type:Object},narrow:{type:Boolean},showMenu:{type:Boolean,value:!1},isWide:{type:Boolean,value:!1}}}computeContentClasses(e){return e?"content ":"content narrow"}computeClasses(e){return"together layout "+(e?"horizontal":"vertical narrow")}})},183:function(e,t,s){"use strict";var r=s(112),a=s(169),o=s(167);const i={humidity:"hass:water-percent",illuminance:"hass:brightness-5",temperature:"hass:thermometer",pressure:"hass:gauge"};s.d(t,"a",function(){return l});const n={binary_sensor:function(e){const t=e.state&&"off"===e.state;switch(e.attributes.device_class){case"battery":return t?"hass:battery":"hass:battery-outline";case"cold":return t?"hass:thermometer":"hass:snowflake";case"connectivity":return t?"hass:server-network-off":"hass:server-network";case"door":return t?"hass:door-closed":"hass:door-open";case"garage_door":return t?"hass:garage":"hass:garage-open";case"gas":case"power":case"problem":case"safety":case"smoke":return t?"hass:shield-check":"hass:alert";case"heat":return t?"hass:thermometer":"hass:fire";case"light":return t?"hass:brightness-5":"hass:brightness-7";case"lock":return t?"hass:lock":"hass:lock-open";case"moisture":return t?"hass:water-off":"hass:water";case"motion":return t?"hass:walk":"hass:run";case"occupancy":return t?"hass:home-outline":"hass:home";case"opening":return t?"hass:square":"hass:square-outline";case"plug":return t?"hass:power-plug-off":"hass:power-plug";case"presence":return t?"hass:home-outline":"hass:home";case"sound":return t?"hass:music-note-off":"hass:music-note";case"vibration":return t?"hass:crop-portrait":"hass:vibrate";case"window":return t?"hass:window-closed":"hass:window-open";default:return t?"hass:radiobox-blank":"hass:checkbox-marked-circle"}},cover:function(e){const t="closed"!==e.state;switch(e.attributes.device_class){case"garage":return t?"hass:garage-open":"hass:garage";default:return Object(o.a)("cover",e.state)}},sensor:function(e){const t=e.attributes.device_class;if(t&&t in i)return i[t];if("battery"===t){const t=Number(e.state);if(isNaN(t))return"hass:battery-unknown";const s=10*Math.round(t/10);return s>=100?"hass:battery":s<=0?"hass:battery-alert":`hass:battery-${s}`}const s=e.attributes.unit_of_measurement;return s===r.j||s===r.k?"hass:thermometer":Object(o.a)("sensor")},input_datetime:function(e){return e.attributes.has_date?e.attributes.has_time?Object(o.a)("input_datetime"):"hass:calendar":"hass:clock"}};function l(e){if(!e)return r.a;if(e.attributes.icon)return e.attributes.icon;const t=Object(a.a)(e.entity_id);return t in n?n[t](e):Object(o.a)(t,e.state)}},191:function(e,t,s){"use strict";var r=s(185);t.a=function(){try{(new Date).toLocaleString("i")}catch(e){return"RangeError"===e.name}return!1}()?(e,t)=>e.toLocaleString(t,{year:"numeric",month:"long",day:"numeric",hour:"numeric",minute:"2-digit"}):e=>r.a.format(e,"haDateTime")},215:function(e,t,s){"use strict";s(73),s(175);var r=s(3),a=s(24);customElements.define("ha-progress-button",class extends a.a{static get template(){return r.a`
      <style>
        .container {
          position: relative;
          display: inline-block;
        }

        mwc-button {
          transition: all 1s;
        }

        .success mwc-button {
          --mdc-theme-primary: white;
          background-color: var(--google-green-500);
          transition: none;
        }

        .error mwc-button {
          --mdc-theme-primary: white;
          background-color: var(--google-red-500);
          transition: none;
        }

        .progress {
          @apply --layout;
          @apply --layout-center-center;
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
        }
      </style>
      <div class="container" id="container">
        <mwc-button
          id="button"
          disabled="[[computeDisabled(disabled, progress)]]"
          on-click="buttonTapped"
        >
          <slot></slot>
        </mwc-button>
        <template is="dom-if" if="[[progress]]">
          <div class="progress"><paper-spinner active=""></paper-spinner></div>
        </template>
      </div>
    `}static get properties(){return{hass:{type:Object},progress:{type:Boolean,value:!1},disabled:{type:Boolean,value:!1}}}tempClass(e){var t=this.$.container.classList;t.add(e),setTimeout(()=>{t.remove(e)},1e3)}ready(){super.ready(),this.addEventListener("click",e=>this.buttonTapped(e))}buttonTapped(e){this.progress&&e.stopPropagation()}actionSuccess(){this.tempClass("success")}actionError(){this.tempClass("error")}computeDisabled(e,t){return e||t}})},224:function(e,t,s){"use strict";s(101);var r=s(168);customElements.define("ha-icon-next",class extends r.a{connectedCallback(){this.icon="ltr"===window.getComputedStyle(this).direction?"hass:chevron-right":"hass:chevron-left",super.connectedCallback()}})},283:function(e,t,s){"use strict";var r=s(5),a=(s(215),s(45));customElements.define("ha-call-api-button",class extends r.a{render(){return r.e`
      <ha-progress-button
        .progress="${this.progress}"
        @click="${this._buttonTapped}"
        ?disabled="${this.disabled}"
        ><slot></slot
      ></ha-progress-button>
    `}constructor(){super(),this.method="POST",this.data={},this.disabled=!1,this.progress=!1}static get properties(){return{hass:{},progress:Boolean,path:String,method:String,data:{},disabled:Boolean}}get progressButton(){return this.renderRoot.querySelector("ha-progress-button")}async _buttonTapped(){this.progress=!0;const e={method:this.method,path:this.path,data:this.data};try{const t=await this.hass.callApi(this.method,this.path,this.data);this.progress=!1,this.progressButton.actionSuccess(),e.success=!0,e.response=t}catch(t){this.progress=!1,this.progressButton.actionError(),e.success=!1,e.response=t}Object(a.a)(this,"hass-api-called",e)}})},385:function(e,t,s){"use strict";var r=s(3),a=s(24),o=(s(168),s(183));customElements.define("ha-state-icon",class extends a.a{static get template(){return r.a`
      <ha-icon icon="[[computeIcon(stateObj)]]"></ha-icon>
    `}static get properties(){return{stateObj:{type:Object}}}computeIcon(e){return Object(o.a)(e)}})},726:function(e,t,s){"use strict";s.r(t);s(146);var r=s(11),a=s(19),o=s(3),i=s(24),n=(s(182),s(73),s(164),s(170),s(198),s(283),s(143),s(85),s(5));s(131),s(175),s(181);const l=e=>e.callWS({type:"webhook/list"}),c=(e,t)=>e.callWS({type:"cloud/cloudhook/create",webhook_id:t}),d=(e,t)=>e.callWS({type:"cloud/cloudhook/delete",webhook_id:t}),p=e=>e.callWS({type:"cloud/subscription"}),u=(e,t)=>e.callWS(Object.assign({type:"cloud/update_prefs"},t));var h=s(45);const m=(e,t)=>{Object(h.a)(e,"show-dialog",{dialogTag:"cloud-webhook-manage-dialog",dialogImport:()=>Promise.all([s.e(1),s.e(15)]).then(s.bind(null,779)),dialogParams:t})};function f(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var s=e[Symbol.toPrimitive];if(void 0!==s){var r=s.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}customElements.define("cloud-webhooks",class extends n.a{static get properties(){return{hass:{},cloudStatus:{},_cloudHooks:{},_localHooks:{},_progress:{}}}constructor(){super(),this.hass=void 0,this.cloudStatus=void 0,this._cloudHooks=void 0,this._localHooks=void 0,this._progress=void 0,this._progress=[]}connectedCallback(){super.connectedCallback(),this._fetchData()}render(){return n.e`
      ${this.renderStyle()}
      <ha-card header="Webhooks">
        <div class="body">
          Anything that is configured to be triggered by a webhook can be given
          a publicly accessible URL to allow you to send data back to Home
          Assistant from anywhere, without exposing your instance to the
          internet.
        </div>

        ${this._renderBody()}

        <div class="footer">
          <a href="https://www.nabucasa.com/config/webhooks" target="_blank">
            Learn more about creating webhook-powered automations.
          </a>
        </div>
      </ha-card>
    `}updated(e){super.updated(e),e.has("cloudStatus")&&this.cloudStatus&&(this._cloudHooks=this.cloudStatus.prefs.cloudhooks||{})}_renderBody(){return this.cloudStatus&&this._localHooks&&this._cloudHooks?0===this._localHooks.length?n.e`
        <div class="body-text">
          Looks like you have no webhooks yet. Get started by configuring a
          <a href="/config/integrations">webhook-based integration</a> or by
          creating a <a href="/config/automation/new">webhook automation</a>.
        </div>
      `:this._localHooks.map(e=>n.e`
        <div class="webhook" .entry="${e}">
          <paper-item-body two-line>
            <div>
              ${e.name}
              ${e.domain===e.name.toLowerCase()?"":` (${e.domain})`}
            </div>
            <div secondary>${e.webhook_id}</div>
          </paper-item-body>
          ${this._progress.includes(e.webhook_id)?n.e`
                <div class="progress">
                  <paper-spinner active></paper-spinner>
                </div>
              `:this._cloudHooks[e.webhook_id]?n.e`
                <mwc-button @click="${this._handleManageButton}">
                  Manage
                </mwc-button>
              `:n.e`
                <paper-toggle-button
                  @click="${this._enableWebhook}"
                ></paper-toggle-button>
              `}
        </div>
      `):n.e`
        <div class="body-text">Loading…</div>
      `}_showDialog(e){const t=this._localHooks.find(t=>t.webhook_id===e),s=this._cloudHooks[e];m(this,{webhook:t,cloudhook:s,disableHook:()=>this._disableWebhook(e)})}_handleManageButton(e){const t=e.currentTarget.parentElement.entry;this._showDialog(t.webhook_id)}async _enableWebhook(e){const t=e.currentTarget.parentElement.entry;let s;this._progress=[...this._progress,t.webhook_id];try{s=await c(this.hass,t.webhook_id)}catch(e){return void alert(e.message)}finally{this._progress=this._progress.filter(e=>e!==t.webhook_id)}this._cloudHooks=Object.assign({},this._cloudHooks,{[t.webhook_id]:s}),0===this._progress.length&&this._showDialog(t.webhook_id)}async _disableWebhook(e){this._progress=[...this._progress,e];try{await d(this.hass,e)}catch(e){return void alert(`Failed to disable webhook: ${e.message}`)}finally{this._progress=this._progress.filter(t=>t!==e)}const t=function(e,t){if(null==e)return{};var s,r,a={},o=Object.keys(e);for(r=0;r<o.length;r++)s=o[r],t.indexOf(s)>=0||(a[s]=e[s]);return a}(this._cloudHooks,[e].map(f));this._cloudHooks=t}async _fetchData(){this._localHooks=this.hass.config.components.includes("webhook")?await l(this.hass):[]}renderStyle(){return n.e`
      <style>
        .body {
          padding: 0 16px 8px;
        }
        .body-text {
          padding: 0 16px;
        }
        .webhook {
          display: flex;
          padding: 4px 16px;
        }
        .progress {
          margin-right: 16px;
          display: flex;
          flex-direction: column;
          justify-content: center;
        }
        .footer {
          padding: 16px;
        }
        .body-text a,
        .footer a {
          color: var(--primary-color);
        }
      </style>
    `}});var g=s(191),b=s(84),y=s(110),v=s(323),w=(s(250),s(385),s(163)),k=s(169);const _=(e,t,s,r)=>{const a=new Set(e),o=new Set(t),i=new Set(s),n=new Set(r),l=a.size>0||o.size>0,c=i.size>0||n.size>0;return l||c?l&&!c?e=>o.has(e)||a.has(Object(k.a)(e)):!l&&c?e=>!n.has(e)&&!i.has(Object(k.a)(e)):a.size?e=>a.has(Object(k.a)(e))?!n.has(e):o.has(e):i.size?e=>i.has(Object(k.a)(e))?o.has(e):!n.has(e):e=>o.has(e):()=>!0};customElements.define("cloud-exposed-entities",class extends n.a{constructor(...e){super(...e),this.hass=void 0,this.filter=void 0,this.supportedDomains=void 0,this._filterFunc=void 0}static get properties(){return{hass:{},filter:{},supportedDomains:{},_filterFunc:{}}}render(){if(!this._filterFunc)return n.e``;const e=[];return Object.keys(this.hass.states).forEach(t=>{if(this._filterFunc(t)){const s=this.hass.states[t];e.push([Object(w.a)(s),s])}}),e.sort(),n.e`
      ${this.renderStyle()}
      ${Object(v.a)(e,e=>e[1].entity_id,e=>n.e`
          <span>
            <ha-state-icon
              .stateObj="${e[1]}"
              @click="${this._handleMoreInfo}"
            ></ha-state-icon>
            <paper-tooltip position="bottom">${e[0]}</paper-tooltip>
          </span>
        `)}
    `}updated(e){if(super.updated(e),e.has("filter")&&e.get("filter")!==this.filter){const e=this.filter,t=_(e.include_domains,e.include_entities,e.exclude_domains,e.exclude_entities),s=new Set(this.supportedDomains);this._filterFunc=(e=>{const r=e.split(".")[0];return s.has(r)&&t(e)})}}_handleMoreInfo(e){Object(h.a)(this,"hass-more-info",{entityId:e.currentTarget.stateObj.entity_id})}renderStyle(){return n.e`
      <style>
        ha-state-icon {
          color: var(--primary-text-color);
          cursor: pointer;
        }
      </style>
    `}});customElements.define("cloud-alexa-pref",class extends n.a{constructor(...e){super(...e),this.hass=void 0,this.cloudStatus=void 0}static get properties(){return{hass:{},cloudStatus:{}}}render(){if(!this.cloudStatus)return n.e``;const e=this.cloudStatus.prefs.alexa_enabled;return n.e`
      <paper-card heading="Alexa">
        <paper-toggle-button
          .checked="${e}"
          @change="${this._toggleChanged}"
        ></paper-toggle-button>
        <div class="card-content">
          With the Alexa integration for Home Assistant Cloud you'll be able to
          control all your Home Assistant devices via any Alexa-enabled device.
          <ul>
            <li>
              To activate, search in the Alexa app for the Home Assistant Smart
              Home skill.
            </li>
            <li>
              <a
                href="https://www.nabucasa.com/config/amazon_alexa/"
                target="_blank"
              >
                Config documentation
              </a>
            </li>
          </ul>
          <em
            >This integration requires an Alexa-enabled device like the Amazon
            Echo.</em
          >
          ${e?n.e`
                <p>Exposed entities:</p>
                <cloud-exposed-entities
                  .hass="${this.hass}"
                  .filter="${this.cloudStatus.alexa_entities}"
                  .supportedDomains="${this.cloudStatus.alexa_domains}"
                ></cloud-exposed-entities>
              `:""}
        </div>
      </paper-card>
    `}async _toggleChanged(e){const t=e.target;try{await u(this.hass,{alexa_enabled:t.checked}),Object(h.a)(this,"ha-refresh-cloud-status")}catch(e){t.checked=!t.checked}}static get styles(){return n.c`
      a {
        color: var(--primary-color);
      }
      paper-card > paper-toggle-button {
        position: absolute;
        right: 8px;
        top: 16px;
      }
    `}});function x(e){var t,s=P(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:s,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function E(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function S(e){return e.decorators&&e.decorators.length}function C(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function A(e,t){var s=e[t];if(void 0!==s&&"function"!=typeof s)throw new TypeError("Expected '"+t+"' to be a function");return s}function P(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var s=e[Symbol.toPrimitive];if(void 0!==s){var r=s.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}customElements.define("cloud-google-pref",class extends n.a{constructor(...e){super(...e),this.hass=void 0,this.cloudStatus=void 0}static get properties(){return{hass:{},cloudStatus:{}}}render(){if(!this.cloudStatus)return n.e``;const{google_enabled:e,google_allow_unlock:t}=this.cloudStatus.prefs;return n.e`
      <paper-card heading="Google Assistant">
        <paper-toggle-button
          id="google_enabled"
          .checked="${e}"
          @change="${this._toggleChanged}"
        ></paper-toggle-button>
        <div class="card-content">
          With the Google Assistant integration for Home Assistant Cloud you'll
          be able to control all your Home Assistant devices via any Google
          Assistant-enabled device.
          <ul>
            <li>
              <a
                href="https://assistant.google.com/services/a/uid/00000091fd5fb875?hl=en-US"
                target="_blank"
              >
                Activate the Home Assistant skill for Google Assistant
              </a>
            </li>
            <li>
              <a
                href="https://www.nabucasa.com/config/google_assistant/"
                target="_blank"
              >
                Config documentation
              </a>
            </li>
          </ul>
          <em
            >This integration requires a Google Assistant-enabled device like
            the Google Home or Android phone.</em
          >
          ${e?n.e`
                <div class="unlock">
                  <div>Allow unlocking locks</div>
                  <paper-toggle-button
                    id="google_allow_unlock"
                    .checked="${t}"
                    @change="${this._toggleChanged}"
                  ></paper-toggle-button>
                </div>
                <p>Exposed entities:</p>
                <cloud-exposed-entities
                  .hass="${this.hass}"
                  .filter="${this.cloudStatus.google_entities}"
                  .supportedDomains="${this.cloudStatus.google_domains}"
                ></cloud-exposed-entities>
              `:""}
        </div>
        <div class="card-actions">
          <ha-call-api-button
            .hass="${this.hass}"
            .disabled="${!e}"
            path="cloud/google_actions/sync"
            >Sync devices</ha-call-api-button
          >
        </div>
      </paper-card>
    `}async _toggleChanged(e){const t=e.target;try{await u(this.hass,{[t.id]:t.checked}),Object(h.a)(this,"ha-refresh-cloud-status")}catch(e){t.checked=!t.checked}}static get styles(){return n.c`
      a {
        color: var(--primary-color);
      }
      paper-card > paper-toggle-button {
        position: absolute;
        right: 8px;
        top: 16px;
      }
      ha-call-api-button {
        color: var(--primary-color);
        font-weight: 500;
      }
      .unlock {
        display: flex;
        flex-direction: row;
        padding-top: 16px;
      }
      .unlock > div {
        flex: 1;
      }
    `}});!function(e,t,s,r){var a=function(){var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach(function(s){t.forEach(function(t){t.kind===s&&"own"===t.placement&&this.defineClassElement(e,t)},this)},this)},initializeClassElements:function(e,t){var s=e.prototype;["method","field"].forEach(function(r){t.forEach(function(t){var a=t.placement;if(t.kind===r&&("static"===a||"prototype"===a)){var o="static"===a?e:s;this.defineClassElement(o,t)}},this)},this)},defineClassElement:function(e,t){var s=t.descriptor;if("field"===t.kind){var r=t.initializer;s={enumerable:s.enumerable,writable:s.writable,configurable:s.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,s)},decorateClass:function(e,t){var s=[],r=[],a={static:[],prototype:[],own:[]};if(e.forEach(function(e){this.addElementPlacement(e,a)},this),e.forEach(function(e){if(!S(e))return s.push(e);var t=this.decorateElement(e,a);s.push(t.element),s.push.apply(s,t.extras),r.push.apply(r,t.finishers)},this),!t)return{elements:s,finishers:r};var o=this.decorateConstructor(s,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,s){var r=t[e.placement];if(!s&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var s=[],r=[],a=e.decorators,o=a.length-1;o>=0;o--){var i=t[e.placement];i.splice(i.indexOf(e.key),1);var n=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,a[o])(n)||n);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);s.push.apply(s,c)}}return{element:e,finishers:r,extras:s}},decorateConstructor:function(e,t){for(var s=[],r=t.length-1;r>=0;r--){var a=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(a)||a);if(void 0!==o.finisher&&s.push(o.finisher),void 0!==o.elements){e=o.elements;for(var i=0;i<e.length-1;i++)for(var n=i+1;n<e.length;n++)if(e[i].key===e[n].key&&e[i].placement===e[n].placement)throw new TypeError("Duplicated element ("+e[i].key+")")}}return{elements:e,finishers:s}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if(Symbol.iterator in Object(e)||"[object Arguments]"===Object.prototype.toString.call(e))return Array.from(e)}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance")}()).map(function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t},this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var s=P(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var a=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:s,placement:r,descriptor:Object.assign({},a)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(a,"get","The property descriptor of a field descriptor"),this.disallowProperty(a,"set","The property descriptor of a field descriptor"),this.disallowProperty(a,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){var t=this.toElementDescriptor(e),s=A(e,"finisher"),r=this.toElementDescriptors(e.extras);return{element:t,finisher:s,extras:r}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var s=A(e,"finisher"),r=this.toElementDescriptors(e.elements);return{elements:r,finisher:s}},runClassFinishers:function(e,t){for(var s=0;s<t.length;s++){var r=(0,t[s])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,s){if(void 0!==e[t])throw new TypeError(s+" can't have a ."+t+" property.")}};return e}();if(r)for(var o=0;o<r.length;o++)a=r[o](a);var i=t(function(e){a.initializeInstanceElements(e,n.elements)},s),n=a.decorateClass(function(e){for(var t=[],s=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var a,o=e[r];if("method"===o.kind&&(a=t.find(s)))if(C(o.descriptor)||C(a.descriptor)){if(S(o)||S(a))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");a.descriptor=o.descriptor}else{if(S(o)){if(S(a))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");a.decorators=o.decorators}E(o,a)}else t.push(o)}return t}(i.d.map(x)),e);a.initializeClassElements(i.F,n.elements),a.runClassFinishers(i.F,n.finishers)}([Object(n.d)("cloud-remote-pref")],function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",key:"hass",value:void 0},{kind:"field",key:"cloudStatus",value:void 0},{kind:"get",static:!0,key:"properties",value:function(){return{hass:{},cloudStatus:{}}}},{kind:"method",key:"render",value:function(){if(!this.cloudStatus)return n.e``;const{remote_connected:e,remote_domain:t,remote_certificate:s}=this.cloudStatus;return s?n.e`
      <paper-card heading="Remote Control">
        <paper-toggle-button
          .checked="${e}"
          @change="${this._toggleChanged}"
        ></paper-toggle-button>
        <div class="card-content">
          Home Assistant Cloud provides you with a secure remote connection to
          your instance while away from home. Your instance
          ${e?"is":"will be"} available at
          <a href="https://${t}" target="_blank">
            https://${t}</a
          >.
          ${s?n.e`
                <div class="data-row">
                  <paper-item-body two-line>
                    Certificate expiration date
                    <div secondary>Will be automatically renewed</div>
                  </paper-item-body>
                  <div class="data-value">
                    ${Object(g.a)(new Date(s.expire_date),this.hass.language)}
                  </div>
                </div>
                <div class="data-row">
                  <paper-item-body>
                    Certificate fingerprint
                  </paper-item-body>
                  <div class="data-value">
                    ${s.fingerprint}
                  </div>
                </div>
              `:""}
        </div>
        <div class="card-actions">
          <a href="https://www.nabucasa.com/config/remote/" target="_blank">
            <mwc-button>Learn how it works</mwc-button>
          </a>
        </div>
      </paper-card>
    `:n.e`
        <paper-card heading="Remote Control">
          <div class="preparing">
            Remote access is being prepared. We will notify you when it's ready.
          </div>
        </paper-card>
      `}},{kind:"method",key:"_toggleChanged",value:async function(e){const t=e.target;try{t.checked?await(e=>e.callWS({type:"cloud/remote/connect"}))(this.hass):await(e=>e.callWS({type:"cloud/remote/disconnect"}))(this.hass),Object(h.a)(this,"ha-refresh-cloud-status")}catch(e){t.checked=!t.checked}}},{kind:"get",static:!0,key:"styles",value:function(){return n.c`
      paper-card {
        display: block;
      }
      .preparing {
        padding: 0 16px 16px;
      }
      .data-row {
        display: flex;
      }
      .data-value {
        padding: 16px 0;
      }
      a {
        color: var(--primary-color);
      }
      paper-card > paper-toggle-button {
        position: absolute;
        right: 8px;
        top: 16px;
      }
      ha-call-api-button {
        color: var(--primary-color);
        font-weight: 500;
      }
      .unlock {
        display: flex;
        flex-direction: row;
        padding-top: 16px;
      }
      .unlock > div {
        flex: 1;
      }
    `}}]}},n.a);let j=!1;customElements.define("ha-config-cloud-account",class extends(Object(b.a)(Object(y.a)(i.a))){static get template(){return o.a`
      <style include="iron-flex ha-style">
        [slot="introduction"] {
          margin: -1em 0;
        }
        [slot="introduction"] a {
          color: var(--primary-color);
        }
        .content {
          padding-bottom: 24px;
          direction: ltr;
        }
        paper-card {
          display: block;
        }
        .account-row {
          display: flex;
          padding: 0 16px;
        }
        mwc-button {
          align-self: center;
        }
        .soon {
          font-style: italic;
          margin-top: 24px;
          text-align: center;
        }
        .nowrap {
          white-space: nowrap;
        }
        .wrap {
          white-space: normal;
        }
        .status {
          text-transform: capitalize;
          padding: 16px;
        }
        a {
          color: var(--primary-color);
        }
      </style>
      <hass-subpage header="Home Assistant Cloud">
        <div class="content">
          <ha-config-section is-wide="[[isWide]]">
            <span slot="header">Home Assistant Cloud</span>
            <div slot="introduction">
              <p>
                Thank you for being part of Home Assistant Cloud. It's because
                of people like you that we are able to make a great home
                automation experience for everyone. Thank you!
              </p>
            </div>

            <paper-card heading="Nabu Casa Account">
              <div class="account-row">
                <paper-item-body two-line="">
                  [[cloudStatus.email]]
                  <div secondary class="wrap">
                    [[_formatSubscription(_subscription)]]
                  </div>
                </paper-item-body>
              </div>

              <div class="account-row">
                <paper-item-body> Cloud connection status </paper-item-body>
                <div class="status">[[cloudStatus.cloud]]</div>
              </div>

              <div class="card-actions">
                <a href="https://account.nabucasa.com" target="_blank"
                  ><mwc-button>Manage Account</mwc-button></a
                >
                <mwc-button style="float: right" on-click="handleLogout"
                  >Sign out</mwc-button
                >
              </div>
            </paper-card>
          </ha-config-section>

          <ha-config-section is-wide="[[isWide]]">
            <span slot="header">Integrations</span>
            <div slot="introduction">
              <p>
                Integrations for Home Assistant Cloud allow you to connect with
                services in the cloud without having to expose your Home
                Assistant instance publicly on the internet.
              </p>
              <p>
                Check the website for
                <a href="https://www.nabucasa.com" target="_blank"
                  >all available features</a
                >.
              </p>
            </div>

            <cloud-remote-pref
              hass="[[hass]]"
              cloud-status="[[cloudStatus]]"
            ></cloud-remote-pref>

            <cloud-alexa-pref
              hass="[[hass]]"
              cloud-status="[[cloudStatus]]"
            ></cloud-alexa-pref>

            <cloud-google-pref
              hass="[[hass]]"
              cloud-status="[[cloudStatus]]"
            ></cloud-google-pref>

            <cloud-webhooks
              hass="[[hass]]"
              cloud-status="[[cloudStatus]]"
            ></cloud-webhooks>
          </ha-config-section>
        </div>
      </hass-subpage>
    `}static get properties(){return{hass:Object,isWide:Boolean,cloudStatus:Object,_subscription:{type:Object,value:null}}}ready(){super.ready(),this._fetchSubscriptionInfo()}connectedCallback(){super.connectedCallback(),j||(j=!0,Object(h.a)(this,"register-dialog",{dialogShowEvent:"manage-cloud-webhook",dialogTag:"cloud-webhook-manage-dialog",dialogImport:()=>Promise.all([s.e(1),s.e(15)]).then(s.bind(null,779))}))}_computeRemoteConnected(e){return e?"Connected":"Not Connected"}async _fetchSubscriptionInfo(){this._subscription=await p(this.hass),this._subscription.provider&&this.cloudStatus&&"connected"!==this.cloudStatus.cloud&&this.fire("ha-refresh-cloud-status")}handleLogout(){this.hass.callApi("post","cloud/logout").then(()=>this.fire("ha-refresh-cloud-status"))}_formatSubscription(e){if(null===e)return"Fetching subscription…";let t=e.human_description;return e.plan_renewal_date&&(t=t.replace("{periodEnd}",Object(g.a)(new Date(1e3*e.plan_renewal_date),this.hass.language))),t}});s(83),s(215);customElements.define("ha-config-cloud-forgot-password",class extends(Object(b.a)(i.a)){static get template(){return o.a`
      <style include="iron-flex ha-style">
        .content {
          padding-bottom: 24px;
          direction: ltr;
        }

        paper-card {
          display: block;
          max-width: 600px;
          margin: 0 auto;
          margin-top: 24px;
        }
        h1 {
          @apply --paper-font-headline;
          margin: 0;
        }
        .error {
          color: var(--google-red-500);
        }
        .card-actions {
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        .card-actions a {
          color: var(--primary-text-color);
        }
        [hidden] {
          display: none;
        }
      </style>
      <hass-subpage header="Forgot Password">
        <div class="content">
          <paper-card>
            <div class="card-content">
              <h1>Forgot your password?</h1>
              <p>
                Enter your email address and we will send you a link to reset
                your password.
              </p>
              <div class="error" hidden$="[[!_error]]">[[_error]]</div>
              <paper-input
                autofocus=""
                id="email"
                label="E-mail"
                value="{{email}}"
                type="email"
                on-keydown="_keyDown"
                error-message="Invalid email"
              ></paper-input>
            </div>
            <div class="card-actions">
              <ha-progress-button
                on-click="_handleEmailPasswordReset"
                progress="[[_requestInProgress]]"
                >Send reset email</ha-progress-button
              >
            </div>
          </paper-card>
        </div>
      </hass-subpage>
    `}static get properties(){return{hass:Object,email:{type:String,notify:!0,observer:"_emailChanged"},_requestInProgress:{type:Boolean,value:!1},_error:{type:String,value:""}}}_emailChanged(){this._error="",this.$.email.invalid=!1}_keyDown(e){13===e.keyCode&&(this._handleEmailPasswordReset(),e.preventDefault())}_handleEmailPasswordReset(){this.email&&this.email.includes("@")||(this.$.email.invalid=!0),this.$.email.invalid||(this._requestInProgress=!0,this.hass.callApi("post","cloud/forgot_password",{email:this.email}).then(()=>{this._requestInProgress=!1,this.fire("cloud-done",{flashMessage:"Check your email for instructions on how to reset your password."})},e=>this.setProperties({_requestInProgress:!1,_error:e&&e.body&&e.body.message?e.body.message:"Unknown error"})))}});s(100),s(104);var O=s(209);s(224);customElements.define("ha-config-cloud-login",class extends(Object(O.a)(Object(b.a)(i.a))){static get template(){return o.a`
      <style include="iron-flex ha-style">
        .content {
          padding-bottom: 24px;
          direction: ltr;
        }
        [slot="introduction"] {
          margin: -1em 0;
        }
        [slot="introduction"] a {
          color: var(--primary-color);
        }
        paper-card {
          display: block;
        }
        paper-item {
          cursor: pointer;
        }
        paper-card:last-child {
          margin-top: 24px;
        }
        h1 {
          @apply --paper-font-headline;
          margin: 0;
        }
        .error {
          color: var(--google-red-500);
        }
        .card-actions {
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        [hidden] {
          display: none;
        }
        .flash-msg {
          padding-right: 44px;
        }
        .flash-msg paper-icon-button {
          position: absolute;
          top: 8px;
          right: 8px;
          color: var(--secondary-text-color);
        }
      </style>
      <hass-subpage header="Cloud Login">
        <div class="content">
          <ha-config-section is-wide="[[isWide]]">
            <span slot="header">Home Assistant Cloud</span>
            <div slot="introduction">
              <p>
                Home Assistant Cloud provides you with a secure remote
                connection to your instance while away from home. It also allows
                you to connect with cloud-only services: Amazon Alexa and Google
                Assistant.
              </p>
              <p>
                This service is run by our partner
                <a href="https://www.nabucasa.com" target="_blank"
                  >Nabu&nbsp;Casa,&nbsp;Inc</a
                >, a company founded by the founders of Home Assistant and
                Hass.io.
              </p>
              <p>
                Home Assistant Cloud is a subscription service with a free one
                month trial. No payment information necessary.
              </p>
              <p>
                <a href="https://www.nabucasa.com" target="_blank"
                  >Learn more about Home Assistant Cloud</a
                >
              </p>
            </div>

            <paper-card hidden$="[[!flashMessage]]">
              <div class="card-content flash-msg">
                [[flashMessage]]
                <paper-icon-button icon="hass:close" on-click="_dismissFlash"
                  >Dismiss</paper-icon-button
                >
                <paper-ripple id="flashRipple" noink=""></paper-ripple>
              </div>
            </paper-card>

            <paper-card>
              <div class="card-content">
                <h1>Sign In</h1>
                <div class="error" hidden$="[[!_error]]">[[_error]]</div>
                <paper-input
                  label="Email"
                  id="email"
                  type="email"
                  value="{{email}}"
                  on-keydown="_keyDown"
                  error-message="Invalid email"
                ></paper-input>
                <paper-input
                  id="password"
                  label="Password"
                  value="{{_password}}"
                  type="password"
                  on-keydown="_keyDown"
                  error-message="Passwords are at least 8 characters"
                ></paper-input>
              </div>
              <div class="card-actions">
                <ha-progress-button
                  on-click="_handleLogin"
                  progress="[[_requestInProgress]]"
                  >Sign in</ha-progress-button
                >
                <button
                  class="link"
                  hidden="[[_requestInProgress]]"
                  on-click="_handleForgotPassword"
                >
                  forgot password?
                </button>
              </div>
            </paper-card>

            <paper-card>
              <paper-item on-click="_handleRegister">
                <paper-item-body two-line="">
                  Start your free 1 month trial
                  <div secondary="">No payment information necessary</div>
                </paper-item-body>
                <ha-icon-next></ha-icon-next>
              </paper-item>
            </paper-card>
          </ha-config-section>
        </div>
      </hass-subpage>
    `}static get properties(){return{hass:Object,isWide:Boolean,email:{type:String,notify:!0},_password:{type:String,value:""},_requestInProgress:{type:Boolean,value:!1},flashMessage:{type:String,notify:!0},_error:String}}static get observers(){return["_inputChanged(email, _password)"]}connectedCallback(){super.connectedCallback(),this.flashMessage&&requestAnimationFrame(()=>requestAnimationFrame(()=>this.$.flashRipple.simulatedRipple()))}_inputChanged(){this.$.email.invalid=!1,this.$.password.invalid=!1,this._error=!1}_keyDown(e){13===e.keyCode&&(this._handleLogin(),e.preventDefault())}_handleLogin(){let e=!1;this.email&&this.email.includes("@")||(this.$.email.invalid=!0,this.$.email.focus(),e=!0),this._password.length<8&&(this.$.password.invalid=!0,e||(e=!0,this.$.password.focus())),e||(this._requestInProgress=!0,this.hass.callApi("post","cloud/login",{email:this.email,password:this._password}).then(()=>{this.fire("ha-refresh-cloud-status"),this.setProperties({email:"",_password:""})},e=>{this._password="";const t=e&&e.body&&e.body.code;if("PasswordChangeRequired"===t)return alert("You need to change your password before logging in."),void this.navigate("/config/cloud/forgot-password");const s={_requestInProgress:!1,_error:e&&e.body&&e.body.message?e.body.message:"Unknown error"};"UserNotConfirmed"===t&&(s._error="You need to confirm your email before logging in."),this.setProperties(s),this.$.email.focus()}))}_handleRegister(){this.flashMessage="",this.navigate("/config/cloud/register")}_handleForgotPassword(){this.flashMessage="",this.navigate("/config/cloud/forgot-password")}_dismissFlash(){setTimeout(()=>{this.flashMessage=""},200)}});customElements.define("ha-config-cloud-register",class extends(Object(b.a)(i.a)){static get template(){return o.a`
    <style include="iron-flex ha-style">
      .content {
        direction: ltr;
      }

      [slot=introduction] {
        margin: -1em 0;
      }
      [slot=introduction] a {
        color: var(--primary-color);
      }
      a {
        color: var(--primary-color);
      }
      paper-card {
        display: block;
      }
      paper-item {
        cursor: pointer;
      }
      paper-card:last-child {
        margin-top: 24px;
      }
      h1 {
        @apply --paper-font-headline;
        margin: 0;
      }
      .error {
        color: var(--google-red-500);
      }
      .card-actions {
        display: flex;
        justify-content: space-between;
        align-items: center;
      }
      [hidden] {
        display: none;
      }
    </style>
    <hass-subpage header="Register Account">
      <div class="content">
        <ha-config-section is-wide="[[isWide]]">
          <span slot="header">Start your free trial</span>
          <div slot="introduction">
            <p>
              Create an account to start your free one month trial with Home Assistant Cloud. No payment information necessary.
            </p>
            <p>
              The trial will give you access to all the benefits of Home Assistant Cloud, including:
            </p>
            <ul>
              <li>Control of Home Assistant away from home</li>
              <li>Integration with Google Assistant</li>
              <li>Integration with Amazon Alexa</li>
              <li>Easy integration with webhook-based apps like OwnTracks</li>
            </ul>
            <p>
              This service is run by our partner <a href='https://www.nabucasa.com' target='_blank'>Nabu&nbsp;Casa,&nbsp;Inc</a>, a company founded by the founders of Home Assistant and Hass.io.
            </p>

            <p>
              By registering an account you agree to the following terms and conditions.
              </p><ul>
                <li><a href="https://home-assistant.io/tos/" target="_blank">Terms and Conditions</a></li>
                <li><a href="https://home-assistant.io/privacy/" target="_blank">Privacy Policy</a></li>
              </ul>
            </p>
          </div>

          <paper-card>
            <div class="card-content">
              <div class="header">
                <h1>Create Account</h1>
                <div class="error" hidden$="[[!_error]]">[[_error]]</div>
              </div>
              <paper-input autofocus="" id="email" label="Email address" type="email" value="{{email}}" on-keydown="_keyDown" error-message="Invalid email"></paper-input>
              <paper-input id="password" label="Password" value="{{_password}}" type="password" on-keydown="_keyDown" error-message="Your password needs to be at least 8 characters"></paper-input>
            </div>
            <div class="card-actions">
              <ha-progress-button on-click="_handleRegister" progress="[[_requestInProgress]]">Start trial</ha-progress-button>
              <button class="link" hidden="[[_requestInProgress]]" on-click="_handleResendVerifyEmail">Resend confirmation email</button>
            </div>
          </paper-card>
        </ha-config-section>
      </div>
    </hass-subpage>
`}static get properties(){return{hass:Object,isWide:Boolean,email:{type:String,notify:!0},_requestInProgress:{type:Boolean,value:!1},_password:{type:String,value:""},_error:{type:String,value:""}}}static get observers(){return["_inputChanged(email, _password)"]}_inputChanged(){this._error="",this.$.email.invalid=!1,this.$.password.invalid=!1}_keyDown(e){13===e.keyCode&&(this._handleRegister(),e.preventDefault())}_handleRegister(){let e=!1;this.email&&this.email.includes("@")||(this.$.email.invalid=!0,this.$.email.focus(),e=!0),this._password.length<8&&(this.$.password.invalid=!0,e||(e=!0,this.$.password.focus())),e||(this._requestInProgress=!0,this.hass.callApi("post","cloud/register",{email:this.email,password:this._password}).then(()=>this._verificationEmailSent(),e=>{this._password="",this.setProperties({_requestInProgress:!1,_error:e&&e.body&&e.body.message?e.body.message:"Unknown error"})}))}_handleResendVerifyEmail(){this.email?this.hass.callApi("post","cloud/resend_confirm",{email:this.email}).then(()=>this._verificationEmailSent(),e=>this.setProperties({_error:e&&e.body&&e.body.message?e.body.message:"Unknown error"})):this.$.email.invalid=!0}_verificationEmailSent(){this.setProperties({_requestInProgress:!1,_password:""}),this.fire("cloud-done",{flashMessage:"Account created! Check your email for instructions on how to activate your account."})}});const D=["/cloud/account"],$=["/cloud/login","/cloud/register","/cloud/forgot-password"];customElements.define("ha-config-cloud",class extends(Object(O.a)(i.a)){static get template(){return o.a`
      <app-route
        route="[[route]]"
        pattern="/cloud/:page"
        data="{{_routeData}}"
        tail="{{_routeTail}}"
      ></app-route>

      <template
        is="dom-if"
        if='[[_equals(_routeData.page, "account")]]'
        restamp=""
      >
        <ha-config-cloud-account
          hass="[[hass]]"
          cloud-status="[[cloudStatus]]"
          is-wide="[[isWide]]"
        ></ha-config-cloud-account>
      </template>

      <template
        is="dom-if"
        if='[[_equals(_routeData.page, "login")]]'
        restamp=""
      >
        <ha-config-cloud-login
          page-name="login"
          hass="[[hass]]"
          is-wide="[[isWide]]"
          email="{{_loginEmail}}"
          flash-message="{{_flashMessage}}"
        ></ha-config-cloud-login>
      </template>

      <template
        is="dom-if"
        if='[[_equals(_routeData.page, "register")]]'
        restamp=""
      >
        <ha-config-cloud-register
          page-name="register"
          hass="[[hass]]"
          is-wide="[[isWide]]"
          email="{{_loginEmail}}"
        ></ha-config-cloud-register>
      </template>

      <template
        is="dom-if"
        if='[[_equals(_routeData.page, "forgot-password")]]'
        restamp=""
      >
        <ha-config-cloud-forgot-password
          page-name="forgot-password"
          hass="[[hass]]"
          email="{{_loginEmail}}"
        ></ha-config-cloud-forgot-password>
      </template>
    `}static get properties(){return{hass:Object,isWide:Boolean,loadingAccount:{type:Boolean,value:!1},cloudStatus:{type:Object},_flashMessage:{type:String,value:""},route:Object,_routeData:Object,_routeTail:Object,_loginEmail:String}}static get observers(){return["_checkRoute(route, cloudStatus)"]}ready(){super.ready(),this.addEventListener("cloud-done",e=>{this._flashMessage=e.detail.flashMessage,this.navigate("/config/cloud/login")})}_checkRoute(e){e&&"/cloud"===e.path.substr(0,6)&&(this._debouncer=a.a.debounce(this._debouncer,r.d.after(0),()=>{this.cloudStatus&&(this.cloudStatus.logged_in||$.includes(e.path))?this.cloudStatus.logged_in&&!D.includes(e.path)&&this.navigate("/config/cloud/account",!0):this.navigate("/config/cloud/login",!0)}))}_equals(e,t){return e===t}})}}]);