(window.webpackJsonp=window.webpackJsonp||[]).push([[13],{778:function(a,t,e){"use strict";e.r(t);var i=e(5),r=(e(188),e(195),e(83),e(44));customElements.define("dialog-area-registry-detail",class extends i.a{constructor(...a){super(...a),this.hass=void 0,this._name=void 0,this._error=void 0,this._params=void 0,this._submitting=void 0}static get properties(){return{_error:{},_name:{},_params:{}}}async showDialog(a){this._params=a,this._error=void 0,this._name=this._params.entry?this._params.entry.name:"",await this.updateComplete}render(){if(!this._params)return i.e``;const a=""===this._name.trim();return i.e`
      <paper-dialog
        with-backdrop
        opened
        @opened-changed="${this._openedChanged}"
      >
        <h2>
          ${this._params.entry?this._params.entry.name:this.hass.localize("ui.panel.config.area_registry.editor.default_name")}
        </h2>
        <paper-dialog-scrollable>
          ${this._error?i.e`
                <div class="error">${this._error}</div>
              `:""}
          <div class="form">
            <paper-input
              .value=${this._name}
              @value-changed=${this._nameChanged}
              .label=${this.hass.localize("ui.dialogs.more_info_settings.name")}
              error-message="Name is required"
              .invalid=${a}
            ></paper-input>
          </div>
        </paper-dialog-scrollable>
        <div class="paper-dialog-buttons">
          ${this._params.entry?i.e`
                <mwc-button
                  class="warning"
                  @click="${this._deleteEntry}"
                  .disabled=${this._submitting}
                >
                  ${this.hass.localize("ui.panel.config.area_registry.editor.delete")}
                </mwc-button>
              `:i.e``}
          <mwc-button
            @click="${this._updateEntry}"
            .disabled=${a||this._submitting}
          >
            ${this._params.entry?this.hass.localize("ui.panel.config.area_registry.editor.update"):this.hass.localize("ui.panel.config.area_registry.editor.create")}
          </mwc-button>
        </div>
      </paper-dialog>
    `}_nameChanged(a){this._error=void 0,this._name=a.detail.value}async _updateEntry(){this._submitting=!0;try{const a={name:this._name.trim()};this._params.entry?await this._params.updateEntry(a):await this._params.createEntry(a),this._params=void 0}catch(a){this._error=a.message||"Unknown error"}finally{this._submitting=!1}}async _deleteEntry(){this._submitting=!0;try{await this._params.removeEntry()&&(this._params=void 0)}finally{this._submitting=!1}}_openedChanged(a){a.detail.value||(this._params=void 0)}static get styles(){return[r.b,i.c`
        paper-dialog {
          min-width: 400px;
        }
        .form {
          padding-bottom: 24px;
        }
        mwc-button.warning {
          margin-right: auto;
        }
        .error {
          color: var(--google-red-500);
        }
      `]}})}}]);