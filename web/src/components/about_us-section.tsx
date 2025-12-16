"use client"

import { CometCard } from "@/components/ui/comet-card"
import { useEffect, useRef, useState } from "react"
import "./ProfileCard.css"

export function AboutUsSection() {
  const sectionRef = useRef<HTMLElement>(null)
  const [isVisible, setIsVisible] = useState(false)
  const cards = [
    { title: "Halim Elsa Putra", code: "FrontEnd", img: "/orang1.png", alt: "Portrait invitation 1" },
    { title: "Faris Zain As-Shadiq", code: "FrontEnd", img: "/orang2.png", alt: "Portrait invitation 2" },
    { title: "Tinsari Rauhana", code: "BackEnd", img: "/orang3.png", alt: "Portrait invitation 3" },
    { title: "Yuyun Nailufar", code: "BackEnd", img: "/orang4.png", alt: "Portrait invitation 4" },
  ]

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) setIsVisible(true)
      },
      { threshold: 0.1, rootMargin: "0px 0px -100px 0px" },
    )

    if (sectionRef.current) observer.observe(sectionRef.current)
    return () => {
      if (sectionRef.current) observer.unobserve(sectionRef.current)
    }
  }, [])

  return (
    <section
      ref={sectionRef}
      className="pt-16 sm:pt-40 pb-24 sm:pb-32 px-4 relative z-10 mb-24 sm:mb-32"
    >
      <div className="max-w-6xl mx-auto">
        <div
          className={`text-center mb-16 sm:mb-40 transition-all duration-1000 ${
            isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
          }`}
        >
          <h2 className="text-2xl sm:text-3xl md:text-4xl lg:text-5xl font-bold text-white text-balance mb-4 sm:mb-6">
            <span className="text">About Us</span>
          </h2>
          <p className="text-base sm:text-lg md:text-xl text-white/70 max-w-3xl mx-auto font-light leading-relaxed">
            We are aspiring developers from Universitas Syiah Kuala. This project represents our commitment to mastering
            technologies of Artificial Intelligence.
          </p>
        </div>

        <div
          className={`grid gap-x-12 gap-y-10 md:gap-x-60 md:gap-y-12 grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 justify-items-center transition-all duration-1000 delay-300 ${
            isVisible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-12"
          }`}
        >
          {cards.map((card) => (
            <div key={card.code} className="flex justify-center">
              <CometCard>
                <div className="profile-card-wrap">
                  <div className="profile-card">
                    <div className="profile-card-filter"></div>
                    <img
                      loading="lazy"
                      className="profile-card-bg"
                      alt={card.alt}
                      src={card.img}
                    />

                    <div className="profile-card-content">
                      <div className="profile-card-name-wrap">
                        <div className="profile-card-name">{card.title}</div>
                      </div>

                      <div className="profile-card-tags">
                        <span className="profile-card-tag">{card.code}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </CometCard>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
