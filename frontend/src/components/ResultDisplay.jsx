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
    if (assessment.includes('可考慮購買')) return 'text-green-700 bg-green-50 border-green-200'
    if (assessment.includes('合理')) return 'text-blue-700 bg-blue-50 border-blue-200'
    if (assessment.includes('略高')) return 'text-yellow-700 bg-yellow-50 border-yellow-200'
    if (assessment.includes('建議議價')) return 'text-orange-700 bg-orange-50 border-orange-200'
    return 'text-red-700 bg-red-50 border-red-200'
  }

  const getPriceBorderColor = (assessment) => {
    if (assessment.includes('可考慮購買')) return 'border-green-500'
    if (assessment.includes('合理')) return 'border-blue-500'
    if (assessment.includes('略高')) return 'border-yellow-500'
    if (assessment.includes('建議議價')) return 'border-orange-500'
    return 'border-red-500'
  }

  const scoreToFivePoint = (score) => {
    if (score <= 5) return score
    return Math.round(score / 20)
  }

  const downPayment = Math.round(asking_price * 0.3)

  return (
    <div className="space-y-6">
      {/* Report Header & Price Overview */}
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-800 mb-6 border-b pb-3">🏠 房屋價格分析報告</h2>

        {/* 1. 價格分析總覽 */}
        <div className="mb-8">
          <h3 className="text-lg font-bold text-gray-800 mb-4">1. 價格分析總覽</h3>
          <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
            <div className="space-y-1">
              {/* 賣家定價 */}
              <div className="flex justify-between items-center py-4 border-b border-gray-100">
                <div className="flex flex-col pr-4">
                  <span className="text-gray-500 font-medium text-sm sm:text-base">賣家定價</span>
                  {asking_price > reasonable_price_range.max && (
                    <span className="text-[11px] sm:text-xs font-semibold text-red-500 mt-1">
                      ⚠️ 高於市場合理價格
                    </span>
                  )}
                  {asking_price >= reasonable_price_range.min && asking_price <= reasonable_price_range.max && (
                    <span className="text-[11px] sm:text-xs font-semibold text-green-600 mt-1">
                      ✅ 價格合理
                    </span>
                  )}
                  {asking_price < reasonable_price_range.min && (
                    <span className="text-[11px] sm:text-xs font-semibold text-emerald-600 mt-1">
                      ✨ 低於合理價格
                    </span>
                  )}
                </div>
                <span className="text-xl sm:text-2xl md:text-3xl font-bold text-red-600 whitespace-nowrap">
                  {Math.round(asking_price)}萬
                </span>
              </div>

              {/* 市場合理價格區間 */}
              <div className="flex justify-between items-center py-4 border-b border-gray-100">
                <div className="flex flex-col pr-4">
                  <span className="text-gray-500 font-medium text-sm sm:text-base">市場合理價格區間</span>
                  <span className="text-[11px] sm:text-xs text-gray-400 font-normal mt-1">
                    依據相似成交案例估算
                  </span>
                </div>
                <span className="text-xl sm:text-2xl md:text-3xl font-bold text-blue-600 whitespace-nowrap">
                  {Math.round(reasonable_price_range.min)}萬 ~ {Math.round(reasonable_price_range.max)}萬
                </span>
              </div>

              {/* 建議準備自備款 */}
              <div className="flex justify-between items-center py-4">
                <div className="flex flex-col pr-4">
                  <span className="text-gray-500 font-medium text-sm sm:text-base">建議準備自備款</span>
                  <span className="text-[11px] sm:text-xs text-gray-400 font-normal mt-1">
                    一般銀行約需 30% 自備款
                  </span>
                </div>
                <span className="text-xl sm:text-2xl md:text-3xl font-bold text-green-600 whitespace-nowrap">
                  {downPayment}萬
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* 2. 價格判斷 */}
        <div className="mb-6">
          <h3 className="text-lg font-bold text-gray-800 mb-3">2. 價格判斷</h3>
          <div className={`p-4 rounded-lg border-l-4 ${getPriceBorderColor(price_assessment)} ${getPriceColor(price_assessment)}`}>
            <p className="font-bold text-lg">開價評估：{price_assessment}</p>
          </div>
        </div>

        {/* 3. 綜合評分 */}
        <div className="mb-6">
          <h3 className="text-lg font-bold text-gray-800 mb-3">3. 綜合評分</h3>
          <div className="bg-gray-50 border border-gray-200 rounded-lg p-5 flex flex-col items-center justify-center text-center">
            <span className="text-sm font-medium text-gray-500 mb-1">評級指數</span>
            <div className="flex items-baseline space-x-2">
              <span className="text-3xl font-extrabold text-indigo-600">{weighted_score}</span>
              <span className="text-sm text-gray-400">/ 100 分</span>
            </div>
            <span className="text-lg font-bold text-indigo-500 mt-1">
              ({scoreToFivePoint(weighted_score)} / 5 分)
            </span>
          </div>
        </div>

        {/* 4. 周邊生活機能 */}
        <div className="mb-6">
          <h3 className="text-lg font-bold text-gray-800 mb-4">4. 周邊生活機能</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <table className="w-full border-collapse border border-gray-200 rounded-lg overflow-hidden">
                <thead>
                  <tr className="bg-gray-50 border-b border-gray-200">
                    <th className="px-4 py-2.5 border-r border-gray-200 text-left text-sm font-semibold text-gray-700">🚇 最近捷運站</th>
                    <th className="px-4 py-2.5 text-left text-sm font-semibold text-gray-700">🏥 最近醫院</th>
                  </tr>
                </thead>
                <tbody>
                  <tr className="border-b border-gray-100">
                    <td className="px-4 py-4 border-r border-gray-200 text-gray-800 align-top">
                      <div className="text-2xl md:text-3xl font-extrabold text-gray-800">
                        {Math.round(nearby_facilities.mrt.distance)}m
                      </div>
                      <div className="mt-2 text-xs md:text-sm text-gray-500 font-medium">
                        ⭐ {scoreToFivePoint(nearby_facilities.mrt.score)}分
                      </div>
                    </td>
                    <td className="px-4 py-4 text-gray-800 align-top">
                      <div className="text-2xl md:text-3xl font-extrabold text-gray-800">
                        {Math.round(nearby_facilities.hospital.distance)}m
                      </div>
                      <div className="mt-2 text-xs md:text-sm text-gray-500 font-medium">
                        ⭐ {scoreToFivePoint(nearby_facilities.hospital.score)}分
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div>
              <table className="w-full border-collapse border border-gray-200 rounded-lg overflow-hidden">
                <thead>
                  <tr className="bg-gray-50 border-b border-gray-200">
                    <th className="px-4 py-2.5 border-r border-gray-200 text-left text-sm font-semibold text-gray-700">🎓 最近學校</th>
                    <th className="px-4 py-2.5 text-left text-sm font-semibold text-gray-700">🌳 最近公園</th>
                  </tr>
                </thead>
                <tbody>
                  <tr className="border-b border-gray-100">
                    <td className="px-4 py-4 border-r border-gray-200 text-gray-800 align-top">
                      <div className="text-2xl md:text-3xl font-extrabold text-gray-800">
                        {Math.round(nearby_facilities.school.distance)}m
                      </div>
                      <div className="mt-2 text-xs md:text-sm text-gray-500 font-medium">
                        ⭐ {scoreToFivePoint(nearby_facilities.school.score)}分
                      </div>
                    </td>
                    <td className="px-4 py-4 text-gray-800 align-top">
                      <div className="text-2xl md:text-3xl font-extrabold text-gray-800">
                        {Math.round(nearby_facilities.park.distance)}m
                      </div>
                      <div className="mt-2 text-xs md:text-sm text-gray-500 font-medium">
                        ⭐ {scoreToFivePoint(nearby_facilities.park.score)}分
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* 5. 相似成交案例 */}
        {similar_cases && similar_cases.length > 0 && (
          <div className="mb-4">
            <h3 className="text-lg font-bold text-gray-800 mb-3">
              5. 相似成交案例
            </h3>
            <div className="overflow-x-auto">
              <table className="w-full border-collapse border border-gray-200 rounded-lg overflow-hidden">
                <thead>
                  <tr className="bg-gray-50 border-b border-gray-200 text-left">
                    <th className="px-4 py-2.5 text-sm font-semibold text-gray-700">成交地址</th>
                    <th className="px-4 py-2.5 text-sm font-semibold text-gray-700">成交日期</th>
                    <th className="px-4 py-2.5 text-sm font-semibold text-gray-700">坪數</th>
                    <th className="px-4 py-2.5 text-sm font-semibold text-gray-700">屋齡</th>
                    <th className="px-4 py-2.5 text-sm font-semibold text-gray-700 text-right">成交總價</th>
                  </tr>
                </thead>
                <tbody>
                  {similar_cases.map((case_, idx) => (
                    <tr key={idx} className="border-b border-gray-100 hover:bg-gray-50 transition">
                      <td className="px-4 py-3 text-sm text-gray-800 font-medium">{case_.address}</td>
                      <td className="px-4 py-3 text-sm text-gray-600">{case_.transaction_date}</td>
                      <td className="px-4 py-3 text-sm text-gray-600">{case_.area}坪</td>
                      <td className="px-4 py-3 text-sm text-gray-600">{case_.age}年</td>
                      <td className="px-4 py-3 text-sm font-bold text-gray-800 text-right">{Math.round(case_.price)}萬</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>

      {/* 購買建議 */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg shadow-lg p-6 border-l-4 border-indigo-500">
        <h3 className="text-xl font-bold text-gray-800 mb-2">💡 專家報告分析建議</h3>
        <p className="text-gray-700 leading-relaxed text-base">
          {recommendation}
        </p>
      </div>
    </div>
  )
}

export default ResultDisplay
