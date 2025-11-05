'use client'

import { MapPin, Navigation, Phone, Train } from 'lucide-react'

interface ResultListProps {
  results: any[]
  userLocation: { lat: number; lng: number } | null
}

export default function ResultList({ results, userLocation }: ResultListProps) {
  const formatDistance = (meters: number) => {
    if (meters < 1000) {
      return `${Math.round(meters)}米`
    }
    return `${(meters / 1000).toFixed(1)}公里`
  }

  const handleNavigate = (result: any) => {
    if (!userLocation) return
    
    // 调起高德地图导航
    const url = `https://uri.amap.com/navigation?from=${userLocation.lng},${userLocation.lat}&to=${result.location.lng},${result.location.lat}&name=${encodeURIComponent(result.name)}&mode=walking`
    window.open(url, '_blank')
  }

  return (
    <div className="bg-white/5 border border-white/10 rounded-xl p-4 h-[600px] overflow-y-auto">
      <h2 className="text-xl font-bold mb-4">搜索结果 ({results.length})</h2>
      
      <div className="space-y-3">
        {results.map((result, index) => (
          <div
            key={result.id || index}
            className="bg-white/5 border border-white/10 rounded-lg p-4 hover:bg-white/10 transition-colors"
          >
            {/* 标题 */}
            <div className="flex items-start justify-between mb-2">
              <div className="flex items-start gap-2">
                <span className="flex-shrink-0 w-6 h-6 bg-primary rounded-full flex items-center justify-center text-sm font-bold">
                  {index + 1}
                </span>
                <div>
                  <h3 className="font-medium text-white">{result.name}</h3>
                  <p className="text-sm text-gray-400">{result.category}</p>
                </div>
              </div>
            </div>

            {/* 距离信息 */}
            <div className="space-y-1 mb-3">
              <div className="flex items-center gap-2 text-sm text-gray-300">
                <MapPin className="w-4 h-4" />
                <span>距离您：{formatDistance(result.distance)}</span>
              </div>
              
              {result.nearest_subway && (
                <div className="flex items-center gap-2 text-sm text-gray-300">
                  <Train className="w-4 h-4" />
                  <span>
                    距离地铁站：{formatDistance(result.nearest_subway.distance)}
                    （{result.nearest_subway.name}）
                  </span>
                </div>
              )}

              {result.phone && (
                <div className="flex items-center gap-2 text-sm text-gray-300">
                  <Phone className="w-4 h-4" />
                  <span>{result.phone}</span>
                </div>
              )}
            </div>

            {/* 地址 */}
            <p className="text-sm text-gray-400 mb-3">{result.address}</p>

            {/* 操作按钮 */}
            <div className="flex gap-2">
              <button
                onClick={() => handleNavigate(result)}
                className="flex-1 px-4 py-2 bg-primary hover:opacity-90 rounded-lg text-sm font-bold text-white transition-opacity flex items-center justify-center gap-2"
              >
                <Navigation className="w-4 h-4" />
                导航
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

