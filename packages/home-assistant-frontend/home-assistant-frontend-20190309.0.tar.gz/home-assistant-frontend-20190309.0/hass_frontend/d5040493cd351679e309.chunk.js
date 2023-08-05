(window.webpackJsonp=window.webpackJsonp||[]).push([[75],{168:function(e,t,s){"use strict";s.d(t,"a",function(){return i});s(101);const a=customElements.get("iron-icon");let r=!1;class i extends a{constructor(...e){super(...e),this._iconsetName=void 0}listen(e,t,a){super.listen(e,t,a),r||"mdi"!==this._iconsetName||(r=!0,s.e(59).then(s.bind(null,209)))}}customElements.define("ha-icon",i)},224:function(e,t,s){"use strict";s(101);var a=s(168);customElements.define("ha-icon-next",class extends a.a{connectedCallback(){this.icon="ltr"===window.getComputedStyle(this).direction?"hass:chevron-right":"hass:chevron-left",super.connectedCallback()}})},337:function(e,t,s){"use strict";s.d(t,"a",function(){return a});const a=async e=>e.callWS({type:"config/auth/list"})},729:function(e,t,s){"use strict";s.r(t);s(146);var a=s(11),r=s(19),i=s(3),c=s(24),o=s(205),n=(s(230),s(131),s(164),s(170),s(143),s(224),s(110)),u=s(84),d=s(102);let l=!1;customElements.define("ha-config-user-picker",class extends(Object(u.a)(Object(o.a)(Object(n.a)(c.a)))){static get template(){return i.a`
      <style>
        paper-fab {
          position: fixed;
          bottom: 16px;
          right: 16px;
          z-index: 1;
        }
        paper-fab[is-wide] {
          bottom: 24px;
          right: 24px;
        }
        paper-fab[rtl] {
          right: auto;
          left: 16px;
        }
        paper-fab[rtl][is-wide] {
          bottom: 24px;
          right: auto;
          left: 24px;
        }

        paper-card {
          display: block;
          max-width: 600px;
          margin: 16px auto;
        }
        a {
          text-decoration: none;
          color: var(--primary-text-color);
        }
      </style>

      <hass-subpage header="[[localize('ui.panel.config.users.picker.title')]]">
        <paper-card>
          <template is="dom-repeat" items="[[users]]" as="user">
            <a href="[[_computeUrl(user)]]">
              <paper-item>
                <paper-item-body two-line>
                  <div>[[_withDefault(user.name, 'Unnamed User')]]</div>
                  <div secondary="">
                    [[user.id]]
                    <template is="dom-if" if="[[user.system_generated]]">
                      - System Generated
                    </template>
                  </div>
                </paper-item-body>
                <ha-icon-next></ha-icon-next>
              </paper-item>
            </a>
          </template>
        </paper-card>

        <paper-fab
          is-wide$="[[isWide]]"
          icon="hass:plus"
          title="[[localize('ui.panel.config.users.picker.add_user')]]"
          on-click="_addUser"
          rtl$="[[rtl]]"
        ></paper-fab>
      </hass-subpage>
    `}static get properties(){return{hass:Object,users:Array,rtl:{type:Boolean,reflectToAttribute:!0,computed:"_computeRTL(hass)"}}}connectedCallback(){super.connectedCallback(),l||(l=!0,this.fire("register-dialog",{dialogShowEvent:"show-add-user",dialogTag:"ha-dialog-add-user",dialogImport:()=>Promise.all([s.e(1),s.e(23)]).then(s.bind(null,776))}))}_withDefault(e,t){return e||t}_computeUrl(e){return`/config/users/${e.id}`}_computeRTL(e){return Object(d.a)(e)}_addUser(){this.fire("show-add-user",{hass:this.hass,dialogClosedCallback:async({userId:e})=>{this.fire("reload-users"),e&&this.navigate(`/config/users/${e}`)}})}});s(73);customElements.define("ha-user-editor",class extends(Object(u.a)(Object(o.a)(Object(n.a)(c.a)))){static get template(){return i.a`
      <style include="ha-style">
        paper-card {
          display: block;
          max-width: 600px;
          margin: 0 auto 16px;
        }
        paper-card:first-child {
          margin-top: 16px;
        }
        paper-card:last-child {
          margin-bottom: 16px;
        }
        hass-subpage paper-card:first-of-type {
          direction: ltr;
        }
      </style>

      <hass-subpage
        header="[[localize('ui.panel.config.users.editor.caption')]]"
      >
        <paper-card heading="[[_computeName(user)]]">
          <table class="card-content">
            <tr>
              <td>ID</td>
              <td>[[user.id]]</td>
            </tr>
            <tr>
              <td>Owner</td>
              <td>[[user.is_owner]]</td>
            </tr>
            <tr>
              <td>Active</td>
              <td>[[user.is_active]]</td>
            </tr>
            <tr>
              <td>System generated</td>
              <td>[[user.system_generated]]</td>
            </tr>
          </table>
        </paper-card>
        <paper-card>
          <div class="card-actions">
            <mwc-button
              class="warning"
              on-click="_deleteUser"
              disabled="[[user.system_generated]]"
            >
              [[localize('ui.panel.config.users.editor.delete_user')]]
            </mwc-button>
            <template is="dom-if" if="[[user.system_generated]]">
              Unable to remove system generated users.
            </template>
          </div>
        </paper-card>
      </hass-subpage>
    `}static get properties(){return{hass:Object,user:Object}}_computeName(e){return e&&(e.name||"Unnamed user")}async _deleteUser(e){if(confirm(`Are you sure you want to delete ${this._computeName(this.user)}`)){try{await this.hass.callWS({type:"config/auth/delete",user_id:this.user.id})}catch(e){return void alert(e.code)}this.fire("reload-users"),this.navigate("/config/users")}else e.target.blur()}});var p=s(45),h=s(337);customElements.define("ha-config-users",class extends(Object(o.a)(c.a)){static get template(){return i.a`
      <app-route
        route="[[route]]"
        pattern="/users/:user"
        data="{{_routeData}}"
      ></app-route>

      <template is="dom-if" if='[[_equals(_routeData.user, "picker")]]'>
        <ha-config-user-picker
          hass="[[hass]]"
          users="[[_users]]"
        ></ha-config-user-picker>
      </template>
      <template
        is="dom-if"
        if='[[!_equals(_routeData.user, "picker")]]'
        restamp
      >
        <ha-user-editor
          hass="[[hass]]"
          user="[[_computeUser(_users, _routeData.user)]]"
        ></ha-user-editor>
      </template>
    `}static get properties(){return{hass:Object,route:{type:Object,observer:"_checkRoute"},_routeData:Object,_user:{type:Object,value:null},_users:{type:Array,value:null}}}ready(){super.ready(),this._loadData(),this.addEventListener("reload-users",()=>this._loadData())}_handlePickUser(e){this._user=e.detail.user}_checkRoute(e){e&&"/users"===e.path.substr(0,6)&&(Object(p.a)(this,"iron-resize"),this._debouncer=r.a.debounce(this._debouncer,a.d.after(0),()=>{"/users"===e.path&&this.navigate("/config/users/picker",!0)}))}_computeUser(e,t){return e&&e.filter(e=>e.id===t)[0]}_equals(e,t){return e===t}async _loadData(){this._users=await Object(h.a)(this.hass)}})}}]);