'use client'

import { useEffect, useRef } from 'react'

interface MapViewProps {
  results: any[]
  userLocation: { lat: number; lng: number } | null
}

declare global {
  interface Window {
    AMap: any
  }
}

export default function MapView({ results, userLocation }: MapViewProps) {
  const mapRef = useRef<HTMLDivElement>(null)
  const mapInstanceRef = useRef<any>(null)
  const markersRef = useRef<any[]>([])

  useEffect(() => {
    if (!mapRef.current || !window.AMap || !userLocation) return

    // 初始化地图
    if (!mapInstanceRef.current) {
      mapInstanceRef.current = new window.AMap.Map(mapRef.current, {
        zoom: 13,
        center: [userLocation.lng, userLocation.lat],
        mapStyle: 'amap://styles/dark',
      })
    }

    // 清除旧标记
    markersRef.current.forEach((marker) => marker.setMap(null))
    markersRef.current = []

    // 添加用户位置标记
    const userMarker = new window.AMap.Marker({
      position: [userLocation.lng, userLocation.lat],
      icon: new window.AMap.Icon({
        size: new window.AMap.Size(25, 34),
        image: '//a.amap.com/jsapi_demos/static/demo-center/icons/poi-marker-default.png',
        imageSize: new window.AMap.Size(25, 34),
      }),
      title: '您的位置',
    })
    userMarker.setMap(mapInstanceRef.current)
    markersRef.current.push(userMarker)

    // 添加结果标记
    const bounds: any[] = [[userLocation.lng, userLocation.lat]]
    
    results.forEach((result, index) => {
      const marker = new window.AMap.Marker({
        position: [result.location.lng, result.location.lat],
        label: {
          content: `${index + 1}`,
          direction: 'center',
        },
        title: result.name,
      })

      // 添加信息窗口
      const infoWindow = new window.AMap.InfoWindow({
        content: `
          <div style="padding: 10px; color: #333;">
            <h3 style="margin: 0 0 8px 0; font-weight: bold;">${result.name}</h3>
            <p style="margin: 4px 0; font-size: 12px;">${result.address}</p>
            <p style="margin: 4px 0; font-size: 12px;">距离：${(result.distance / 1000).toFixed(1)}公里</p>
            ${result.phone ? `<p style="margin: 4px 0; font-size: 12px;">电话：${result.phone}</p>` : ''}
          </div>
        `,
      })

      marker.on('click', () => {
        infoWindow.open(mapInstanceRef.current, marker.getPosition())
      })

      marker.setMap(mapInstanceRef.current)
      markersRef.current.push(marker)
      bounds.push([result.location.lng, result.location.lat])
    })

    // 自动调整视野
    if (bounds.length > 1) {
      mapInstanceRef.current.setFitView(null, false, [50, 50, 50, 50])
    }
  }, [results, userLocation])

  return (
    <div className="bg-white/5 border border-white/10 rounded-xl overflow-hidden h-[600px]">
      <div ref={mapRef} className="w-full h-full" />
    </div>
  )
}

