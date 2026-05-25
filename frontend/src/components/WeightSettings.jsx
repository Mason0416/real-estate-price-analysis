import { useState } from 'react'

const WeightSettings = ({ weights, onWeightsChange, onReset }) => {
  const handleWeightChange = (key, value) => {
    const newVal = parseInt(value, 10)
    const newWeights = {
      ...weights,
      [key]: newVal,
    }
    onWeightsChange(newWeights)
  }

  const total = Object.values(weights).reduce((a, b) => a + b, 0)

  const weightLabels = {
    price: '價格合理性',
    mrt: '捷運距離',
    hospital: '醫院距離',
    school: '學校距離',
    park: '公園距離',
  }

  const weightDescriptions = {
    price: '房屋開價與市場合理價格的差距',
    mrt: '最近捷運站的距離',
    hospital: '最近醫院的距離',
    school: '最近學校的距離',
    park: '最近公園的距離',
  }

  const options = [0, 20, 40, 60, 80, 100]

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 mt-6 border border-gray-100">
      <h3 className="text-lg font-bold text-gray-800 mb-2 flex items-center gap-2">
        ⚙️ 權重設定
      </h3>
      <p className="text-xs text-gray-500 mb-4">
        調整各項因素對分析結果的影響程度。請使用下拉選單選擇權重（系統將在分析時自動進行等比例轉換）。
      </p>

      <div className="space-y-4">
        {Object.entries(weights).map(([key, value]) => (
          <div key={key} className="flex items-center justify-between border-b border-gray-100 pb-3 last:border-b-0 last:pb-0">
            <div className="flex-1 pr-4">
              <label className="text-sm font-semibold text-gray-700 block">
                {weightLabels[key]}
              </label>
              <p className="text-xs text-gray-400 mt-0.5">
                {weightDescriptions[key]}
              </p>
            </div>
            <div className="w-28">
              <select
                value={value}
                onChange={(e) => handleWeightChange(key, e.target.value)}
                className="w-full px-3 py-1.5 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 font-semibold text-gray-800 bg-white shadow-sm cursor-pointer hover:border-gray-400 transition"
              >
                {options.map((opt) => (
                  <option key={opt} value={opt}>
                    {opt}
                  </option>
                ))}
              </select>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-6 p-4 bg-blue-50 border border-blue-100 rounded-lg flex justify-between items-center shadow-sm">
        <span className="text-sm font-medium text-gray-700">
          權重數值總和
        </span>
        <span className="text-lg font-bold text-blue-700">
          {total}
        </span>
      </div>

      <button
        onClick={onReset}
        className="w-full mt-4 bg-gray-50 text-gray-700 font-medium py-2 px-4 rounded-md hover:bg-gray-100 transition text-sm border border-gray-200"
      >
        恢復預設權重
      </button>
    </div>
  )
}

export default WeightSettings
