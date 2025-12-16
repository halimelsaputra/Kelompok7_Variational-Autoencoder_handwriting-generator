"use client"

import { Github, Code, Terminal, Braces, GitPullRequest } from "lucide-react"

export function Footer() {
  return (
    <footer className="relative mx-auto mt-10 w-full max-w-4xl bg-black px-5 py-8 text-white sm:px-6 sm:py-10">
      <div className="absolute top-0 -left-120 -right-120 h-px bg-white/20" />

      <div className="relative flex flex-col items-center gap-5 sm:gap-6">
        <div className="text-2xl sm:text-3xl font-extrabold tracking-tight">Handwriting Generator</div>

        <div className="flex flex-wrap items-center justify-center gap-x-4 gap-y-1.5 text-[11px] sm:text-xs text-white/80">
          <span>サイトマップ</span>
          <span>プライバシーポリシー</span>
          <span>サイトご利用規約</span>
          <span>お問い合わせ</span>
          <span>Abema公式ショップ</span>
        </div>

        <div className="flex items-center gap-3 sm:gap-4 text-[11px] sm:text-xs text-white/90">
          {[Github, Code, Terminal, GitPullRequest, Braces].map((Icon, idx) => (
            <span
              key={idx}
              className="inline-flex items-center gap-1 rounded-full border border-white/40 px-3 py-1 text-[11px] sm:text-xs font-semibold text-white/90"
            >
              <Icon className="h-4 w-4" />
              <span>{Icon.displayName || "Link"}</span>
            </span>
          ))}
        </div>

        <div className="text-[11px] sm:text-xs text-white/70">Variational Autoencoder</div>
      </div>
    </footer>
  )
}
