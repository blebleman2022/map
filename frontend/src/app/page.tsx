'use client'

import { useState, useEffect } from 'react'
import SearchBox from '@/components/SearchBox'
import ResultList from '@/components/ResultList'
import MapView from '@/components/MapView'
import Header from '@/components/Header'
import { Search, MapPin } from 'lucide-react'

export default function Home() {
  // 默认位置：北京天安门（不再自动获取系统位置）
  const [userLocation, setUserLocation] = useState<{ lat: number; lng: number }>({
    lat: 39.9042,
    lng: 116.4074
  })
  const [searchResults, setSearchResults] = useState<any[]>([])
  const [loading, setLoading] = useState(false)
  const [parsedQuery, setParsedQuery] = useState<any>(null)

  const handleSearch = async (query: string) => {
    setLoading(true)
    setParsedQuery(null)
    setSearchResults([])

    try {
      // 1. 解析查询
      const parseResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/parse-query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: query,
          location: userLocation,
        }),
      })

      const parseData = await parseResponse.json()
      
      if (!parseData.success) {
        alert(parseData.message || '解析失败')
        setLoading(false)
        return
      }

      setParsedQuery(parseData)

      // 使用解析后的位置（如果有）或默认位置
      const searchLocation = parseData.data.filters?.location || userLocation

      // 2. 搜索
      const searchResponse = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/search`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          category: parseData.data.category,
          subcategory: parseData.data.subcategory,
          radius: parseData.data.radius,
          limit: parseData.data.limit,
          sort_by: parseData.data.sort_by,
          brands: parseData.data.filters?.brands,
          proximity: parseData.data.filters?.proximity,
          location: searchLocation,
        }),
      })

      const searchData = await searchResponse.json()

      if (searchData.success) {
        setSearchResults(searchData.data.results || [])
      } else {
        alert(searchData.message || '搜索失败')
      }
    } catch (error) {
      console.error('搜索错误:', error)
      alert('搜索失败，请检查后端服务是否启动')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      
      <main className="flex-1 flex flex-col">
        {/* 搜索区域 */}
        <div className="w-full max-w-4xl mx-auto px-4 py-8">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold mb-4">智能对话导航</h1>
            <p className="text-gray-400">用自然语言描述您要找的地点</p>
          </div>

          <SearchBox onSearch={handleSearch} loading={loading} />

          {/* 解析结果展示 */}
          {parsedQuery && (
            <div className="mt-4 p-4 bg-white/5 border border-white/10 rounded-lg">
              <h3 className="text-sm font-medium text-gray-400 mb-2">查询解析：</h3>
              <div className="flex flex-wrap gap-2">
                {parsedQuery.display.location && (
                  <span className="px-3 py-1 bg-green-500/20 text-green-400 rounded-full text-sm">
                    📍 位置: {parsedQuery.display.location}
                  </span>
                )}
                <span className="px-3 py-1 bg-primary/20 text-primary rounded-full text-sm">
                  类型: {parsedQuery.display.type}
                </span>
                <span className="px-3 py-1 bg-primary/20 text-primary rounded-full text-sm">
                  范围: {parsedQuery.display.range}
                </span>
                <span className="px-3 py-1 bg-primary/20 text-primary rounded-full text-sm">
                  数量: {parsedQuery.display.count}
                </span>
                <span className="px-3 py-1 bg-primary/20 text-primary rounded-full text-sm">
                  排序: {parsedQuery.display.sort}
                </span>
              </div>
            </div>
          )}
        </div>

        {/* 结果区域 */}
        {searchResults.length > 0 && (
          <div className="flex-1 flex flex-col lg:flex-row gap-4 px-4 pb-8">
            {/* 左侧：结果列表 */}
            <div className="lg:w-2/5">
              <ResultList results={searchResults} userLocation={userLocation} />
            </div>

            {/* 右侧：地图 */}
            <div className="lg:w-3/5">
              <MapView
                results={searchResults}
                userLocation={userLocation}
              />
            </div>
          </div>
        )}

        {/* 空状态 */}
        {!loading && searchResults.length === 0 && !parsedQuery && (
          <div className="flex-1 flex items-center justify-center px-4">
            <div className="text-center text-gray-400">
              <MapPin className="w-16 h-16 mx-auto mb-4 opacity-50" />
              <p className="text-lg">输入查询开始搜索</p>
              <div className="mt-6 flex flex-wrap gap-2 justify-center">
                <button
                  onClick={() => handleSearch('东方明珠塔附近1公里内的星巴克')}
                  className="px-4 py-2 bg-white/5 hover:bg-white/10 rounded-lg text-sm transition-colors"
                >
                  东方明珠塔附近的星巴克
                </button>
                <button
                  onClick={() => handleSearch('北京天安门周边3公里内的地铁站')}
                  className="px-4 py-2 bg-white/5 hover:bg-white/10 rounded-lg text-sm transition-colors"
                >
                  天安门周边的地铁站
                </button>
                <button
                  onClick={() => handleSearch('上海外滩5公里内的川菜馆')}
                  className="px-4 py-2 bg-white/5 hover:bg-white/10 rounded-lg text-sm transition-colors"
                >
                  外滩附近的川菜馆
                </button>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

