import { Suspense } from "react"
import "./App.css"
import HomePage from "./page"

function App() {
  return (
    <div className="dark">
      <Suspense fallback={null}>
        <HomePage />
      </Suspense>
    </div>
  )
}

export default App
