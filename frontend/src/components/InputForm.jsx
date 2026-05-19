import { useState } from 'react'

const InputForm = ({ onSubmit, loading, onToggleWeights }) => {
  const [formData, setFormData] = useState({
    address: '',
    askingPrice: '',
    area: '',
    age: '',
    buildingType: 'building',
    floor: '',
    totalFloors: '',
    parking: 'yes',
    layout: '',
  })

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value === '' ? '' : isNaN(value) ? value : value,
    }))
  }

  const handleSubmit = (e) => {
    e.preventDefault()

    const numericData = {
      ...formData,
      askingPrice: parseFloat(formData.askingPrice),
      area: parseFloat(formData.area),
      age: parseInt(formData.age),
      floor: parseInt(formData.floor),
      totalFloors: parseInt(formData.totalFloors),
    }

    onSubmit(numericData)
  }

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-lg p-6 space-y-4">
      <h2 className="text-2xl font-bold text-gray-800 mb-6">房屋資訊</h2>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          地址
        </label>
        <input
          type="text"
          name="address"
          value={formData.address}
          onChange={handleChange}
          placeholder="例：台北市信義區光復路"
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          賣家開價 (萬元)
        </label>
        <input
          type="number"
          name="askingPrice"
          value={formData.askingPrice}
          onChange={handleChange}
          placeholder="1000"
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          坪數
        </label>
        <input
          type="number"
          name="area"
          value={formData.area}
          onChange={handleChange}
          placeholder="30"
          step="0.1"
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          屋齡 (年)
        </label>
        <input
          type="number"
          name="age"
          value={formData.age}
          onChange={handleChange}
          placeholder="10"
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          建物型態
        </label>
        <select
          name="buildingType"
          value={formData.buildingType}
          onChange={handleChange}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="apartment">公寓</option>
          <option value="building">電梯大樓</option>
          <option value="house">透天</option>
        </select>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            樓層
          </label>
          <input
            type="number"
            name="floor"
            value={formData.floor}
            onChange={handleChange}
            placeholder="5"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            總樓層
          </label>
          <input
            type="number"
            name="totalFloors"
            value={formData.totalFloors}
            onChange={handleChange}
            placeholder="12"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            required
          />
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          車位
        </label>
        <select
          name="parking"
          value={formData.parking}
          onChange={handleChange}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          <option value="yes">有</option>
          <option value="no">無</option>
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 mb-1">
          格局
        </label>
        <input
          type="text"
          name="layout"
          value={formData.layout}
          onChange={handleChange}
          placeholder="2房1廳1衛"
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div className="pt-4 space-y-3">
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white font-bold py-2 px-4 rounded-md hover:bg-blue-700 disabled:bg-gray-400 transition"
        >
          {loading ? '分析中...' : '開始分析'}
        </button>
        <button
          type="button"
          onClick={onToggleWeights}
          className="w-full bg-gray-200 text-gray-800 font-bold py-2 px-4 rounded-md hover:bg-gray-300 transition"
        >
          進階設定
        </button>
      </div>
    </form>
  )
}

export default InputForm
