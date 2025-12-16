import { HeroSection } from "@/components/hero-section"
import { AboutUsSection } from "@/components/about_us-section"
import Aurora from "@/components/Aurora"
import { ConcepsSection } from "@/components/conceps-section"
import { GeneratingSection } from "@/components/generating-section"
import { Footer } from "@/components/footer"

export default function HomePage() {
  return (
    <div className="min-h-screen bg-black overflow-hidden">
      <main className="min-h-screen relative overflow-hidden">
        <div className="fixed inset-0 w-full h-full">
          <Aurora colorStops={["#475569", "#64748b", "#475569"]} amplitude={1.2} blend={0.6} speed={0.8} />
        </div>
        <div className="relative z-10">
          <HeroSection />
          <GeneratingSection />
          <ConcepsSection />
          <AboutUsSection />
          <Footer />
        </div>
      </main>
    </div>
  )
}
