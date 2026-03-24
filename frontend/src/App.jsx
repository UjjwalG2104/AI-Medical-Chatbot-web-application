import { useState } from 'react'
import Dashboard from './pages/Dashboard'
import Auth from './pages/Auth'
import LandingPage from './pages/LandingPage'

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'))
  const [showApp, setShowApp] = useState(false)

  if (!token && !showApp) {
    return <LandingPage onGetStarted={() => setShowApp(true)} />
  }

  if (!token && showApp) {
    return <Auth setToken={setToken} />
  }

  return <Dashboard token={token} setToken={setToken} />
}

export default App
