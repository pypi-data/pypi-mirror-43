(window.webpackJsonp=window.webpackJsonp||[]).push([[64],{201:function(e,a,t){"use strict";function s(e,a){return e&&-1!==e.config.components.indexOf(a)}t.d(a,"a",function(){return s})},205:function(e,a,t){"use strict";var s=t(6),i=t(120);a.a=Object(s.a)(e=>(class extends e{navigate(...e){Object(i.a)(this,...e)}}))},736:function(e,a,t){"use strict";t.r(a);t(146),t(118);var s=t(3),i=t(24),o=t(201),r=t(84),n=t(205);customElements.define("ha-panel-config",class extends(Object(r.a)(Object(n.a)(i.a))){static get template(){return s.a`
      <app-route
        route="[[route]]"
        pattern="/:page"
        data="{{_routeData}}"
      ></app-route>

      <iron-media-query query="(min-width: 1040px)" query-matches="{{wide}}">
      </iron-media-query>
      <iron-media-query
        query="(min-width: 1296px)"
        query-matches="{{wideSidebar}}"
      >
      </iron-media-query>

      <template
        is="dom-if"
        if='[[_equals(_routeData.page, "area_registry")]]'
        restamp
      >
        <ha-config-area-registry
          page-name="area_registry"
          route="[[route]]"
          hass="[[hass]]"
          is-wide="[[isWide]]"
        ></ha-config-area-registry>
      </template>

      <template is="dom-if" if='[[_equals(_routeData.page, "core")]]' restamp>
        <ha-config-core
          page-name="core"
          hass="[[hass]]"
          is-wide="[[isWide]]"
        ></ha-config-core>
      </template>

      <template is="dom-if" if='[[_equals(_routeData.page, "cloud")]]' restamp>
        <ha-config-cloud
          page-name="cloud"
          route="[[route]]"
          hass="[[hass]]"
          is-wide="[[isWide]]"
          cloud-status="[[_cloudStatus]]"
        ></ha-config-cloud>
      </template>

      <template is="dom-if" if='[[_equals(_routeData.page, "dashboard")]]'>
        <ha-config-dashboard
          page-name="dashboard"
          hass="[[hass]]"
          is-wide="[[isWide]]"
          cloud-status="[[_cloudStatus]]"
          narrow="[[narrow]]"
          show-menu="[[showMenu]]"
        ></ha-config-dashboard>
      </template>

      <template
        is="dom-if"
        if='[[_equals(_routeData.page, "automation")]]'
        restamp
      >
        <ha-config-automation
          page-name="automation"
          route="[[route]]"
          hass="[[hass]]"
          is-wide="[[isWide]]"
        ></ha-config-automation>
      </template>

      <template is="dom-if" if='[[_equals(_routeData.page, "script")]]' restamp>
        <ha-config-script
          page-name="script"
          route="[[route]]"
          hass="[[hass]]"
          is-wide="[[isWide]]"
        ></ha-config-script>
      </template>

      <template
        is="dom-if"
        if='[[_equals(_routeData.page, "entity_registry")]]'
        restamp
      >
        <ha-config-entity-registry
          page-name="entity_registry"
          route="[[route]]"
          hass="[[hass]]"
          is-wide="[[isWide]]"
        ></ha-config-entity-registry>
      </template>

      <template is="dom-if" if='[[_equals(_routeData.page, "zha")]]' restamp>
        <ha-config-zha
          page-name="zha"
          hass="[[hass]]"
          is-wide="[[isWide]]"
        ></ha-config-zha>
      </template>

      <template is="dom-if" if='[[_equals(_routeData.page, "zwave")]]' restamp>
        <ha-config-zwave
          page-name="zwave"
          hass="[[hass]]"
          is-wide="[[isWide]]"
        ></ha-config-zwave>
      </template>

      <template is="dom-if" if='[[_equals(_routeData.page, "person")]]' restamp>
        <ha-config-person
          page-name="person"
          route="[[route]]"
          hass="[[hass]]"
          is-wide="[[isWide]]"
        ></ha-config-person>
      </template>

      <template
        is="dom-if"
        if='[[_equals(_routeData.page, "customize")]]'
        restamp
      >
        <ha-config-customize
          page-name="customize"
          hass="[[hass]]"
          is-wide="[[isWide]]"
        ></ha-config-customize>
      </template>

      <template
        is="dom-if"
        if='[[_equals(_routeData.page, "integrations")]]'
        restamp
      >
        <ha-config-entries
          route="[[route]]"
          page-name="integrations"
          hass="[[hass]]"
          is-wide="[[isWide]]"
          narrow="[[narrow]]"
        ></ha-config-entries>
      </template>

      <template is="dom-if" if='[[_equals(_routeData.page, "users")]]' restamp>
        <ha-config-users
          page-name="users"
          route="[[route]]"
          hass="[[hass]]"
        ></ha-config-users>
      </template>
    `}static get properties(){return{hass:Object,narrow:Boolean,showMenu:Boolean,_cloudStatus:{type:Object,value:null},route:{type:Object,observer:"_routeChanged"},_routeData:Object,wide:Boolean,wideSidebar:Boolean,isWide:{type:Boolean,computed:"computeIsWide(showMenu, wideSidebar, wide)"}}}ready(){super.ready(),Object(o.a)(this.hass,"cloud")&&this._updateCloudStatus(),this.addEventListener("ha-refresh-cloud-status",()=>this._updateCloudStatus()),Promise.all([t.e(121),t.e(65)]).then(t.bind(null,734)),Promise.all([t.e(0),t.e(1),t.e(2),t.e(3),t.e(66)]).then(t.bind(null,721)),Promise.all([t.e(0),t.e(122),t.e(67)]).then(t.bind(null,722)),Promise.all([t.e(0),t.e(1),t.e(4),t.e(5),t.e(68)]).then(t.bind(null,726)),Promise.all([t.e(0),t.e(123),t.e(69)]).then(t.bind(null,731)),Promise.all([t.e(0),t.e(1),t.e(4),t.e(5),t.e(70)]).then(t.bind(null,724)),Promise.all([t.e(124),t.e(71)]).then(t.bind(null,732)),Promise.all([t.e(0),t.e(1),t.e(2),t.e(3),t.e(74)]).then(t.bind(null,728)),Promise.all([t.e(125),t.e(72)]).then(t.bind(null,733)),Promise.all([t.e(10),t.e(75)]).then(t.bind(null,729)),Promise.all([t.e(0),t.e(1),t.e(4),t.e(5),t.e(76)]).then(t.bind(null,723)),Promise.all([t.e(0),t.e(1),t.e(4),t.e(5),t.e(77)]).then(t.bind(null,725)),Promise.all([t.e(10),t.e(73)]).then(t.bind(null,730))}async _updateCloudStatus(){this._cloudStatus=await this.hass.callWS({type:"cloud/status"}),"connecting"===this._cloudStatus.cloud&&setTimeout(()=>this._updateCloudStatus(),5e3)}computeIsWide(e,a,t){return e?a:t}_routeChanged(e){""===e.path&&"/config"===e.prefix&&this.navigate("/config/dashboard",!0),this.fire("iron-resize")}_equals(e,a){return e===a}})}}]);