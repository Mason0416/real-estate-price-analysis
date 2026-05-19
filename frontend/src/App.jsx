import { useState } from 'react'
import InputForm from './components/InputForm'
import ResultDisplay from './components/ResultDisplay'
import WeightSettings from './components/WeightSettings'

function App() {
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)
  const [showWeights, setShowWeights] = useState(false)

  const defaultWeights = {
    price: 30,
    mrt: 20,
    hospital: 10,
    school: 15,
    park: 10,
    age: 10,
    area: 0,
    floor: 0,
    parking: 5,
  }

  const [weights, setWeights] = useState(defaultWeights)

  const normalizeWeights = (weightObj) => {
    const total = Object.values(weightObj).reduce((a, b) => a + b, 0)
    if (total === 0) return weightObj

    return Object.entries(weightObj).reduce((acc, [key, value]) => {
      acc[key] = Math.round((value / total) * 100) / 100
      return acc
    }, {})
  }

  const handleSubmit = async (formData) => {
    setLoading(true)
    try {
      const normalizedWeights = normalizeWeights(weights)

      const payload = {
        ...formData,
        weights: normalizedWeights,
      }

      console.log('Sending payload:', payload)

      const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`)
      }

      const data = await response.json()
      setResults(data)
    } catch (error) {
      console.error('Error:', error)
      alert(`分析失敗: ${error.message}`)
    } finally {
      setLoading(false)
    }
  }

  const handleWeightsChange = (newWeights) => {
    setWeights(newWeights)
  }

  const resetWeights = () => {
    setWeights(defaultWeights)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="max-w-6xl mx-auto px-4 py-8">
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            🏠 房屋價格合理性分析
          </h1>
          <p className="text-gray-600">
            幫助您判斷房屋開價是否合理
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-1">
            <InputForm
              onSubmit={handleSubmit}
              loading={loading}
              onToggleWeights={() => setShowWeights(!showWeights)}
            />
            {showWeights && (
              <WeightSettings
                weights={weights}
                onWeightsChange={handleWeightsChange}
                onReset={resetWeights}
              />
            )}
          </div>

          <div className="lg:col-span-2">
            {loading && (
              <div className="bg-white rounded-lg shadow-lg p-8 text-center">
                <p className="text-gray-600">分析中...</p>
              </div>
            )}
            {results && !loading && <ResultDisplay results={results} />}
            {!results && !loading && (
              <div className="bg-white rounded-lg shadow-lg p-8 text-center">
                <p className="text-gray-500">
                  請輸入房屋資訊以開始分析
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
