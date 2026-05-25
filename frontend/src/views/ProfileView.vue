<script setup>
import { ref, onMounted } from 'vue'
import { getProfile, updateProfile } from '../api'

const profile = ref({
  province: '',
  gaokao_score: null,
  gaokao_year: null,
  subject_type: '',
  interested_majors: '',
})
const loading = ref(true)
const saving = ref(false)
const saved = ref(false)

const provinces = ['北京', '天津', '河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江', '上海', '江苏', '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南', '广东', '广西', '海南', '重庆', '四川', '贵州', '云南', '西藏', '陕西', '甘肃', '青海', '宁夏', '新疆']

const subjectTypes = ['文科', '理科', '新高考-3+3', '新高考-3+1+2']

onMounted(async () => {
  try {
    const data = await getProfile()
    if (data) {
      profile.value.province = data.province || ''
      profile.value.gaokao_score = data.gaokao_score
      profile.value.gaokao_year = data.gaokao_year
      profile.value.subject_type = data.subject_type || ''
      profile.value.interested_majors = data.interested_majors || ''
    }
  } finally {
    loading.value = false
  }
})

async function handleSave() {
  saving.value = true
  saved.value = false
  try {
    await updateProfile({
      province: profile.value.province || null,
      gaokao_score: profile.value.gaokao_score,
      gaokao_year: profile.value.gaokao_year,
      subject_type: profile.value.subject_type || null,
      interested_majors: profile.value.interested_majors || null,
    })
    saved.value = true
    setTimeout(() => { saved.value = false }, 2500)
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div class="profile-page">
    <div class="profile-card">
      <div class="profile-header">
        <h2>个人信息</h2>
        <p>完善以下信息，AI 将为你提供更精准的志愿填报建议</p>
      </div>

      <div v-if="loading" class="profile-loading">加载中...</div>

      <form v-else class="profile-form" @submit.prevent="handleSave">
        <div class="field">
          <label>省份</label>
          <select v-model="profile.province">
            <option value="">请选择省份</option>
            <option v-for="p in provinces" :key="p" :value="p">{{ p }}</option>
          </select>
        </div>

        <div class="field-row">
          <div class="field">
            <label>高考年份</label>
            <input
              v-model.number="profile.gaokao_year"
              type="number"
              placeholder="如 2025"
            />
          </div>
          <div class="field">
            <label>高考分数</label>
            <input
              v-model.number="profile.gaokao_score"
              type="number"
              placeholder="如 580"
              step="0.5"
            />
          </div>
        </div>

        <div class="field">
          <label>选科类型</label>
          <select v-model="profile.subject_type">
            <option value="">请选择选科类型</option>
            <option v-for="s in subjectTypes" :key="s" :value="s">{{ s }}</option>
          </select>
        </div>

        <div class="field">
          <label>感兴趣的专业</label>
          <input
            v-model="profile.interested_majors"
            type="text"
            placeholder="如：计算机、纺织工程（用逗号分隔）"
          />
        </div>

        <div class="form-actions">
          <button type="submit" class="save-btn" :disabled="saving">
            {{ saving ? '保存中...' : '保存' }}
          </button>
          <span v-if="saved" class="saved-tip">已保存</span>
        </div>
      </form>
    </div>
  </div>
</template>

<style scoped>
.profile-page {
  display: flex;
  align-items: flex-start;
  justify-content: center;
  height: 100%;
  padding: 40px 24px;
  overflow-y: auto;
}

.profile-card {
  width: 100%;
  max-width: 520px;
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-md);
  padding: 32px;
  border: 1px solid var(--color-border);
}

.profile-header {
  margin-bottom: 28px;
}

.profile-header h2 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 6px;
}

.profile-header p {
  font-size: 13px;
  color: var(--color-text-muted);
}

.profile-loading {
  text-align: center;
  color: var(--color-text-muted);
  padding: 24px 0;
}

.field {
  margin-bottom: 16px;
}

.field label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  margin-bottom: 6px;
  color: var(--color-text-secondary);
}

.field input,
.field select {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-size: 14px;
  font-family: inherit;
  outline: none;
  transition: border-color 0.2s;
  background: var(--color-surface);
}

.field input:focus,
.field select:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.08);
}

.field-row {
  display: flex;
  gap: 12px;
}

.field-row .field {
  flex: 1;
}

.form-actions {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-top: 8px;
}

.save-btn {
  padding: 10px 28px;
  border: none;
  border-radius: var(--radius-sm);
  background: var(--color-primary);
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  font-family: inherit;
  transition: background 0.2s;
}

.save-btn:hover {
  background: var(--color-primary-hover);
}

.save-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.saved-tip {
  color: #16a34a;
  font-size: 13px;
  font-weight: 500;
}
</style>
