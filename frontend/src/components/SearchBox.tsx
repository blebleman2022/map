'use client'

import { useState } from 'react'
import { Search, Loader2 } from 'lucide-react'

interface SearchBoxProps {
  onSearch: (query: string) => void
  loading: boolean
}

export default function SearchBox({ onSearch, loading }: SearchBoxProps) {
  const [query, setQuery] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (query.trim()) {
      onSearch(query.trim())
    }
  }

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <div className="relative">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="例如：东方明珠塔附近5公里内离地铁站最近的3个星巴克..."
          className="w-full px-6 py-4 pr-32 bg-white/5 border-2 border-white/20 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-primary transition-colors"
          disabled={loading}
        />
        <button
          type="submit"
          disabled={loading || !query.trim()}
          className="absolute right-2 top-1/2 -translate-y-1/2 px-6 py-2 bg-primary hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg font-bold text-white transition-opacity flex items-center gap-2"
        >
          {loading ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              搜索中...
            </>
          ) : (
            <>
              <Search className="w-4 h-4" />
              搜索
            </>
          )}
        </button>
      </div>
    </form>
  )
}

