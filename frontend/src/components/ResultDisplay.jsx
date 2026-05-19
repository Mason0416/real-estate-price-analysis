const ResultDisplay = ({ results }) => {
  const {
    asking_price,
    reasonable_price_range,
    price_assessment,
    weighted_score,
    nearby_facilities,
    similar_cases,
    recommendation,
  } = results

  const getPriceColor = (assessment) => {
    if (assessment.includes('偏低')) return 'text-green-600'
    if (assessment.includes('合理')) return 'text-blue-600'
    if (assessment.includes('略高')) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getScoreColor = (score) => {
    if (score >= 80) return 'bg-green-100 text-green-800'
    if (score >= 60) return 'bg-blue-100 text-blue-800'
    if (score >= 40) return 'bg-yellow-100 text-yellow-800'
    return 'bg-red-100 text-red-800'
  }

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-6">分析結果</h2>

        <div className="grid grid-cols-2 gap-4 mb-6">
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600 mb-1">賣家開價</p>
            <p className="text-2xl font-bold text-gray-800">
              {asking_price}萬元
            </p>
          </div>
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-sm text-gray-600 mb-1">合理價格區間</p>
            <p className="text-lg font-bold text-blue-600">
              {reasonable_price_range.min}~{reasonable_price_range.max}萬元
            </p>
          </div>
        </div>

        <div className={`p-4 rounded-lg mb-6 ${getPriceColor(price_assessment)} bg-opacity-10`}>
          <p className="font-bold text-lg">{price_assessment}</p>
        </div>

        <div className={`text-center p-6 rounded-lg mb-6 ${getScoreColor(weighted_score)}`}>
          <p className="text-sm font-medium mb-2">綜合合理性分數</p>
          <p className="text-5xl font-bold">{weighted_score}</p>
          <p className="text-sm mt-2">/100</p>
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-800 mb-4">周邊生活機能</h3>
        <div className="grid grid-cols-2 gap-4">
          {Object.entries(nearby_facilities).map(([facility, info]) => (
            <div key={facility} className="bg-gray-50 p-4 rounded-lg">
              <p className="text-sm text-gray-600 mb-1">
                {facility === 'mrt' && '🚇 捷運'}
                {facility === 'hospital' && '🏥 醫院'}
                {facility === 'school' && '🎓 學校'}
                {facility === 'park' && '🌳 公園'}
              </p>
              <p className="text-lg font-bold text-gray-800">
                {info.distance} m
              </p>
              <p className="text-xs text-gray-500 mt-1">
                {info.rating}
              </p>
            </div>
          ))}
        </div>
      </div>

      {similar_cases && similar_cases.length > 0 && (
        <div className="bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-xl font-bold text-gray-800 mb-4">
            相似成交案例 ({similar_cases.length})
          </h3>
          <div className="space-y-3">
            {similar_cases.slice(0, 3).map((case_, idx) => (
              <div key={idx} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-semibold text-gray-800">
                    {case_.area}坪 - {case_.age}年屋
                  </p>
                  <p className="text-sm text-gray-600">
                    成交: {case_.transaction_date}
                  </p>
                </div>
                <div className="text-right">
                  <p className="font-bold text-gray-800">
                    {case_.price}萬元
                  </p>
                  <p className="text-sm text-gray-600">
                    {case_.unit_price}萬/坪
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg shadow-lg p-6 border-l-4 border-blue-600">
        <h3 className="text-xl font-bold text-gray-800 mb-3">
          購買建議
        </h3>
        <p className="text-gray-700 leading-relaxed">
          {recommendation}
        </p>
      </div>
    </div>
  )
}

export default ResultDisplay
