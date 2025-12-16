"use client"

import { useEffect, useRef } from "react"
import { TestimonialsColumn } from "@/components/ui/testimonials-column"

export function ConcepsSection() {
  const sectionRef = useRef<HTMLElement>(null)

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const elements = entry.target.querySelectorAll(".fade-in-element")
            elements.forEach((element, index) => {
              setTimeout(() => {
                element.classList.add("animate-fade-in-up")
              }, index * 300)
            })
          }
        })
      },
      { threshold: 0.1 },
    )

    if (sectionRef.current) {
      observer.observe(sectionRef.current)
    }

    return () => observer.disconnect()
  }, [])

  const testimonials = [
    {
      text: "The encoder network compresses input images into a compact latent vector representation efficiently.",
      name: "Encoder Network",
      role: "Dimensionality Reduction",
    },
    {
      text: "The decoder reconstructs handwriting images from latent vectors to match the original data distribution.",
      name: "Decoder Network",
      role: "Image Reconstruction",
    },
    {
      text: "Our model uses a continuous latent space which allows for smooth interpolation between different digit styles.",
      name: "Latent Space",
      role: "Smooth Interpolation",
    },
    {
      text: "Unlike standard autoencoders, VAE generates diverse outputs by sampling from a probability distribution.",
      name: "Generative Capability",
      role: "Sampling Diversity",
    },
    {
      text: "We optimize the Evidence Lower Bound to balance reconstruction quality and regularization during training.",
      name: "Loss Function",
      role: "ELBO Optimization",
    },
    {
      text: "The model learns from the MNIST dataset to understand various handwriting patterns and structural distinctness.",
      name: "Training Data",
      role: "MNIST Knowledge",
    },
  ]

  return (
    <section
      id="testimonials"
      ref={sectionRef}
      className="relative pt-16 sm:pt-40 pb-24 sm:pb-32 px-4 sm:px-6 lg:px-8 z-10 mb-24 sm:mb-32"
    >
      {/* Grid Background */}
      <div className="absolute inset-0 opacity-10">
        <div
          className="h-full w-full"
          style={{
            backgroundImage: `
            linear-gradient(rgba(255,255,255,0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.1) 1px, transparent 1px)
          `,
            backgroundSize: "80px 80px",
          }}
        />
      </div>

      <div className="relative max-w-7xl mx-auto">
        {/* Header Section - Keep as user loves it */}
        <div className="text-center mb-16 md:mb-32">
          <div className="fade-in-element opacity-0 translate-y-8 transition-all duration-1000 ease-out inline-flex items-center gap-2 text-white/60 text-sm font-medium tracking-wider uppercase mb-6">
          </div>
          <h2 className="fade-in-element opacity-0 translate-y-8 transition-all duration-1000 ease-out text-5xl md:text-6xl lg:text-7xl font-bold text-white mb-8 tracking-tight text-balance">
            Core Concepts & <span className="font-bold">Architecture</span>
          </h2>
          <p className="fade-in-element opacity-0 translate-y-8 transition-all duration-1000 ease-out text-xl text-white/70 max-w-2xl mx-auto leading-relaxed">
            Explore the technical components and advantages of this Variational Autoencoder project
          </p>
        </div>

        {/* Testimonials Carousel */}
        <div className="fade-in-element opacity-0 translate-y-8 transition-all duration-1000 ease-out relative flex justify-center items-center min-h-[600px] md:min-h-[800px] overflow-hidden">
          <div
            className="flex gap-8 max-w-6xl"
            style={{
              maskImage: "linear-gradient(to bottom, transparent 0%, black 10%, black 90%, transparent 100%)",
              WebkitMaskImage: "linear-gradient(to bottom, transparent 0%, black 10%, black 90%, transparent 100%)",
            }}
          >
            <TestimonialsColumn testimonials={testimonials.slice(0, 3)} duration={15} className="flex-1" />
            <TestimonialsColumn
              testimonials={testimonials.slice(2, 5)}
              duration={12}
              className="flex-1 hidden md:block"
            />
            <TestimonialsColumn
              testimonials={testimonials.slice(1, 4)}
              duration={18}
              className="flex-1 hidden lg:block"
            />
          </div>
        </div>
      </div>
    </section>
  )
}
