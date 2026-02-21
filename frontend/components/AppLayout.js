import { useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/router'

export default function AppLayout({ children, currentPage }) {
  return (
    <div className="min-h-screen bg-[#f8f6f3]">
      {/* Top Decorative Border */}
      <div className="fixed top-0 left-0 right-0 h-1 bg-gradient-to-r from-[#8b6f47] via-[#c2794d] to-[#8b6f47] z-50"></div>

      {/* App Header */}
      <header className="fixed top-1 left-0 right-0 z-40 bg-[#f8f6f3]/98 backdrop-blur-md border-b-2 border-[#d4c5b0]/40 shadow-sm">
        <div className="px-6 py-4">
          <div className="flex items-center justify-between">
            {/* Logo */}
            <Link href="/" className="flex items-center space-x-3 group cursor-pointer">
              <div className="w-11 h-11 bg-gradient-to-br from-[#c2794d] to-[#8b6f47] rounded-xl flex items-center justify-center shadow-md group-hover:shadow-lg transition-all">
                <span className="text-white font-bold text-xl">अ</span>
              </div>
              <div>
                <h1 className="text-2xl font-bold text-[#3d3021] font-display">Artify Bharat</h1>
                <p className="text-xs text-[#8b6f47] font-hindi">कारीगरों का बाज़ार</p>
              </div>
            </Link>

            {/* Search Bar */}
            <div className="flex-1 max-w-xl mx-8 hidden md:block">
              <div className="relative">
                <input
                  type="text"
                  placeholder="Search for handmade crafts..."
                  className="w-full px-4 py-2.5 pl-10 bg-white border-2 border-[#d4c5b0]/50 rounded-xl focus:outline-none focus:border-[#c2794d] transition-colors text-sm"
                />
                <span className="absolute left-3 top-1/2 -translate-y-1/2 text-[#8b6f47] text-lg">🔍</span>
              </div>
            </div>

            {/* Right Side Actions */}
            <div className="flex items-center space-x-4">
              {/* Verify Product Button */}
              <button className="hidden md:flex items-center space-x-2 px-6 py-2.5 bg-gradient-to-r from-[#c2794d] to-[#8b6f47] text-white font-semibold rounded-xl hover:shadow-lg transition-all duration-300">
                <span>✓</span>
                <span>Verify Product</span>
              </button>

              {/* Profile Dropdown */}
              <div className="relative group">
                <button className="flex items-center space-x-2 px-4 py-2 bg-white border-2 border-[#d4c5b0]/50 rounded-xl hover:border-[#c2794d] transition-all">
                  <div className="w-8 h-8 bg-gradient-to-br from-[#c2794d] to-[#8b6f47] rounded-full flex items-center justify-center">
                    <span className="text-white text-sm">👤</span>
                  </div>
                  <span className="hidden md:block text-sm font-medium text-[#3d3021]">Profile</span>
                  <span className="text-[#6d5a3d]">▼</span>
                </button>

                {/* Dropdown Menu */}
                <div className="absolute right-0 mt-2 w-48 bg-white border-2 border-[#d4c5b0]/50 rounded-xl shadow-lg opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200">
                  <div className="py-2">
                    <Link href="/buyer/profile" className="block px-4 py-2 text-sm text-[#3d3021] hover:bg-[#f8f6f3] transition-colors">
                      👤 My Profile
                    </Link>
                    <Link href="/buyer/orders" className="block px-4 py-2 text-sm text-[#3d3021] hover:bg-[#f8f6f3] transition-colors">
                      📦 My Orders
                    </Link>
                    <Link href="/buyer/wishlist" className="block px-4 py-2 text-sm text-[#3d3021] hover:bg-[#f8f6f3] transition-colors">
                      ❤️ Wishlist
                    </Link>
                    <hr className="my-2 border-[#d4c5b0]/40" />
                    <Link href="/artisan/dashboard" className="block px-4 py-2 text-sm text-[#3d3021] hover:bg-[#f8f6f3] transition-colors">
                      🎨 Artisan Dashboard
                    </Link>
                    <hr className="my-2 border-[#d4c5b0]/40" />
                    <button
                      onClick={() => {
                        localStorage.clear()
                        window.location.href = '/login/login'
                      }}
                      className="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
                    >
                      🚪 Logout
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </header>

      <div className="flex pt-20">
        {/* Main Content Area - Full Width */}
        <main className="flex-1 w-full">
          {children}
        </main>
      </div>
    </div>
  )
}