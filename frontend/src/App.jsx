import { BrowserRouter, Routes, Route } from "react-router"
import RootLayout from "@/layouts/RootLayout"
import Home from "@/pages/Home"
import About from "@/pages/About"
import NotFound from "@/pages/NotFound"
import Dashboard from "@/pages/dashboard/Dashboard"
import DashboardHome from "@/pages/dashboard/DashboardHome"
import Settings from "@/pages/dashboard/Settings"

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<RootLayout />}>
          <Route path="/" element={<Home />} />
          <Route path="about" element={<About />} />
          <Route path="dashboard" element={<Dashboard />}>
            <Route index element={<DashboardHome />} />
            <Route path="settings" element={<Settings />} />
          </Route>
          <Route path="*" element={<NotFound />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
