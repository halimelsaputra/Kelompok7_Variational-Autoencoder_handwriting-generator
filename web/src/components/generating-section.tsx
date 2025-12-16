"use client"

import { useState, useEffect, useRef } from "react"
import { Slider } from "@/components/ui/slider"
import "./CatDropdown.css"
import "./GenerateButton.css"
import "./LoadingAnimation.css"
import "./GeneratingCard.css"

interface CalculatorInputs {
  z1: number
  z2: number
  selectedDigit: string
}

export function GeneratingSection() {
  const [inputs, setInputs] = useState<CalculatorInputs>({
    z1: 0,
    z2: 0,
    selectedDigit: "",
  })

  const [isVisible, setIsVisible] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const [generatedImage, setGeneratedImage] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [lastRequest, setLastRequest] = useState<{ url: string; status?: number } | null>(null)
  const [dropdownOpen, setDropdownOpen] = useState(false)
  const dropRef = useRef<HTMLDivElement | null>(null)

  const digitOptions = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setIsVisible(true)
          }
        })
      },
      { threshold: 0.1 },
    )

    const section = document.getElementById("roi-calculator")
    if (section) {
      observer.observe(section)
    }

    return () => observer.disconnect()
  }, [])

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropRef.current && !dropRef.current.contains(event.target as Node)) {
        setDropdownOpen(false)
      }
    }
    document.addEventListener("click", handleClickOutside)
    return () => document.removeEventListener("click", handleClickOutside)
  }, [])

  const handleGenerate = async () => {
    if (!inputs.selectedDigit) {
      setError("Please select a digit to generate")
      return
    }

    const digit = Number(inputs.selectedDigit)
    if (Number.isNaN(digit)) {
      setError("Digit must be a number between 0-9")
      return
    }

    setIsLoading(true)
    setError(null)
    setGeneratedImage(null)
    setLastRequest(null)

    try {
      // Support both Next.js and Vite environment variables
      const apiBase =
        (typeof globalThis !== "undefined" && (globalThis as any)?.process?.env?.NEXT_PUBLIC_API_URL?.trim()) ||
        (typeof import.meta !== "undefined" && import.meta.env?.VITE_API_URL) ||
        "https://halimelsa-backend-vae.hf.space"
      const url = `${apiBase}/generate?latent_x=${inputs.z1}&latent_y=${inputs.z2}&digit_label=${digit}`
      console.log("[fetch] Requesting:", url)

      const response = await fetch(url, { method: "GET", mode: "cors" })
      console.log("[fetch] Status:", response.status)
      setLastRequest({ url, status: response.status })

      if (!response.ok) {
        const errorText = await response.text()
        console.error("[fetch] Error response:", errorText)
        throw new Error(`Server error: ${response.status}`)
      }

      // Backend returns PNG image directly, convert to base64
      const blob = await response.blob()
      console.log("[fetch] Blob size:", blob.size)
      
      const base64Image = await new Promise<string>((resolve, reject) => {
        const reader = new FileReader()
        reader.onloadend = () => {
          const base64data = reader.result as string
          resolve(base64data.split(",")[1])
        }
        reader.onerror = () => reject(new Error("Failed to read image data"))
        reader.readAsDataURL(blob)
      })

      console.log("[generate] Image generated successfully")
      setGeneratedImage(base64Image)
    } catch (err) {
      console.error("[generate] error:", err)
      setError(
        err instanceof Error
          ? err.message
          : "Failed to connect to API server. Make sure the backend is reachable."
      )
    } finally {
      setIsLoading(false)
    }
  }

  const handleDownload = () => {
    if (!generatedImage) return

    const byteCharacters = atob(generatedImage)
    const byteNumbers = new Array(byteCharacters.length)
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i)
    }
    const byteArray = new Uint8Array(byteNumbers)
    const blob = new Blob([byteArray], { type: "image/png" })

    const url = URL.createObjectURL(blob)
    const link = document.createElement("a")
    link.href = url
    link.download = `handwriting_${inputs.selectedDigit}_z1_${inputs.z1.toFixed(2)}_z2_${inputs.z2.toFixed(2)}.png`
    document.body.appendChild(link)
    link.click()
    link.remove()
    URL.revokeObjectURL(url)
  }

  return (
    <section
      id="roi-calculator"
      className="pt-16 sm:pt-40 pb-24 sm:pb-32 px-4 relative z-10 mb-24 sm:mb-32"
    >
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div
          className={`text-center mb-12 md:mb-16 transition-all duration-700 ${isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}
        >
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-white mb-4 md:mb-6 text-balance">
            Generate{" "}
            <span className="bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
              Handwriting
            </span>
          </h2>

          <p className="text-lg md:text-xl text-gray-300 max-w-2xl mx-auto text-balance">
            Adjust the model parameters below to explore the VAE's latent space and generate unique handwritten digits.
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8 lg:gap-10 items-stretch">
          {/* Calculator Inputs */}
          <div
            className={`transition-all duration-700 delay-200 ${isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}
          >
            <div className="tk-card-wrap">
              <div className="tk-card p-6 md:p-8 h-full">
                <div className="tk-card-border"></div>
                <div className="tk-card-blob"></div>
                <div className="tk-card-content flex flex-col h-full">
                  <h3 className="text-xl md:text-2xl font-semibold text-white mb-6 md:mb-8">VAE Controls</h3>

                  <div className="space-y-8 flex-1">
                    {/* Business Type */}
                    <div>
                      <div className="mouse-detector">
                        <div className="cat">
                          <div className="sleep-symbol">
                            <span>Z</span>
                            <span>z</span>
                            <span>z</span>
                          </div>
                          <div className="thecat">
                            <svg width="45.952225mm" height="35.678726mm" viewBox="0 0 45.952225 35.678726" version="1.1" id="svg1" xmlns="http://www.w3.org/2000/svg">
                              <g id="layer1" style={{display:'inline'}} transform="translate(-121.80376,-101.90461)">
                                <path style={{display:'inline',fill:'#778899',stroke:'none',strokeWidth:'0.264583',strokeLinecap:'round',strokeLinejoin:'round',strokeDasharray:'none',strokeOpacity:'0.988235'}} d="m 144.95859,104.74193 c 6.01466,-2.1201 14.02915,-0.85215 17.62787,2.77812 3.59872,3.63027 2.91927,7.6226 -0.0661,11.80703 -2.98542,4.18443 -9.54667,3.58363 -15.1474,3.43959 -5.60073,-0.14404 -10.30411,-0.0586 -11.67474,-3.9026 7.85671,-2.22341 3.24576,-12.00205 9.26042,-14.12214 z" id="path1" />
                                <path style={{display:'inline',fill:'#778899',stroke:'none',strokeWidth:'0.264583',strokeLinecap:'round',strokeLinejoin:'round',strokeDasharray:'none',strokeOpacity:'0.988235'}} d="m 156.30732,121.30486 c 0,0 -3.82398,2.52741 -4.14054,3.7997 -0.31656,1.2723 0.31438,2.18109 0.95701,2.55128 0.64264,0.3702 1.59106,-0.085 2.13559,-0.75306 0.54452,-0.6681 1.5629,-2.25488 2.47945,-3.20579 0.91654,-0.95091 2.96407,-2.74361 2.96407,-2.74361 l 0.73711,-3.60348 z" id="path2" />
                                <path style={{display:'inline',fill:'#778899',stroke:'none',strokeWidth:'0.264583',strokeLinecap:'round',strokeLinejoin:'round',strokeDasharray:'none',strokeOpacity:'0.988235'}} d="m 136.93356,123.08347 c 0,0 -3.20149,3.2804 -3.24123,4.59088 -0.0397,1.31049 0.60411,1.83341 1.3106,2.05901 0.7065,0.22559 1.60304,-0.55255 1.99363,-1.32084 0.39056,-0.76832 1.14875,-2.30337 2.04139,-3.29463 0.89264,-0.99126 3.37363,-3.37561 3.37363,-3.37561 l -1.30007,-3.61169 z" id="path3" />
                                <path style={{display:'inline',fill:'#778899',stroke:'none',strokeWidth:'0.264583',strokeLinecap:'round',strokeLinejoin:'round',strokeDasharray:'none',strokeOpacity:'0.988235'}} d="m 130.12859,121.60522 c -2.15849,1.92962 -3.38576,3.23532 -3.61836,4.5256 -0.23257,1.2903 0.0956,1.80324 0.76105,2.13059 0.66549,0.32733 1.66701,-0.31006 2.16665,-1.01233 0.49961,-0.70231 1.04598,-1.14963 2.83575,-3.05671 1.78977,-1.90708 5.91823,-3.27102 5.91823,-3.27102 l -0.75313,-3.99546 c 0,0 -5.15171,2.7497 -7.31019,4.67933 z" id="path4" />
                                <path id="path5" style={{display:'inline',fill:'#778899',stroke:'none',strokeWidth:'0.292536',strokeLinecap:'round',strokeLinejoin:'round',strokeOpacity:'0.988235'}} d="m 147.59927,113.85404 c 0.68896,4.40837 -4.04042,7.93759 -10.51533,8.9455 -6.47491,1.00791 -12.24344,-0.88717 -12.9324,-5.29555 -0.68895,-4.40838 3.44199,-9.94186 9.9169,-10.94977 6.47491,-1.0079 12.84186,2.89144 13.53083,7.29982 z" />
                                <path style={{display:'inline',fill:'#778899',stroke:'none',strokeWidth:'0.264583',strokeLinecap:'round',strokeLinejoin:'round',strokeDasharray:'none',strokeOpacity:'0.988235'}} d="m 126.36446,111.82609 c 0,0 -2.37067,-6.28072 -0.86724,-7.10855 1.50342,-0.82783 5.87139,3.72617 5.87139,3.72617 z" id="path6" />
                                <path style={{display:'inline',fill:'#778899',stroke:'none',strokeWidth:'0.264583',strokeLinecap:'round',strokeLinejoin:'round',strokeDasharray:'none',strokeOpacity:'0.988235'}} d="m 143.50182,108.85407 c 0,0 -0.0544,-6.71302 -1.75519,-6.94283 -1.70081,-0.22982 -4.13211,5.59314 -4.13211,5.59314 z" id="path7" />
                                <g id="g25" style={{display:'inline'}}>
                                  <path style={{fill:'none',stroke:'#778899',strokeWidth:'0.529167',strokeLinecap:'round',strokeLinejoin:'round',strokeDasharray:'none',strokeOpacity:'0.988235'}} d="m 125.27102,116.06007 -2.97783,-1.05373" id="path8" />
                                  <path style={{fill:'none',stroke:'#778899',strokeWidth:'0.529167',strokeLinecap:'round',strokeLinejoin:'round',strokeDasharray:'none',strokeOpacity:'0.988235'}} d="m 124.91643,116.80991 -2.84808,0.0754" id="path9" />
                                  <path style={{fill:'none',stroke:'#778899',strokeWidth:'0.529167',strokeLinecap:'round',strokeLinejoin:'round',strokeDasharray:'none',strokeOpacity:'0.988235'}} d="m 124.97798,118.00308 -2.53111,0.5156" id="path10" />
                                </g>
                                <g id="g13" transform="rotate(-23.188815,49.755584,71.047761)" style={{display:'inline',fill:'none',stroke:'#000000'}}>
                                  <path style={{fill:'none',stroke:'#778899',strokeWidth:'0.529167',strokeLinecap:'round',strokeLinejoin:'round',strokeDasharray:'none',strokeOpacity:'0.988235'}} d="m 121.77448,146.87682 3.00963,-0.95912" id="path11" />
                                  <path style={{fill:'none',stroke:'#778899',strokeWidth:'0.529167',strokeLinecap:'round',strokeLinejoin:'round',strokeDasharray:'none',strokeOpacity:'0.988235'}} d="m 122.10521,147.63749 2.84427,0.16537" id="path12" />
                                  <path style={{fill:'none',stroke:'#778899',strokeWidth:'0.529167',strokeLinecap:'round',strokeLinejoin:'round',strokeDasharray:'none',strokeOpacity:'0.988235'}} d="m 122.00599,148.82812 2.51354,0.59531" id="path13" />
                                </g>
                                <ellipse style={{display:'inline',fill:'#ffffff',stroke:'none',strokeWidth:'0.56967',strokeLinecap:'round',strokeLinejoin:'round',strokeDasharray:'none',strokeOpacity:'0.988235'}} id="path14" cx="142.61723" cy="108.6707" rx="3.0261719" ry="3.0757811" transform="rotate(1.8105864)" />
                                <ellipse style={{display:'inline',fill:'#778899',stroke:'none',strokeWidth:'0.597086',strokeLinecap:'round',strokeLinejoin:'round',strokeDasharray:'none',strokeOpacity:'0.988235'}} id="ellipse15" cx="112.57543" cy="138.29808" rx="1.0380507" ry="1.3097118" transform="matrix(0.98048242,-0.19660678,0.20800608,0.97812753,0,0)" />
                                <ellipse style={{display:'inline',fill:'#f9f9f9',fillOpacity:'1',stroke:'none',strokeWidth:'0.184905',strokeLinecap:'round',strokeLinejoin:'round',strokeDasharray:'none',strokeOpacity:'0.988235'}} id="ellipse16" cx="112.70263" cy="137.817" rx="0.32146212" ry="0.40558979" transform="matrix(0.98048242,-0.19660678,0.20800608,0.97812753,0,0)" />
                                <ellipse style={{display:'inline',fill:'#ffffff',stroke:'none',strokeWidth:'0.56967',strokeLinecap:'round',strokeLinejoin:'round',strokeDasharray:'none',strokeOpacity:'0.988235'}} id="ellipse17" cx="135.40735" cy="110.12592" rx="3.0261719" ry="3.0757811" transform="rotate(1.8105864)" />
                                <ellipse style={{display:'inline',fill:'#778899',stroke:'none',strokeWidth:'0.597086',strokeLinecap:'round',strokeLinejoin:'round',strokeDasharray:'none',strokeOpacity:'0.988235'}} id="ellipse18" cx="105.22613" cy="138.07497" rx="1.0380507" ry="1.3097118" transform="matrix(0.98048242,-0.19660678,0.20800608,0.97812753,0,0)" />
                                <ellipse style={{display:'inline',fill:'#f9f9f9',fillOpacity:'1',stroke:'none',strokeWidth:'0.184905',strokeLinecap:'round',strokeLinejoin:'round',strokeDasharray:'none',strokeOpacity:'0.988235'}} id="ellipse19" cx="105.35332" cy="137.59389" rx="0.32146212" ry="0.40558979" transform="matrix(0.98048242,-0.19660678,0.20800608,0.97812753,0,0)" />
                                <path style={{display:'inline',fill:'#778899',stroke:'none',strokeWidth:'0.264583',strokeLinecap:'round',strokeLinejoin:'round',strokeDasharray:'none',strokeOpacity:'0.988235'}} d="m 163.77708,109.27292 c 4.36563,2.71198 4.26447,17.63497 3.70417,21.03437 -0.5603,3.3994 -1.86906,4.06275 -4.53099,4.49791 -5.87463,0.96037 -8.39724,-5.87134 -5.7547,-5.72161 2.64254,0.14973 3.15958,3.46446 5.95314,2.05052 2.79356,-1.41394 -1.42214,-13.46068 -1.42214,-13.46068 z" id="tail" />
                                <path style={{display:'inline',fill:'#778899',stroke:'none',strokeWidth:'0.264583',strokeLinecap:'round',strokeLinejoin:'round',strokeDasharray:'none',strokeOpacity:'0.988235'}} d="m 159.74981,121.34445 c 0,0 -2.98896,3.47517 -2.94624,4.78555 0.0427,1.31039 0.89775,2.01247 1.61702,2.1932 0.71928,0.18075 1.50745,-0.51603 1.84897,-1.30735 0.34149,-0.79135 0.88811,-2.59584 1.51032,-3.76081 0.62219,-1.16497 2.10268,-3.44845 2.10268,-3.44845 l -0.27441,-3.66785 z" id="path20" />
                                <g id="lefteyelid" style={{display:'inline'}}>
                                  <ellipse style={{fill:'#778899',fillOpacity:'1',stroke:'none',strokeWidth:'0.529167',strokeLinecap:'round',strokeLinejoin:'round',strokeDasharray:'none',strokeOpacity:'0.988235'}} id="path21" cx="131.94429" cy="114.29948" rx="3.1571214" ry="3.2155864" />
                                  <path style={{fill:'#778899',fillOpacity:'1',stroke:'#ffffff',strokeWidth:'0.529167',strokeLinecap:'round',strokeLinejoin:'round',strokeDasharray:'none',strokeOpacity:'0.988235'}} d="m 129.32504,114.80228 c 2.54908,-1.14592 4.60706,-0.65481 4.60706,-0.65481" id="path22" />
                            </g>
                            <g id="righteyelid" style={{display:'inline'}}>
                              <ellipse style={{fill:'#778899',fillOpacity:'1',stroke:'none',strokeWidth:'0.529167',strokeLinecap:'round',strokeLinejoin:'round',strokeDasharray:'none',strokeOpacity:'0.988235'}} id="ellipse22" cx="139.07704" cy="113.0834" rx="3.1571214" ry="3.2155864" />
                              <path style={{fill:'#778899',fillOpacity:'1',stroke:'#ffffff',strokeWidth:'0.529167',strokeLinecap:'round',strokeLinejoin:'round',strokeDasharray:'none',strokeOpacity:'0.988235'}} d="m 136.48089,113.70683 c 2.48528,-1.2784 4.56624,-0.89621 4.56624,-0.89621" id="path23" />
                            </g>
                            <g id="eyesdown">
                              <ellipse style={{fill:'#ffffff',fillOpacity:'1',stroke:'none',strokeWidth:'0.529167',strokeLinecap:'round',strokeLinejoin:'round',strokeDasharray:'none',strokeOpacity:'0.988235'}} id="path26" cx="139.12122" cy="113.61373" rx="1.8686198" ry="2.0422525" />
                              <ellipse style={{fill:'#778899',stroke:'none',strokeWidth:'0.597086',strokeLinecap:'round',strokeLinejoin:'round',strokeDasharray:'none',strokeOpacity:'0.988235'}} id="ellipse25" cx="112.24622" cy="139.77037" rx="1.0380507" ry="1.3097118" transform="matrix(0.98048242,-0.19660678,0.20800608,0.97812753,0,0)" />
                              <ellipse style={{fill:'#f9f9f9',fillOpacity:'1',stroke:'none',strokeWidth:'0.184905',strokeLinecap:'round',strokeLinejoin:'round',strokeDasharray:'none',strokeOpacity:'0.988235'}} id="ellipse26" cx="112.37342" cy="139.28929" rx="0.32146212" ry="0.40558979" transform="matrix(0.98048242,-0.19660678,0.20800608,0.97812753,0,0)" />
                              <ellipse style={{fill:'#ffffff',fillOpacity:'1',stroke:'none',strokeWidth:'0.529167',strokeLinecap:'round',strokeLinejoin:'round',strokeDasharray:'none',strokeOpacity:'0.988235'}} id="ellipse27" cx="131.994" cy="114.92011" rx="1.8686198" ry="2.0422525" />
                              <ellipse style={{fill:'#778899',stroke:'none',strokeWidth:'0.597086',strokeLinecap:'round',strokeLinejoin:'round',strokeDasharray:'none',strokeOpacity:'0.988235'}} id="ellipse28" cx="105.00267" cy="139.64998" rx="1.0380507" ry="1.3097118" transform="matrix(0.98048242,-0.19660678,0.20800608,0.97812753,0,0)" />
                              <ellipse style={{fill:'#f9f9f9',fillOpacity:'1',stroke:'none',strokeWidth:'0.184905',strokeLinecap:'round',strokeLinejoin:'round',strokeDasharray:'none',strokeOpacity:'0.988235'}} id="ellipse29" cx="105.12987" cy="139.1689" rx="0.32146212" ry="0.40558979" transform="matrix(0.98048242,-0.19660678,0.20800608,0.97812753,0,0)" />
                            </g>
                            <path id="longtail" style={{display:'inline',fill:'#778899',fillOpacity:'1',stroke:'none',strokeWidth:'0.529167',strokeLinecap:'round',strokeLinejoin:'round',strokeDasharray:'none',strokeOpacity:'0.988235'}} d="m 164.24062,110.09354 -2.10788,6.5381 c 0,0 0.84017,12.88397 0.35269,20.95169 h 4.78291 c 0.83489,-8.63528 0.13334,-24.78453 -3.02772,-27.48979 z" />
                          </g>
                        </svg>
                      </div>
                      <div
                        className={`drop-skin ${dropdownOpen ? "liquid" : ""}`}
                        ref={dropRef}
                        onClick={(e) => {
                          e.stopPropagation()
                          setDropdownOpen((prev) => !prev)
                        }}
                        role="listbox"
                        aria-expanded={dropdownOpen}
                        aria-label="Select digit"
                      >
                        <div className="label">
                          {inputs.selectedDigit
                            ? `Digit ${inputs.selectedDigit}`
                            : "what number you want to generate?"}
                        </div>
                        <div className="options">
                          {digitOptions.map((digit) => (
                            <div
                              key={digit}
                              className={digit === inputs.selectedDigit ? "active" : ""}
                              onClick={(e) => {
                                e.stopPropagation()
                                setInputs((prev) => ({ ...prev, selectedDigit: digit }))
                                setDropdownOpen(false)
                              }}
                              role="option"
                              aria-selected={digit === inputs.selectedDigit}
                            >
                              {digit}
                            </div>
                          ))}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Latent Z1 */}
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-3">
                    Latent Dimension Z1:{" "}
                    <span className="text-white font-semibold">{inputs.z1.toFixed(2)}</span>
                  </label>
                  <Slider
                    value={[inputs.z1]}
                    onValueChange={([value]) => setInputs((prev) => ({ ...prev, z1: value }))}
                    max={3}
                    min={-3}
                    step={0.1}
                    className="w-full"
                  />
                  <div className="flex justify-between text-xs text-gray-400 mt-1">
                    <span>-3</span>
                    <span>3</span>
                  </div>
                </div>

                {/* Latent Z2 */}
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-3">
                    Latent Dimension Z2:{" "}
                    <span className="text-white font-semibold">{inputs.z2.toFixed(2)}</span>
                  </label>
                  <Slider
                    value={[inputs.z2]}
                    onValueChange={([value]) => setInputs((prev) => ({ ...prev, z2: value }))}
                    max={3}
                    min={-3}
                    step={0.1}
                    className="w-full"
                  />
                  <div className="flex justify-between text-xs text-gray-400 mt-1">
                    <span>-3</span>
                    <span>3</span>
                  </div>
                </div>

                {/* Generate Button */}
                <div className="pt-10">
                  <div className="flex justify-center">
                    <div className="container-button">
                      <div className="hover bt-1"></div>
                      <div className="hover bt-2"></div>
                      <div className="hover bt-3"></div>
                      <div className="hover bt-4"></div>
                      <div className="hover bt-5"></div>
                      <div className="hover bt-6"></div>
                      <button 
                        className="generate-btn" 
                        onClick={handleGenerate} 
                        disabled={isLoading}
                        type="button"
                        aria-label="Generate handwriting"
                      ></button>
                    </div>
                  </div>
                </div>

                <div className="flex-1"></div>
              </div>

              <div className="mt-6 lg:hidden">
                <div className="flex items-center justify-center gap-2 p-3 rounded-lg bg-primary/10 border border-primary/20">
                  <div className="animate-bounce">
                    <svg className="w-4 h-4 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M19 14l-7 7m0 0l-7-7m7 7V3"
                      />
                    </svg>
                  </div>
                  <span className="text-sm text-primary font-medium">Scroll down to see your results</span>
                </div>
              </div>
            </div>
          </div>
        </div>
          </div>

          {/* Generated Handwriting Results */}
          <div
            className={`transition-all duration-700 delay-400 ${isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}
          >
            <div className="tk-card-wrap">
              <div className="tk-card p-6 md:p-8 h-full">
                <div className="tk-card-border"></div>
                <div className="tk-card-blob"></div>
                <div className="tk-card-content flex flex-col h-full">
                  <h3 className="text-xl md:text-2xl font-semibold text-white mb-6 md:mb-8">
                    Generated Handwriting
                  </h3>

                  <div className="flex flex-col items-center justify-center flex-1 text-center gap-6 p-6">
                    {isLoading ? (
                      <div className="text-center">
                        <div className="banter-loader">
                          <div className="banter-loader__box"></div>
                          <div className="banter-loader__box"></div>
                          <div className="banter-loader__box"></div>
                          <div className="banter-loader__box"></div>
                          <div className="banter-loader__box"></div>
                          <div className="banter-loader__box"></div>
                          <div className="banter-loader__box"></div>
                          <div className="banter-loader__box"></div>
                          <div className="banter-loader__box"></div>
                        </div>
                        <p className="text-gray-300 text-sm mt-6">Generating handwriting...</p>
                      </div>
                    ) : error ? (
                      <div className="text-center">
                        <svg className="w-16 h-16 mx-auto text-red-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <p className="text-red-400 text-lg mb-2">Error</p>
                        <p className="text-gray-400 text-sm">{error}</p>
                      </div>
                    ) : generatedImage ? (
                      <div className="text-center">
                        <img src={`data:image/png;base64,${generatedImage}`} alt="Generated handwriting" className="mx-auto" style={{imageRendering: 'pixelated', width: '280px', height: '280px'}} />
                        <p className="text-gray-300 text-sm mt-4">Digit: {inputs.selectedDigit} | Z1: {inputs.z1.toFixed(2)} | Z2: {inputs.z2.toFixed(2)}</p>
                        {lastRequest?.url && (
                          <p className="text-gray-500 text-xs mt-2 break-all">Source: {lastRequest.url}</p>
                        )}
                      </div>
                    ) : (
                      <div className="text-center">
                        <div className="banter-loader">
                          <div className="banter-loader__box"></div>
                          <div className="banter-loader__box"></div>
                          <div className="banter-loader__box"></div>
                          <div className="banter-loader__box"></div>
                          <div className="banter-loader__box"></div>
                          <div className="banter-loader__box"></div>
                          <div className="banter-loader__box"></div>
                          <div className="banter-loader__box"></div>
                          <div className="banter-loader__box"></div>
                        </div>
                        
                        {lastRequest?.url && (
                          <p className="text-gray-500 text-xs mt-2 break-all">
                            Last request: {lastRequest.url} {lastRequest.status ? `(status ${lastRequest.status})` : ""}
                          </p>
                        )}
                      </div>
                    )}
                    {generatedImage && (
                      <div className="flex justify-center">
                        <div className="container-button">
                          <div className="hover bt-1"></div>
                          <div className="hover bt-2"></div>
                          <div className="hover bt-3"></div>
                          <div className="hover bt-4"></div>
                          <div className="hover bt-5"></div>
                          <div className="hover bt-6"></div>
                          <button
                            className="generate-btn download-btn"
                            type="button"
                            onClick={handleDownload}
                            aria-label="Download generated handwriting"
                          ></button>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* CTA */}
        <div
          className={`text-center mt-12 md:mt-16 transition-all duration-700 delay-600 ${isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}
        >
        </div>
      </div>
    </section>
  )
}
