import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'DollyNav - 智能对话导航',
  description: '基于自然语言的智能导航服务',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-CN" className="dark">
      <head>
        <script
          type="text/javascript"
          src={`https://webapi.amap.com/maps?v=2.0&key=${process.env.NEXT_PUBLIC_AMAP_KEY || 'YOUR_KEY'}`}
        ></script>
      </head>
      <body className="bg-background-dark text-white">{children}</body>
    </html>
  )
}

