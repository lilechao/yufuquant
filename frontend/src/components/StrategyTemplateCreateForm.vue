<template>
  <b-form @submit="onSubmit">
    <b-form-group
        label="策略代码："
        label-for="id_code"
    >
      <b-form-input
          id="id_code"
          v-model="form.code"
          type="text"
          required
          :state="validationStateForField('code', formErrors)"
      ></b-form-input>
      <b-form-invalid-feedback :state="validationStateForField('code', formErrors)">
        {{ getErrorForField('code', formErrors) }}
      </b-form-invalid-feedback>
    </b-form-group>

    <b-form-group
        label="策略名称："
        label-for="id_name"
    >
      <b-form-input
          id="id_name"
          v-model="form.name"
          type="text"
          required
          :state="validationStateForField('name', formErrors)"
      ></b-form-input>
      <b-form-invalid-feedback :state="validationStateForField('name', formErrors)">
        {{ getErrorForField('name', formErrors) }}
      </b-form-invalid-feedback>
    </b-form-group>
    <b-form-group
        label="策略描述："
        label-for="id_description"
    >
      <b-form-textarea
          id="id_description"
          v-model="form.description"
          rows="3"
          max-rows="6"
          :state="validationStateForField('description', formErrors)"
      ></b-form-textarea>
      <b-form-invalid-feedback :state="validationStateForField('description', formErrors)">
        {{ getErrorForField('description', formErrors) }}
      </b-form-invalid-feedback>
    </b-form-group>
    <b-form-group
        label="策略参数规格："
        label-for="id_parameter_spec"
    >
      <b-tabs content-class="mt-3" small>
        <b-tab title="编辑模式" active @click="parameterSpecMode='ui'">
          <JsonEditor
              :options="{
                            confirmText: '确认',
                            cancelText: '取消',
                        }"
              :objData="form.parameterSpecUI"
              v-model="form.parameterSpecUI">
          </JsonEditor>
        </b-tab>
        <b-tab title="文本模式" @click="parameterSpecMode='text'">
          <b-form-textarea
              id="textarea"
              v-model="form.parameterSpecText"
              placeholder=""
              rows="3"
              max-rows="6"
              :state="validationStateForField('parameter_spec', formErrors)"
          ></b-form-textarea>
          <b-form-invalid-feedback :state="validationStateForField('parameter_spec', formErrors)">
            {{ getErrorForField('parameter_spec', formErrors) }}
          </b-form-invalid-feedback>
        </b-tab>
      </b-tabs>
    </b-form-group>
    <b-button type="submit" variant="primary" class="mt-2">提交</b-button>
  </b-form>
</template>

<script>
import {createStrategyTemplate} from "@/api";
import formErrorMixin from "@/mixins/formError"

export default {
  name: 'StrategyTemplateCreateForm',
  mixins: [formErrorMixin],
  data() {
    return {
      parameterSpecMode: "ui",
      form: {
        code: '',
        name: '',
        parameterSpecUI: {},
        parameterSpecText: "",
      },
      formProcessing: false,
      formErrors: []
    }
  },
  methods: {
    async onSubmit(e) {
      e.preventDefault()
      let data = {
        "code": this.form.code,
        "name": this.form.name,
        "parameter_spec": this.parameterSpecMode === "ui" ? JSON.stringify(this.form.parameterSpecUI) : this.form.parameterSpecText,
      }
      try {
        await createStrategyTemplate(data)
        await this.$router.push('/strategy-template/list')
      } catch (error) {
        if (error.response) {
          if (error.response.status === 500) {
            this.$bvToast.toast('服务端错误', {
              title: '策略模板创建失败',
              autoHideDelay: 3000,
              toaster: 'b-toaster-top-center',
              variant: 'danger',
              appendToast: false
            });
          } else if (error.response.status === 400) {
            // form validation error
            console.log(error.response)
            this.formErrors = error.response.data.errors
          }
        } else {
          this.$bvToast.toast(error.message, {
            title: '策略模板创建失败',
            autoHideDelay: 3000,
            toaster: 'b-toaster-top-center',
            variant: 'danger',
            appendToast: false
          });
        }
      }
    },
  }
}
</script>
<style scoped>
</style>
