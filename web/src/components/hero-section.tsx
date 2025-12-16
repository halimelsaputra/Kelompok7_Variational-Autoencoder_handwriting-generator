import RotatingText from "./RotatingText"

export function HeroSection() {
  return (
    <section className="min-h-screen flex items-center justify-center px-4 py-20 relative">
      <div className="max-w-4xl mx-auto text-center relative z-10 animate-fade-in-hero">

        {/* Main Heading */}
        <h1 className="text-3xl sm:text-4xl md:text-6xl lg:text-7xl font-bold text-balance mb-6 animate-fade-in-heading">
          <span className="text-foreground">Handwriting</span>
          <br />
          <span className="inline-flex items-center justify-center flex-wrap gap-2 mt-4 sm:mt-6 md:mt-8">
            <span className="text-foreground">Generator</span>
            <RotatingText
              texts={["VAE", "Variational", "Autoencoder"]}
              mainClassName="px-2 sm:px-2 md:px-3 bg-white text-black overflow-hidden py-1 sm:py-1 md:py-2 justify-center rounded-lg shadow-lg"
              staggerFrom={"last"}
              initial={{ y: "100%" }}
              animate={{ y: 0 }}
              exit={{ y: "-120%" }}
              staggerDuration={0.025}
              splitLevelClassName="overflow-hidden pb-1 sm:pb-1 md:pb-1"
              transition={{ type: "spring", damping: 30, stiffness: 400 }}
              rotationInterval={2000}
            />
          </span>
        </h1>

        {/* Subheading */}
        <p className="text-base sm:text-xl md:text-2xl text-white text-balance max-w-sm sm:max-w-3xl mx-auto mb-8 sm:mb-12 leading-relaxed px-4 sm:px-0 animate-fade-in-subheading font-light">
          Generate handwriting samples using Artificial Intelligence.
        </p>

        {/* CTA Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4 mb-8 sm:mb-16 animate-fade-in-buttons">



        </div>

        {/* Trust Indicators */}
        <div className="text-center px-4 hidden sm:block overflow-hidden animate-fade-in-trust">
          <p className="text-sm text-white mb-6">Powered by</p>
          <div className="relative overflow-hidden w-full max-w-4xl mx-auto">
            <div className="flex items-center gap-8 opacity-60 hover:opacity-80 transition-all duration-500 animate-slide-left">
              <div className="flex items-center gap-8 whitespace-nowrap">
                <div className="text-base sm:text-lg font-semibold">Python</div>
                <div className="text-base sm:text-lg font-semibold">TensorFlow</div>
                <div className="text-base sm:text-lg font-semibold">PyTorch</div>
                <div className="text-base sm:text-lg font-semibold">Flask</div>
                <div className="text-base sm:text-lg font-semibold">NumPy</div>
              </div>
              {/* Duplicate for seamless loop */}
              <div className="flex items-center gap-8 whitespace-nowrap">
                <div className="text-base sm:text-lg font-semibold">Python</div>
                <div className="text-base sm:text-lg font-semibold">TensorFlow</div>
                <div className="text-base sm:text-lg font-semibold">PyTorch</div>
                <div className="text-base sm:text-lg font-semibold">Flask</div>
                <div className="text-base sm:text-lg font-semibold">NumPy</div>
              </div>

              <div className="flex items-center gap-8 whitespace-nowrap">
                <div className="text-base sm:text-lg font-semibold">Python</div>
                <div className="text-base sm:text-lg font-semibold">TensorFlow</div>
                <div className="text-base sm:text-lg font-semibold">PyTorch</div>
                <div className="text-base sm:text-lg font-semibold">Flask</div>
                <div className="text-base sm:text-lg font-semibold">NumPy</div>
              </div>
            </div>
          </div>
        </div>

        {/* Mobile Trust Indicators */}
        <div className="text-center px-4 mb-8 sm:hidden overflow-hidden animate-fade-in-trust">
          <p className="text-sm text-white mb-6">Powered by</p>
          <div className="relative overflow-hidden w-full max-w-sm mx-auto">
            {/* Left blur fade */}
            <div className="absolute left-0 top-0 w-8 h-full bg-gradient-to-r from-black to-transparent z-10 pointer-events-none"></div>
            {/* Right blur fade */}
            <div className="absolute right-0 top-0 w-8 h-full bg-gradient-to-l from-black to-transparent z-10 pointer-events-none"></div>
            <div className="flex items-center gap-6 opacity-60 animate-slide-left-mobile">
              <div className="flex items-center gap-6 whitespace-nowrap">
                <div className="text-sm font-semibold">Python</div>
                <div className="text-sm font-semibold">TensorFlow</div>
                <div className="text-sm font-semibold">PyTorch</div>
                <div className="text-sm font-semibold">Flask</div>
                <div className="text-sm font-semibold">NumPy</div>
              </div>
              {/* Duplicate for seamless loop */}
              <div className="flex items-center gap-6 whitespace-nowrap">
                <div className="text-sm font-semibold">Python</div>
                <div className="text-sm font-semibold">TensorFlow</div>
                <div className="text-sm font-semibold">PyTorch</div>
                <div className="text-sm font-semibold">Flask</div>
                <div className="text-sm font-semibold">NumPy</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
