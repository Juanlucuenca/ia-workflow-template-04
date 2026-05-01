import { Outlet, NavLink } from "react-router"

export default function Dashboard() {
  return (
    <div>
      <nav>
        <NavLink to="/dashboard" end className={({ isActive }) => isActive ? "active" : ""}>Overview</NavLink>
        {" | "}
        <NavLink to="/dashboard/settings" className={({ isActive }) => isActive ? "active" : ""}>Settings</NavLink>
      </nav>
      <Outlet />
    </div>
  )
}
