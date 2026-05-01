import { Outlet, NavLink } from "react-router"

export default function RootLayout() {
  return (
    <div className="min-h-screen flex flex-col">
      <header>
        <nav>
          <NavLink to="/" end className={({ isActive }) => isActive ? "active" : ""}>Home</NavLink>
          {" | "}
          <NavLink to="/about" className={({ isActive }) => isActive ? "active" : ""}>About</NavLink>
          {" | "}
          <NavLink to="/dashboard" className={({ isActive }) => isActive ? "active" : ""}>Dashboard</NavLink>
        </nav>
      </header>
      <main className="flex-1">
        <Outlet />
      </main>
    </div>
  )
}
