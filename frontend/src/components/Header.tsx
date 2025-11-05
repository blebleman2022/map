'use client'

export default function Header() {
  return (
    <header className="sticky top-4 z-50 mx-auto w-full max-w-6xl px-4">
      <div className="flex items-center justify-between whitespace-nowrap rounded-lg border border-white/10 bg-glass p-3 shadow-lg backdrop-blur-md">
        {/* Logo */}
        <div className="flex items-center gap-4 text-white">
          <div className="w-5 h-5">
            <svg fill="none" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
              <path d="M6 6H42L36 24L42 42H6L12 24L6 6Z" fill="currentColor"></path>
            </svg>
          </div>
          <h2 className="text-white text-lg font-bold tracking-tight">DollyNav</h2>
        </div>

        {/* 导航 */}
        <div className="flex items-center gap-6">
          <a href="/" className="text-sm font-medium text-white transition-colors">
            首页
          </a>
          <a href="/tutors.html" className="text-sm font-medium text-white/80 hover:text-white transition-colors">
            Tutors
          </a>
        </div>
      </div>
    </header>
  )
}

