"use client"

import Aurora from "@/components/Aurora"
import { Footer } from "@/components/footer"
import { HeroSection } from "@/components/hero-section"

export default function CarDealershipsPage() {
  return (
    <div className="min-h-screen bg-black overflow-hidden">
      <main className="min-h-screen relative overflow-hidden">
        {/* Aurora background */}
        <div className="fixed inset-0 w-full h-full">
          <Aurora colorStops={["#475569", "#64748b", "#475569"]} amplitude={1.2} blend={0.6} speed={0.8} />
        </div>

        <div className="relative z-10">
          <HeroSection />

          {/* Footer */}
          <Footer />
        </div>
      </main>
    </div>
  )
}
