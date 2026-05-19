import { useState } from 'react'

const WeightSettings = ({ weights, onWeightsChange, onReset }) => {
  const [localWeights, setLocalWeights] = useState(weights)

  const handleWeightChange = (key, value) => {
    const newVal = Math.max(0, Math.min(100, parseInt(value) || 0))
    const newWeights = {
      ...localWeights,
      [key]: newVal,
    }
    setLocalWeights(newWeights)
    onWeightsChange(newWeights)
  }

  const handleReset = () => {
    setLocalWeights(weights)
    onReset()
  }

  const total = Object.values(localWeights).reduce((a, b) => a + b, 0)

  const weightLabels = {
    price: '價格合理性',
    mrt: '捷運距離',
    hospital: '醫院距離',
    school: '學校距離',
    park: '公園距離',
    age: '屋齡',
    area: '坪數',
    floor: '樓層',
    parking: '車位',
  }

  const weightDescriptions = {
    price: '房屋開價與市場合理價格的差距',
    mrt: '最近捷運站的距離',
    hospital: '最近醫院的距離',
    school: '最近學校的距離',
    park: '最近公園的距離',
    age: '房屋年齡',
    area: '房屋坪數',
    floor: '房屋樓層位置',
    parking: '是否有停車位',
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6 mt-6">
      <h3 className="text-lg font-bold text-gray-800 mb-2">
        權重設定 (進階)
      </h3>
      <p className="text-xs text-gray-500 mb-4">
        調整各項因素對分析結果的影響程度
      </p>

      <div className="space-y-4">
        {Object.entries(localWeights).map(([key, value]) => (
          <div key={key} className="border-b pb-3">
            <div className="flex justify-between items-start mb-2">
              <div>
                <label className="text-sm font-medium text-gray-700 block">
                  {weightLabels[key]}
                </label>
                <p className="text-xs text-gray-500 mt-1">
                  {weightDescriptions[key]}
                </p>
              </div>
              <span className="text-sm font-bold text-blue-600 bg-blue-50 px-2 py-1 rounded">
                {value}%
              </span>
            </div>
            <input
              type="range"
              min="0"
              max="100"
              value={value}
              onChange={(e) => handleWeightChange(key, e.target.value)}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
            />
          </div>
        ))}
      </div>

      <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
        <div className="flex justify-between items-center mb-2">
          <p className="text-sm font-medium text-gray-800">
            權重總和
          </p>
          <span className={`text-lg font-bold px-3 py-1 rounded ${
            total === 100
              ? 'text-green-700 bg-green-100'
              : 'text-orange-700 bg-orange-100'
          }`}>
            {total}%
          </span>
        </div>
        {total === 100 ? (
          <p className="text-xs text-green-600">
            ✓ 權重設置完成，可以進行分析
          </p>
        ) : (
          <p className="text-xs text-orange-600">
            ⚠ 建議調整至 100% 以獲得最佳分析結果
          </p>
        )}
      </div>

      <button
        onClick={handleReset}
        className="w-full mt-4 bg-gray-300 text-gray-800 font-medium py-2 px-4 rounded-md hover:bg-gray-400 transition text-sm"
      >
        恢復預設權重
      </button>
    </div>
  )
}

export default WeightSettings
